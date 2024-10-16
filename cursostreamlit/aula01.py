# No prompt instale: 
# pip install streamlit
# pip install plotly.express
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pandas as std
import json

st.title("Dashboard de Vendas:shopping_trolley: ")
url="https://labdados.com/produtos" # https://labdados.com/produtos?regiao=norte&ano=2022
response= requests.get(url)

# json > convertido para dicionário > Convertido para databframe
df = pd.DataFrame.from_dict(response.json())
if st.button("todos"):
    st.balloons()
        
    def muda_valor(valor):
        if valor == 1000000:
            return f" {valor/1000000:.1f} milhão"
        elif valor > 1000000:
            return f" {valor/1000000:.1f} milhões"
        elif valor >= 1000:
            return f" {valor/1000:.1f} mil"
        else:
            return f" {valor:.2f}"      
        
    st.metric("Receita:",muda_valor(df['Preço'].sum()))
    st.metric("Quantidade de vendas (linhas)",muda_valor(df.shape[0]))
    st.metric("Quantidade de variaveis (colunas)",df.shape[1])
    
    st.dataframe(df)
    st.snow()
else:
    st.write("Clique no botão todos")
    
# streamlit run aula01.py

# Considerando que o valor esta muito grande, crie uma forma de visualizaçao mais agradável para o usuário:
# 1 milhão.
# 2 milhoes.
# 500 mil.
# 999.

# receita=df['Preço'].sum()
# if(receita > 1000000):
#     if(round(receita/1000000) == 1):
#         st.metric("Receita:",round(receita/1000000), " milhão")
#     else:
#         st.metric("Receita:",round(receita/1000000), " milhões")
# elif(receita > 100000):
#    st.metric("Receita:",round(receita/100000), " mil")
# elif(receita > 100):
#     st.write("Receita:",round(receita/100), " centenas")   
