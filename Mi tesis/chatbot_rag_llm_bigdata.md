

Desarrollo de un Chatbot Personalizable con RAG, LLM y Big Data para Optimización Empresarial

















## Autor Carlos Arturo Corredor Muñoz



















## UNAD (Universidad Abierta y a Distancia)

## ECBIT: Escuela de ciencias básicas e ingenierías

## FACULTAD DE INGENIERIA DE SISTEMAS

## Tutor: JAIME RUBIANO LLORENTE

## 16 febrero 2026

## Dedicatoria

Este trabajo está dedicado a mi familia, quienes han sido mi motor y mi mayor inspiración durante todo este proceso. Gracias por creer en mí incluso en los momentos de mayor dificultad.



A Dios, por darme la fortaleza para no rendirme y la claridad para continuar aprendiendo.

Cada línea de este proyecto refleja no solo conocimiento técnico, sino también sacrificio, perseverancia y sueños que hoy comienzan a materializarse.



































## Agradecimientos

Expreso mi más sincero agradecimiento a la Universidad Nacional Abierta y a Distancia – UNAD, por brindarme la oportunidad de formarme profesionalmente bajo un modelo educativo que promueve la autonomía, la disciplina y el aprendizaje continuo.



A los docentes de la Escuela de Ciencias Básicas, Tecnología e Ingeniería, por su acompañamiento académico, orientación y exigencia, los cuales fueron fundamentales para el desarrollo de este proyecto.

De manera especial, agradezco a mi asesor, por su guía y retroalimentación constante, que permitieron fortalecer tanto la estructura como el enfoque técnico de esta propuesta.



Finalmente, agradezco a mi familia por su apoyo incondicional durante este proceso académico, siendo el pilar que impulsó cada uno de mis esfuerzos.





















## Tabla de contenido



















## Glosario

Arquitectura de Software:
Estructura organizacional de un sistema informático que define sus componentes, relaciones, principios de diseño y lineamientos tecnológicos para su implementación y escalabilidad.

Big Data:
Conjunto de tecnologías y metodologías orientadas al almacenamiento, procesamiento y análisis de grandes volúmenes de datos caracterizados por su variedad, velocidad y volumen, con el fin de extraer información útil para la toma de decisiones.

Chatbot:
Sistema informático basado en inteligencia artificial diseñado para interactuar con usuarios mediante lenguaje natural, simulando una conversación humana en tiempo real.

Embeddings:
Representaciones vectoriales numéricas de texto que permiten capturar relaciones semánticas entre palabras o documentos, facilitando tareas de búsqueda y recuperación de información.

Indexación Semántica:
Proceso de organización y almacenamiento de información en estructuras optimizadas que permiten búsquedas basadas en significado y no únicamente en coincidencias exactas de palabras.

Large Language Model (LLM):
Modelo de lenguaje de gran escala entrenado mediante técnicas de aprendizaje profundo sobre grandes volúmenes de texto, capaz de comprender y generar lenguaje natural con alta coherencia contextual.

Metodología Ágil:
Enfoque de gestión de proyectos basado en iteraciones cortas, mejora continua y adaptación constante a cambios, comúnmente implementado mediante marcos como Scrum.

Procesamiento de Lenguaje Natural (NLP):
Rama de la inteligencia artificial que permite a los sistemas computacionales comprender, interpretar y generar lenguaje humano de manera automática.

Prototipo Funcional:
Versión preliminar operativa de un sistema que permite validar su funcionamiento antes de su implementación definitiva.

Retrieval-Augmented Generation (RAG):
Técnica que combina un sistema de recuperación de información con un modelo generativo, permitiendo que las respuestas sean construidas a partir de datos específicos previamente indexados.

Sistema Escalable:
Sistema diseñado para aumentar su capacidad de procesamiento o almacenamiento sin comprometer su rendimiento cuando incrementa la demanda.

