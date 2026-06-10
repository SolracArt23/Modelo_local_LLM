# Modelo local LLM con Flask y RAG sobre PDF

Este proyecto implementa una aplicacion web en Flask para interactuar con un modelo LLM local mediante Ollama. El sistema permite registrar usuarios, cargar archivos PDF, usar ese contenido como contexto tipo RAG y consultar el modelo desde la interfaz web.

## Que hace el proyecto

- Levanta una aplicacion web con Flask.
- Usa una base de datos SQLite local para usuarios y configuracion.
- Permite subir archivos PDF al directorio `uploads/`.
- Extrae texto del PDF con `PyPDF2`.
- Envia preguntas al modelo local a traves de la API de Ollama.
- Soporta personalizacion de comportamiento del modelo por usuario.

## Librerias principales

Estas son las librerias detectadas en el codigo del proyecto:

- `flask`: framework web usado para rutas, vistas HTML, sesiones y respuestas JSON.
- `requests`: cliente HTTP usado para enviar peticiones al endpoint local de Ollama.
- `PyPDF2`: lectura y extraccion de texto desde archivos PDF.
- `werkzeug`: utilidades de Flask para manejo seguro de archivos y hash de contrasenas.
- `sqlite3`: base de datos local incluida en Python, usada para persistencia.
- `os`, `datetime`, `uuid`, `threading`: modulos estandar de Python usados para archivos, fechas, tokens y concurrencia.

## Requisitos previos

Antes de ejecutar el proyecto necesitas tener instalado:

- Python 3.9 o superior.
- `pip`.
- Ollama instalado y ejecutandose localmente.
- El modelo descargado en Ollama. En el codigo aparecen referencias a `llama3` y `llama3.1:latest`.

## Instalacion

Si vas a usar un entorno virtual nuevo en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias principales del proyecto:

```powershell
pip install flask requests PyPDF2 werkzeug
```

Si vas a usar Ollama, asegurate de tener el modelo disponible:

```powershell
ollama pull llama3
ollama pull llama3.1:latest
```

Luego inicia Ollama en tu maquina. El proyecto espera encontrar la API en:

```text
http://127.0.0.1:11434
```

## Archivo que debe ejecutar el programador

El archivo principal recomendado para ejecutar la aplicacion es:

```text
app/backend.py
```

Ejecutalo desde la raiz del proyecto con:

```powershell
python app/backend.py
```

Ese archivo:

- crea la aplicacion Flask,
- prepara las tablas principales en SQLite,
- administra usuarios, creditos y widgets,
- procesa PDFs cargados,
- y expone las rutas principales del sistema.

## Archivos importantes

- `app/backend.py`: punto de entrada principal de la aplicacion.
- `app/ai-conexion.py`: version simplificada con rutas de carga, login y prueba de conexion.
- `app/general_func/chatting.py`: construccion del contexto RAG y lectura del PDF.
- `app/general_func/BD_conn.py`: conexion SQLite y ejecucion de consultas.
- `app/templates/`: vistas HTML del sistema.
- `app/static/`: archivos estaticos.
- `uploads/`: PDFs cargados por la aplicacion.
- `db/mi_base.db`: base de datos SQLite generada o reutilizada por el sistema.

## Flujo de ejecucion esperado

1. Activar el entorno virtual.
2. Iniciar Ollama localmente.
3. Verificar que el modelo exista en Ollama.
4. Ejecutar `python app/backend.py`.
5. Abrir en el navegador la URL local mostrada por Flask, normalmente `http://127.0.0.1:5000`.

## Notas tecnicas

- La clave secreta de Flask se toma desde la variable de entorno `SECRET_KEY`. Si no existe, usa un valor por defecto de desarrollo.
- La ruta de la base de datos puede configurarse con la variable de entorno `DB_PATH`.
- El proyecto crea automaticamente la carpeta `uploads/` si no existe.
- La base de datos SQLite tambien se crea automaticamente si no existe.

## Ejemplo rapido de arranque

```powershell
.\.venv\Scripts\Activate.ps1
python app/backend.py
```

Si Ollama ya esta corriendo, con eso deberias poder entrar a la aplicacion desde el navegador.

## Ejecutar con Docker

Tambien puedes levantar todo el entorno con Docker, incluyendo la aplicacion Flask y un contenedor de Ollama.

### Archivos agregados para Docker

- `Dockerfile`: construye la imagen de la aplicacion Python.
- `docker-compose.yml`: levanta la web, Ollama y descarga el modelo automaticamente.
- `.dockerignore`: evita copiar archivos innecesarios al contexto de build.
- `requirements.txt`: dependencias Python necesarias para la app.

### Requisito en el host

- Docker Desktop instalado y ejecutandose.

### Construccion y arranque

Desde la raiz del proyecto ejecuta:

```powershell
docker compose up --build
```

Si quieres dejarlo ejecutandose en segundo plano:

```powershell
docker compose up --build -d
```

Ese comando hace lo siguiente:

- construye la imagen de la aplicacion,
- inicia un contenedor con Ollama,
- descarga automaticamente el modelo `llama3.1:latest`,
- y luego levanta la aplicacion web.

En la primera ejecucion, la descarga del modelo puede tardar varios minutos porque baja aproximadamente 4.9 GB.

### URLs esperadas

- Aplicacion web: `http://127.0.0.1:5000`

En esta configuracion Docker, Ollama queda accesible solo dentro de la red interna de Compose para evitar conflictos si ya tienes Ollama ejecutandose en el host.

### Detener los contenedores

```powershell
docker compose down
```

Si tambien quieres eliminar el volumen donde Ollama guarda el modelo descargado:

```powershell
docker compose down -v
```

### Variables usadas en Docker

En `docker-compose.yml` se configuran estas variables importantes:

- `OLLAMA_URL=http://ollama:11434/api/chat`
- `FLASK_HOST=0.0.0.0`
- `FLASK_PORT=5000`
- `DB_PATH=db/mi_base.db`

### Nota importante sobre el modelo

La configuracion de Docker descarga `llama3.1:latest`, porque es el modelo referenciado en la logica principal del proyecto. Si quieres usar otro modelo, debes cambiar:

- el nombre del modelo en `docker-compose.yml`,
- y, si aplica, el modelo enviado desde el codigo Python.

### Verificar que quedo corriendo

Puedes revisar el estado de los contenedores con:

```powershell
docker compose ps
```

Y validar que la web responde con:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000 -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

Si todo esta bien, ese comando debe devolver `200`.

### Estado validado en esta configuracion

La aplicacion fue probada en este entorno con los siguientes resultados:

- `docker compose up --build -d` completo la construccion y el arranque.
- `ollama-init` descargo correctamente el modelo `llama3.1:latest`.
- `docker compose ps` dejo `modelo-local-ollama` en estado `healthy` y `modelo-local-web` en ejecucion.
- `http://127.0.0.1:5000` respondio con codigo HTTP `200`.