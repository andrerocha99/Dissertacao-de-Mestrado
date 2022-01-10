import pandas as pd
import numpy as np

dados = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_7.xlsx')

labels = dados.columns

## array(['Machine Gun', 'Desconhecido', 'Knives', 'RPG'], dtype=object)
## array(['High', 'Low', 'Medium'], dtype=object)

Perigosidade = []

for i in range(len(dados)):
    arma = dados.Armamento[i]
    crim = dados.N_Criminosos[i]
    if arma == 'Machine Gun':
        if crim in ['High','Medium']:
            Perigosidade.append(3)
        else:
            Perigosidade.append(2)
    elif arma == 'Desconhecido':
        if crim == 'High':
            Perigosidade.append(3)
        else:
            Perigosidade.append(2)
    elif arma == 'Knives':
        if crim in ['High']:
            Perigosidade.append(2)
        else:
            Perigosidade.append(1)
    elif arma == 'RPG':
        Perigosidade.append(3)

dados['Perigosidade'] = Perigosidade

dados.to_excel('Base_Dados_7.1.xlsx')

Meteorologia = []

for x in range(len(dados)):
    onda = dados.onda[x]
    vento = dados.vento[x]
    chuva = dados.chuva[x]
    if onda == 'Mediana':
        if vento == 'Aragem':
            if chuva in ['Light','Moderate']:
                Meteorologia.append(1)
            else:
                Meteorologia.append(2)
        elif vento == 'Fraco':
                Meteorologia.append(2)
        elif vento == 'Moderado':
            if chuva in ['Light','Moderate']:
                Meteorologia.append(2)
            else:
                Meteorologia.append(3)
    if onda == 'Crescente':
        if vento == 'Aragem':
            if chuva == 'Light':
                Meteorologia.append(1)
            else:
                Meteorologia.append(2)
        elif vento == 'Fraco':
            if chuva in ['Light','Moderate']:
                Meteorologia.append(2)
            else:
                Meteorologia.append(3)
        elif vento == 'Moderado':
            if chuva == 'Light':
                Meteorologia.append(2)
            else:
                Meteorologia.append(3)
    if onda == 'Elevada':
        if vento == 'Aragem':
            if chuva in ['Light','Moderate']:
                Meteorologia.append(2)
            else:
                Meteorologia.append(3)
        elif vento == 'Fraco':
            if chuva in ['Light','Moderate']:
                Meteorologia.append(2)
            else:
                Meteorologia.append(3)
        elif vento == 'Moderado':
                 Meteorologia.append(3)
            
dados['Meteorologia'] = Meteorologia

Nivel_Ataque = []

for j in range(len(dados)):
    Classificação_Ataque = dados.Classificação_Ataque[j]
    if Classificação_Ataque in ['HIJACK','SEQUESTRO']:
        Nivel_Ataque.append(3)
    elif Classificação_Ataque in ['RAPTO','ROUBO']:
        Nivel_Ataque.append(2)
    else:
        Nivel_Ataque.append(1)
        
dados['Nivel_Ataque'] = Nivel_Ataque

Risco_Bandeira = []

for z in range(len(dados)):
    Bandeira = dados.Bandeira[z]
    if Bandeira in ['Singapura','Panamá','Libéria','Ilhas Marshall']:
        Risco_Bandeira.append(3)
    elif Bandeira in ['Nigéria','China','Malta']:
        Risco_Bandeira.append(2)
    else:
        Risco_Bandeira.append(1)
        
dados['Risco_Bandeira'] = Risco_Bandeira 
   
dados = dados.replace('Bulk Carrier','Cargo Ship')
dados = dados.replace('Supply Ship','Cargo Ship')
dados = dados.replace('Tug','outros')

dados.to_excel('Base_Dados_5.1.xlsx')
# dados[['Perigosidade','N_Criminosos','Armamento']][dados.Perigosidade==1].head(50)