Validación de Desempeño:
Proceso mediante el cual se evalúan métricas como precisión, velocidad de respuesta y estabilidad para determinar la eficacia de un sistema desarrollado.





## Resumen

El presente proyecto tuvo como objetivo diseñar e implementar un chatbot inteligente basado en modelos de lenguaje de gran escala (LLM) integrados con la técnica Retrieval-Augmented Generation (RAG), con el fin de mejorar la personalización y contextualización de respuestas en entornos organizacionales. La problemática abordada se centra en la limitada capacidad de los chatbots tradicionales para utilizar información específica de cada empresa, lo que reduce su precisión y utilidad operativa.

Para su desarrollo, se adoptó un enfoque de proyecto tecnológico con metodología iterativa e incremental. Se diseñó una arquitectura compuesta por un módulo de carga y procesamiento de documentos, un sistema de indexación semántica, un motor de recuperación de información y un modelo generativo condicionado por contexto. El sistema fue implementado utilizando herramientas de procesamiento de lenguaje natural y tecnologías de almacenamiento optimizadas para grandes volúmenes de datos. Posteriormente, se realizaron pruebas funcionales y de desempeño para evaluar precisión, tiempos de respuesta y estabilidad del sistema.

Como resultado, se obtuvo un prototipo funcional capaz de generar respuestas contextualizadas a partir de información proporcionada por el usuario, evidenciando mejoras en relevancia y eficiencia frente a soluciones convencionales. Se concluye que la integración de RAG con LLM es técnicamente viable y constituye una solución escalable para optimizar procesos en áreas como ventas, soporte y gestión del conocimiento.





## Abstract

This project aimed to design and implement an intelligent chatbot architecture based on Large Language Models (LLMs) integrated with the Retrieval-Augmented Generation (RAG) technique, in order to enhance response personalization and contextualization within organizational environments. The problem addressed lies in the limited ability of traditional chatbots to incorporate organization-specific information, which reduces their accuracy and operational effectiveness.

The project followed an iterative and incremental technological development approach. The proposed architecture includes a document ingestion and processing module, a semantic indexing system, an information retrieval engine, and a context-conditioned generative model. The system was implemented using Natural Language Processing (NLP) tools and data storage technologies optimized for handling large volumes of information. Functional and performance testing was conducted to evaluate response accuracy, processing time, and system stability.

The outcome was a functional prototype capable of generating context-aware responses based on user-provided documents, demonstrating improved relevance and efficiency compared to conventional conversational systems. It is concluded that the integration of RAG and LLM technologies is technically feasible and represents a scalable solution for optimizing processes in areas such as sales, customer support, and knowledge management.

Keywords: Intelligent chatbot, Retrieval-Augmented Generation (RAG), Large Language Models (LLM), Natural Language Processing, Big Data, Technological development



## Introducción

Este artículo presenta el desarrollo de un chatbot inteligente personalizable, diseñado mediante la técnica de generación aumentada por recuperación (Retrieval-Augmented Generation, RAG), modelos de lenguaje de gran escala (Large Language Models, LLMs) e integración de tecnologías Big Data. Esta solución fue concebida para responder a la creciente necesidad de automatizar la atención al cliente y optimizar procesos empresariales mediante herramientas conversacionales más precisas, escalables y adaptables al contexto.



Los chatbots tradicionales presentan limitaciones significativas al depender de respuestas genéricas y carecer de adaptabilidad a los datos específicos de cada organización. En contraste, el enfoque propuesto permite a los usuarios cargar sus propios documentos, mejorando así la capacidad del sistema para generar respuestas relevantes y contextualizadas. La implementación de esta arquitectura se enfocó inicialmente en el área de ventas, pero su diseño modular permite su aplicabilidad en múltiples dominios, como la educación, el soporte técnico y la atención institucional.



El proyecto fue desarrollado utilizando herramientas de código abierto, bajo una metodología ágil, y desplegado en una infraestructura basada en la nube. Durante las pruebas realizadas, se evidenció un incremento en la precisión de las respuestas.



