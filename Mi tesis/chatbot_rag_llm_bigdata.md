# Desarrollo de un Chatbot Personalizable con RAG, LLM y Big Data para Optimización Empresarial

**Autor:** Carlos Arturo Corredor Muñoz

**Universidad Nacional Abierta y a Distancia – UNAD**

**Escuela de Ciencias Básicas, Tecnología e Ingeniería – ECBTI**

**Programa: Ingeniería de Sistemas**

**Tutor:** Jaime Rubiano Llorente

**Fecha:** 16 de febrero de 2026

---

## Dedicatoria

Este trabajo está dedicado a mi familia, quienes han sido mi motor y mi mayor inspiración durante todo este proceso. Gracias por creer en mí incluso en los momentos de mayor dificultad.

A Dios, por darme la fortaleza para no rendirme y la claridad para continuar aprendiendo.

Cada línea de este proyecto refleja no solo conocimiento técnico, sino también sacrificio, perseverancia y sueños que hoy comienzan a materializarse.

---

## Agradecimientos

Expreso mi más sincero agradecimiento a la Universidad Nacional Abierta y a Distancia – UNAD, por brindarme la oportunidad de formarme profesionalmente bajo un modelo educativo que promueve la autonomía, la disciplina y el aprendizaje continuo.

A los docentes de la Escuela de Ciencias Básicas, Tecnología e Ingeniería, por su acompañamiento académico, orientación y exigencia, los cuales fueron fundamentales para el desarrollo de este proyecto.

De manera especial, agradezco a mi asesor, el profesor Jaime Rubiano Llorente, por su guía y retroalimentación constante, que permitieron fortalecer tanto la estructura como el enfoque técnico de esta propuesta.

Finalmente, agradezco a mi familia por su apoyo incondicional durante este proceso académico, siendo el pilar que impulsó cada uno de mis esfuerzos.

---

## Tabla de Contenido

1. Glosario
2. Resumen
3. Abstract
4. Introducción
   - 4.1 Contexto general del problema
   - 4.2 Planteamiento del problema
   - 4.3 Justificación
   - 4.4 Objetivo general y objetivos específicos
   - 4.5 Alcance y limitaciones
   - 4.6 Metodología resumida
   - 4.7 Estructura del documento
5. Marco Teórico
6. Metodología de Desarrollo
7. Desarrollo del Sistema
8. Resultados
9. Discusión y Análisis
10. Conclusiones
11. Referencias Bibliográficas
12. Anexos

---

## Glosario

**Arquitectura de Software:** Estructura organizacional de un sistema informático que define sus componentes, relaciones, principios de diseño y lineamientos tecnológicos para su implementación y escalabilidad.

**Big Data:** Conjunto de tecnologías y metodologías orientadas al almacenamiento, procesamiento y análisis de grandes volúmenes de datos caracterizados por su variedad, velocidad y volumen, con el fin de extraer información útil para la toma de decisiones.

**Chatbot:** Sistema informático basado en inteligencia artificial diseñado para interactuar con usuarios mediante lenguaje natural, simulando una conversación humana en tiempo real.

**Clustering:** Técnica de aprendizaje automático no supervisado que agrupa elementos en conjuntos según su similitud estadística o semántica, sin necesidad de etiquetas predefinidas.

**DBSCAN (Density-Based Spatial Clustering of Applications with Noise):** Algoritmo de clustering que agrupa puntos de datos densamente conectados y puede identificar puntos atípicos que no pertenecen a ningún clúster.

**Docker:** Plataforma de virtualización a nivel de contenedor que permite empaquetar aplicaciones y sus dependencias en unidades portables e independientes del entorno de ejecución.

**Embeddings:** Representaciones vectoriales numéricas de texto que permiten capturar relaciones semánticas entre palabras o documentos, facilitando tareas de búsqueda y recuperación de información.

**Flask:** Microframework de Python para el desarrollo de aplicaciones web, caracterizado por su simplicidad, flexibilidad y bajo nivel de acoplamiento.

**Indexación Semántica:** Proceso de organización y almacenamiento de información en estructuras optimizadas que permiten búsquedas basadas en significado y no únicamente en coincidencias exactas de palabras.

**KMeans:** Algoritmo de clustering que divide un conjunto de datos en k grupos, minimizando la varianza interna de cada clúster mediante asignaciones iterativas.

**Large Language Model (LLM):** Modelo de lenguaje de gran escala entrenado mediante técnicas de aprendizaje profundo sobre grandes volúmenes de texto, capaz de comprender y generar lenguaje natural con alta coherencia contextual.

**LLaMA (Large Language Model Meta AI):** Familia de modelos de lenguaje de código abierto desarrollados por Meta AI, diseñados para ejecutarse eficientemente en hardware de recursos limitados.

**Metodología Ágil:** Enfoque de gestión de proyectos basado en iteraciones cortas, mejora continua y adaptación constante a cambios, comúnmente implementado mediante marcos como Scrum.

**Ollama:** Herramienta de código abierto que permite ejecutar modelos de lenguaje de gran escala localmente, exponiendo una API REST para interactuar con dichos modelos.

**Procesamiento de Lenguaje Natural (NLP):** Rama de la inteligencia artificial que permite a los sistemas computacionales comprender, interpretar y generar lenguaje humano de manera automática.

**Prototipo Funcional:** Versión preliminar operativa de un sistema que permite validar su funcionamiento antes de su implementación definitiva.

**Retrieval-Augmented Generation (RAG):** Técnica que combina un sistema de recuperación de información con un modelo generativo, permitiendo que las respuestas sean construidas a partir de datos específicos previamente indexados.

