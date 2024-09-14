# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:16:14 2024

@author: nfama
"""

import streamlit as st
import pandas as pd
import source



# CONFIGURANDO A PÁGINA
# É possível adicionar algumas configurações das páginas
st.set_page_config(
    page_title='Visualizaçãoes de dados Titanic', # título da página
    layout='wide' # permite uma visualização mais horizontal
    )

# IMPORTANDO DADOS
df = st.session_state['df']
df = source.clean_data(df)
df = source.change_names(df)

# salvando os dados para serem compartilhados entre páginas
st.session_state['df'] = df 

# taxa de sobrevivência geral
tx_sobrev = sum(df['Sobreviveu'] == 'Sobreviveu') / len(df)

# Os elementos vão aparecendo de cima pra baixo,
# conforme vão aparecendo no código

# VAMOS ADICIONAR ALGUNS FILTROS NA SIDEBAR
# para deixar o dash mais limpo, usaremos o sidebar para alocar os filtros
# para isso, só precisamos usar o st.sidebar. na frente dos elementos que queremos que fiquem na sidebar
# sexo
sexs = ['All'] + list(df['Gênero'].unique())                        # lista de sexos
sex = st.sidebar.selectbox('Gênero',sexs, index=0, placeholder='Gênero...')   # sexo selecionado no dash, index = 0 pra inicializar sem filtro (all)

# classe
classes = ['All'] + list(df['Classe'].unique())                        # lista de sexos
classe = st.sidebar.selectbox('Classe',classes, index=0, placeholder='Classe...')

# idade
age_max = round(df['Idade'].max())
age_start, age_end = st.sidebar.select_slider("Intervalo de idade",
                                      options=range(age_max + 1), value=[0,age_max])

# FILTRANDO O DF COM OS FILTROS SELECIONADOS PELO USUÁRIO
df_filt = df[df['Gênero'] == sex] if sex != 'All' else df  # não filtra o df original se não tiver nada selecionado - sexo
df_filt = df_filt[(df_filt['Idade'] >= age_start) & (df_filt['Idade'] <= age_end)]
df_filt = df[df['Classe'] == classe] if classe != 'All' else df_filt


## ADICIONANDO ELEMENTOS NA PÁGINA

# colocando um título
st.title('Analisando dados - dataset Titanic')

# PRIMEIRO BLOCO DE COLUNAS
# também é possível adicionar colunas
col1, col2, col3, col4 = st.columns(4)

# pessoas embarcadas
n_embarc = len(df_filt)
col1.metric(label="Pessoas embarcadas", value= f"{n_embarc}")

# pessoas sobreviventes
n_sobrev = sum(df_filt['Sobreviveu'] == 'Sobreviveu')
col2.metric(label="Sobreviventes", value= f"{n_sobrev}")

# taxa de sobrevivência filtrada
tx_sobrev_ =sum(df_filt['Sobreviveu'] == 'Sobreviveu') / len(df_filt)
dl_sobrev_ = (tx_sobrev_ - tx_sobrev) / tx_sobrev
col3.metric(label="Taxa sobrevivência", value= f"{100*tx_sobrev_:,.2f} %", delta=f"{100*dl_sobrev_:,.2f} %")

# ticket médio
ticket_med = df_filt['Preço passagem'].mean()
col4.metric(label="Ticket médio", value= f"U${ticket_med:.2f}")


# PLOTANDO O DATAFRAME

show_df = st.checkbox('Mostrar dataframe', value=False)  # criando um elemento de checkbox para mostrar ou não o df
if show_df:
    st.dataframe(df,
                 column_config={
                     'Preço passagem':st.column_config.ProgressColumn(
                         'Preço passagem',min_value=0, max_value=df['Preço passagem'].max(), format='%d' # formatação de inteiro
                         )
                     })

## SEGUNDO BLOCO DE COLUNAS
# também é possível adicionar colunas (com tamanhos diferentes)
col1, col2, col3 = st.columns(3) 
# gráficos
# sexo
col1.markdown('### Gênero')
gender = pd.crosstab(df_filt['Gênero'], df_filt['Sobreviveu'])
col1.bar_chart(gender, horizontal = True)

# local de embarque
col2.markdown('### Local de embarque')
loc_embarq = pd.crosstab(df_filt['Porto de embarque'], df_filt['Sobreviveu'])
col2.bar_chart(loc_embarq, horizontal = True)

# classe
col3.markdown('### Classe')
graf_classe = pd.crosstab(df_filt['Classe'], df_filt['Sobreviveu'])
col3.bar_chart(graf_classe, horizontal = True)

## TERCEIRO BLOCO DE COLUNAS
# também é possível adicionar colunas (com tamanhos diferentes)
col1, col2, col3 = st.columns([.4,.3,.3]) 
# gráficos

# idade
col1.markdown('### Idade')
aux = pd.crosstab(df_filt['Idade'], df_filt['Sobreviveu'])
col1.bar_chart(aux)

# Qtd. irmãos/companheiros
col2.markdown('### Irmãos ou companheiros')
sib = pd.crosstab(df_filt['Qtd irmãos ou companheiros'], df_filt['Sobreviveu'])
col2.bar_chart(sib)

# local de embarque
col3.markdown('### Pais ou filhos')
parch = pd.crosstab(df_filt['Qtd pais ou filhos'].astype(str), df_filt['Sobreviveu'])
col3.bar_chart(parch)
