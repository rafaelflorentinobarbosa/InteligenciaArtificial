# Importação do opencv-python
import cv2
# pip install mediapipe

# criar uma variavel para camera
cap = cv2.VideoCapture(0)

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
    # carregar nosso frame - com Titulo
    cv2.imshow('Camera', frame)
    # bitwise - tabela ASC II
    # 10 milissegundos
    # ord() - retorna o valor Unicode
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break
cap.release()
cv2.destroyAllWindows()


# pip install opencv-python

