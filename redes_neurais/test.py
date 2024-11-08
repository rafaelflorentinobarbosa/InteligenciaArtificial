#importação do opencv-python
import cv2
import mediapipe as mp  # importação do mediapipe para usar o facemesh
import numpy as np  # função EAR
import time
import pygame

# Inicializa o mixer de áudio
pygame.mixer.init()
# Carrega o arquivo de som
pygame.mixer.music.load("instrumental.mp3")

# Pontos dos olhos e boca
p_olho_esq = [385, 380, 387, 373, 362, 263]  # olho esquerdo
p_olho_dir = [160, 144, 158, 153, 33, 133]   # olho direito
p_olhos = p_olho_esq + p_olho_dir

p_boca = [82, 87, 131, 14, 312, 317, 78, 308]  # variáveis da boca

# Criar uma variável para a câmera
cap = cv2.VideoCapture(0)

# Usando uma solução de desenho e uma solução para o Face Mesh Detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Variáveis para controlar o estado do som e o limiar
som_tocando = False
mar_limiar = 0.5  # Defina um valor de limiar apropriado para MAR

def calculo_mar(face, p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca, :]
        
        mar = (np.linalg.norm(face_boca[0] - face_boca[1]) +
            np.linalg.norm(face_boca[2] - face_boca[3]) +
               np.linalg.norm(face_boca[4] - face_boca[5])) / (2 * (np.linalg.norm(face_boca[6] - face_boca[7])))
    except:
        mar = 0.0

    return mar

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print("Ignorando o frame vazio da câmera")
            continue

        comprimento, largura, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if saida_facemesh.multi_face_landmarks:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                face = face_landmarks.landmark
                mar = calculo_mar(face, p_boca)

                # Verifica se a boca está aberta com base no MAR e controla o som
                if mar > mar_limiar:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Boca Aberta", (80, 435),
                        cv2.FONT_HERSHEY_DUPLEX,
                    0.85, (58,58,55), 1)            
                    print("Boca Aberta")
                    print("Boca Aberta")
                    if not som_tocando:
                        pygame.mixer.music.play(-1)  # Toca continuamente
                        som_tocando = True
                else:
                    print("Boca Fechada")
                    if som_tocando:
                        pygame.mixer.music.stop()  # Para o som
                        som_tocando = False

                # Desenha os pontos da boca
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_boca:
                        coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                        if coord_cv:
                            cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(10) & 0xFF in [ord('c'), ord('C')]:
            break

# Libera o recurso de captura de vídeo
cap.release()
# Fecha todas as janelas abertas pelo OpenCV
cv2.destroyAllWindows()