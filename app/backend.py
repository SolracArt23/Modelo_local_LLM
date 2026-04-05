from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory, redirect, url_for, session, make_response
from backend import *
import requests
import sqlite3
import os
from datetime import datetime
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import PyPDF2
from general_func.chatting import Chating_func
from general_func.BD_conn import BD_conn
# Configuracion del servidor
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
# Configuración para subir archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_CREDITS = 30
ADMIN_ROLE = 'A'
CLIENT_ROLE = 'C'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_uploaded_pdf_files():
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        return []

    return sorted(
        file_name for file_name in os.listdir(app.config['UPLOAD_FOLDER'])
        if allowed_file(file_name)
    )


def get_db():
    if BD_conn.instancia == 0:
        global bd
        bd = BD_conn()
    return bd


def ensure_users_table():
    database = get_db()
    database.execute_query(
        '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            password TEXT NOT NULL,
            empresa TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL DEFAULT 'C',
            creditos INTEGER NOT NULL DEFAULT 30,
            widget_token TEXT
        )
        '''
    )


def generate_widget_token():
    return f"widget_{uuid4().hex}{uuid4().hex}"


def normalize_user_type(value):
    normalized_value = normalize_text(value).upper()
    return ADMIN_ROLE if normalized_value == ADMIN_ROLE else CLIENT_ROLE


def get_user_role_label(user_type):
    return 'Administrador' if normalize_user_type(user_type) == ADMIN_ROLE else 'Cliente'


def count_admin_users():
    database = get_db()
    rows = database.execute_query(
        'SELECT COUNT(*) FROM usuarios WHERE tipo_usuario = ?',
        (ADMIN_ROLE,)
    ) or []
    return rows[0][0] if rows else 0


def ensure_user_account_columns():
    database = get_db()
    columns = database.execute_query('PRAGMA table_info(usuarios)') or []
    column_names = {column[1] for column in columns}

    if 'tipo_usuario' not in column_names:
        database.execute_query(
            f"ALTER TABLE usuarios ADD COLUMN tipo_usuario TEXT NOT NULL DEFAULT '{CLIENT_ROLE}'"
        )

    database.execute_query(
        'UPDATE usuarios SET tipo_usuario = ? WHERE tipo_usuario IS NULL OR tipo_usuario NOT IN (?, ?)',
        (CLIENT_ROLE, ADMIN_ROLE, CLIENT_ROLE)
    )

    if 'creditos' not in column_names:
        database.execute_query(
            f'ALTER TABLE usuarios ADD COLUMN creditos INTEGER NOT NULL DEFAULT {DEFAULT_CREDITS}'
        )

    if 'widget_token' not in column_names:
        database.execute_query('ALTER TABLE usuarios ADD COLUMN widget_token TEXT')

    users_without_token = database.execute_query(
        'SELECT id FROM usuarios WHERE widget_token IS NULL OR widget_token = ""'
    ) or []
    for row in users_without_token:
        database.execute_query(
            'UPDATE usuarios SET widget_token = ? WHERE id = ?',
            (generate_widget_token(), row[0])
        )

    database.execute_query(
        'UPDATE usuarios SET creditos = ? WHERE creditos IS NULL',
        (DEFAULT_CREDITS,)
    )

    if count_admin_users() == 0:
        first_user = database.execute_query(
            'SELECT id FROM usuarios ORDER BY id ASC LIMIT 1'
        ) or []
        if first_user:
            database.execute_query(
                'UPDATE usuarios SET tipo_usuario = ? WHERE id = ?',
                (ADMIN_ROLE, first_user[0][0])
            )


def ensure_user_files_table():
    database = get_db()
    database.execute_query(
        '''
        CREATE TABLE IF NOT EXISTS user_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL UNIQUE,
            description TEXT,
            use_case TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        )
        '''
    )


def ensure_user_model_settings_table():
    database = get_db()
    database.execute_query(
        '''
        CREATE TABLE IF NOT EXISTS user_model_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            behavior_prompt TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        )
        '''
    )


def ensure_core_tables():
    ensure_users_table()
    ensure_user_account_columns()
    ensure_user_files_table()
    ensure_user_model_settings_table()


def is_password_hash(password_value):
    return password_value.startswith("scrypt:") or password_value.startswith("pbkdf2:")


def verify_user_password(stored_password, plain_password):
    if is_password_hash(stored_password):
        return check_password_hash(stored_password, plain_password)
    return stored_password == plain_password


def normalize_text(value):
    return (value or "").strip()


def get_current_timestamp():
    return datetime.utcnow().isoformat()


def get_user_account(user_id):
    ensure_core_tables()
    database = get_db()
    rows = database.execute_query(
        'SELECT id, nombre, empresa, tipo_usuario, creditos, widget_token FROM usuarios WHERE id = ?',
        (user_id,)
    ) or []
    if not rows:
        return None

    row = rows[0]
    return {
        'id': row[0],
        'nombre': row[1],
        'empresa': row[2],
        'tipo_usuario': normalize_user_type(row[3]),
        'rol_nombre': get_user_role_label(row[3]),
        'creditos': row[4],
        'widget_token': row[5],
    }


def get_user_by_widget_token(widget_token):
    ensure_core_tables()
    database = get_db()
    rows = database.execute_query(
        'SELECT id, nombre, empresa, tipo_usuario, creditos, widget_token FROM usuarios WHERE widget_token = ?',
        (widget_token,)
    ) or []
    if not rows:
        return None

    row = rows[0]
    return {
        'id': row[0],
        'nombre': row[1],
        'empresa': row[2],
        'tipo_usuario': normalize_user_type(row[3]),
        'rol_nombre': get_user_role_label(row[3]),
        'creditos': row[4],
        'widget_token': row[5],
    }


def list_user_accounts():
    ensure_core_tables()
    database = get_db()
    rows = database.execute_query(
        '''
        SELECT id, nombre, empresa, tipo_usuario, creditos, widget_token
        FROM usuarios
        ORDER BY CASE WHEN tipo_usuario = ? THEN 0 ELSE 1 END, id ASC
        ''',
        (ADMIN_ROLE,)
    ) or []

    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'nombre': row[1],
            'empresa': row[2],
            'tipo_usuario': normalize_user_type(row[3]),
            'rol_nombre': get_user_role_label(row[3]),
            'creditos': row[4],
            'widget_token': row[5],
        })
    return users


def create_user_account(nombre, password, empresa, tipo_usuario=CLIENT_ROLE, creditos=DEFAULT_CREDITS):
    ensure_core_tables()
    database = get_db()
    password_hash = generate_password_hash(password)
    normalized_role = normalize_user_type(tipo_usuario)
    safe_credits = max(0, int(creditos))

    database.execute_query(
        'INSERT INTO usuarios (nombre,password,empresa,tipo_usuario,creditos,widget_token) VALUES (?,?,?,?,?,?)',
        (nombre, password_hash, empresa, normalized_role, safe_credits, generate_widget_token())
    )

    created_user = database.execute_query(
        'SELECT id FROM usuarios WHERE nombre = ? ORDER BY id DESC LIMIT 1',
        (nombre,)
    ) or []
    return get_user_account(created_user[0][0]) if created_user else None


def delete_user_account(target_user_id):
    account = get_user_account(target_user_id)
    if not account:
        return None

    for file_record in get_user_files(target_user_id):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record['stored_name'])
        if os.path.isfile(file_path):
            os.remove(file_path)

    database = get_db()
    database.execute_query('DELETE FROM user_files WHERE user_id = ?', (target_user_id,))
    database.execute_query('DELETE FROM user_model_settings WHERE user_id = ?', (target_user_id,))
    database.execute_query('DELETE FROM usuarios WHERE id = ?', (target_user_id,))
    return account


def update_user_credits(user_id, new_credit_value):
    database = get_db()
    safe_value = max(0, int(new_credit_value))
    database.execute_query(
        'UPDATE usuarios SET creditos = ? WHERE id = ?',
        (safe_value, user_id)
    )
    return get_user_account(user_id)


def change_user_credits(user_id, delta):
    account = get_user_account(user_id)
    if not account:
        return None
    return update_user_credits(user_id, account['creditos'] + int(delta))


def add_widget_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response


def get_user_model_behavior(user_id):
    ensure_user_model_settings_table()
    database = get_db()
    rows = database.execute_query(
        'SELECT behavior_prompt FROM user_model_settings WHERE user_id = ?',
        (user_id,)
    ) or []
    return rows[0][0] if rows else ""


def upsert_user_model_behavior(user_id, behavior_prompt):
    ensure_user_model_settings_table()
    database = get_db()
    timestamp = get_current_timestamp()
    existing_rows = database.execute_query(
        'SELECT id FROM user_model_settings WHERE user_id = ?',
        (user_id,)
    ) or []

    if existing_rows:
        database.execute_query(
            'UPDATE user_model_settings SET behavior_prompt = ?, updated_at = ? WHERE user_id = ?',
            (behavior_prompt, timestamp, user_id)
        )
    else:
        database.execute_query(
            'INSERT INTO user_model_settings (user_id, behavior_prompt, updated_at) VALUES (?, ?, ?)',
            (user_id, behavior_prompt, timestamp)
        )

    return {
        "behavior_prompt": behavior_prompt,
        "updated_at": timestamp,
    }


def build_stored_filename(user_id, original_filename):
    safe_name = secure_filename(original_filename)
    return f"user_{user_id}_{uuid4().hex}_{safe_name}"


def row_to_user_file(row):
    return {
        "id": row[0],
        "original_name": row[1],
        "stored_name": row[2],
        "description": row[3] or "",
        "use_case": row[4] or "",
        "is_active": bool(row[5]),
        "created_at": row[6],
        "updated_at": row[7],
    }


def get_user_files(user_id, only_active=False):
    ensure_user_files_table()
    database = get_db()
    query = '''
        SELECT id, original_name, stored_name, description, use_case, is_active, created_at, updated_at
        FROM user_files
        WHERE user_id = ?
    '''
    params = [user_id]

    if only_active:
        query += ' AND is_active = 1'

    query += ' ORDER BY id DESC'
    rows = database.execute_query(query, tuple(params)) or []
    return [row_to_user_file(row) for row in rows]


def get_user_file_by_id(user_id, file_id):
    ensure_user_files_table()
    database = get_db()
    rows = database.execute_query(
        '''
        SELECT id, original_name, stored_name, description, use_case, is_active, created_at, updated_at
        FROM user_files
        WHERE id = ? AND user_id = ?
        ''',
        (file_id, user_id)
    ) or []
    return row_to_user_file(rows[0]) if rows else None


def get_user_file_by_reference(user_id, reference, require_active=False):
    ensure_user_files_table()
    database = get_db()
    query = '''
        SELECT id, original_name, stored_name, description, use_case, is_active, created_at, updated_at
        FROM user_files
        WHERE user_id = ? AND (
            stored_name = ? OR
            original_name = ? OR
            CAST(id AS TEXT) = ?
        )
    '''
    params = [user_id, reference, reference, reference]

    if require_active:
        query += ' AND is_active = 1'

    query += ' ORDER BY id DESC'
    rows = database.execute_query(query, tuple(params)) or []
    return row_to_user_file(rows[0]) if rows else None


def create_user_file_record(user_id, original_name, stored_name, description, use_case):
    ensure_user_files_table()
    timestamp = get_current_timestamp()
    database = get_db()
    database.execute_query(
        '''
        INSERT INTO user_files (user_id, original_name, stored_name, description, use_case, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
        ''',
        (user_id, original_name, stored_name, description, use_case, timestamp, timestamp)
    )
    created_rows = database.execute_query(
        'SELECT id FROM user_files WHERE stored_name = ?',
        (stored_name,)
    ) or []
    if not created_rows:
        return None
    return get_user_file_by_id(user_id, created_rows[0][0])


def update_user_file_status(user_id, file_id, is_active):
    ensure_user_files_table()
    database = get_db()
    database.execute_query(
        'UPDATE user_files SET is_active = ?, updated_at = ? WHERE id = ? AND user_id = ?',
        (1 if is_active else 0, get_current_timestamp(), file_id, user_id)
    )
    return get_user_file_by_id(user_id, file_id)


def delete_user_file(user_id, file_id):
    file_record = get_user_file_by_id(user_id, file_id)
    if not file_record:
        return None

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record['stored_name'])
    if os.path.isfile(file_path):
        os.remove(file_path)

    database = get_db()
    database.execute_query(
        'DELETE FROM user_files WHERE id = ? AND user_id = ?',
        (file_id, user_id)
    )
    return file_record


def get_session_user_id():
    return session.get('user_id')


def require_session_user():
    user_id = get_session_user_id()
    if not user_id:
        return None, (jsonify({"message": "Debes iniciar sesión para realizar esta acción."}), 401)
    return user_id, None


def get_request_api_token():
    authorization_header = normalize_text(request.headers.get('Authorization'))
    if authorization_header.lower().startswith('bearer '):
        return authorization_header[7:].strip()

    json_data = request.get_json(silent=True) if request.is_json else {}
    json_data = json_data or {}

    return normalize_text(
        request.headers.get('X-API-Token') or
        request.headers.get('X-Widget-Token') or
        request.args.get('token') or
        request.args.get('api_token') or
        request.form.get('token') or
        request.form.get('api_token') or
        json_data.get('token') or
        json_data.get('api_token') or
        json_data.get('widget_token')
    )


def require_api_user(allow_session_fallback=True):
    api_token = get_request_api_token()
    if api_token:
        account = get_user_by_widget_token(api_token)
        if not account:
            return None, None, (jsonify({"message": "El token de la API no es válido."}), 401)
        return account['id'], account, None

    if allow_session_fallback:
        user_id, auth_error = require_session_user()
        if auth_error:
            return None, None, (jsonify({"message": "Debes enviar un token válido o iniciar sesión para usar la API."}), 401)

        account = get_user_account(user_id)
        if not account:
            return None, None, (jsonify({"message": "Usuario no encontrado."}), 404)
        return user_id, account, None

    return None, None, (jsonify({"message": "Debes enviar un token válido para usar la API."}), 401)


def require_admin_user():
    user_id, auth_error = require_session_user()
    if auth_error:
        return None, None, auth_error

    account = get_user_account(user_id)
    if not account:
        return None, None, (jsonify({"message": "Usuario no encontrado."}), 404)

    if account['tipo_usuario'] != ADMIN_ROLE:
        return user_id, account, (jsonify({"message": "Solo un administrador puede realizar esta acción."}), 403)

    return user_id, account, None


def ejecutar_chat_archivo(nombre_archivo, mensaje, custom_behavior=""):
    chatting = Chating_func(
        folder_chatting=app.config['UPLOAD_FOLDER'],
        selected_file=nombre_archivo,
        custom_behavior=custom_behavior,
    )

    if not chatting.content_pdf:
        raise FileNotFoundError(nombre_archivo)

    peticion = chatting.RAG_model(mensaje)
    response = requests.post(OLLAMA_URL, json=peticion, timeout=60)
    response.raise_for_status()
    data = response.json()

    return {
        "archivo": nombre_archivo,
        "prompt": mensaje,
        "respuesta": data["message"]["content"],
        "modelo": peticion["model"],
    }



# Funcion de gestion
@app.route("/",methods=["GET"])
def main():
    if "usuario" not in session or not session.get("user_id"):
        session.clear()
        return redirect(url_for("Login"))

    ensure_core_tables()

    account = get_user_account(session.get("user_id"))
    managed_users = list_user_accounts() if account and account['tipo_usuario'] == ADMIN_ROLE else []

    return render_template(
        "main.html",
        usuario=session.get("usuario"),
        empresa=session.get("empresa"),
        user_files=get_user_files(session.get("user_id")),
        model_behavior=get_user_model_behavior(session.get("user_id")),
        user_credits=account['creditos'] if account else DEFAULT_CREDITS,
        widget_token=account['widget_token'] if account else '',
        user_role=account['tipo_usuario'] if account else CLIENT_ROLE,
        user_role_name=account['rol_nombre'] if account else get_user_role_label(CLIENT_ROLE),
        is_admin=bool(account and account['tipo_usuario'] == ADMIN_ROLE),
        managed_users=managed_users,
        current_user_id=account['id'] if account else None,
    )

@app.route("/descargar_api")
def descargar_api():
    return send_from_directory(
        directory="static",
        path="Api.html",
        as_attachment=True  # Esto fuerza la descarga
    )


@app.route('/descargar_widget')
def descargar_widget():
    user_id, auth_error = require_session_user()
    if auth_error:
        return redirect(url_for('Login'))

    account = get_user_account(user_id)
    widget_html = render_template(
        'widget_embed.html',
        widget_api_url=request.host_url.rstrip('/'),
        widget_token=account['widget_token'],
        widget_title=f"Asistente de {account['empresa']}",
    )

    response = make_response(widget_html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=chat_widget_embed.html'
    return response


#Funcion de login y resgistro
@app.route('/Envio_datos', methods=['POST'])
def registrar():
    ensure_core_tables()
    data = request.get_json(silent=True) or {}
    nombre = normalize_text(data.get('nombre'))
    password = normalize_text(data.get('password'))
    empresa = normalize_text(data.get('empresa'))

    if not nombre or not password or not empresa:
        return jsonify({"message": "Nombre, contraseña y empresa son obligatorios."}), 400

    if len(password) < 6:
        return jsonify({"message": "La contraseña debe tener al menos 6 caracteres."}), 400

    ensure_users_table()
    database = get_db()
    existing_user = database.execute_query(
        'SELECT id FROM usuarios WHERE nombre = ?',
        (nombre,)
    )

    if existing_user:
        return jsonify({"message": "El usuario ya existe."}), 409

    default_role = ADMIN_ROLE if count_admin_users() == 0 else CLIENT_ROLE
    create_user_account(nombre, password, empresa, default_role, DEFAULT_CREDITS)

    return jsonify({
        "message": "Usuario registrado correctamente.",
        "usuario": nombre,
        "empresa": empresa,
        "tipo_usuario": default_role,
        "rol_nombre": get_user_role_label(default_role),
    }), 201


@app.route('/register', methods=['POST'])
def register_alias():
    return registrar()



# --- Logout ---
@app.route("/logout", methods=["POST"])
def logout():
    if "usuario" not in session:
        return jsonify({"message": "No hay una sesión activa."}), 404

    session.clear()
    return jsonify({"message": "Logout exitoso"}), 200

@app.route("/login", methods=["GET", "POST"])
def Login():
    ensure_core_tables()

    if request.method == "POST":
        contenido = request.get_json(silent=True) or {}
        usuario = normalize_text(contenido.get("usuario"))
        password = normalize_text(contenido.get("password"))

        if not usuario or not password:
            return jsonify({"message": "Faltan campos"}), 400

        database = get_db()
        result = database.execute_query(
            "SELECT id, nombre, password, empresa FROM usuarios WHERE nombre = ?",
            (usuario,)
        )

        if not result:
            return jsonify({"message": "Credenciales incorrectas"}), 401

        user_id, stored_name, stored_password, empresa = result[0]
        if not verify_user_password(stored_password, password):
            return jsonify({"message": "Credenciales incorrectas"}), 401

        if not is_password_hash(stored_password):
            database.execute_query(
                "UPDATE usuarios SET password = ? WHERE id = ?",
                (generate_password_hash(password), user_id)
            )

        user_account = get_user_account(user_id)

        session["user_id"] = user_id
        session["usuario"] = stored_name
        session["empresa"] = empresa
        return jsonify({
            "message": "Credenciales correctas",
            "usuario":stored_name,
            "empresa":empresa,
            "creditos": user_account['creditos'] if user_account else DEFAULT_CREDITS,
            "tipo_usuario": user_account['tipo_usuario'] if user_account else CLIENT_ROLE,
            "rol_nombre": user_account['rol_nombre'] if user_account else get_user_role_label(CLIENT_ROLE),
        }), 200
    else:
        if "usuario" in session:
            return redirect(url_for("main"))
        return render_template("login.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    user_id, _, auth_error = require_api_user()
    if auth_error:
        return auth_error

    if 'file' not in request.files:
        return jsonify({"message": "No se envió ningún archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No se seleccionó ningún archivo"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Archivo no permitido"}), 400

    description = normalize_text(request.form.get('description'))
    use_case = normalize_text(request.form.get('casos_de_uso'))
    original_name = secure_filename(file.filename)
    stored_name = build_stored_filename(user_id, original_name)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], stored_name))
    created_file = create_user_file_record(user_id, original_name, stored_name, description, use_case)

    return jsonify({
        "message": "Archivo subido correctamente",
        "file": created_file,
    }), 200


@app.route('/model-settings', methods=['POST'])
def save_model_settings():
    user_id, auth_error = require_session_user()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    behavior_prompt = normalize_text(data.get('behavior_prompt'))

    if len(behavior_prompt) > 4000:
        return jsonify({"message": "La configuración es demasiado larga."}), 400

    updated_settings = upsert_user_model_behavior(user_id, behavior_prompt)
    return jsonify({
        "message": "Configuración del modelo guardada correctamente.",
        "settings": updated_settings,
    }), 200


@app.route('/credits', methods=['POST'])
def manage_credits():
    admin_user_id, admin_account, auth_error = require_admin_user()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    action = normalize_text(data.get('action')).lower()
    amount = data.get('amount', 0)
    target_user_id = data.get('target_user_id', admin_user_id)

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return jsonify({"message": "El monto de créditos no es válido."}), 400

    try:
        target_user_id = int(target_user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "El usuario objetivo no es válido."}), 400

    if action not in {'add', 'subtract', 'set'}:
        return jsonify({"message": "La acción de créditos no es válida."}), 400

    if amount < 0:
        return jsonify({"message": "El monto de créditos debe ser positivo."}), 400

    current_account = get_user_account(target_user_id)
    if not current_account:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if action == 'add':
        updated_account = update_user_credits(target_user_id, current_account['creditos'] + amount)
    elif action == 'subtract':
        updated_account = update_user_credits(target_user_id, current_account['creditos'] - amount)
    else:
        updated_account = update_user_credits(target_user_id, amount)

    return jsonify({
        "message": "Créditos actualizados correctamente.",
        "creditos": updated_account['creditos'],
        "target_user_id": updated_account['id'],
        "target_user_name": updated_account['nombre'],
        "updated_by": admin_account['nombre'],
    }), 200


@app.route('/admin/users', methods=['POST'])
def admin_create_user():
    _, _, auth_error = require_admin_user()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    nombre = normalize_text(data.get('nombre'))
    password = normalize_text(data.get('password'))
    empresa = normalize_text(data.get('empresa'))
    tipo_usuario = normalize_user_type(data.get('tipo_usuario'))
    creditos = data.get('creditos', DEFAULT_CREDITS)

    if not nombre or not password or not empresa:
        return jsonify({"message": "Nombre, contraseña y empresa son obligatorios."}), 400

    if len(password) < 6:
        return jsonify({"message": "La contraseña debe tener al menos 6 caracteres."}), 400

    try:
        creditos = int(creditos)
    except (TypeError, ValueError):
        return jsonify({"message": "Los créditos iniciales no son válidos."}), 400

    if creditos < 0:
        return jsonify({"message": "Los créditos iniciales deben ser positivos."}), 400

    database = get_db()
    existing_user = database.execute_query(
        'SELECT id FROM usuarios WHERE nombre = ?',
        (nombre,)
    ) or []

    if existing_user:
        return jsonify({"message": "El usuario ya existe."}), 409

    created_user = create_user_account(nombre, password, empresa, tipo_usuario, creditos)
    return jsonify({
        "message": "Usuario creado correctamente.",
        "user": created_user,
    }), 201


@app.route('/admin/users/<int:target_user_id>/delete', methods=['POST'])
def admin_delete_user(target_user_id):
    admin_user_id, _, auth_error = require_admin_user()
    if auth_error:
        return auth_error

    if target_user_id == admin_user_id:
        return jsonify({"message": "No puedes eliminar tu propio usuario administrador desde este panel."}), 400

    target_account = get_user_account(target_user_id)
    if not target_account:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if target_account['tipo_usuario'] == ADMIN_ROLE and count_admin_users() <= 1:
        return jsonify({"message": "Debe existir al menos un administrador activo en el sistema."}), 400

    deleted_user = delete_user_account(target_user_id)
    return jsonify({
        "message": "Usuario eliminado correctamente.",
        "user": deleted_user,
    }), 200


@app.route('/api/files', methods=['GET'])
def list_uploaded_files():
    user_id, _, auth_error = require_api_user()
    if auth_error:
        return auth_error

    user_files = get_user_files(user_id)
    return jsonify({
        "files": [file_record['original_name'] for file_record in user_files],
        "items": user_files,
        "total": len(user_files),
    })


@app.route('/files/<int:file_id>/toggle', methods=['POST'])
def toggle_user_file(file_id):
    user_id, auth_error = require_session_user()
    if auth_error:
        return auth_error

    file_record = get_user_file_by_id(user_id, file_id)
    if not file_record:
        return jsonify({"message": "Archivo no encontrado."}), 404

    updated_file = update_user_file_status(user_id, file_id, not file_record['is_active'])
    action_message = 'Archivo activado correctamente.' if updated_file['is_active'] else 'Archivo desactivado correctamente.'
    return jsonify({"message": action_message, "file": updated_file}), 200


@app.route('/files/<int:file_id>/delete', methods=['POST'])
def delete_user_file_route(file_id):
    user_id, auth_error = require_session_user()
    if auth_error:
        return auth_error

    deleted_file = delete_user_file(user_id, file_id)
    if not deleted_file:
        return jsonify({"message": "Archivo no encontrado."}), 404

    return jsonify({"message": "Archivo eliminado correctamente.", "file": deleted_file}), 200


@app.route('/api/widget/chat', methods=['POST', 'OPTIONS'])
def widget_chat():
    if request.method == 'OPTIONS':
        return add_widget_cors_headers(make_response('', 204))

    def widget_error(message, status_code, extra_payload=None):
        payload = {"message": message}
        if extra_payload:
            payload.update(extra_payload)
        response = jsonify(payload)
        response.status_code = status_code
        return add_widget_cors_headers(response)

    data = request.get_json(silent=True) or {}
    widget_token = normalize_text(data.get('widget_token'))
    mensaje = normalize_text(data.get('prompt') or data.get('mensaje'))

    if not widget_token:
        return widget_error("El widget_token es obligatorio.", 400)

    if not mensaje:
        return widget_error("El prompt es obligatorio.", 400)

    account = get_user_by_widget_token(widget_token)
    if not account:
        return widget_error("Token del widget no válido.", 401)

    if account['creditos'] <= 0:
        return widget_error(
            "No tienes créditos disponibles para usar el widget.",
            402,
            {"creditos_restantes": 0},
        )

    archivos_activos = get_user_files(account['id'], only_active=True)
    if not archivos_activos:
        return widget_error("No hay archivos activos configurados para este widget.", 404)

    try:
        result = ejecutar_chat_archivo(
            archivos_activos[0]['stored_name'],
            mensaje,
            custom_behavior=get_user_model_behavior(account['id']),
        )
    except FileNotFoundError:
        return widget_error("El archivo de contexto no existe.", 404)
    except requests.RequestException as exc:
        return widget_error(f"Error al consultar el modelo: {str(exc)}", 502)

    updated_account = change_user_credits(account['id'], -1)
    payload = jsonify({
        "respuesta": result['respuesta'],
        "modelo": result['modelo'],
        "archivo": archivos_activos[0]['original_name'],
        "creditos_restantes": updated_account['creditos'] if updated_account else 0,
    })
    payload.status_code = 200
    return add_widget_cors_headers(payload)


@app.route('/api/chat', methods=['POST'])
def api_chat_with_file():
    user_id, _, auth_error = require_api_user()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    mensaje = (data.get('prompt') or data.get('mensaje') or '').strip()
    nombre_archivo = (data.get('archivo') or data.get('filename') or '').strip()
    

    if not mensaje:
        return jsonify({"message": "El campo 'prompt' es obligatorio"}), 400

    if not nombre_archivo:
        return jsonify({"message": "El campo 'archivo' es obligatorio"}), 400

    file_record = get_user_file_by_reference(user_id, nombre_archivo, require_active=True)
    if not file_record:
        return jsonify({"message": "El archivo no existe para este usuario o está desactivado."}), 404

    try:
        result = ejecutar_chat_archivo(
            file_record['stored_name'],
            mensaje,
            custom_behavior=get_user_model_behavior(user_id),
        )
        result['archivo'] = file_record['original_name']
        result['archivo_id'] = file_record['id']
        return jsonify(result), 200
    except FileNotFoundError:
        return jsonify({"message": "El archivo solicitado no existe en uploads"}), 404
    except requests.RequestException as exc:
        return jsonify({"message": f"Error al consultar el modelo: {str(exc)}"}), 502


#Funcion de testeo de conexion
@app.route("/test_connection", methods=["GET", "POST"])
def index():
    if "usuario" not in session or not session.get("user_id"):
        session.clear()
        return redirect(url_for("Login"))

    respuesta = ""
    mensaje = "" 

    # leer archivo 
    if request.method == "POST":
        #leer elmensaje del usuario y generr una peticion para el modelo RAG
        mensaje = request.form.get("mensaje")
        archivos = get_user_files(session.get("user_id"), only_active=True)
        model_behavior = get_user_model_behavior(session.get("user_id"))

        if mensaje and archivos:
            try:
                result = ejecutar_chat_archivo(
                    archivos[0]['stored_name'],
                    mensaje,
                    custom_behavior=model_behavior,
                )
                respuesta = result["respuesta"]
            except (FileNotFoundError, requests.RequestException):
                respuesta = "No fue posible generar una respuesta en este momento."
        elif mensaje:
            respuesta = "No hay archivos PDF activos disponibles para construir el contexto."

        #Agregar al contexto
        
    return render_template(
        "index.html",
        mensaje=mensaje,
        respuesta=respuesta,
        model_behavior=get_user_model_behavior(session.get("user_id")),
    )

if __name__ == "__main__":
    app.run(debug=True)