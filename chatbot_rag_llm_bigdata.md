# Chatbot RAG + LLM — Guía de Desarrollo Big Data

## Descripción general

Este proyecto es un chatbot de inteligencia artificial basado en la arquitectura **RAG (Retrieval-Augmented Generation)** que utiliza modelos de lenguaje grande (**LLM**) ejecutados localmente mediante **Ollama**. Permite a los usuarios cargar documentos PDF como base de conocimiento, realizar consultas en lenguaje natural y obtener respuestas contextualizadas con los documentos proporcionados.

---

## Arquitectura del sistema

```
┌─────────────┐     HTTP/REST      ┌──────────────────────────┐
│  Frontend   │ ◄────────────────► │  Flask Backend (app/)    │
│  (HTML/JS)  │                    │  backend.py              │
└─────────────┘                    └──────────┬───────────────┘
                                              │
                          ┌───────────────────┼────────────────────┐
                          │                   │                    │
                   ┌──────▼──────┐   ┌────────▼────────┐  ┌───────▼──────┐
                   │ Chating_func│   │    BD_conn       │  │ Ollama API   │
                   │ (RAG Model) │   │ (SQLite - Users) │  │ llama3.1     │
                   └──────┬──────┘   └─────────────────┘  └──────────────┘
                          │
                   ┌──────▼──────┐
                   │  uploads/   │
                   │  (PDFs)     │
                   └─────────────┘
```

### Componentes principales

| Componente | Archivo | Descripción |
|---|---|---|
| Servidor Flask | `app/backend.py` | API REST y gestión de rutas |
| Modelo RAG | `app/general_func/chatting.py` | Extracción de PDF y construcción del contexto |
| Conexión BD | `app/general_func/BD_conn.py` | Gestión de base de datos SQLite con thread safety |
| Widget API | `app/static/Api.html` | Widget de chat embebible para sitios externos |
| Tests | `Tests/test_con.py` | Verificación de conexión y datos en BD |

---

## Stack tecnológico

