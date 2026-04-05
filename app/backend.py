from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory, redirect, url_for, session
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
            empresa TEXT NOT NULL
        )
        '''
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

    return render_template(
        "main.html",
        usuario=session.get("usuario"),
        empresa=session.get("empresa"),
        user_files=get_user_files(session.get("user_id")),
        model_behavior=get_user_model_behavior(session.get("user_id")),
    )

@app.route("/descargar_api")
def descargar_api():
    return send_from_directory(
        directory="static",
        path="Api.html",
        as_attachment=True  # Esto fuerza la descarga
    )


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

    password_hash = generate_password_hash(password)
    database.execute_query(
        'INSERT INTO usuarios (nombre,password,empresa) VALUES (?,?,?)',
        (nombre, password_hash, empresa)
    )

    return jsonify({"message": "Usuario registrado correctamente.", "usuario": nombre, "empresa": empresa}), 201


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

        session["user_id"] = user_id
        session["usuario"] = stored_name
        session["empresa"] = empresa
        return jsonify({"message": "Credenciales correctas","usuario":stored_name,"empresa":empresa}), 200
    else:
        if "usuario" in session:
            return redirect(url_for("main"))
        return render_template("login.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    user_id, auth_error = require_session_user()
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


@app.route('/api/files', methods=['GET'])
def list_uploaded_files():
    user_id, auth_error = require_session_user()
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


@app.route('/api/chat', methods=['POST'])
def api_chat_with_file():
    user_id, auth_error = require_session_user()
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