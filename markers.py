import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import folium
from folium.plugins import MarkerCluster


m = folium.Map(location=[-2.0, 5], zoom_start=4.25)

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_7.xlsx')

#Para selecionar o ano a partir do qual queremos que apareçam os dados dos ataques

in_ano = 2009

ataques = ataques[ataques.Ano>in_ano]

fg = folium.FeatureGroup(name='my map')

#Para inserir os markers com a  classificação do ataque

lat = list(ataques['lat_d'])
lon = list(ataques['lon_d'])
Data_hora = list(ataques['Data_hora'])
Nivel_Protecao = list(ataques['Nível_Proteção'])
Numero_Criminosos = list(ataques['Numero_Criminosos'])

def select_marker_color(row):
    if row['Classificação_Ataque'] == 'HIJACK' :
        return 'red'
    elif row['Classificação_Ataque'] == 'RAPTO' :
        return 'orange'
    elif row['Classificação_Ataque'] == 'SEQUESTRO' :
        return 'gray'
    elif row['Classificação_Ataque'] == 'ROUBO' :
        return 'blue'
    return 'green' #se a classificação do ataque for não conseguido
ataques['color'] = ataques.apply(select_marker_color, axis=1)
col_ata = list(ataques['color'])


for lat,lon,dh,nip,nc,colored in zip(lat,lon,Data_hora,Nivel_Protecao,Numero_Criminosos,col_ata):
    fg.add_child(folium.Marker(location=[lat,lon],
                               popup=folium.Popup("<b>Data Hora : </b>"+str(dh) +
                                                  "<br> <b>Nível de Proteção : </b> "+
                                                  str(nip) +"<br><b>Nº de Criminosos : </b>" +
                                                  str(nc),max_width=300,min_width=0),
                               icon=folium.Icon(color=colored)
                 )).add_to(m)
                        
 
m.add_child(fg)

m.save('markers.html')

