# Importando as bibliotecas
from SECCAO import ImageCropperApp
from Tratamento import contar_objetos
from PIL import Image
import tkinter as tk
import cv2 

# Inicializações
cap = cv2.VideoCapture("Dados/Uberabinha.mp4")
frame_atual = 1  # Frame de trabalho
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_anterior = None

# Determinação do primeiro frame
ret, frame = cap.read()
h, w, c = frame.shape
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame_img = Image.fromarray(frame_rgb)

# Inicialização do aplicativo de recorte
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root, image=frame_img)
    root.mainloop()

# Coleta das coordenadas de recorte
left, top, right, bottom = app.infos()

# Loop principal de leitura de frames
while frame_atual < num_frames:
    ret, frame = cap.read()
    if not ret:
        break

    # Redefinição do tamanho da imagem para o recorte especificado
    frame_resize = frame[top:bottom, left:right]
    frame_resize = cv2.resize(frame_resize, (500, 500), interpolation=cv2.INTER_LINEAR)
    frame_tela = cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 3)

    # Armazenamento da primeira imagem de referência (sem modais)
    if frame_atual == 1:
        img_sem_modais_path = "Dados/frame_sem_modais.jpg"
        cv2.imwrite(img_sem_modais_path, frame_resize)
    
    # Processamento a cada 60 frames
    if frame_atual % 60 == 0:
        img2_50pixels_path = "Dados/frame_50_pixels.jpg"
        cv2.imwrite(img2_50pixels_path, frame_resize)

        # Chamar a função contar_objetos se frame_anterior estiver definido
        if frame_anterior is not None:
            n_modais, lista_cx, lista_cy = contar_objetos(img_sem_modais_path, img2_50pixels_path, exibir_graficos=False)

            print("Coordenadas dos modais:", list(zip(lista_cx, lista_cy)))

    # Exibição do frame com recorte
    cv2.imshow("Video", frame_tela)

    # Atualizar o frame_anterior
    frame_anterior = frame_resize.copy()

    # Incremento do frame atual
    frame_atual += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
