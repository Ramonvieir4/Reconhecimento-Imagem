import cv2
from ultralytics import YOLO
from tkinter import Tk, filedialog
import os

modelo = YOLO("yolo11n.pt")

Tk().withdraw()

arquivo = filedialog.askopenfilename(
    title="Selecione uma imagem",
    filetypes=[
        ("Imagens", "*.jpg *.jpeg *.png")
    ]
)

if arquivo:

    resultado = modelo(arquivo)

    imagem_analisada = resultado[0].plot()

    nome_arquivo = os.path.basename(arquivo)

    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

    caminho_resultado = f"resultado/{nome_sem_extensao}_reconhecida.jpg"

    cv2.imwrite(caminho_resultado, imagem_analisada)

    print("Imagem salva em:", caminho_resultado)

    cv2.imshow("Imagem Reconhecida", imagem_analisada)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:

    print("Nenhuma imagem foi selecionada.")