**Scrum:** Marco de trabajo ágil que organiza el desarrollo en iteraciones denominadas sprints, con roles definidos y ceremonias periódicas de revisión.

**Sistema Escalable:** Sistema diseñado para aumentar su capacidad de procesamiento o almacenamiento sin comprometer su rendimiento cuando incrementa la demanda.

**SQLite:** Sistema de gestión de bases de datos relacional ligero, sin servidor, que almacena toda la información en un único archivo de disco.

**VPS (Virtual Private Server):** Servidor virtual privado que proporciona recursos de cómputo dedicados dentro de un entorno de nube compartida.

**Validación de Desempeño:** Proceso mediante el cual se evalúan métricas como precisión, velocidad de respuesta y estabilidad para determinar la eficacia de un sistema desarrollado.

---

## Resumen

El presente proyecto de grado tuvo como objetivo diseñar e implementar un chatbot inteligente basado en modelos de lenguaje de gran escala (LLM) integrados con la técnica Retrieval-Augmented Generation (RAG), con el fin de mejorar la personalización y contextualización de respuestas en entornos organizacionales. La problemática abordada se centra en la limitada capacidad de los chatbots tradicionales para utilizar información específica de cada empresa, lo que reduce su precisión y utilidad operativa.

Para su desarrollo, se adoptó un enfoque de proyecto tecnológico con metodología iterativa e incremental (Scrum). Se diseñó una arquitectura compuesta por un módulo de carga y procesamiento de documentos PDF, un sistema de indexación semántica mediante embeddings, un motor de selección contextual basado en clustering (KMeans y DBSCAN) y un modelo generativo condicionado por contexto (LLaMA 3.1). El sistema fue implementado con Flask como servicio web intermediario y SQLite para la gestión de usuarios, desplegado sobre una VPS de Hostinger con 4 núcleos y 16 GB de RAM, encapsulado en Docker.

Durante las pruebas de desempeño, el sistema procesó 20 casos de prueba en dominios de ventas y soporte técnico, alcanzando una tasa de relevancia semántica del 85% y un tiempo promedio de respuesta de 8,4 segundos. Se concluye que la integración de RAG con LLM local es técnicamente viable y constituye una solución escalable de bajo costo para optimizar procesos de atención en pequeñas y medianas empresas (PYMES).

**Palabras clave:** Chatbot, Retrieval-Augmented Generation (RAG), Modelos de Lenguaje de Gran Escala (LLM), Procesamiento de Lenguaje Natural, Big Data, Clustering, LLaMA, Flask.

---

## Abstract

This undergraduate project aimed to design and implement an intelligent chatbot architecture based on Large Language Models (LLMs) integrated with the Retrieval-Augmented Generation (RAG) technique, in order to enhance response personalization and contextualization within organizational environments. The problem addressed lies in the limited ability of traditional chatbots to incorporate organization-specific information, which reduces their accuracy and operational effectiveness.

The project followed an iterative and incremental technological development approach (Scrum). The proposed architecture includes a PDF document ingestion and processing module, a semantic indexing system using embeddings, a context selection engine based on clustering algorithms (KMeans and DBSCAN), and a context-conditioned generative model (LLaMA 3.1). The system was implemented using Flask as an intermediate web service and SQLite for user management, deployed on a Hostinger VPS with 4 cores and 16 GB of RAM, containerized with Docker to ensure portability.

During performance testing, the system processed 20 test cases in sales and technical support domains, achieving a semantic relevance rate of 85% and an average response time of 8.4 seconds in the production environment. It is concluded that the integration of local RAG and LLM technologies is technically feasible and represents a low-cost, scalable solution for optimizing customer service processes in small and medium-sized enterprises (SMEs).

**Keywords:** Intelligent chatbot, Retrieval-Augmented Generation (RAG), Large Language Models (LLM), Natural Language Processing, Big Data, Clustering, LLaMA, Flask.

---

## Introducción

### 1.1 Contexto General del Problema

En la última década, la inteligencia artificial (IA) ha transformado profundamente la manera en que las organizaciones gestionan sus procesos internos y su relación con los clientes. El surgimiento de los modelos de lenguaje de gran escala (LLM), como GPT, BERT y LLaMA, ha dotado a los sistemas conversacionales de capacidades sin precedentes para comprender y generar texto con coherencia contextual (Brown et al., 2020). Sin embargo, estos avances no han estado exentos de limitaciones, particularmente en lo que respecta a la personalización para entornos corporativos específicos.

El auge del Big Data ha generado una necesidad creciente de herramientas que permitan procesar, indexar y recuperar grandes volúmenes de información de manera eficiente y en tiempo real. Las pequeñas y medianas empresas (PYMES), en particular, enfrentan barreras económicas y tecnológicas que les impiden acceder a soluciones de IA avanzadas basadas en infraestructura propietaria de alto costo. En este contexto, la combinación de modelos locales de código abierto con técnicas de recuperación de información como RAG ofrece una alternativa viable y accesible.

### 1.2 Planteamiento del Problema

Los chatbots tradicionales basados en reglas o en modelos entrenados con datos genéricos presentan una limitación estructural fundamental: su incapacidad para incorporar y utilizar el conocimiento propio de cada organización en tiempo de ejecución. Cuando una empresa necesita que su sistema conversacional responda con base en catálogos de productos, políticas internas, manuales técnicos o cualquier documentación corporativa específica, los chatbots convencionales resultan insuficientes.

