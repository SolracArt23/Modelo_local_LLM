import requests
import time

def test_api(url="http://127.0.0.1:5000",file='test.pdf',mensaje="¿Cuál es el contenido del archivo PDF cargado?"):
    inicio = time.time()
    peticion ={
                "archivo": file,
                "prompt": mensaje
            }
    response = requests.post(f"{url}/api/chat", json=peticion)
    final = time.time()
    diferencia = final - inicio
    
    if response.status_code == 200:
        data = response.json()
        return data["respuesta"]
    else:
        print("Error en la solicitud:", response.status_code, response.text)

if __name__ == "__main__":
    file ="Soluciones_DataNova_Servicios.pdf"
    test_api(file=file)