Esta propuesta demuestra la viabilidad de integrar técnicas avanzadas de inteligencia artificial con procesamiento de grandes volúmenes de datos, ofreciendo una solución escalable y eficaz para pequeñas y medianas empresas (PYMES) e instituciones educativa

## Justificación

El desarrollo de soluciones basadas en inteligencia artificial se ha convertido en un factor estratégico para las organizaciones que buscan mejorar su competitividad y eficiencia operativa. Sin embargo, muchos sistemas conversacionales actuales presentan limitaciones en la personalización y contextualización de sus respuestas, debido a que operan con información genérica y no integran adecuadamente los datos propios de cada organización. Esta situación reduce su impacto en la optimización de procesos y en la toma de decisiones empresariales.

El presente proyecto se justifica desde el punto de vista tecnológico, ya que propone la integración de modelos de lenguaje de gran escala (LLM) con la técnica Retrieval-Augmented Generation (RAG), permitiendo que el sistema genere respuestas fundamentadas en información específica proporcionada por el usuario. Esta arquitectura mejora la precisión, relevancia y utilidad del chatbot frente a soluciones tradicionales, aportando una alternativa escalable y adaptable a distintos sectores.

Desde la perspectiva académica, el proyecto permite aplicar conocimientos adquiridos en áreas como desarrollo de software, procesamiento de lenguaje natural, bases de datos y arquitecturas distribuidas, consolidando competencias propias del programa de Ingeniería/Tecnología en Sistemas. Asimismo, fomenta la innovación y el uso responsable de tecnologías emergentes.

En el ámbito empresarial y social, la implementación de esta solución contribuye a la optimización de procesos en áreas como ventas, soporte y gestión del conocimiento, reduciendo tiempos de respuesta y mejorando la experiencia del usuario. De esta manera, el proyecto no solo demuestra viabilidad técnica, sino también pertinencia práctica y potencial impacto económico.



## Objetivos

## Objetivo general

Desarrollar una arquitectura de despliegue en entorno virtual para un sistema conversacional basado en un modelo de lenguaje de gran escala (LLM) con integración de RAG, que permita la comprensión de documentos cargados por el usuario y optimice procesos mediante el manejo eficiente de datos en un entorno Big Data.































## Objetivos específicos

Diseñar la arquitectura lógica y técnica del sistema, definiendo los componentes necesarios para la integración de un modelo LLM con un pipeline RAG, en un entorno de procesamiento de datos a gran escala.

Implementar el módulo de carga y procesamiento de documentos, permitiendo al sistema extraer información relevante desde archivos provistos por el usuario para su posterior uso en la generación de respuestas.

Desarrollar la integración entre el modelo LLM y el mecanismo de recuperación RAG, habilitando la generación de respuestas contextuales basadas en el contenido de los documentos cargados.

Desplegar la solución en un entorno virtualizado (VPS) con capacidades escalables, utilizando herramientas de código abierto para garantizar portabilidad, eficiencia y bajo costo de operación.

Evaluar el rendimiento del chatbot mediante métricas cuantitativas como el tiempo de respuesta, la precisión semántica y la satisfacción del usuario en escenarios simulados de atención en ventas.

Explorar la aplicabilidad del sistema en otros contextos, como soporte técnico o educación, evaluando su capacidad a diferentes dominios temáticos.













## Marco teórico



El avance en inteligencia artificial (IA), especialmente en el área del procesamiento de lenguaje natural (NLP), ha permitido la evolución de sistemas conversacionales más precisos, contextuales y eficientes. Los chatbots1 representan una de las aplicaciones más relevantes de estas tecnologías, al ofrecer interfaces de comunicación hombre-máquina mediante lenguaje natural.



Tradicionalmente, los chatbots se basaban en reglas estáticas o respuestas predefinidas, lo cual limitaba su adaptabilidad a diferentes contextos empresariales. Con la aparición de los Modelos de Lenguaje de Gran Escala (LLM)2, como GPT y BERT, los chatbots han ganado la capacidad de generar respuestas dinámicas, coherentes y más precisas. No obstante, estos modelos pueden presentar limitaciones en cuanto a personalización, ya que están entrenados con información genérica.