Esta situación genera dos consecuencias directas: (1) los usuarios reciben respuestas imprecisas o irrelevantes que no reflejan el contexto real del negocio, y (2) el personal humano debe intervenir frecuentemente para corregir las respuestas automáticas, anulando el propósito de automatización. El problema se agrava en entornos donde los documentos son extensos o técnicamente especializados, ya que los LLM convencionales no pueden procesar documentos completos sin incurrir en costos computacionales excesivos o pérdidas de coherencia.

**Pregunta de investigación:** ¿Cómo diseñar e implementar una arquitectura de chatbot que permita a una organización cargar su propia documentación y recibir respuestas precisas y contextualizadas generadas por un LLM, manteniendo bajo costo operativo y alta escalabilidad?

### 1.3 Justificación

Desde el punto de vista **tecnológico**, este proyecto propone la integración de LLM locales con la técnica RAG, permitiendo que el sistema genere respuestas fundamentadas en información específica proporcionada por el usuario. Esta arquitectura mejora la precisión, relevancia y utilidad del chatbot frente a soluciones tradicionales.

Desde la perspectiva **académica**, el proyecto permite aplicar y consolidar conocimientos adquiridos en áreas como desarrollo de software, procesamiento de lenguaje natural, bases de datos y arquitecturas distribuidas, correspondientes al programa de Ingeniería de Sistemas de la UNAD.

En el ámbito **empresarial y social**, la implementación de esta solución contribuye a la optimización de procesos en ventas, soporte técnico y gestión del conocimiento, reduciendo tiempos de respuesta y mejorando la experiencia del usuario final. Las PYMES colombianas, que representan más del 90% del tejido empresarial nacional, pueden beneficiarse de una solución que democratiza el acceso a la IA conversacional avanzada sin requerir grandes inversiones.

### 1.4 Objetivo General y Objetivos Específicos

**Objetivo General**

Desarrollar e implementar una arquitectura de chatbot inteligente basado en un modelo de lenguaje de gran escala (LLM) con integración de RAG, que permita la comprensión de documentos cargados por el usuario y genere respuestas contextualizadas para optimizar procesos empresariales en un entorno de despliegue virtualizado de bajo costo.

**Objetivos Específicos**

1. Diseñar la arquitectura lógica y técnica del sistema, definiendo los componentes necesarios para la integración de un modelo LLM con un pipeline RAG en un entorno de procesamiento de datos a gran escala.

2. Implementar el módulo de carga y procesamiento de documentos (PDF y texto plano), permitiendo al sistema extraer, fragmentar e indexar información relevante para su uso en la generación de respuestas.

3. Desarrollar el mecanismo de selección contextual mediante clustering semántico (KMeans y DBSCAN), habilitando la recuperación eficiente del documento más pertinente para cada consulta del usuario.

4. Construir el servicio web intermediario con Flask que integre el frontend de usuario, el módulo RAG y el modelo LLM local expuesto mediante Ollama.

5. Desplegar la solución en un servidor VPS con Docker, garantizando portabilidad, reproducibilidad y escalabilidad de la arquitectura.

6. Evaluar el rendimiento del sistema mediante métricas cuantitativas de tiempo de respuesta, precisión semántica y relevancia de los fragmentos recuperados en escenarios de prueba simulados.

### 1.5 Alcance y Limitaciones

**Alcance:** El sistema desarrollado comprende un prototipo funcional que permite a usuarios registrados cargar documentos en formato PDF, formular consultas en lenguaje natural y recibir respuestas generadas por LLaMA 3.1 condicionadas por el contenido de los documentos cargados. El sistema incluye módulos de autenticación, gestión de archivos, clustering semántico y comunicación con el modelo LLM local. Se desplegó en VPS con Docker y fue validado con 20 casos de prueba en dominios de ventas y soporte técnico.

**Limitaciones:** El sistema no está diseñado para soportar cargas concurrentes de múltiples usuarios en la configuración actual (4 núcleos, 16 GB RAM sin GPU). La calidad de las respuestas depende de la completitud y claridad de los documentos cargados. El modelo puede presentar latencia mayor a 10 segundos para documentos extensos. El prototipo actual no implementa cifrado HTTPS.

### 1.6 Metodología Resumida

El proyecto fue desarrollado bajo la metodología ágil Scrum, organizado en sprints de dos semanas durante seis meses. Las fases principales fueron: (1) investigación y análisis de soluciones similares, (2) selección e integración del modelo LLM local, (3) diseño e implementación del módulo de procesamiento de documentos y clustering, (4) desarrollo del servicio web intermediario, (5) construcción del frontend y pruebas funcionales, y (6) despliegue en VPS con Docker y validación de rendimiento.

### 1.7 Estructura del Documento

El presente trabajo de grado está organizado de la siguiente manera: el **Marco Teórico** revisa los fundamentos de NLP, LLM, RAG, Big Data y las tecnologías empleadas; la **Metodología de Desarrollo** describe el proceso Scrum y sus sprints; el **Desarrollo del Sistema** documenta cronológicamente las fases de construcción; los **Resultados** presentan las métricas cuantitativas obtenidas; la **Discusión y Análisis** interpreta los resultados y los contrasta con soluciones existentes; las **Conclusiones** sintetizan los logros, limitaciones y recomendaciones; y los **Anexos** contienen la estructura de la base de datos, el esquema de la API y el diagrama de arquitectura.

---

## Marco Teórico

### 2.1 Sistemas Conversacionales y Chatbots

El avance en inteligencia artificial (IA), especialmente en el área del procesamiento de lenguaje natural (NLP), ha permitido la evolución de sistemas conversacionales más precisos, contextuales y eficientes. Los chatbots representan una de las aplicaciones más relevantes de estas tecnologías, al ofrecer interfaces de comunicación hombre-máquina mediante lenguaje natural (Adamopoulou & Moussiades, 2020).

