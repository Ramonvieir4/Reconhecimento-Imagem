import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import requests


def selecionar_imagem():

    arquivo = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.jpg *.jpeg *.png")
        ]
    )

    if arquivo:

        try:

            with open(arquivo, "rb") as imagem:

                resposta = requests.post(
                    "http://127.0.0.1:8000/reconhecer",
                    files={
                        "arquivo": imagem
                    }
                )

            if resposta.status_code == 200:

                dados = resposta.json()

                mensagem = "Objetos reconhecidos:\n\n"

                for objeto in dados["objetos"]:

                    confianca = objeto["confianca"] * 100

                    posicao = objeto["posicao"]

                    mensagem += (
                        f"Objeto: {objeto['classe']}\n"
                        f"Confiança: {confianca:.0f}%\n"
                        f"Posição:\n"
                        f"X1: {posicao['x1']}\n"
                        f"Y1: {posicao['y1']}\n"
                        f"X2: {posicao['x2']}\n"
                        f"Y2: {posicao['y2']}\n\n"
    
                    )

                messagebox.showinfo(
                    "Resultado do Reconhecimento",
                    mensagem
                )

            else:

                messagebox.showerror(
                    "Erro",
                    "A API não conseguiu processar a imagem."
                )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Erro de conexão",
                "A API não está funcionando. "
                "Verifique se o servidor está ligado."
            )

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

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():

        messagebox.showerror(
            "Erro",
            "Não foi possível acessar a câmera."
        )

        return

    while True:

        sucesso, imagem = camera.read()

        if not sucesso:
            break

        # Exibe a imagem da câmera
        cv2.imshow(
            "Reconhecimento pela Camera",
            imagem
        )

        # Envia a imagem para a API ao pressionar ENTER
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == 13:

            sucesso, buffer = cv2.imencode(".jpg", imagem)

            if sucesso:

                resposta = requests.post(
                    "http://127.0.0.1:8000/reconhecer",
                    files={
                        "arquivo": (
                            "camera.jpg",
                            buffer.tobytes(),
                            "image/jpeg"
                        )
                    }
                )

                if resposta.status_code == 200:

                    dados = resposta.json()

                    mensagem = "Objetos reconhecidos:\n\n"

                    for objeto in dados["objetos"]:

                        confianca = objeto["confianca"] * 100

                        mensagem += (
                            f"Objeto: {objeto['classe']}\n"
                            f"Confiança: {confianca:.0f}%\n\n"
                        )

                    if not dados["objetos"]:
                        mensagem = "Nenhum objeto reconhecido."

                    messagebox.showinfo(
                        "Resultado do Reconhecimento",
                        mensagem
                    )

                else:

                    messagebox.showerror(
                        "Erro",
                        "A API não conseguiu processar a imagem."
                    )

        if tecla == ord("q") or tecla == 27:
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