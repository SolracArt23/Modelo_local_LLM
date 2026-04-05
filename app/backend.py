from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory, redirect, url_for, session
from backend import *
import requests
import sqlite3
import os
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


def is_password_hash(password_value):
    return password_value.startswith("scrypt:") or password_value.startswith("pbkdf2:")


def verify_user_password(stored_password, plain_password):
    if is_password_hash(stored_password):
        return check_password_hash(stored_password, plain_password)
    return stored_password == plain_password


def normalize_text(value):
    return (value or "").strip()


def ejecutar_chat_archivo(nombre_archivo, mensaje):
    chatting = Chating_func(
        folder_chatting=app.config['UPLOAD_FOLDER'],
        selected_file=nombre_archivo,
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
    if "usuario" not in session:
        return redirect(url_for("Login"))

    return render_template(
        "main.html",
        usuario=session.get("usuario"),
        empresa=session.get("empresa"),
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
    ensure_users_table()

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

        session["usuario"] = stored_name
        session["empresa"] = empresa
        return jsonify({"message": "Credenciales correctas","usuario":stored_name,"empresa":empresa}), 200
    else:
        if "usuario" in session:
            return redirect(url_for("main"))
        return render_template("login.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No se envió ningún archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No se seleccionó ningún archivo"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Archivo no permitido"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"message": "Archivo subido correctamente", "filename": filename}), 200


@app.route('/api/files', methods=['GET'])
def list_uploaded_files():
    return jsonify({"files": get_uploaded_pdf_files()})


@app.route('/api/chat', methods=['POST'])
def api_chat_with_file():
    data = request.get_json(silent=True) or {}
    mensaje = (data.get('prompt') or data.get('mensaje') or '').strip()
    nombre_archivo = (data.get('archivo') or data.get('filename') or '').strip()

    if not mensaje:
        return jsonify({"message": "El campo 'prompt' es obligatorio"}), 400

    if not nombre_archivo:
        return jsonify({"message": "El campo 'archivo' es obligatorio"}), 400

    if not allowed_file(nombre_archivo):
        return jsonify({"message": "Solo se permiten archivos PDF"}), 400

    try:
        result = ejecutar_chat_archivo(nombre_archivo, mensaje)
        return jsonify(result), 200
    except FileNotFoundError:
        return jsonify({"message": "El archivo solicitado no existe en uploads"}), 404
    except requests.RequestException as exc:
        return jsonify({"message": f"Error al consultar el modelo: {str(exc)}"}), 502


#Funcion de testeo de conexion
@app.route("/test_connection", methods=["GET", "POST"])
def index():
    respuesta = ""
    mensaje = "" 

    # leer archivo 
    if request.method == "POST":
        #leer elmensaje del usuario y generr una peticion para el modelo RAG
        mensaje = request.form.get("mensaje")
        archivos = get_uploaded_pdf_files()

        if mensaje and archivos:
            try:
                result = ejecutar_chat_archivo(archivos[0], mensaje)
                respuesta = result["respuesta"]
            except (FileNotFoundError, requests.RequestException):
                respuesta = "No fue posible generar una respuesta en este momento."
        elif mensaje:
            respuesta = "No hay archivos PDF disponibles en uploads para construir el contexto."

        #Agregar al contexto
        
    return render_template("index.html", mensaje=mensaje, respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)