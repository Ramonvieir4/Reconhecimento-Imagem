import tkinter as tk
from tkinter import filedialog
import cv2
from ultralytics import YOLO
modelo = YOLO("yolo11n.pt")

def selecionar_imagem():

    arquivo = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.jpg *.jpeg *.png")
        ]
    )

    if arquivo:

        resultado = modelo(arquivo)

        imagem_analisada = resultado[0].plot()

        cv2.imshow(
            "Imagem Reconhecida",
            imagem_analisada
        )

        cv2.waitKey(0)
        cv2.destroyAllWindows()

janela = tk.Tk()

janela.title("Sistema de Reconhecimento de Imagens")

janela.geometry("600x400")

titulo = tk.Label(
    janela,
    text="SISTEMA DE RECONHECIMENTO DE IMAGENS",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=40)

botao_imagem = tk.Button(
    janela,
    text="SELECIONAR IMAGEM",
    font=("Arial", 12),
    width=25,
    height=2,
    command=selecionar_imagem,
    
)

def abrir_camera():

    camera = cv2.VideoCapture(0)

    while True:

        sucesso, imagem = camera.read()

        if not sucesso:
            print("Não foi possível acessar a câmera.")
            break

        resultado = modelo(imagem)

        imagem_analisada = resultado[0].plot()

        cv2.imshow(
            "Reconhecimento pela Camera",
            imagem_analisada
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

botao_imagem.pack(pady=10)

botao_camera = tk.Button(
    janela,
    text="ABRIR CÂMERA",
    font=("Arial", 12),
    width=25,
    height=2,
    command=abrir_camera
)

botao_camera.pack(pady=10)

botao_sair = tk.Button(
    janela,
    text="SAIR",
    font=("Arial", 12),
    width=25,
    height=2,
    command=janela.destroy
)

botao_sair.pack(pady=10)

janela.mainloop()