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
        if not os.path.isdir(self.folder_chatting):
            return ""

        if self.selected_file:
            pdf_path = os.path.join(self.folder_chatting, self.selected_file)
            if not os.path.isfile(pdf_path):
                return ""
        else:
            uploaded_files = [
                file_name for file_name in os.listdir(self.folder_chatting)
                if file_name.lower().endswith(".pdf")
            ]
            if not uploaded_files:
                return ""
            pdf_path = os.path.join(self.folder_chatting, uploaded_files[0])

        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                pdf_content = ""
                for page in reader.pages:
                    extracted_text = page.extract_text() or ""
                    pdf_content += extracted_text
            return pdf_content
        except Exception:
            return ""

    def __init__(self,folder_chatting:str=None, selected_file:str=None):
        #Generar una instancia 
        Chating_func.instancia += 1
        #Descargar el archivo PDF cargado
        self.folder_chatting = folder_chatting
        self.selected_file = selected_file
        self.content_pdf = self.Read_content()

