from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()

modelo = YOLO("yolo11n.pt")


@app.get("/")
def inicio():
    return {
        "mensagem": "API de Reconhecimento de Imagens funcionando!"
    }


@app.post("/reconhecer")
async def reconhecer_imagem(arquivo: UploadFile = File(...)):

    conteudo = await arquivo.read()

    imagem = np.frombuffer(conteudo, np.uint8)

    imagem = cv2.imdecode(imagem, cv2.IMREAD_COLOR)

    resultado = modelo(imagem)

    imagem_analisada = resultado[0].plot()

    caminho_resultado = f"resultado/{arquivo.filename}"

    cv2.imwrite(caminho_resultado, imagem_analisada)

    objetos = []

    for deteccao in resultado[0].boxes:

        classe = int(deteccao.cls[0])

    confianca = float(deteccao.conf[0])

    nome = modelo.names[classe]

    coordenadas = deteccao.xyxy[0].tolist()

    x1, y1, x2, y2 = coordenadas

    objetos.append({
        "classe": nome,
        "confianca": round(confianca, 2),
        "posicao": {
            "x1": round(x1),
            "y1": round(y1),
            "x2": round(x2),
            "y2": round(y2)
        }
    })

    return {
            "sucesso": True,
            "arquivo": arquivo.filename,
            "objetos": objetos
        }