Para superar estas limitaciones, surge el enfoque Retrieval-Augmented Generation (RAG), el cual combina mecanismos de recuperación de documentos relevantes con la generación de texto por parte de un LLM. Este modelo híbrido permite que los chatbots integren conocimiento actualizado y específico, ajustado a los requerimientos del usuario, mediante el uso de bases de datos externas o documentos cargados por el usuario.







## Metodologia de Desarrollo

El desarrollo del sistema se realizó bajo un enfoque iterativo e incremental basado en la metodología ágil Scrum, distribuyendo el trabajo en sprints de 2 semanas durante un período de seis meses. El objetivo fue construir un chatbot inteligente, personalizable y con soporte para grandes volúmenes de datos, utilizando tecnologías de código abierto, procesamiento local y servicios web ligeros. A continuación, se describen las etapas clave del proceso:

## Análisis de requerimientos y planificación

Se llevó a cabo un levantamiento de necesidades enfocadas en el contexto empresarial, particularmente en procesos de ventas. Se identificaron los siguientes requisitos principales: personalización por parte del usuario, capacidad de manejar documentos extensos, generación de respuestas relevantes y despliegue en infraestructura accesible (VPS).



## Descarga e integración del modelo LLM local

Se empleó el framework LLaMA (Large Language Model Meta AI) como modelo generativo principal. Se optó por su ejecución local para mantener el control total sobre los datos y reducir la latencia. El modelo fue descargado e implementado en un entorno optimizado, y se expuso como una API REST local mediante el uso del método POST.



## Procesamiento y partición de documentos

Se diseñó un sistema de carga de documentos donde los usuarios pueden subir archivos en formato PDF o texto plano. Estos documentos fueron particionados en fragmentos de contexto utilizando técnicas de ventana deslizante con preservación semántica, facilitando su uso como contexto de entrada para el modelo LLM. Los textos fueron vectorizados mediante embeddings, y almacenados para recuperación eficiente.



## Parametrización mediante clustering

En lugar de usar directamente NLP clásico, se implementó un enfoque de clustering no supervisado para agrupar los fragmentos de texto en tópicos o temáticas, con el objetivo de mejorar la pertinencia de las respuestas. Se utilizaron algoritmos como KMeans y DBSCAN sobre los embeddings generados, lo que permitió asignar etiquetas temáticas y reducir la ambigüedad en las consultas.



## Desarrollo de servicio web intermedio

Se construyó un servicio Web utilizando Flask de python, que actúa como mediador entre el modelo LLaMA local y el frontend. Este servicio se encarga de:

## Recibir peticiones del usuario (frontend)

Ejecutar el proceso de búsqueda del fragmento relevante (basado en clustering y recuperación)

## Enviar el contexto al modelo LLM mediante POST

## Devolver la respuesta generada al usuario



Este enfoque permitió desacoplar la lógica del frontend de la ejecución del modelo, facilitando su mantenimiento y escalabilidad.



## Interfaz de usuario (Frontend)

## Se desarrolló una interfaz web básica que permite a los usuarios:

## Subir documentos

## Formular preguntas

## Visualizar las respuestas generadas en tiempo real

## La capacidad de generación de un Token para la implementación en pagina locales

El frontend se comunica directamente con Flask a través de peticiones HTTP, y fue diseñado para ser ligero, funcional y fácil de adaptar a distintos dispositivos.



## Pruebas y despliegue

El sistema fue probado utilizando datos reales de catálogos comerciales, documentos de políticas internas y casos de uso frecuentes. Se evaluó su rendimiento en un entorno de VPS con 4 cores y 16 GB de RAM. Las pruebas incluyeron:

## Medición de tiempo de respuesta

## Evaluación de coherencia de la respuesta



















