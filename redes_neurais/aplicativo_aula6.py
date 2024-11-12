import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import os
import sys

# Inicializa o mixer de áudio
pygame.mixer.init()

# Carrega o arquivo de som
pygame.mixer.music.load("Camera/Instrumental.mp3")

# Pontos dos olhos e boca
p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]
p_olhos = p_olho_esq + p_olho_dir
p_boca = [82, 87, 13, 14, 312, 317, 78, 308]

# Função EAR
def calculo_ear(face, p_olho_dir, p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]

        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * (np.linalg.norm(face_esq[4] - face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * (np.linalg.norm(face_dir[4] - face_dir[5])))
    except:
        ear_esq = 0.0
        ear_dir = 0.0
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

# Função MAR
def calculo_mar(face, p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca, :]

        mar = (np.linalg.norm(face_boca[0] - face_boca[1]) + np.linalg.norm(face_boca[2] - face_boca[3]) + np.linalg.norm(face_boca[4] - face_boca[5])) / (2 * (np.linalg.norm(face_boca[6] - face_boca[7])))
    except:
        mar = 0.0
    return mar

# Limiares
ear_limiar = 0.27
mar_limiar = 0.17
dormindo = 0

# Inicializa a câmera
cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Estado do som
som_tocando = False

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera.')
            continue
        
        comprimento, largura, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if saida_facemesh.multi_face_landmarks:
            print("Rosto detectado")
            try:
                for face_landmarks in saida_facemesh.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        face_landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 102, 102), thickness=1, circle_radius=1),
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=(102, 204, 0), thickness=1, circle_radius=1)
                    )
                    
                    face = face_landmarks.landmark
                    
                    for id_coord, coord_xyz in enumerate(face):
                        if id_coord in p_olhos:
                            coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                            cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)
                        if id_coord in p_boca:
                            coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y, largura, comprimento)
                            cv2.circle(frame, coord_cv, 2, (255, 0, 0), -1)

                    # Chamada do EAR e print (Mensagem olhos)
                    ear = calculo_ear(face, p_olho_dir, p_olho_esq)
                    cv2.rectangle(frame, (0, 1), (690, 80), (58, 58, 55), -1)
                    
                    # Desenhar "EAR" com cor azul
                    cv2.putText(frame, "EAR:", (10, 28), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 0, 0), 2)
                    # Desenhar o valor de EAR com cor branca
                    cv2.putText(frame, f"{round(ear, 2)}" , (85, 28), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                    estado_ear = 'abertos' if ear >= ear_limiar else 'fechados'
                    # Desenhar o estado "abertos" ou "fechados" com cor e fonte diferentes
                    estado_color_ear = (0, 255, 0) if estado_ear == 'abertos' else (0, 255, 255)
                    estado_font_ear = cv2.FONT_HERSHEY_SIMPLEX if estado_ear == 'abertos' else cv2.FONT_HERSHEY_PLAIN
                    cv2.putText(frame, estado_ear, (155, 28), estado_font_ear, 0.9, estado_color_ear, 2)
                

                    # Chamada do MAR e print (Mensagem Boca)
                    mar = calculo_mar(face, p_boca)
                    # Desenhar "MAR" com cor vermelha
                    cv2.putText(frame, "MAR:", (300, 28), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 2)
                    # Desenhar o valor de MAR com cor branca
                    cv2.putText(frame, f"{round(mar, 2)}", (375, 28), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                    # Determinar se é "abertos" ou "fechada"
                    estado_mar = 'aberta' if mar >= mar_limiar else 'fechada'
                    # Desenhar o estado "aberta" ou "fechada" com cor e fonte diferentes
                    estado_color_mar = (0, 255, 0) if estado_mar == 'aberta' else (0, 255, 255)
                    estado_font_mar = cv2.FONT_HERSHEY_SIMPLEX if estado_mar == 'aberta' else cv2.FONT_HERSHEY_PLAIN
                    cv2.putText(frame, estado_mar, (440, 28), estado_font_mar, 0.9, estado_color_mar, 2)

                    # Controla o som baseado no estado da boca
                    if estado_mar == 'aberta' and not som_tocando:
                        pygame.mixer.music.play(-1)  # Toca continuamente
                        som_tocando = True  # Atualiza o estado para som tocando
                    elif estado_mar == 'fechada' and som_tocando:
                        pygame.mixer.music.stop()  # Para o som
                        som_tocando = False  # Atualiza o estado para som parado

                    # Verificação da limiar
                    if ear < ear_limiar:
                        t_inicial = time.time() if dormindo == 0 else t_inicial
                        dormindo = 1
                    if dormindo == 1 and ear >= ear_limiar:
                        dormindo = 0
                    t_final = time.time()

                    tempo = (t_final - t_inicial) if dormindo == 1 else 0.0
                    cv2.putText(frame, f"Tempo: {round(tempo, 3)}", (10, 60),
                                cv2.FONT_HERSHEY_DUPLEX,
                                0.9, (255, 255, 255), 2)
                    if tempo >= 1.5:
                        cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                        cv2.putText(frame, f"Muito tempo com olhos fechados!", (80, 435),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    0.85, (58, 58, 55), 1)

            except Exception as e:
                print("Erro:", e)

            finally:
                print("Processamento concluído")
        else:
            print("Nenhum rosto detectado")
            if som_tocando:
                pygame.mixer.music.stop()  # Para o som
                som_tocando = False  # Atualiza o estado para som parado

        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break

cap.release()
cv2.destroyAllWindows()
