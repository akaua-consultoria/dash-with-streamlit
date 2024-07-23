# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:16:14 2024

@author: nfama
"""

import streamlit as st
import source ## codigos leitura e limpeza dos dados

# CONFIGURANDO A PÁGINA
# É possível adicionar algumas configurações das páginas
st.set_page_config(
    page_title='Visualizaçãoes de dados Titanic', # título da página
    layout='wide' # permite uma visualização mais horizontal
    )

# IMPORTANDO DADOS
@st.cache_data   # guardando os dados no cache pra evitar execuções repetitivas
                 # PRECISA estar antes de uma função
def load_data():
    df = source.read_data()
    return(df)

df = load_data()

# salvando os dados para serem compartilhados entre páginas
st.session_state['df'] = df 

# taxa de sobrevivência geral
tx_sobrev = df['Survived'].mean()

# Os elementos vão aparecendo de cima pra baixo,
# conforme vão aparecendo no código

# VAMOS ADICIONAR ALGUNS FILTROS
# para deixar o dash mais limpo, usaremos o sidebar para alocar os filtros
# para isso, só precisamos usar o st.sidebar. na frente dos elementos que queremos que fiquem na sidebar
# sexo
sexs = ['all'] + list(df['Sex'].unique())                        # lista de sexos
sex = st.sidebar.selectbox('Sexo',sexs, index=0, placeholder='Sexo...')   # sexo selecionado no dash, index = 0 pra inicializar sem filtro (all)

# idade
age_max = round(df['Age'].max())
age_start, age_end = st.sidebar.select_slider("Intervalo de idade",
                                      options=range(age_max + 1), value=[0,age_max])

# FILTRANDO O DF COM OS FILTROS SELECIONADOS PELO USUÁRIO
df_filt = df[df['Sex'] == sex] if sex != 'all' else df  # não filtra o df original se não tiver nada selecionado - sexo
df_filt = df_filt[(df_filt['Age'] >= age_start) & (df_filt['Age'] <= age_end)]

# ADICIONANDO ELEMENTOS NA PÁGINA
# colocando um título
st.title('Analisando dados - dataset Titanic')

# também é possível adicionar colunas
col1, col2, col3, col4 = st.columns(4)

# pessoas embarcadas
n_embarc = len(df_filt)
col1.metric(label="Pessoas embarcadas", value= f"{n_embarc}")

# pessoas sobreviventes
n_sobrev = sum(df_filt['Survived'])
col2.metric(label="Sobreviventes", value= f"{n_sobrev}")

# taxa de sobrevivência filtrada
tx_sobrev_ = df_filt['Survived'].mean()
dl_sobrev_ = (tx_sobrev_ - tx_sobrev) / tx_sobrev
col3.metric(label="Taxa sobrevivência", value= f"{100*tx_sobrev_:,.2f} %", delta=f"{100*dl_sobrev_:,.2f} %")


# plotando dataframe
show_df = st.checkbox('Mostrar dataframe', value=False)  # criando um elemento de checkbox para mostrar ou não o df
if show_df:
    st.dataframe(df_filt)

# também é possível adicionar colunas (com tamanhos diferentes)
col1, col2 = st.columns([0.4,0.8]) 
# gráficos
col1.markdown('### Distribuição por local de embarque')
col1.bar_chart(df_filt['Embarked'].value_counts())

col2.markdown('### Distribuição por classe')
col2.bar_chart(df_filt['Pclass'].value_counts())

