import cv2
from ultralytics import YOLO

modelo = YOLO("yolo11n.pt")

camera = cv2.VideoCapture(0)

while True:

    sucesso, imagem = camera.read()

    if not sucesso:
        print("Não foi possível acessar a câmera.")
        break

    resultado = modelo(imagem)

    imagem_analisada = resultado[0].plot()

    cv2.imshow("Reconhecimento de Imagens", imagem_analisada)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()