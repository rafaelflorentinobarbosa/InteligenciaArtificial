import cv2
import mediapipe as mp # impotação do mediapipe para usar o
# pip install mediapipe

# criar uma variavel para camera  
cap = cv2.VideoCapture(0)

# Usando uma solução de desenho
mp_drawing = mp.solutions.drawing_utils

#usando uma soluçao para o face Mesh Detection
mp_face_mesh = mp.solutions.face_mesh

# liberação automática
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    # enquanto a camera estiver aberta 
    while cap.isOpened():
        # Sucesso - booleana (verificar se o frame esta vazio)
        # frame - captura
        sucesso, frame = cap.read()
        # realizar a varificação 
        # sucesso = 1 fracaso = 0
        if not sucesso:
            print("ignorando o frame vazio da camêra")
            continue    
        # tranformando de BGR para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # criar uma variavel, dados processados
        saida_facemesh = facemesh.process(frame)
        # OpenCV - entende BGR
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        """
        1 - Mostar os pontos da nossa face
        2 - o process - processar os dados
        3 - face_landmarks - (Cordenadas)
        """
        for face_landmarks in saida_facemesh.multi_face_landmarks:
            # Desenhar
            mp_drawing.draw_landmarks(frame,face_landmarks,mp_face_mesh.FACEMESH_COUNTOURS)
        
        # Carregar nosso frame - com titulo
        cv2.imshow('Camera', frame)
        # bitwise - tabela ASC II
        # 10 milissegundos
        # ord() - retorna o valor Unicode
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
    cap.release()
    cv2.destroyAllWindows()