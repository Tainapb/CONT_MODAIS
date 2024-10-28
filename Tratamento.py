import cv2
import numpy as np
import matplotlib.pyplot as plt
def contagem(img_sem_modais, img2_50pixels):
    offset=50
    n_modais=0
    # -------------------------------------------------------------------------
    #img_sem_modais= cv2.imread("Dados/frame_sem_modais.jpg", 1)
    #img2_50pixels = cv2.imread("Dados/frame_50_pixels.jpg", 1)

    # Converter para HSV
    img_hsv_1 = cv2.cvtColor(img_sem_modais, cv2.COLOR_BGR2HSV)
    img_hsv_2 = cv2.cvtColor(img2_50pixels, cv2.COLOR_BGR2HSV)

    # Separar a componente V (brilho)
    v1 = img_hsv_1[:, :, 2]
    v2 = img_hsv_2[:, :, 2]
    # ---------------------------------------------------------------------------
    # Definir os pontos da linha inclinada
    x1, y1 = 0, 150  # Ponto inicial da linha
    x2, y2 = img2_50pixels.shape[0], 150  # Ponto final da linha
    # Calcular a inclinação da linha (m) e o intercepto (b)
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    # -------------------------------------------------------------------------------------
    imagem_subtraida = cv2.absdiff(v1, v2)
    imagem_bin = np.where(imagem_subtraida > 50, 255, 0).astype(np.uint8)
    kernel = np.ones((9,9), np.uint8)
    dilate = cv2.dilate(imagem_bin, kernel=kernel, iterations=1)
    erode = cv2.erode(dilate, kernel=kernel, iterations=1)
    # -------------------------------------------------------------------------------------
    # Encontrar contornos
    contours, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 14000:
                # -------------------------------------------------------------------------
            # Obter a caixa delimitadora (bounding box)
                x, y, w, h = cv2.boundingRect(contour)
                # Encontrar o centroide do contorno
                cx = int(x + w / 2)
                cy = int(y + h / 2)
                # Calcular o valor de y da linha no ponto cx
                line_y_at_cx = m * cx + b
                if abs(cy - line_y_at_cx) < offset:
                    n_modais+=1
                # -------------------------------------------------------------------------
                # Desenhar contorno e o centroide no frame
                #cv2.circle(img2_50pixels, (cx, cy), 5, (0, 255, 0), -1)
                #cv2.rectangle(img2_50pixels, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Desenhar a linha inclinada
        #cv2.line(img2_50pixels, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return n_modais

'''print(n_modais)
# Criar figuras
plt.figure(figsize=(10, 7))
# Plotar a imagem erodida (binária)
plt.subplot(2, 2, 1)
plt.imshow(erode, cmap='gray')
plt.title("Imagem Binária Erodida")
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(img2_50pixels, cv2.COLOR_BGR2RGB)) 
plt.title("Imagem Binária Erodida")
plt.axis('off')

plt.show()
# ---------------------------------------------------------------------------'''