import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import folium
from folium.plugins import MarkerCluster


m = folium.Map(location=[2.5, 0], zoom_start=6)

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_7.xlsx')

#Para selecionar o ano a partir do qual queremos que apareçam os dados dos ataques

in_ano = 2010
out_ano = 2011
add_ano = 2012
lo_ano = 2013
kik_ano = 2014
jul_ano = 2015

ataques = ataques[ataques.Ano.isin([in_ano,out_ano,add_ano,lo_ano,kik_ano,jul_ano])]  #quando se quer apenas para 1 ano especifico
#ataques = ataques[ataques.Ano>in_ano]


fg = folium.FeatureGroup(name='my map')

#Para inserir os markers com a  classificação do ataque

# lat = list(ataques['lat_d'])
# lon = list(ataques['lon_d'])
# Data_hora = list(ataques['Data_hora'])
# Nivel_Protecao = list(ataques['Nível_Proteção'])
# Numero_Criminosos = list(ataques['Numero_Criminosos'])

# def select_marker_color(row):
#     if row['Classificação_Ataque'] == 'HIJACK' :
#         return 'red'
#     elif row['Classificação_Ataque'] == 'RAPTO' :
#         return 'orange'
#     elif row['Classificação_Ataque'] == 'SEQUESTRO' :
#         return 'gray'
#     elif row['Classificação_Ataque'] == 'ROUBO' :
#         return 'blue'
#     return 'green' #se a classificação do ataque for não conseguido
# ataques['color'] = ataques.apply(select_marker_color, axis=1)
# col_ata = list(ataques['color'])


# for lat,lon,dh,nip,nc,colored in zip(lat,lon,Data_hora,Nivel_Protecao,Numero_Criminosos,col_ata):
#     fg.add_child(folium.Marker(location=[lat,lon],
#                                popup=folium.Popup("<b>Data Hora : </b>"+str(dh) +
#                                                   "<br> <b>Nível de Proteção : </b> "+
#                                                    str(nip) +"<br><b>Nº de Criminosos : </b>" +
#                                                    str(nc),max_width=300,min_width=0),
#                                 icon=folium.Icon(color=colored)
#                   )).add_to(m)
                        
 
# m.add_child(fg)

#m.save('markers.html')


#para gerar círculos com o número de casos por área

# locations = list(zip(ataques.lat_d, ataques.lon_d))
# icons = [folium.Icon(icon="info-circle", prefix="fa") for _ in range(len(locations))]

# cluster = MarkerCluster(locations=locations, icons=icons)
# m.add_child(cluster)

#m.save('casos_por_area.html')

#Para definir a grid

def get_geojson_grid(upper_right, lower_left, n=6, m=6):
#     """Returns a grid of geojson rectangles, and computes the exposure in each section of the grid based on the vessel data.

#     Parameters
#     ----------
#     upper_right: array_like
#         The upper right hand corner of "grid of grids" (the default is the upper right hand [lat, lon] of the USA).

#     lower_left: array_like
#         The lower left hand corner of "grid of grids"  (the default is the lower left hand [lat, lon] of the USA).

#     n: integer
#         The number of rows/columns in the (n,n) grid.

#     Returns
#     -------

#     list
#         List of "geojson style" dictionary objects   
#     """

    all_boxes = []

    lat_steps = np.linspace(lower_left[0], upper_right[0], n+1)
    lon_steps = np.linspace(lower_left[1], upper_right[1], m+1)

    lat_stride = lat_steps[1] - lat_steps[0]
    lon_stride = lon_steps[1] - lon_steps[0]

    for lat in lat_steps[:-1]:
        for lon in lon_steps[:-1]:
            # Define dimensions of box in grid
            upper_left = [lon, lat + lat_stride]
            upper_right = [lon + lon_stride, lat + lat_stride]
            lower_right = [lon + lon_stride, lat]
            lower_left = [lon, lat]

            # Define json coordinates for polygon
            coordinates = [
                upper_left,
                upper_right,
                lower_right,
                lower_left,
                upper_left
            ]

            geo_json = {"type": "FeatureCollection",
                        "properties":{
                            "lower_left": lower_left,
                            "upper_right": upper_right
                        },
                        "features":[]}

            grid_feature = {
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates": [coordinates],
                }
            }

            geo_json["features"].append(grid_feature)

            all_boxes.append(geo_json)

    return all_boxes



lower_left = [-18, -18]
upper_right = [14, 15]

# ataques = ataques[ataques.Ano>2019]



coordenadas=[]
for lat,lng in zip(ataques.lat_d.values[:750],ataques.lon_d.values[:750]): #número de ataques limitados a 750
    coordenadas.append([lat,lng])

from folium import plugins

#Visualização em forma de mapa de calor

#m.add_child(plugins.HeatMap(coordenadas))

n_lat_quad = 38
n_lon_quad = 38

grid = get_geojson_grid(upper_right, lower_left , n=n_lat_quad, m=n_lon_quad)

popups = []
counts = []
niveis = []
grid_coord = []