## Desarrollo

## Primer mes: Investigacion de app similares



Durante la fase inicial del proyecto se realizó una investigación exhaustiva sobre herramientas existentes con objetivos similares, con el fin de entender las arquitecturas empleadas por soluciones comerciales avanzadas y explorar alternativas para establecer una conexión externa estable y eficiente entre sistemas.



Se analizaron soluciones como las APIs proporcionadas por plataformas líderes como DeepSeek y ChatGPT. A partir de esta revisión se identificó un patrón arquitectónico común en el manejo de las consultas: cada solicitud enviada por el usuario es direccionada a un clúster de servidores, donde una copia del modelo de lenguaje reside en cada nodo.



El procesamiento de la respuesta se lleva a cabo de forma distribuida, dividiendo la carga de cómputo entre múltiples nodos que trabajan en paralelo. Una vez que cada nodo ejecuta su parte del proceso, los resultados parciales se reenvían al nodo maestro a través de una red interna de alta velocidad. Este nodo central se encarga de consolidar la información, construir la respuesta final y enviarla al cliente mediante un protocolo HTTP.



Este enfoque permitió comprender los principios de escalabilidad, paralelismo y resiliencia que rigen las arquitecturas modernas de servicios LLM. Tales hallazgos fueron clave para diseñar una solución local que pudiera replicar, en menor escala, una arquitectura robusta y eficiente de procesamiento de lenguaje natural distribuido.



## Segundo mes: Descarga e integración con modelo local



Como primer acercamiento, se utilizó la aplicación de OLlama Lab el cual contenía distintos modelos de LLM, cada uno con su tamaño y capacidad de memoria; con base en ello se busco un modelo optimo en rendimiento y memoria, siendo el tamaño como indicador de inteligencia y la capacidad de memoria como indicador de capacidad para retención de archivos y preguntas generadas en memoria, sin perder coherencia.

A su vez se generó un tercer indicador el cual fue el presupuesto, dado que se había planteado que por presupuesto se iba a escoger una VPS con los siguientes aspectos:

## Tabla 1

## Descripción del hardware de la VPN de testeo





Con base en esta última premisa se evaluaron modelos cuya KPIs previos fuesen buenos pero que a su vez se adaptaran al entorno donde serian desplegados, dejándonos las siguientes posibilidades:

## Tabla 2

## Descripción del rendimiento de los modelos en el Hardware de Pruebas







Tercer y cuarto mes: Partición de documentos y Parametrización mediante clustering



Se comenzó con la planeación de la arquitectura de funcionamiento del modelo, donde se empezaba a plantear la pregunta de ¿Cómo integrar el modelo con RAG?.

Para ello se estableció un sistema de carpeta el cual recibiría archivos de tipo TXT o PDF, los cuales seria leídos por el servidor y particionados, a su vez se generó una base de datos el cual contenía la tabla Registro_documentos, donde se almacenaba la siguiente información:

## Nombre del documento: Nombre de máximo 50 caracteres

descripción corta: Descripción proporcionado por el usuario de máximo 350 caracteres donde describía el documento y posible uso.

Ruta del documento: Se especificaba donde se había guardado el documento generado por el usuario.

Id del usuario: Identificador que relacionaba al usuario que subió dicho documento.

Con base en ello se generó un modelo clúster que evaluaba la cercanía estadística entre la pregunta generada por el usuario y las distintas descripciones que tenia cada documento subido por el usuario; una vez validado que información a de utilizarse se une la pregunta suministrada por el usuario con el documento escogido por el modelo de clúster y se le hace envió LLM.

## Figura X. Diagrama de secuencia del sistema chatbot basado en RAG

## La figura muestra el flujo de interacción entre los componentes del sistema:



Frontend, Backend, módulo RAG, gestión de documentos y modelo LLaMA. El usuario envía un mensaje que es procesado por el Backend y el módulo RAG, el cual recupera el documento más relevante y lo envía junto con la consulta al modelo LLaMA para generar una respuesta contextualizada. Además, se ilustra el proceso de carga de archivos PDF, los cuales son almacenados e indexados para su posterior uso en la generación de respuestas.

