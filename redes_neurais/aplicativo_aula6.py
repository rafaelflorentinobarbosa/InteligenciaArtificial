import cv2
import mediapipe as mp # importação do mediapipe para usar o facemesh
import numpy as np # função EAR
import time
import pygame

som_tocando = False

# olho esquerdo
p_olho_esq = [385,380,387,373,362,263]
# olho direito
p_olho_dir = [160,144,158,153,33,133]
# Calculo Olhos
p_olhos = p_olho_esq+p_olho_dir

# variaveis da boca
p_boca = [82,87,131,14,312,317,78,308]

# Inicializa o mixer de áudio
pygame.mixer.init()
# Carrega o arquivo de som
pygame.mixer.music.load("instrumental.mp3")

# função calculo boca

def calculo_mar(face, p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca, :]
        
        mar = (np.linalg.norm(face_boca[0]-face_boca[1]) +
            np.linalg.norm(face_boca[2]-face_boca[3]) +
            np.linalg.norm(face_boca[4]-face_boca[5])) / (2 * (np.linalg.norm(face_boca[6]-face_boca[7])))
    except:
        mar = 0.0

    return mar

# uma função que calcula o EAR
def calculo_ear(face,p_olho_dir,p_olho_esq):

    try:
        face = np.array([[coord.x,coord.y] for coord  in face] )
        # face_esq
        face_esq = face[p_olho_esq, :]
        # face_dir
        face_dir = face[p_olho_dir, :]
        
        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * (np.linalg.norm(face_esq[4] - face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * (np.linalg.norm(face_dir[4] - face_dir[5])))
    except:
        # zerando
        ear_esq = 0.0
        ear_dir = 0.0
    #fórmula
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear

# criando a variável limiar
ear_limiar = 0.31
mar_limiar = 0.17

# dormir = 0 (dormindo)  1 (dormindo)
dormindo = 0

#criar uma variável para camera
cap = cv2.VideoCapture(0)
# usando uma solução de desenho
mp_drawing = mp.solutions.drawing_utils
# usando uma solução para o Face Mesh Detection
mp_face_mesh = mp.solutions.face_mesh
#liberação automática
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    # enquanto a camera estiver aberta
    while cap.isOpened():
        # sucesso-booleana (verificar se o frame esta vazio)

        sucesso, frame = cap.read()
        # realizar a verificação
        if not sucesso:
            print("ignorando o frame vazio da camêra")
            continue
        comprimento,largura,_=frame.shape
        # transformando de BGR para RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # criar uma variável      dados processados (ex.pontos do rosto)
        #FIXME: processamento do frame (saida_facemesh)
        saida_facemesh = facemesh.process(frame)
        # O OpenCV - entende BGR
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        
        if saida_facemesh.multi_face_landmarks:
            cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
            cv2.putText(frame, f"Boca Aberta", (80, 435),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    0.85, (58,58,55), 1)            
            print("Boca Aberta")
            if not som_tocando:
                pygame.mixer.music.play(-1)  # Toca continuamente
                som_tocando = True  # Atualiza o estado para som tocando
        else:
            print("Boca Fechada")
            if som_tocando:
                pygame.mixer.music.stop()  # Para o som
                som_tocando = False  # Atualiza o estado para som parado
        
        # O try - tratando o erro de ausência de usuário em frente a camera
        try: 
            for face_landmarks in saida_facemesh.multi_face_landmarks:

                mp_drawing.draw_landmarks(frame, 
                                    face_landmarks, 
                                    mp_face_mesh.FACEMESH_CONTOURS,
                                    landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,102,102),thickness=1,circle_radius=1),
                                    connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1)) 
                
                #FIXME: normalização para pixel
                face  = face_landmarks.landmark
                for id_coord,coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                        coord_cv=mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y,largura,comprimento)
                        cv2.circle(frame,coord_cv,2,(255,0,0),-1)
                    if id_coord in p_boca:
                        coord_cv=mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y,largura,comprimento)
                        cv2.circle(frame,coord_cv,2,(255,0,0),-1)
                #FIXME: chamada do EAR e print
                ear = calculo_ear(face,p_olho_dir,p_olho_esq)
                # mostrando o EAR na tela
                # criando um retangulo cinza solido  (-1)
                cv2.rectangle(frame, (0,1),(290,140),(58,58,55),-1)
                # mostrando os valores no frame
                cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 24),
                                cv2.FONT_HERSHEY_DUPLEX,
                                0.9, (255, 255, 255), 2)
                
                # Passo 1 - verificação ear < ear_limiar
                if ear < ear_limiar:                    
                    t_inicial = time.time() if dormindo == 0 else t_inicial
                    dormindo = 1
                if dormindo == 1 and ear >= ear_limiar:
                    dormindo = 0
                t_final = time.time()            
                tempo = (t_final-t_inicial) if dormindo == 1 else 0.0

                # Passo 2 - Mostrar o tempo
                cv2.putText(frame, f"Tempo: {round(tempo, 3)}", (1, 80),
                                        cv2.FONT_HERSHEY_DUPLEX,
                                        0.9, (255, 255, 255), 2)
                
                # Passo 3 - Muito tempo com olhos fechados
                if tempo>=1.5:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Muito tempo com olhos fechados!", (80, 435),
                                    cv2.FONT_HERSHEY_DUPLEX,
                                    0.85, (58,58,55), 1)
        except:
            print("algo deu errado")
        finally:
            print("encerrando o processo")    
        # carregar nosso frame - com título
        cv2.imshow('Camera',frame)
    
        if cv2.waitKey(10) & 0xFF in [ord('c'), ord('C')]:
            break
# Libera o recurso de captura de vídeo 
cap.release()
# Esse método fecha todas as janelas abertas pelo OpenCV.
cv2.destroyAllWindows()


