# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:18:19 2024

@author: nfama
"""

import streamlit as st
import source
import pandas as pd


# CONFIGURANDO A PÁGINA
# É possível adicionar algumas configurações das páginas
st.set_page_config(
    page_title='Visualizaçãoes de dados Titanic' # título da página
    )


# IMPORTANDO DADOS
df = st.session_state['df']
df = source.clean_data(df)
df = source.change_names(df)

# ADICIONANDO ELEMENTOS AS PAGINAS

# colunas
col1, col2, col3 = st.columns([0.2,0.6,0.2])

# botoes de navegação
def set_state(step):
    st.session_state.page += step
    
if 'page' not in st.session_state:
    st.session_state.page = 1

max_page = 4 # apontar o número máximo de página ----------------------------

if st.session_state.page > 1:
    b1 = col1.button("Anterior", type="primary", on_click=set_state, args=[-1])

if st.session_state.page < max_page:
    b2 = col3.button("Próxima", type="primary", on_click=set_state, args=[1])


# MÉTRICAS
# taxa de sobrevivência geral
tx_sobrev = sum(df['Sobreviveu'] == 'Sobreviveu') / len(df)

# filtrando o df para mulheres
df_mulher = df[df['Gênero'] == 'Mulher']
tx_sobrev_mulher = sum(df_mulher['Sobreviveu'] == 'Sobreviveu') / len(df_mulher)
tx_sobrev_homem = sum((df['Sobreviveu'] == 'Sobreviveu') & (df['Gênero'] == 'Homem')) / len(df)

# classe
tx_sobrev_mulher1 = sum(((df_mulher['Sobreviveu'] == 'Sobreviveu')) & \
                        (df_mulher['Classe'] == 'Primeira')) / \
    sum(df_mulher['Classe'] == 'Primeira') 
    
tx_sobrev_mulher2 = sum(((df_mulher['Sobreviveu'] == 'Sobreviveu')) & \
                        (df_mulher['Classe'] == 'Segunda')) / \
    sum(df_mulher['Classe'] == 'Segunda')

tx_sobrev_mulher3 = sum(((df_mulher['Sobreviveu'] == 'Sobreviveu')) & \
                        (df_mulher['Classe'] == 'Terceira')) / \
    sum(df_mulher['Classe'] == 'Terceira')
    
tx_nsobrev_mulher3_mulher = sum(((df_mulher['Sobreviveu'] == 'Não sobreviveu')) & \
                        (df_mulher['Classe'] == 'Terceira')) / \
    sum(df_mulher['Sobreviveu'] == 'Não sobreviveu')

# PÁGINA 01
if st.session_state.page == 1:
    st.markdown(
        """
        Podemos criar um atributo `page` no `st.session_state` e assim organizar
        as visualizações em páginas controladas por botões. 
        
        
        Isso pode ser particularmente útil para apresentar dados de uma maneira contínua,
        em série. Ou seja, para contar uma história que pode ser observada nos dados.
        
        Por exemplo, vamos falar da **taxa de sobrevivência de mulheres**.
        """
                )
    
# PÁGINA 02
if st.session_state.page == 2:
    st.markdown(
        """ **A taxa de sobrevivência das mulheres ficou bem acima da geral**. \nEnquanto 
        {:.2f}% das pessoas sobreviveram ao naufrágio do titanic,
        essa taxa sobe para {:.2f}% no recorte de mulheres e cai para {:.2f}% no de homens.
        """.format(100*tx_sobrev, 100*tx_sobrev_mulher, 100*tx_sobrev_homem)
        )
    
    gender = pd.crosstab(df['Gênero'], df['Sobreviveu'])
    st.bar_chart(gender, horizontal = False)

if st.session_state.page == 3:
    st.markdown(
        """ Entretanto, quando olhamos para os dados sob uma perspectiva de classe
        (de acordo com as passagens), notamos que **a taxa de mulheres
        que sobreviveram e que estavam na primeira ({:.2f}%) e segunda classe ({:.2f}%) é muito superior
        à taxa de sobrevivência de mulheres na terceira classe ({:.2f}%)**. Esta última,
        inclusive, superior à taxa de sobrevivência geral ({:.2f}%).
        """.format(100*tx_sobrev_mulher1, 100*tx_sobrev_mulher2, 100*tx_sobrev_mulher3,100*tx_sobrev)
        )
    
    aux = pd.crosstab(df_mulher['Classe'], df['Sobreviveu'])
    st.bar_chart(aux, horizontal = False)

if st.session_state.page == 4:
    st.markdown(
        """ **Em outras palavras, do total de mulheres que morreram no naufrágio, {:.2f}%
        estavam na terceira classe**. Ou seja, apesar de observar que mulheres tiveram
        maior probabilidade de não morrer durante o naufrágio, essa estatística não se
        mantém para mulheres da terceira classe.
        """.format(100*tx_nsobrev_mulher3_mulher)
        )
    
    aux = pd.crosstab(df_mulher['Classe'], df['Sobreviveu'])
    st.bar_chart(aux, horizontal = False)
    