## Mes cinco: Desarrollo de servicio web intermedio



Durante el desarrollo se necesitaba la forma de Conectar el modelo LLM, el RAG y los mensajes enviados por el usuario; para ello se decidió implementar un servicio web con un backend de Python (flask), es escogió este lenguaje de programación y esta librería debido a la facilidad con la que se puede desplegar e implementar el modelo de clustering, con ello se relaciona el RAG con el usuario. Para relacionar el modelo LLM con el servicio web se ele estableció al modelo que escuchas en un puerto 1414, donde recibirá en un formato Json bajo la siguiente estructura:

## POST http://localhost:11434/api/generate



## {

"model": "llama2", // o "mistral", "codellama", etc. "prompt": "Hola, ¿cómo estás?",

## "stream": false

## }



## Figura 3.1: Prompt que se envia via HTTP con un método POST

## Tabla 3

## Descipcion de los elementos presentes en el método HTTP que se envia









## Sexto Mes: Despliegue en la VPS

Para el sexto mes, se plantea el despliegue de la aplicación en un entorno ya de producción, donde como mencionamos previamente usaremos una VPS de Hostinger  con los recursos que establecimos en la  Tabla 1, y para facilitar el despliegue se utilizó la herramienta de Docker, donde lo que se realizo fue un encapsulamiento del Código fuente y el modelo de Ollama. Para ello se seguirá el siguiente plan de despliegue:

## Generar la imagen Docker de la aplicación del entorno de pruebas

## Desplegar la imagen en el entorno de Docker hub con el usuario ccorredor21

## En la VPS instalar Docker

## En la VPS, descargar la imagen del Docker hub del usuario ccorredor21

## Ejecutar la imagen Docker que está en la VPS

## Establecer puertos de conexión















## Limitaciones encontradas

Durante el desarrollo, encontramos que el entorno seleccionado si bien se ajusta lo mínimo para un funcionamiento correcto, encontramos que los modelos funcionan mejor cuando la VPS tiene GPU o TPU, sin embargo, por cuestión costos se optó por un modelo ligero que tenga una codificación 7de INT o de FLOAT16, con la finalidad de tener más velocidad a la hora de generar la respuesta.

























## Conclusion

El desarrollo de un chatbot basado en un modelo LLaMA local, combinado con técnicas de recuperación (RAG) y partición inteligente de documentos, permitió construir una solución efectiva para la atención automatizada con documentos cargados por el usuario. Durante el proceso se logró establecer una arquitectura funcional sin necesidad de depender de servicios externos, utilizando únicamente herramientas de código abierto y un entorno VPS de bajo costo.



El modelo LLaMA 3 fue seleccionado por su estabilidad y balance entre memoria y capacidad de contexto, convirtiéndose en una alternativa viable a otros modelos evaluados. Se demostró que es posible ejecutar un LLM localmente con recursos limitados (16 GB RAM, sin GPU), aunque se evidenció que su rendimiento mejora considerablemente en entornos con procesamiento especializado (GPU o FLOAT16 optimizado).



El uso de clustering como mecanismo de selección contextual fue clave para mejorar la pertinencia de las respuestas, reduciendo la necesidad de una infraestructura de NLP clásica. Esta solución simplificó el diseño y permitió respuestas temáticas más alineadas con el contenido real de los documentos cargados por los usuarios. Sin embargo, también se identificaron limitaciones importantes, como:

La latencia en las respuestas cuando se excede la capacidad de memoria del modelo.

La complejidad del despliegue en entornos sin herramientas como Docker o sin permisos de root.

El rendimiento limitado para cargas concurrentes de usuarios.

## Referencias Bibliograficas

Adamopoulou, E., & Moussiades, L. (2020). Chatbots: History, technology, and applications. Machine Learning with Applications, 2, 100006. https://doi.org/10.1016/j.mlwa.2020.100006

