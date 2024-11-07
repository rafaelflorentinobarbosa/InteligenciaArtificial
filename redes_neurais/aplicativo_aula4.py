# Objetivos da Aula 4

#importação do opencv-python
import cv2
import mediapipe as mp # importação do mediapipe para usar o facemesh
import numpy as np

# Entender as cordenadas do mediaPipe
# Entender a normalização e desnormalização dos pontos do MediaPipe
# Analisar os olhos
# Utilizar a função EAR (Distância euclidiana) - segundo o artigo

# Pontos dos olhos
p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]

# Funcção  que calcula EAR
def calculo_ear(face, p_olho_dir, p_olho_esq):
    # FIXME: List comprehension
    # [[]] - lista dentro de outra lista
    # tente
    try:    
        # 1 - face é uma variável que vai resceber as cordenadas
        # 2 - np.array()
        # 3 - List comprehension - for
        # 4 - face (numpy) --- in face (mediapipe)
        
        face = np.array([[coord.x, coord.y] for coord in face])
        # matriz (array) Linhas e colunas
        face_esq = face[p_olho_esq, :]
        face_dir = face[p_olho_dir, :]
        
        ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * (np.linalg.norm(face_esq[4] - face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * (np.linalg.norm(face_dir[4] - face_dir[5])))
    except:
        ear_esq = 0.0
        ear_dir = 0.0
        
    media_ear = (ear_esq + ear_dir) / 2
    return media_ear


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
        # frame - captura
        sucesso, frame = cap.read()
        # realizar a verificação
        # sucesso = 1   fracasso = 0
        if not sucesso:
            print("ignorando o frame vazio da camêra")
            continue
        # transformando de BGR para RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # FIXME: criar uma variável, dados processados (ex.pontos do rosto), saida_facemesh
        saida_facemesh = facemesh.process(frame)
        # O OpenCV - entende BGR
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        
        # O try - tratando o erro de ausência de usuário em frente a camera
        try: 
            #mostrar os pontos, mostrar a detecção que o MediaPipe fez
            # vou criar uma variável face_landmarks - que são as coordenadas da nossa face
            # Ele vai ser atribuido ao nosso conjunto de coordenadas
            # saida_facemesh é o nosso conjunto de coordenadas
            # o multi_face_landmarks vai retornas as coordenadas
            # após isso ele deve desenhar esses pontos no nosso rosto
            #FIXME: acesso as cordenadas (multi_face_landmarks)
            # Traz as cordenadas da malha 3D (x,y,z)
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                # desenhar
                # uso o método draw_landmarks para pontuar os desenhos
                # dentro dos parenteses
                # o nosso (frame)
                # as coordenadas - (face_landmarks)
                # Especificar os nossos pontos : FACEMESH_CONTOURS
                mp_drawing.draw_landmarks(frame,face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,202,102),thickness=1,circle_radius=1),
                connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1))
                
            #FIXME: Normalização para pixel
            

            # face = face_landmarks.landmark
            # for id_coord, coord_xyz in enumerate(face): .
            #     if id_coord in p_olhos:
            #         coord_cv = mp_drawing._normalized_to_pixel_coordinates
            #         cv2.circle(frame,coord_cv,2,(255,0,0), -1)
            

            
            #FIXME: Chamada do EAR e print
            
            # mostrando o EAR na tela
            #  cv2.rectangle(frame, (0,1),(290,140),(58,58,55),-1)
            #                 cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 24),
            #                                 cv2.FONT_HERSHEY_DUPLEX,
            #                                 0.9, (255, 255, 255), 2)

            # {documentação do OpenCV}
            # https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html

        except:
            print("algo deu errado")
        finally:
            print("encerrando o processo")    
        # carregar nosso frame - com título
        cv2.imshow('Camera',frame)
        # Estude sobre bitwise
        # Estude sobre tabela ASC II estendida
        # ord() - retorna o valor Unicode (ou ASC II)
        # o valor 0xFF é tabela ASC II estendida
    
        if cv2.waitKey(10) & 0xFF in [ord('c'), ord('C')]:
            break
# Libera o recurso de captura de vídeo 
cap.release()
# Esse método fecha todas as janelas abertas pelo OpenCV.
cv2.destroyAllWindows()