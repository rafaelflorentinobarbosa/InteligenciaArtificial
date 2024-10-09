# import o streamlit - 1
import streamlit as st
# Interface gráfica entre com um número - 2
numero = st.number_input("Digite um número: ",step=1)
# verifique se o numero e positivo, negativo ou nulo - 3
if numero > 0:
    st.write(f"O número {numero} é positivo")
elif numero < 0:
    st.write(f"O número {numero} é negativo")
else:
    st.write(f"O número {numero} é nulo")