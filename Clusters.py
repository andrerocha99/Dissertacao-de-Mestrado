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

in_ano = 2010
out_ano = 2011


ataques = ataques[ataques.Ano.isin([in_ano,out_ano])]

#para gerar círculos com o número de casos por área

locations = list(zip(ataques.lat_d, ataques.lon_d))
icons = [folium.Icon(icon="info-circle", prefix="fa") for _ in range(len(locations))]

cluster = MarkerCluster(locations=locations, icons=icons)
m.add_child(cluster)

#Para definir a grid



m.save('layer1.html')