from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory
from backend import *
import requests
import sqlite3
import os
from werkzeug.utils import secure_filename
import PyPDF2
from general_func.chatting import Chating_func
from general_func.BD_conn import BD_conn
# Configuracion del servidor
app = Flask(__name__)
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
    return render_template("main.html")

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
    data = request.get_json()
    # Conectar a la base de datos SQLite (se creará si no existe)
        #testar si ya existia una conexion previa 
    if BD_conn.instancia == 0:
        global bd
        bd = BD_conn()
    
    # Insertar los datos recibidos en la tabla
    bd.execute_query('INSERT INTO usuarios (nombre,password,empresa) VALUES (?,?,?)', (str(data['nombre']),str(data['password']),str(data['empresa']),))

    return jsonify({"message": "Datos recibidos correctamente."})



# --- Cache para login ---
login_cache = {}

# --- Logout ---
@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    if not usuario or not password:
        return jsonify({"message": "Faltan campos"}), 400
    cache_key = f"{usuario}:{password}"
    print(f"Eliminando sesión de caché para {login_cache}")
    if cache_key in login_cache:
        del login_cache[cache_key]
        return jsonify({"message": "Logout exitoso"}), 200
    else:
        return jsonify({"message": "No hay sesión activa para ese usuario"}), 404

@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        contenido = request.get_json()
        usuario = contenido.get("usuario")
        password = contenido.get("password")

        if not usuario or not password:
            return jsonify({"message": "Faltan campos"}), 400

        # Verificar en caché primero
        cache_key = f"{usuario}:{password}"
        if cache_key in login_cache:
            empresa = login_cache[cache_key]
            return jsonify({"message": "Credenciales correctas","usuario":usuario,"empresa":empresa}), 200

        # Si no está en caché, es obligatorio pasar por el login real
        if BD_conn.instancia == 0:
            global bd
            bd = BD_conn()

        result = bd.execute_query("SELECT id,empresa FROM usuarios WHERE nombre = ? AND password = ?", (usuario, password))
        print(result,usuario,password)
        if result and len(result) > 0:
            empresa = result[0][1]
            # Guardar en caché solo si el login es correcto
            login_cache[cache_key] = empresa
            return jsonify({"message": "Credenciales correctas","usuario":usuario,"empresa":empresa}), 200
        else:
            # No guardar en caché si el login falla
            return jsonify({"message": "Credenciales incorrectas"}), 401
    else:
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