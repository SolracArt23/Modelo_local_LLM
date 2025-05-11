from flask import Flask, request, render_template_string,render_template, jsonify,send_from_directory
from backend import *
import requests
import sqlite3
import os
from werkzeug.utils import secure_filename
import PyPDF2

# Configuracion del servidor
app = Flask(__name__)
# Configuración para subir archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de subida si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Verificar si se envió un archivo
        if 'file' not in request.files:
            return jsonify({"message": "No se envió ningún archivo"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No se seleccionó ningún archivo"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": "Archivo subido correctamente", "filename": filename}), 200
        else:
            return jsonify({"message": "Archivo no permitido"}), 400
    return render_template("upload.html")


#Funcion de login y resgistro
@app.route('/Envio_datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print(data)  # Aquí guardarías en base de datos o procesas
    # Conectar a la base de datos SQLite (se creará si no existe)
    conn = sqlite3.connect('db/mi_base.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    # Insertar los datos recibidos en la tabla
    cursor.execute('INSERT INTO usuarios (nombre,password,empresa) VALUES (?,?,?)', (str(data['nombre']),str(data['password']),str(data['empresa']),))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    return jsonify({"message": "Datos recibidos correctamente."})



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

#Funcion de testeo de conexion
@app.route("/test_connection", methods=["GET", "POST"])
def index():
    respuesta = ""
    mensaje = ""
    # Leer el archivo PDF cargado
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if uploaded_files:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0])
        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                pdf_content = ""
                for page in reader.pages:
                    pdf_content += page.extract_text()
            context = [{"role": "system", "content": f"El contenido del archivo PDF cargado es: {pdf_content}"}]
        except Exception as e:
            context = [{"role": "system", "content": ""}]
    else:
        context = [{"role": "system", "content": ""}]
    #context = [{"role": "user", "content": "Existen 3 personas en este servidor carlos un estudiante de IA, juan un micologo y adriana una literaria con base en ello comportate como su profesor, no cometes anda de los otros estudiantes",}]

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        #Agregar nueva peticion 
        context += [{"role": "user", "content": mensaje,}]
        peticion ={
            "model": "llama3",
            "messages": context,
            "stream": False,
            
        }
        #Agregar el contexto si lo hay  

        print(peticion)
        r = requests.post("http://127.0.0.1:11434/api/chat", json=peticion)
        respuesta = r.json()["message"]["content"]

        #Agregar al contexto
        
    return render_template("index.html", mensaje=mensaje, respuesta=respuesta)


# PAgina de aurora
@app.route("/aurora")
def Aurora():
    return render_template("pagina-nomral.html")
#Ejecucion 
if __name__ == "__main__":
    app.run(debug=True)
