# Importando as bibliotecas 
from CONT_MODAIS.SECCAO import ImageCropperApp
from CONT_MODAIS.Tratamento import contagem
from PIL import Image
import tkinter as tk
import cv2 

cap = cv2.VideoCapture("Dados/Uberabinha.mp4")
# Frame de trabalho
frame_atual = 1
# Determinação do primeiro frame
ret,frame=cap.read()
# Determinação das propriedades 
h,w,c=frame.shape
# Conversão do frame de bgr para rgb
frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Conversão 
frame=Image.fromarray(frame)
# Quantidade de frames no vídeo Q 
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Rotina principal
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root,image=frame)
    root.mainloop()
left, top, right, bottom= app.infos()
# Loop principal

while (frame_atual < num_frames): 
    # Coleta dos frames
    ret, frame = cap.read() # coleta dos frames
    # redefinição do tamanho da imagem 
    frame_resize=frame[top:bottom,left:right]
    frame_resize=cv2.resize(frame_resize, (500,500), interpolation = cv2.INTER_LINEAR) # redimensionamento do frame
    frame_tela = cv2.rectangle(frame,  (left, top), (right, bottom), (255,0,0), 3)
    # -------------------------------------------------------------------------------------------------
    if frame_atual ==1:
        cv2.imwrite("Dados/frame_sem_modais.jpg",frame_resize)
        img_sem_modais= cv2.imread("Dados/frame_sem_modais.jpg", 1)
    # -------------------------------------------------------------------------------------------------
    if frame_atual%50==0:
        cv2.imwrite("Dados/frame_50_pixels.jpg", frame_resize)
        img2_50pixels = cv2.imread("Dados/frame_50_pixels.jpg", 1)
        print(contagem(img_sem_modais,img2_50pixels))
    # -------------------------------------------------------------------------------------------------
    
    cv2.imshow("Video", frame_tela) 
    frame_atual+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break