import streamlit as st
import random

# streamlit run aula03.py

# 1. Inicializar o estado da sessão
if 'numero_secreto' not in st.session_state:
    st.session_state.numero_secreto = random.randint(1, 10)  # Criar número secreto
    st.session_state.tentativas = 0  # Inicializar tentativas

# 2. Título da aplicação
st.title("Jogo do Número Secreto")

# 3. Mensagem de boas-vindas
st.write("Bem-vindo ao jogo! Tente adivinhar o número secreto entre 1 e 10.")

# 4. Receber o chute do usuário
chute = st.number_input("Escolha um número de 1 a 10", min_value=1, max_value=10)

# 5. Verificar o chute com o número secreto
if st.button('Verificar'):
    st.session_state.tentativas += 1  # Incrementar tentativas
    
    if chute == st.session_state.numero_secreto:
        # 6. Mostrar mensagem de sucesso
        st.balloons()
        st.success(f"Isso aí! Você acertou o número secreto: {st.session_state.numero_secreto}.")
        st.write(f"Você acertou em {st.session_state.tentativas} tentativas.")
        st.session_state.numero_secreto = random.randint(1, 10)  # Reiniciar o número secreto
        st.session_state.tentativas = 0  # Reiniciar tentativas
    else:
        # 7. Mostrar dica se o chute for maior ou menor
        st.snow()
        if chute < st.session_state.numero_secreto:
            st.warning("Dica: O número secreto é maior.")
        else:
            st.warning("Dica: O número secreto é menor.")

# 8. Mostrar o número de tentativas
if st.session_state.tentativas > 0:
    st.write(f"Tentativas até agora: {st.session_state.tentativas}")

# 9. Botão para reiniciar o jogo
if st.button("Reiniciar o Jogo"):
    st.session_state.numero_secreto = random.randint(1, 10)  # Reiniciar o número secreto
    st.session_state.tentativas = 0  # Reiniciar tentativas
    st.success("O jogo foi reiniciado! Tente adivinhar o novo número secreto.")