for i in range(n_lat_quad):
    for j in range(n_lon_quad):
        coord_grid = (i,j)
        grid_coord.append(coord_grid)

# box=grid[175]
# box 

def select_box(grid_coord,coord):
    coord1 = coord[0]
    coord2 = coord[1]
    selection = []
    for pos in grid_coord:
        pos1 = pos[0]
        pos2 = pos[1]
        if np.square(coord1-pos1)+np.square(coord2-pos2)<=2:
            selection.append(pos)
    
    return selection

box_coord_exp = select_box(grid_coord, grid_coord[900])

#coeficientes dos quadrados vizinhos

def pesos(box_coord,coord):
    coord1 = coord[0]
    coord2 = coord[1]
    pesos = []
    for i in range(len(box_coord)):
        pos = box_coord[i]
        pos1 = pos[0]
        pos2 = pos[1]
        #print(pos)
        #print(np.square(coord1-pos1)+np.square(coord2-pos2))
        if np.square(coord1-pos1)+np.square(coord2-pos2)==0:
            pesos.append(8)
        elif np.square(coord1-pos1)+np.square(coord2-pos2)==1:
            pesos.append(2)
        else:
            pesos.append(1)
    return pesos

pesos_exp = pesos(box_coord_exp, grid_coord[900])



#fazer a média ponderada

def weighted_average (niveis, pesos):
    
    pesos_media = []
    for j in range(len(pesos)):
            pesos_media.append(pesos[j] / sum(pesos))

    pesos_media_calculada = []
    for i in range(len(niveis)):
        pesos_media_calculada.append(niveis[i] * pesos_media[i])
            #print(pesos_media_calculada)
            
    peso_calculado = sum(pesos_media_calculada)
    return(peso_calculado)



for i, box in enumerate(grid):
    box_coord_max = box['properties']['upper_right']
    box_coord_min = box['properties']['lower_left']
    

    condi_box = (
        (ataques.lon_d < box_coord_max[0]) & (ataques.lon_d > box_coord_min[0]) & 
        (ataques.lat_d < box_coord_max[1]) & (ataques.lat_d > box_coord_min[1])
        )
    
    amostra_box = ataques[condi_box]
    perigosidade = amostra_box.Perigosidade.mean()
    if np.isnan(perigosidade):
        perigosidade = 0
    n_ataques = len(amostra_box)
    niveis.append(perigosidade)
    counts.append(n_ataques)

    perigosidade = amostra_box.Perigosidade.mean()
    if np.isnan(perigosidade):
        perigosidade = 0
    nivel = amostra_box.Nível_Ataque.mean()
    if np.isnan(nivel):
        nivel = 0
    texto = 'Média de criminosos: {}; <br>Média de perigosidade: {}; <br>N.º de ataques registados: {}; <br>Nível de ataque médio: {}; ggg:{}'.format(str(criminosos)
                                                                                                              ,str(perigosidade),
                                                                                                              str(n_ataques),
                                                                                                              str(nivel),
                                                                                                              str(grid_coord[i]))
    popup = folium.Popup(texto)
    popups.append(popup)

box_coord_exp = select_box(grid_coord, grid_coord[900])
pesos_exp = pesos(box_coord_exp, grid_coord[900])
index_exp = [grid_coord.index(coord) for coord in box_coord_exp]
niveis_exp = [niveis[i]  for i in index_exp]
media_pond_exp = weighted_average(niveis_exp, pesos_exp)

niveis_pond = []

for i in range(len(niveis)):
    box_coord = select_box(grid_coord, grid_coord[i])
    box_pesos = pesos(box_coord, grid_coord[i])
    index_box = [grid_coord.index(coord) for coord in box_coord]
    niveis_para_media = [niveis[i]  for i in index_box]
    media_pond = weighted_average(niveis_para_media, box_pesos)
    #print(str(media_pond)+' '+str(len(box_pesos)))
    #print(index_box)
    niveis_pond.append(media_pond)
    
    



max_ataques = max(counts)
max_nivel = 2 #permite alterar o quão vermelho e o quanto queremos dar destaque à pintura, se diminuir muito o valor as cores ficam muito parecidas

for i, box in enumerate(grid):
    geo_json = json.dumps(box)

    #color = plt.cm.Reds(niveis[i]/max_nivel)
    
    color = plt.cm.Reds(niveis_pond[i]/max_nivel)
    color = mpl.colors.to_hex(color)

    gj = folium.GeoJson(geo_json,
                        style_function=lambda feature, YlOrRd=color: {
                                                                        'fillColor': YlOrRd,
                                                                        'color':"black",
                                                                        'weight': 0.6,
                                                                        'dashArray': '0, 0',
                                                                        'fillOpacity': 0.5,
                                                                    })
    
    gj.add_child(popups[i])

    m.add_child(gj)
#     #print(color)

#ano = in_ano+1

title = 'Mapa de calor com grelha de {0} desde {1}'.format('risco',in_ano)
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(title)

m.get_root().html.add_child(folium.Element(title_html))


m.save('perigosidade_2010_a_2015.html')