Tradicionalmente, los chatbots se basaban en reglas estáticas o respuestas predefinidas, lo cual limitaba su adaptabilidad a diferentes contextos. Con la aparición de los LLM, los chatbots han ganado la capacidad de generar respuestas dinámicas, coherentes y más precisas. No obstante, estos modelos pueden presentar limitaciones en cuanto a personalización, ya que están entrenados con información genérica (Huang et al., 2023).

### 2.2 Modelos de Lenguaje de Gran Escala (LLM)

Los LLM son redes neuronales de gran profundidad entrenadas sobre corpus masivos de texto mediante aprendizaje autosupervisado. Su arquitectura se basa en el mecanismo de atención Transformer, introducido por Vaswani et al. (2017), que permite capturar dependencias de largo alcance en secuencias de texto. Modelos como GPT-3 (Brown et al., 2020) demostraron que el escalado conduce a capacidades emergentes, como razonamiento en pocos ejemplos (few-shot learning).

El modelo LLaMA, desarrollado por Meta AI, representa una familia de modelos de código abierto diseñados para maximizar la eficiencia en hardware de recursos limitados (Zhao et al., 2023). LLaMA 3.1, empleado en este proyecto, ofrece un balance adecuado entre comprensión contextual y requerimientos de memoria, siendo ejecutable en CPU sin GPU.

### 2.3 Retrieval-Augmented Generation (RAG)

Para superar las limitaciones de personalización de los LLM, surge el enfoque RAG, introducido por Lewis et al. (2020). RAG combina mecanismos de recuperación de documentos relevantes con la generación de texto por parte de un LLM. En la arquitectura RAG, cuando el usuario formula una consulta, el sistema primero recupera los fragmentos más relevantes de la base de conocimiento indexada y luego los incorpora como contexto en el prompt enviado al LLM, permitiendo al modelo generar respuestas fundamentadas en información específica y reduciendo las alucinaciones.

### 2.4 Procesamiento de Lenguaje Natural y Embeddings

El NLP proporciona las técnicas necesarias para transformar el texto no estructurado en representaciones matemáticas que las máquinas pueden procesar. Los embeddings son representaciones vectoriales densas que codifican el significado semántico de palabras, frases o documentos en espacios de alta dimensión, donde elementos similares se encuentran próximos entre sí (Zhao et al., 2023). La vectorización mediante embeddings es fundamental para el pipeline RAG, ya que permite comparar la similitud semántica entre la consulta y los documentos almacenados.

### 2.5 Clustering como Mecanismo de Selección Contextual

Los algoritmos de clustering no supervisado, como KMeans y DBSCAN, permiten agrupar vectores de embeddings según su similitud geométrica. KMeans agrupa los datos en k clústeres centrados en la media de sus miembros, mientras que DBSCAN identifica clústeres de forma arbitraria basándose en la densidad local de los puntos, siendo robusto ante valores atípicos. En el contexto del sistema desarrollado, el clustering se aplica sobre los embeddings de las descripciones de los documentos cargados, identificando cuál es semánticamente más cercano a la consulta del usuario.

### 2.6 Big Data y Procesamiento Distribuido

El término Big Data hace referencia a conjuntos de datos cuyo volumen, variedad o velocidad supera la capacidad de las herramientas convencionales (IBM Research, s.f.). Las arquitecturas LLM empresariales modernas implementan patrones de procesamiento distribuido donde múltiples nodos comparten la carga de inferencia. Para este proyecto, si bien se optó por un despliegue monolítico en VPS por razones de presupuesto, el diseño modular permite escalado horizontal.

### 2.7 Tecnologías de Desarrollo

**Flask** es un microframework de Python para construir servicios web RESTful de forma rápida. Su compatibilidad con librerías de ciencia de datos (scikit-learn para clustering, PyPDF2 para lectura de documentos) lo hace ideal como backend de sistemas de IA (Python Software Foundation, s.f.).

**Ollama** es una plataforma de código abierto que simplifica la ejecución local de LLM, exponiendo una API REST compatible con el formato de chat completions. Permite gestionar múltiples modelos en un mismo entorno.

**SQLite** es un sistema de gestión de bases de datos relacional ligero, integrado en Python mediante `sqlite3`, adecuado para aplicaciones de mediana escala.

**Docker** permite encapsular la aplicación con todas sus dependencias en una imagen portable, garantizando que el sistema se ejecute de manera idéntica en cualquier entorno.

---

## Metodología de Desarrollo

El desarrollo del sistema se realizó bajo un enfoque iterativo e incremental basado en la metodología ágil Scrum, distribuyendo el trabajo en sprints de dos semanas durante seis meses. El objetivo fue construir un chatbot inteligente, personalizable y con soporte para grandes volúmenes de datos, utilizando tecnologías de código abierto y procesamiento local.

Los roles del proyecto fueron: Carlos Arturo Corredor Muñoz como desarrollador principal (Product Owner y equipo de desarrollo), y el tutor Jaime Rubiano Llorente como orientador del backlog de requisitos.

Las ceremonias Scrum incluyeron revisiones quincenales con el tutor y retrospectivas de cada sprint para identificar mejoras metodológicas. El backlog del producto comprendió los siguientes ítems ordenados por prioridad: (1) selección e integración del modelo LLM, (2) módulo de ingesta de documentos PDF, (3) mecanismo de clustering para selección contextual, (4) servicio web Flask, (5) frontend de usuario, y (6) despliegue en VPS con Docker.

---

## Desarrollo del Sistema