Banco Interamericano de Desarrollo (BID). (s.f.). Big data y su impacto en la economía digital. https://publications.iadb.org/es

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., … Amodei, D. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877–1901. https://doi.org/10.48550/arXiv.2005.14165

Congreso de la República de Colombia. (2012). Ley 1581 de 2012 por la cual se dictan disposiciones generales para la protección de datos personales. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981

Google AI. (s.f.). Desarrollo de modelos generativos. https://ai.google/research/

Huang, J., Chang, K. C., & Wu, J. (2023). Conversational AI in business: Applications and challenges. Journal of Business Research, 156, 113475.

IBM Research. (s.f.). Big data en la inteligencia artificial. https://www.research.ibm.com/artificial-intelligence/

Institute of Electrical and Electronics Engineers (IEEE). (s.f.). Ethics in artificial intelligence and autonomous systems. https://standards.ieee.org/industry-connections/ec/autonomous-systems.html

International Organization for Standardization (ISO). (s.f.). ISO 27001: Information security management. https://www.iso.org/iso-27001-information-security.html

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., … Riedel, S. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459–9474. https://doi.org/10.48550/arXiv.2005.11401

Microsoft. (s.f.). Responsible AI development. https://www.microsoft.com/en-us/ai/responsible-ai

## OpenAI. (s.f.). Modelos de lenguaje de gran escala. https://openai.com/research

Organización Mundial de la Propiedad Intelectual (OMPI). (s.f.). Inteligencia artificial y propiedad intelectual. https://www.wipo.int/about-ip/es/artificial_intelligence/

Parlamento Europeo y Consejo de la Unión Europea. (2016). Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo (Reglamento General de Protección de Datos – GDPR). https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32016R0679

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., … Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30. https://doi.org/10.48550/arXiv.1706.03762

World Economic Forum. (2024). Top 10 emerging technologies of 2024. https://www.weforum.org

Zhao, W. X., Zhou, K., Li, J., Tang, T., Wang, X., Hou, Y., … Wen, J. R. (2023). A survey of large language models. arXiv preprint arXiv:2303.18223. https://doi.org/10.48550/arXiv.2303.18223









































## Figura 1
Título en cursiva

Se especifica la autoría de la figura, indicando si es elaboración propia, si fue tomada de otra fuente o si se adaptó de algún lugar. Además, se puede incluir una nota, que es una breve explicación sobre el contenido de la figura, aclarando su contexto o brindando información adicional relevante para el lector.

























## Tabla 1
Título en cursiva

Se especifica la autoría de la figura, indicando si es elaboración propia, si fue tomada de otra fuente o si se adaptó de algún lugar. Además, se puede incluir una nota, que es una breve explicación sobre el contenido de la figura, aclarando su contexto o brindando información adicional relevante para el lector.



























## Conclusiones y recomendaciones































## Referencias

Benedetti, M. (2006) El amor, las mujeres y la vida. (6 ed). Editorial Planeta.

Ley 675 de 2001. (2001, 03 de agosto) Por la cual se expide el régimen de Propiedad Horizontal. D.O. 44509. https://www.sic.gov.co/sites/default/files/normatividad/Ley_675_2001.pdf

Papalia, D. E. & Martorell, G. (2016). Desarrollo humano. McGraw-Hill. https://www-ebooks7-24-com.ezproxy.uniminuto.edu/?il=4610

Rodríguez, J., Acevedo, A. & Restrepo, L. (2024). La Subestimación Del Tamaño De La Economía Informal En Regiones De Colombia. Semestre Económico, 27(62), 1-17. doi:https://doi.org/10.22395/seec.v27n62a4201

Sanabria, C. (2025, 27 de enero). Incendios: no se puede perder de vista a la Amazonia. ElEspectador. https://www.elespectador.com/ambiente/amazonas/incendios-no-se-puede-perder-de-vista-a-la-amazonia/







## Anexos

