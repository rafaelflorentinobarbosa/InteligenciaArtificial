import streamlit as st
# python -m streamlit run aula0.py
"""
    Estamos iniciando o streamlit
    Ele nos ajudará no projeto final
    Em sua instalação vem incluido o pandas e outras libs.
"""

st.write("Alô mundo")

idade = st.number_input("Digite sua idade: ", min_value=14, max_value=120)

if idade >= 18:
    # Uso obrigatório de identação
    st.write(f"Maior de idade: {idade}")
else:
    st.write(f"Menor de idade: {idade}")