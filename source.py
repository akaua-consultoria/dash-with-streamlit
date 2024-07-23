# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 22:33:57 2024

@author: nfama
"""
import pandas as pd

# lê os dados
def read_data():
    df = pd.read_csv('data/train.csv')
    df.set_index('Name', inplace = True)
    return df

# trata os dados
def clean_data(df):
    df = read_data()
    df.drop(columns = ['PassengerId','Ticket'], inplace = True)
    df['Survived'].replace({0: 'Não sobreviveu', 1: 'Sobreviveu'}, 
                           inplace = True)
    df['Pclass'].replace({1: 'Primeira', 2: 'Segunda', 3: 'Terceira'}, 
                           inplace = True)
    df['Sex'].replace({'male': 'Homem', 'female': 'Mulher'}, 
                           inplace = True)
    df.dropna(subset=['Age'], inplace = True)
    df['Cabin'].fillna('--', inplace=True)
    df['Embarked'].replace({'C': 'Cherbourg', 'Q': 'Queenstown','S':'Southampton'}, 
                           inplace = True)
    df['Embarked'].fillna('--', inplace=True)
    return df

def change_names(df):
    dic = {'Survived':'Sobreviveu', 'Pclass':'Classe', 'Sex':'Gênero', 
           'Age':'Idade', 'SibSp': 'Qtd irmãos ou companheiros', 
           'Parch': 'Qtd pais ou filhos', 'Fare': 'Preço passagem', 
           'Cabin': 'Nº cabine','Embarked': 'Porto de embarque'
        }
    df.rename(columns=dic, inplace=True)
    return df