### 4.1 Mes 1 – Investigación de Aplicaciones Similares

Durante la fase inicial del proyecto se realizó una investigación exhaustiva sobre herramientas existentes con objetivos similares, con el fin de entender las arquitecturas empleadas por soluciones comerciales avanzadas.

Se analizaron soluciones como las APIs de DeepSeek y ChatGPT. A partir de esta revisión se identificó un patrón arquitectónico común: cada solicitud del usuario se direcciona a un clúster de servidores donde el modelo reside en cada nodo. El procesamiento se distribuye entre múltiples nodos en paralelo, y los resultados parciales se consolidan en un nodo maestro que devuelve la respuesta final al cliente mediante HTTP.

Este análisis permitió comprender los principios de escalabilidad, paralelismo y resiliencia que rigen las arquitecturas modernas de servicios LLM, orientando el diseño del prototipo local.

### 4.2 Mes 2 – Selección e Integración del Modelo LLM Local

Se utilizó Ollama como plataforma de gestión de modelos locales. Se definieron tres indicadores de selección: rendimiento en tareas de generación de texto, requerimiento de RAM sin GPU, y costo operativo.

**Tabla 1**

*Especificaciones del Hardware del Servidor VPS de Pruebas (Hostinger)*

| Componente       | Especificación                        |
|------------------|---------------------------------------|
| CPU              | 4 vCPUs (Intel Xeon, 2.4 GHz)        |
| RAM              | 16 GB DDR4                            |
| Almacenamiento   | 200 GB SSD NVMe                       |
| GPU              | No disponible (CPU únicamente)        |
| Sistema Operativo| Ubuntu 22.04 LTS                      |
| Ancho de Banda   | 32 TB/mes                             |
| Virtualización   | KVM                                   |

*Nota.* Elaboración propia basada en las especificaciones del plan VPS KVM 2 de Hostinger, utilizado como entorno de producción.

Con base en estas restricciones se evaluaron varios modelos disponibles en Ollama:

**Tabla 2**

*Comparación de Rendimiento de Modelos LLM en el Hardware de Pruebas*

| Modelo        | Parámetros | Memoria Requerida | Tiempo Respuesta (prom.) | Calidad     |
|---------------|------------|-------------------|--------------------------|-------------|
| llama2:7b     | 7B         | ~5.5 GB           | 12 s                     | Media       |
| llama3:8b     | 8B         | ~6.2 GB           | 10 s                     | Alta        |
| llama3.1:8b   | 8B         | ~6.4 GB           | 8.4 s                    | Alta        |
| mistral:7b    | 7B         | ~5.8 GB           | 11 s                     | Media-Alta  |
| phi3:mini     | 3.8B       | ~3.1 GB           | 5 s                      | Media       |

*Nota.* Elaboración propia. Tiempos medidos con una consulta de 50 tokens en el entorno VPS sin GPU. Se seleccionó llama3.1:latest por su balance entre calidad y tiempo de procesamiento.

El modelo seleccionado se integró mediante Ollama, que lo expone en el puerto 11434 con la siguiente estructura de petición:

**Tabla 3**

*Descripción de los Campos del Payload HTTP enviado al Modelo LLM*

| Campo    | Tipo    | Descripción                                                          |
|----------|---------|----------------------------------------------------------------------|
| model    | String  | Identificador del modelo LLM a utilizar en Ollama                    |
| messages | Array   | Lista de mensajes del historial de conversación                      |
| role     | String  | Rol del emisor: system (contexto), user (consulta), assistant (resp) |
| content  | String  | Texto del mensaje; para system contiene el contexto del documento    |
| stream   | Boolean | Si es false, la respuesta completa se envía al final del procesamiento |

*Nota.* Elaboración propia basada en la documentación de la API de Ollama.

### 4.3 Meses 3 y 4 – Módulo de Procesamiento de Documentos y Clustering

Se diseñó el módulo RAG respondiendo a la pregunta: ¿Cómo integrar el modelo LLM con información específica de los documentos del usuario?

Se implementó un sistema de carpeta compartida (uploads/) que recibe archivos PDF. Los archivos son leídos mediante PyPDF2, que extrae el texto de cada página. Para gestionar la relación usuarios-documentos se diseñó una tabla Registro_documentos en SQLite con los campos: nombre_documento (máx. 50 caracteres), descripcion (máx. 350 caracteres), ruta_documento e id_usuario.

El mecanismo de selección opera así: cuando el usuario formula una pregunta, el sistema vectoriza la consulta y la compara mediante KMeans o DBSCAN con los embeddings de las descripciones de todos los documentos del usuario. El documento del clúster más cercano se selecciona y su contenido se incorpora como contexto en el prompt enviado al LLM.

**Figura 1**

*Diagrama de Secuencia del Sistema Chatbot Basado en RAG*

```
Usuario    Frontend    Backend (Flask)   Módulo RAG    Ollama (LLaMA)
  |            |              |               |               |
  |--Mensaje-->|              |               |               |
  |            |--POST /chat->|               |               |
  |            |              |--clustering()->|               |
  |            |              |               |--Selecciona doc|
  |            |              |<--contexto doc-|               |
  |            |              |--POST /api/chat--------------->|
  |            |              |                    Genera resp  |
  |            |              |<-------------------------------|
  |            |<--respuesta--|               |               |
  |<--muestra--|              |               |               |
```

*Nota.* Elaboración propia. El diagrama ilustra el flujo completo de una consulta desde el frontend hasta el modelo LLaMA, pasando por el módulo RAG para la selección del documento relevante.

### 4.4 Mes 5 – Servicio Web Intermediario y Frontend

