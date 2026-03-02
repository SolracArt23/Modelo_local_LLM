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
@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        contenido = request.get_json()
        usuario = contenido.get("usuario")
        password = contenido.get("password")

        if not usuario or not password:
            return jsonify({"message": "Faltan campos"}), 400

        #testar si ya existia una conexion previa 
        if BD_conn.instancia == 0:
            global bd
            bd = BD_conn()
        
        #enviar respuesta al servidor de autenticacion
        result = bd.execute_query("SELECT id,empresa FROM usuarios WHERE nombre = ? AND password = ?", (usuario, password))[0] 
        print(result,usuario,password)
        if result:
            return jsonify({"message": "Credenciales correctas","usuario":usuario,"empresa":result[1]}), 200
        else:
            return jsonify({"message": "Credenciales incorrectas"}), 401
    else:
        return render_template("login.html")
#Funcion de login y resgistro
@app.route('/Envio_datos', methods=['POST'])
def registrar():
    data = request.get_json()
    print(data)  # Aquí guardarías en base de datos o procesas
    # Conectar a la base de datos SQLite (se creará si no existe)
        #testar si ya existia una conexion previa 
    if BD_conn.instancia == 0:
        global bd
        bd = BD_conn()
    
    # Insertar los datos recibidos en la tabla
    bd.execute_query('INSERT INTO usuarios (nombre,password,empresa) VALUES (?,?,?)', (str(data['nombre']),str(data['password']),str(data['empresa']),))

    return jsonify({"message": "Datos recibidos correctamente."})

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