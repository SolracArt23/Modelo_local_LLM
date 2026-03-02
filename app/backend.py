from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory
from backend import *
import requests
import sqlite3
import os
from werkzeug.utils import secure_filename
import PyPDF2
from general_func.chatting import Chating_func
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

        try:
            conn = sqlite3.connect('db/mi_base.db')
            cursor = conn.cursor()

            # Usar parámetros seguros para evitar SQL Injection
            cursor.execute("SELECT id,empresa FROM usuarios WHERE nombre = ? AND password = ?", (usuario, password))
            result = cursor.fetchone()
            print(result)
            conn.close()

            if result:
                return jsonify({"message": "Credenciales correctas","usuario":usuario,"empresa":result[1]}), 200
            else:
                return jsonify({"message": "Credenciales incorrectas"}), 401

        except Exception as e:
            return jsonify({"message": f"Error del servidor: {str(e)}"}), 500

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