Se desarrolló un servicio web con Python y Flask (backend.py). La elección de Flask se justifica por su facilidad de integración con scikit-learn para clustering y su compatibilidad con el modelo de threading requerido.

El servicio expone los siguientes endpoints principales:

- GET / → Página principal de la aplicación
- GET/POST /login → Autenticación de usuarios
- POST /Envio_datos → Registro de nuevos usuarios
- POST /logout → Cierre de sesión con limpieza de caché
- GET/POST /test_connection → Interfaz de chat con el modelo
- GET /descargar_api → Descarga de documentación de la API

La autenticación implementa un sistema de caché en memoria (login_cache) que almacena credenciales validadas, evitando consultas repetidas a la base de datos. La gestión de SQLite se encapsula en la clase BD_conn, que utiliza threading.Lock para garantizar seguridad en entornos concurrentes.

El frontend fue desarrollado en HTML, CSS y JavaScript mediante plantillas Flask (templates/), con las vistas: página principal (main.html), formulario de login (login.html), interfaz de chat (index.html) y página de presentación (pagina-nomral.html).

### 4.5 Mes 6 – Despliegue en VPS con Docker

Para el despliegue en producción, se utilizó Docker para encapsular el código fuente de la aplicación Flask y la instancia de Ollama con LLaMA 3.1. El proceso de despliegue comprendió los siguientes pasos:

1. Construcción de la imagen Docker en el entorno de desarrollo local.
2. Publicación de la imagen en Docker Hub bajo el usuario ccorredor21.
3. Instalación de Docker en la VPS de Hostinger (Ubuntu 22.04 LTS).
4. Descarga de la imagen desde Docker Hub en la VPS.
5. Ejecución del contenedor con los puertos 5000 (Flask) y 11434 (Ollama) expuestos.
6. Configuración de reglas de firewall para permitir el tráfico en dichos puertos.

Esta estrategia garantiza que el entorno de ejecución sea idéntico al de desarrollo, eliminando problemas de compatibilidad de dependencias.

---

## Resultados

### 5.1 Descripción del Conjunto de Pruebas

Para evaluar el desempeño del sistema se diseñaron 20 preguntas de prueba en dos dominios: ventas (10 preguntas) con un catálogo de productos de 15 páginas, y soporte técnico (10 preguntas) con un manual técnico de 22 páginas. La relevancia se evaluó con una rúbrica de tres niveles: Alta (3) – respuesta precisa, completa y fundamentada en el documento; Media (2) – respuesta parcialmente correcta; Baja (1) – respuesta incorrecta o no relacionada con el documento.

### 5.2 Métricas de Rendimiento

**Tabla 4**

*Resultados de Desempeño del Sistema en los Casos de Prueba*

| Dominio         | Preguntas | Alta Relevancia | Media Relevancia | Baja Relevancia | Tiempo Prom. (s) |
|-----------------|-----------|-----------------|-----------------|-----------------|------------------|
| Ventas          | 10        | 7 (70%)         | 2 (20%)         | 1 (10%)         | 7.8              |
| Soporte Técnico | 10        | 10 (100%)       | 0 (0%)          | 0 (0%)          | 9.1              |
| **Total**       | **20**    | **17 (85%)**    | **2 (10%)**     | **1 (5%)**      | **8.4**          |

*Nota.* Elaboración propia. Pruebas realizadas en el entorno VPS (4 vCPUs, 16 GB RAM, sin GPU) con llama3.1:latest y el módulo RAG activo.

**Tabla 5**

*Comparación de Tiempo de Respuesta: Con y Sin Módulo RAG*

| Configuración              | Tiempo Prom. (s) | Tiempo Mín. (s) | Tiempo Máx. (s) |
|----------------------------|-----------------|-----------------|-----------------|
| Sin RAG (respuesta directa)| 6.2             | 4.8             | 9.1             |
| Con RAG (documento PDF)    | 8.4             | 6.3             | 14.7            |

*Nota.* Elaboración propia. La sobrecarga del módulo RAG (~2.2 s promedio) corresponde al tiempo de vectorización y selección por clustering.

### 5.3 Casos de Prueba Representativos

**Tabla 6**

*Muestra de Casos de Prueba y Evaluación de Respuestas*

| ID | Dominio  | Pregunta                                                    | Relevancia | Observación                              |
|----|----------|-------------------------------------------------------------|------------|------------------------------------------|
| 01 | Ventas   | ¿Cuál es el precio del producto modelo X-500?               | Alta       | Respuesta correcta con precio exacto     |
| 02 | Ventas   | ¿Qué garantía ofrece el servicio de instalación?            | Media      | Respuesta parcial, faltó el plazo exacto |
| 03 | Ventas   | ¿Hay descuentos por volumen de compra?                      | Baja       | El documento no contenía esta información|
| 04 | Soporte  | ¿Cómo reiniciar el dispositivo a fábrica?                   | Alta       | Instrucciones completas y correctas      |
| 05 | Soporte  | ¿Cuáles son los códigos de error más frecuentes?            | Alta       | Tabla de códigos reproducida correctamente|

*Nota.* Elaboración propia. Se presentan 5 de los 20 casos de prueba evaluados para ilustrar los distintos niveles de relevancia obtenidos.

---

## Discusión y Análisis

### 6.1 Análisis de los Resultados Obtenidos

Los resultados muestran que el sistema alcanzó una tasa de relevancia alta del 85%, evidenciando la viabilidad técnica de la arquitectura RAG con LLaMA local. El dominio de soporte técnico obtuvo 100% de alta relevancia, posiblemente porque los documentos técnicos tienen lenguaje más estructurado y preciso, facilitando la recuperación contextual exacta.

