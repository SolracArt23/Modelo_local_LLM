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


#Funcion de testeo de conexion
@app.route("/test_connection", methods=["GET", "POST"])
def index():
    respuesta = ""
    mensaje = "" 

    # leer archivo 
    if request.method == "POST":
        #Validacion la creacion de la funcion
        if Chating_func.instancia == 0:
            global chatting
            chatting = Chating_func(folder_chatting=app.config['UPLOAD_FOLDER'])

        #leer elmensaje del usuario y generr una peticion para el modelo RAG
        mensaje = request.form.get("mensaje")
        peticion = chatting.RAG_model(mensaje)

        print(peticion)
        r = requests.post("http://127.0.0.1:11434/api/chat", json=peticion)
        respuesta = r.json()["message"]["content"]

        #Agregar al contexto
        
    return render_template("index.html", mensaje=mensaje, respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)