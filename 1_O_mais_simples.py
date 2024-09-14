# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:25:16 2024

@author: nfama
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/train.csv')


st.title('Este é um título da minha página')
st.write('Este é um texto simples')
st.markdown('Este é um texto formatado com a **linguagem markdown**')

# adicionando filtro
sexs = ['all'] + list(df['Sex'].unique())                        # lista de sexos
sex = st.sidebar.selectbox('Sexo',sexs, placeholder='Sexo...')   # sexo selecionado no dash, index = 0 pra inicializar sem filtro (all)


# filtrando o df
df_original = df.copy()
df = df_original[df_original['Sex'] == sex] if sex != 'all' else df_original

# adicionando o df
df

# adicionando colunas
col1, col2 = st.columns(2)

# adicionando um gráfico de barras
col1.markdown('## Sobrevivência')
col1.bar_chart(df['Survived'].value_counts())

# matplot
col2.markdown('## Histograma da idade')
fig, ax = plt.subplots()
ax.hist(df['Age'], bins=5, edgecolor='black')
ax.set_title('Distribuição de Idades')
ax.set_xlabel('Idade')
ax.set_ylabel('Frequência')
col2.pyplot(fig)