- **Backend:** Python 3.9+, Flask
- **LLM local:** [Ollama](https://ollama.com/) con modelo `llama3.1:latest`
- **RAG:** PyPDF2 para extracción de texto desde PDFs
- **Base de datos:** SQLite (thread-safe con `threading.Lock`)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript vanilla

---

## Instalación y configuración

### 1. Requisitos previos

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar el modelo LLaMA 3.1
ollama pull llama3.1:latest
```

### 2. Entorno virtual y dependencias

```bash
# Crear y activar el entorno virtual
python3 -m venv env
source env/bin/activate        # Linux/macOS
env\Scripts\activate           # Windows

# Instalar dependencias
pip install flask requests PyPDF2 werkzeug
```

### 3. Configuración de la base de datos

Crear el directorio y la base de datos con la tabla de usuarios:

```bash
mkdir -p db
```

```python
import sqlite3
conn = sqlite3.connect('db/mi_base.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        password TEXT NOT NULL,
        empresa TEXT
    )
''')
conn.commit()
conn.close()
```

### 4. Variables de entorno

Editar el archivo `.env` en la raíz del proyecto:

```env
# Ruta a la base de datos. Puede ser relativa al root del proyecto o absoluta.
DB_PATH=db/mi_base.db
```

### 5. Ejecutar el servidor

```bash
cd app
python backend.py
```

El servidor estará disponible en `http://127.0.0.1:5000`.  
Ollama debe estar corriendo en `http://127.0.0.1:11434`.

---

## API REST — Endpoints

### Autenticación

#### `POST /login`
Autentica a un usuario. Implementa caché en memoria para evitar consultas repetidas a la BD.

**Request:**
```json
{
  "usuario": "carlos",
  "password": "mi_password"
}
```

**Response exitosa (200):**
```json
{
  "message": "Credenciales correctas",
  "usuario": "carlos",
  "empresa": "TechCorp"
}
```

**Response fallida (401):**
```json
{ "message": "Credenciales incorrectas" }
```

---

#### `POST /Envio_datos`
Registra un nuevo usuario en la base de datos.

**Request:**
```json
{
  "nombre": "carlos",
  "password": "mi_password",
  "empresa": "TechCorp"
}
```

**Response (200):**
```json
{ "message": "Datos recibidos correctamente." }
```

---

#### `POST /logout`
Elimina la sesión del usuario de la caché en memoria.

**Request:**
```json
{
  "usuario": "carlos",
  "password": "mi_password"
}
```

**Response exitosa (200):**
```json
{ "message": "Logout exitoso" }
```

---

### Gestión de documentos

#### `POST /upload`
Sube un archivo PDF al servidor. Este PDF se utilizará como contexto del RAG.

**Content-Type:** `multipart/form-data`  
**Campo:** `file` — archivo `.pdf`

**Response exitosa (200):**
```json
{
  "message": "Archivo subido correctamente",
  "filename": "documento.pdf"
}
```

---

### Chat e interacción con el LLM

#### `GET/POST /test_connection`
Interfaz de chat. Recibe un mensaje del usuario, lo procesa con el modelo RAG y retorna la respuesta del LLM.

**Request (POST, form-data):**
```
mensaje=¿Cuál es el resumen del documento?
```

**Response:** Página HTML con el mensaje del usuario y la respuesta del LLM.

---

### Páginas y utilidades

| Endpoint | Método | Descripción |
|---|---|---|
| `/` | GET | Dashboard principal |
| `/login` | GET | Página de login/registro |
| `/descargar_api` | GET | Descarga el widget `Api.html` para embeber en sitios externos |
| `/aurora` | GET | Página personalizada Aurora |

---

## Pipeline RAG — Funcionamiento detallado

El flujo completo de una consulta RAG sigue estos pasos:

```
Usuario envía mensaje
        │
        ▼
Chating_func.RAG_model(mensaje)
        │
        ├── Lee PDFs de uploads/ (Read_content)
        │         └── Extrae texto con PyPDF2
        │
        ├── Construye contexto:
        │   [{"role": "system", "content": "<texto_del_PDF>"},
        │    {"role": "user",   "content": "<mensaje_usuario>"}]
        │
        └── Genera petición para Ollama:
            {
              "model": "llama3.1:latest",
              "messages": [...contexto...],
              "stream": false
            }
                    │
                    ▼
        POST http://127.0.0.1:11434/api/chat
                    │
                    ▼
        response["message"]["content"]  →  Respuesta al usuario
```

### Clase `Chating_func`

```python
# app/general_func/chatting.py

class Chating_func():
    instancia = 0           # Contador de instancias (singleton ligero)

    def __init__(self, folder_chatting: str = None):
        Chating_func.instancia += 1
        self.folder_chatting = folder_chatting
        self.content_pdf = self.Read_content()  # Carga PDF al iniciar

    def Read_content(self) -> str:
        # Lee el primer PDF en la carpeta uploads/ y extrae su texto
        ...

    def RAG_model(self, mensaje: str) -> dict:
        # Construye y retorna el payload para la API de Ollama
        ...
```

> **Nota:** La instancia de `Chating_func` se crea una sola vez por sesión del servidor (patrón singleton). Si se sube un nuevo PDF, es necesario reiniciar el servidor o reimplementar la recarga dinámica del contenido.

---

## Base de datos — Esquema

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre   TEXT NOT NULL,
    password TEXT NOT NULL,
    empresa  TEXT
);
```

### Clase `BD_conn`

- **Thread-safe:** Utiliza `threading.Lock()` para acceso concurrente seguro.
- **Configuración:** La ruta a la BD se lee del entorno (`DB_PATH`, por defecto `db/mi_base.db`).
- **Singleton:** El contador `instancia` evita múltiples inicializaciones en el mismo proceso Flask.

---

## Widget embebible (`Api.html`)

El archivo `app/static/Api.html` es un widget de chat flotante listo para insertar en cualquier sitio web. Se descarga desde `/descargar_api` y se incrusta directamente en el HTML del sitio cliente.

**Características:**
- Botón flotante (💬) en la esquina inferior derecha
- Ventana de chat desplegable
- Envía mensajes al endpoint `POST /test_connection` del servidor

**Uso:**
1. Descargar `Api.html` desde el panel principal.
2. Copiar el contenido del `<script>` y los estilos al sitio web destino.
3. Actualizar la URL `http://127.0.0.1:5000/test_connection` con la IP/dominio del servidor de producción.

---

## Integración con Big Data

### Procesamiento de documentos a gran escala

Para escalar el procesamiento de PDFs y soportar grandes volúmenes de datos, se recomienda:

#### 1. Indexación vectorial (recomendado)

Reemplazar el contexto completo del PDF por fragmentos relevantes usando una base de datos vectorial:

```python
# Ejemplo de integración con ChromaDB
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.create_collection("documentos")

# Indexar fragmentos del PDF
fragments = split_text(pdf_content, chunk_size=500)
collection.add(
    documents=fragments,
    ids=[f"frag_{i}" for i in range(len(fragments))]
)

# Recuperar fragmentos relevantes para la consulta
results = collection.query(query_texts=[mensaje], n_results=3)
contexto_relevante = "\n".join(results["documents"][0])
```

#### 2. Cola de procesamiento asíncrono

Para manejar múltiples usuarios simultáneos con documentos grandes:

```python
# Integración con Celery + Redis
from celery import Celery

app_celery = Celery('tasks', broker='redis://localhost:6379/0')

@app_celery.task
def procesar_pdf_async(pdf_path: str) -> str:
    """Procesa un PDF de forma asíncrona y almacena su contenido."""
    ...
```

#### 3. Base de datos relacional para escala

Migrar de SQLite a PostgreSQL para soportar mayor concurrencia:

```env
# .env para producción
DB_PATH=postgresql://user:password@localhost:5432/chatbot_db
```

#### 4. Múltiples archivos PDF en el contexto

Extender `Chating_func.Read_content()` para indexar todos los PDFs disponibles:

```python
def Read_content(self) -> str:
    contenido_total = ""
    for filename in os.listdir(self.folder_chatting):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(self.folder_chatting, filename)
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        contenido_total += page.extract_text() or ""
            except Exception:
                continue
    return contenido_total
```

---

## Estructura del proyecto

```
Modelo_local_LLM/
├── .env                        # Variables de entorno (DB_PATH)
├── chatbot_rag_llm_bigdata.md  # Este archivo — documentación del proyecto
├── app/
│   ├── backend.py              # Servidor Flask principal (versión actual)
│   ├── ai-conexion.py          # Versión anterior del servidor Flask
│   ├── uploads/                # PDFs subidos por los usuarios
│   ├── db/                     # Base de datos SQLite
│   ├── general_func/
│   │   ├── chatting.py         # Clase Chating_func — pipeline RAG
│   │   └── BD_conn.py          # Clase BD_conn — acceso a SQLite
│   ├── templates/
│   │   ├── main.html           # Dashboard principal
│   │   ├── login.html          # Página de login/registro
│   │   ├── index.html          # Interfaz de chat
│   │   └── pagina-normal.html  # Página Aurora
│   └── static/
│       └── Api.html            # Widget de chat embebible
├── Tests/
│   └── test_con.py             # Test de conexión a la base de datos
└── db/
    └── mi_base.db              # Base de datos SQLite
```

---

## Pruebas

### Test de conexión a la base de datos

```bash
cd /ruta/al/proyecto
python Tests/test_con.py
```

Verifica que la base de datos existe y que la tabla `usuarios` tiene registros.

### Verificar que Ollama responde correctamente

```bash
curl -X POST http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:latest",
    "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
    "stream": false
  }'
```

### Verificar el endpoint de chat

```bash
curl -X POST http://127.0.0.1:5000/test_connection \
  -d "mensaje=¿Qué información contiene el documento?"
```

---

## Mejoras propuestas y hoja de ruta

| Prioridad | Mejora | Descripción |
|---|---|---|
| Alta | Historial de conversación | Guardar mensajes previos por sesión para mantener contexto multi-turno |
| Alta | Recarga dinámica de PDFs | Recargar `content_pdf` al subir un nuevo archivo sin reiniciar el servidor |
| Alta | Hashing de contraseñas | Usar `bcrypt` o `werkzeug.security` para no almacenar contraseñas en texto plano |
| Media | Indexación vectorial | Integrar ChromaDB o FAISS para búsqueda semántica en documentos grandes |
| Media | Soporte multi-PDF | Permitir múltiples documentos activos simultáneamente por usuario |
| Media | Streaming de respuestas | Activar `"stream": true` en Ollama para respuestas en tiempo real |
| Baja | Autenticación por tokens JWT | Reemplazar la caché en memoria por tokens JWT para sesiones stateless |
| Baja | Despliegue con Docker | Containerizar la app y Ollama con `docker-compose` |
| Baja | Soporte para otros modelos | Parametrizar el modelo LLM desde `.env` (`LLM_MODEL=llama3.1:latest`) |

---

## Contribución

1. Hacer fork del repositorio
2. Crear una rama descriptiva: `git checkout -b feature/historial-conversacion`
3. Realizar los cambios y ejecutar las pruebas
4. Abrir un Pull Request describiendo los cambios

---

## Licencia

Proyecto de desarrollo local con modelos LLM. Consultar los términos de uso de Ollama y Meta LLaMA para uso comercial.
