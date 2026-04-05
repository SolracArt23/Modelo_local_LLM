import pandas as pd
from test_api import test_api
import time


def Genear_evaluacion():
    df = pd.read_csv('PQrs.txt',sep=';')
    respuestas = []
    for row in df.itertuples():
        print(f"Pregunta: {row.Pregunta}")
        inicio = time.time()
        respuesta = test_api(file=row.Documento,mensaje=row.Pregunta)
        final = time.time()
        diferencia = final - inicio
        respuestas.append({'pregunta': row.Pregunta,'respuesta correcta': row.Respuesta,'respuesta predicha': respuesta,'documento': row.Documento,'tiempo_respuesta': diferencia})
        print(f"Respuesta: {respuesta}")
        print("-" * 50)
    
    df_result = pd.DataFrame(respuestas)
    df_result.to_csv('evaluacion_resultados.csv', index=False)

if __name__ == "__main__":
    Genear_evaluacion()