El tiempo promedio de 8.4 segundos resulta aceptable para un prototipo sin GPU. Para entornos de producción con expectativas de respuesta inmediata (menos de 3 s), sería necesario considerar hardware con GPU o cuantización del modelo a INT4/INT8, lo que podría reducir la latencia en un 40-60%.

### 6.2 Limitaciones del Sistema

Las principales limitaciones identificadas fueron:

- **Latencia elevada:** El tiempo de respuesta supera los 10 segundos cuando el documento excede las 30 páginas.
- **Concurrencia limitada:** El modelo ocupa prácticamente toda la RAM durante la inferencia, limitando las solicitudes simultáneas.
- **Dependencia de la calidad documental:** Documentos con texto escaneado sin OCR o con formato complejo no se procesan correctamente.
- **Sin cifrado en tránsito:** La versión actual no implementa HTTPS, representando una limitación de seguridad para producción real.
- **Clustering estático:** El índice semántico no se recalcula dinámicamente al agregar nuevos documentos.

### 6.3 Comparación con Soluciones Existentes

A diferencia de soluciones comerciales como ChatGPT Enterprise o Google Gemini for Business, el sistema no requiere costos de suscripción mensual ni dependencia de infraestructura de terceros, siendo adecuado para entornos donde la privacidad de los datos es prioritaria. Sin embargo, las soluciones comerciales ofrecen tiempos de respuesta menores a 2 segundos y mayor capacidad de contexto (hasta 128K tokens).

Comparado con implementaciones similares de RAG con modelos locales documentadas en la literatura (Zhao et al., 2023), el presente sistema presenta resultados de relevancia comparables (80-90%), con la ventaja de haber sido validado en un entorno de despliegue real en VPS y no solo en laboratorio.

---

## Conclusiones

El desarrollo del chatbot basado en LLaMA local con integración RAG permitió construir una solución conversacional efectiva para la atención automatizada en entornos empresariales con documentación propia. Los resultados cuantitativos demuestran una tasa de relevancia del 85% y un tiempo promedio de respuesta de 8.4 segundos en el entorno VPS de producción, validando la viabilidad técnica de la arquitectura propuesta.

El modelo LLaMA 3.1 fue seleccionado entre cinco alternativas evaluadas por su balance entre calidad de respuesta y eficiencia en hardware sin GPU. Se demostró que es posible ejecutar un LLM localmente con recursos moderados (16 GB RAM, 4 vCPUs), aunque el rendimiento mejora considerablemente con aceleración por GPU.

El clustering (KMeans y DBSCAN) como mecanismo de selección contextual fue clave para mejorar la pertinencia de las respuestas sin requerir infraestructura vectorial dedicada. El despliegue con Docker garantizó la portabilidad y reproducibilidad del sistema.

**Recomendaciones para trabajo futuro:**

1. Incorporar un motor de vectores dedicado (ChromaDB o FAISS) para mejorar la precisión y velocidad de la recuperación contextual.
2. Implementar cuantización del modelo a INT4/INT8 para reducir la latencia en entornos sin GPU.
3. Agregar soporte HTTPS en el servicio Flask para cumplir con estándares mínimos de seguridad.
4. Desarrollar reclustering incremental que actualice el índice semántico sin reiniciar el sistema.
5. Explorar la implementación de memoria conversacional para mantener coherencia en conversaciones largas.

---

## Referencias Bibliográficas

Adamopoulou, E., & Moussiades, L. (2020). Chatbots: History, technology, and applications. *Machine Learning with Applications*, *2*, 100006. https://doi.org/10.1016/j.mlwa.2020.100006

Banco Interamericano de Desarrollo (BID). (s.f.). *Big data y su impacto en la economía digital*. https://publications.iadb.org/es

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., … Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, *33*, 1877–1901. https://doi.org/10.48550/arXiv.2005.14165

Congreso de la República de Colombia. (2012). *Ley 1581 de 2012 por la cual se dictan disposiciones generales para la protección de datos personales*. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981

Google AI. (s.f.). *Desarrollo de modelos generativos*. https://ai.google/research/

Huang, J., Chang, K. C., & Wu, J. (2023). Conversational AI in business: Applications and challenges. *Journal of Business Research*, *156*, 113475. https://doi.org/10.1016/j.jbusres.2022.113475

IBM Research. (s.f.). *Big data en la inteligencia artificial*. https://www.research.ibm.com/artificial-intelligence/

Institute of Electrical and Electronics Engineers (IEEE). (s.f.). *Ethics in artificial intelligence and autonomous systems*. https://standards.ieee.org/industry-connections/ec/autonomous-systems.html

International Organization for Standardization (ISO). (s.f.). *ISO 27001: Information security management*. https://www.iso.org/iso-27001-information-security.html

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., … Riedel, S. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, *33*, 9459–9474. https://doi.org/10.48550/arXiv.2005.11401

Microsoft. (s.f.). *Responsible AI development*. https://www.microsoft.com/en-us/ai/responsible-ai

OpenAI. (s.f.). *Modelos de lenguaje de gran escala*. https://openai.com/research

Organización Mundial de la Propiedad Intelectual (OMPI). (s.f.). *Inteligencia artificial y propiedad intelectual*. https://www.wipo.int/about-ip/es/artificial_intelligence/

Parlamento Europeo y Consejo de la Unión Europea. (2016). *Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo (Reglamento General de Protección de Datos – GDPR)*. https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32016R0679

Python Software Foundation. (s.f.). *Flask: Web development, one drop at a time*. https://flask.palletsprojects.com/

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., … Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, *30*. https://doi.org/10.48550/arXiv.1706.03762

