import os
import PyPDF2

class Chating_func():
    instancia = 0
    def RAG_model (self, mensaje:str) -> str:
        if self.content_pdf is not None:
            context = [{"role": "system", "content": f"El contenido del archivo PDF cargado es: {self.content_pdf}"}]
        else:
            context = [{"role": "system", "content": ""}]
        
        #Agregar mensaje del usuario
        context += [{"role": "user", "content": mensaje,}]

        #Generar la estriuctura de la peticion
        peticion ={
            "model": "llama3.1:latest",
            "messages": context,
            "stream": False,
            
        }
        return peticion

    def Read_content (self) -> str:
        #Descargar el archivo PDF cargado
        uploaded_files = os.listdir(self.folder_chatting)
        if uploaded_files:
            pdf_path = os.path.join(self.folder_chatting, uploaded_files[0])
            try:
                with open(pdf_path, 'rb') as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    pdf_content = ""
                    for page in reader.pages:
                        pdf_content += page.extract_text()
                return pdf_content
            except Exception as e:
                return ""
        else:
            return ""
    def __init__(self,folder_chatting:str=None):
        #Generar una instancia 
        Chating_func.instancia += 1
        #Descargar el archivo PDF cargado
        self.folder_chatting = folder_chatting
        self.content_pdf = self.Read_content()

