#importação do opencv-python
import cv2
import mediapipe as mp # importação do mediapipe para usar o facemesh
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
        # criar uma variável      dados processados (ex.pontos do rosto)
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