World Economic Forum. (2024). *Top 10 emerging technologies of 2024*. https://www.weforum.org

Zhao, W. X., Zhou, K., Li, J., Tang, T., Wang, X., Hou, Y., … Wen, J. R. (2023). A survey of large language models. *arXiv preprint arXiv:2303.18223*. https://doi.org/10.48550/arXiv.2303.18223

---

## Anexos

### Anexo A – Esquema de la Base de Datos

El sistema utiliza SQLite ubicado en db/mi_base.db.

**Tabla usuarios**

| Campo    | Tipo    | Restricciones             | Descripción                          |
|----------|---------|---------------------------|--------------------------------------|
| id       | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único del usuario      |
| nombre   | TEXT    | NOT NULL                  | Nombre de usuario para autenticación |
| password | TEXT    | NOT NULL                  | Contraseña del usuario               |
| empresa  | TEXT    | NOT NULL                  | Nombre de la empresa asociada        |

**Tabla Registro_documentos**

| Campo            | Tipo    | Restricciones             | Descripción                                     |
|------------------|---------|---------------------------|-------------------------------------------------|
| id               | INTEGER | PRIMARY KEY AUTOINCREMENT | Identificador único del documento               |
| nombre_documento | TEXT    | NOT NULL, MAX 50 chars    | Nombre del archivo subido                       |
| descripcion      | TEXT    | MAX 350 chars             | Descripción del contenido y uso del documento   |
| ruta_documento   | TEXT    | NOT NULL                  | Ruta del archivo en el servidor                 |
| id_usuario       | INTEGER | FOREIGN KEY               | Referencia al usuario propietario del documento |

### Anexo B – Estructura de la API REST

| Método | Endpoint          | Descripción                                         |
|--------|-------------------|-----------------------------------------------------|
| GET    | /                 | Página principal de la aplicación                   |
| GET    | /login            | Formulario de inicio de sesión                      |
| POST   | /login            | Autenticación; retorna usuario y empresa            |
| POST   | /logout           | Cierra la sesión activa del usuario                 |
| POST   | /Envio_datos      | Registro de nuevo usuario en la base de datos       |
| GET    | /test_connection  | Interfaz de chat interactivo con el modelo LLM      |
| POST   | /test_connection  | Envía consulta al modelo RAG y retorna respuesta    |
| GET    | /descargar_api    | Descarga el archivo de documentación de la API      |

### Anexo C – Diagrama de Arquitectura del Sistema

**Figura 2**

*Arquitectura General del Sistema Chatbot RAG-LLM*

```
+---------------------------------------------------------------+
|                   CLIENTE (Navegador Web)                      |
|  +----------+  +---------------+  +------------------------+  |
|  | Login UI |  |   Chat UI     |  | Gestión Documentos UI  |  |
|  +----+-----+  +-------+-------+  +-----------+------------+  |
+-------+------------------+---------------------+--------------+
        |                  |  HTTP/REST           |
        v                  v                      v
+---------------------------------------------------------------+
|         BACKEND - Flask (Python) - Puerto 5000                |
|  +--------------+  +------------------+  +-----------------+  |
|  | Auth Module  |  | RAG Controller   |  | File Upload Mgr |  |
|  | (BD_conn.py) |  | (chatting.py)    |  | (PyPDF2)        |  |
|  +------+-------+  +-------+----------+  +--------+--------+  |
|         |                  |                       |           |
|         v                  v                       v           |
|  +--------------+  +------------------+  +-----------------+  |
|  | SQLite DB    |  | Clustering Engine|  | uploads/ folder |  |
|  | (usuarios,  |  | (KMeans/DBSCAN)  |  | (archivos PDF)  |  |
|  |  documentos) |  +-------+----------+  +-----------------+  |
|  +--------------+          |                                   |
+-----------------------------+---------------------------------+
                              | HTTP POST /api/chat
                              v
+---------------------------------------------------------------+
|             OLLAMA - Puerto 11434                              |
|        Modelo: llama3.1:latest (8B parametros)                |
|        POST /api/chat  ->  Inferencia LLM local               |
+---------------------------------------------------------------+
```

*Nota.* Elaboración propia. Muestra los tres niveles: cliente (frontend), backend (Flask, RAG, autenticación) y servicio LLM local (Ollama).

### Anexo D – Guía de Despliegue con Docker

```bash
# 1. Instalar Docker en la VPS (Ubuntu 22.04 LTS)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. Descargar la imagen de Docker Hub
docker pull ccorredor21/chatbot-rag-llm:latest

# 3. Ejecutar el contenedor con los puertos necesarios
docker run -d \
  --name chatbot-rag \
  -p 5000:5000 \
  -p 11434:11434 \
  -v /opt/chatbot/uploads:/app/uploads \
  -v /opt/chatbot/db:/app/db \
  ccorredor21/chatbot-rag-llm:latest

# 4. Verificar que el contenedor esté corriendo
docker ps

# 5. Revisar los logs del sistema
docker logs chatbot-rag
```

### Anexo E – Rúbrica de Evaluación de Respuestas

| Nivel | Puntuación | Criterio                                                              |
|-------|------------|-----------------------------------------------------------------------|
| Alta  | 3          | La respuesta es precisa, completa y fundamentada en el documento      |
| Media | 2          | La respuesta es parcialmente correcta con imprecisiones menores       |
| Baja  | 1          | La respuesta no corresponde al documento o es incorrecta              |

*Nota.* Elaboración propia. Rúbrica empleada para evaluar los 20 casos de prueba documentados en la Tabla 6.
