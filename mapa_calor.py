import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import folium
from folium.plugins import MarkerCluster


m = folium.Map(location=[-2.0, 5], zoom_start=4.25)

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_4.xlsx')

#Para selecionar o ano a partir do qual queremos que apareçam os dados dos ataques

in_ano = 2019

ataques = ataques[ataques.Ano>in_ano]

#Para inserir os markers com a classificação do ataque

for _, ataque in ataques.iterrows():
   folium.Marker(
       location= [ataque['lat_d'], ataque['lon_d']],
       tooltip= [ataque['Data_hora'],ataque['Nível_Proteção'],ataque['Numero_Criminosos']],
       popup=ataque['Classificação_Ataque'],
   ).add_to(m)


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

for _, ataque in ataques.iterrows():
   folium.Marker(
       location= [ataque['lat_d'], ataque['lon_d']],
       tooltip= [ataque['Data_hora'],ataque['Nível_Proteção'],ataque['Numero_Criminosos']],
       popup=ataque['Classificação_Ataque'],
       icon=folium.Icon(color=ataque['color']),
   ).add_to(m)


#para gerar círculos com o número de casos por área

#locations = list(zip(ataques.lat_d, ataques.lon_d))
#icons = [folium.Icon(icon="info-circle", prefix="fa") for _ in range(len(locations))]

#cluster = MarkerCluster(locations=locations, icons=icons)
#m.add_child(cluster)

#m.save('casos_por_area.html')

#Para definir a grid

def get_geojson_grid(upper_right, lower_left, n=6, m=6):
    """Returns a grid of geojson rectangles, and computes the exposure in each section of the grid based on the vessel data.

    Parameters
    ----------
    upper_right: array_like
        The upper right hand corner of "grid of grids" (the default is the upper right hand [lat, lon] of the USA).

    lower_left: array_like
        The lower left hand corner of "grid of grids"  (the default is the lower left hand [lat, lon] of the USA).

    n: integer
        The number of rows/columns in the (n,n) grid.

    Returns
    -------

    list
        List of "geojson style" dictionary objects   
    """

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
m.add_child(plugins.HeatMap(coordenadas))

grid = get_geojson_grid(upper_right, lower_left , n=16, m=18)

popups = []
counts = []

# box=grid[175]
# box 

for box in grid:
    box_coord_max = box['properties']['upper_right']
    box_coord_min = box['properties']['lower_left']
    

    condi_box = (
        (ataques.lat_d < box_coord_max[0]) & (ataques.lat_d > box_coord_min[0]) & 
        (ataques.lon_d < box_coord_max[1]) & (ataques.lon_d > box_coord_min[1])
        )
    
    amostra_box = ataques[condi_box]
    n_ataques = len(amostra_box)
    counts.append(n_ataques)

    criminosos = amostra_box.Numero_Criminosos.mean()
    perigosidade = amostra_box.Perigosidade.mean()
    texto = 'média de criminosos: {}; média de perigosidade: {}'.format(str(criminosos),str(perigosidade))
    popup = folium.Popup(texto)
    popups.append(popup)


for i, box in enumerate(grid):
    geo_json = json.dumps(box)

    color = plt.cm.Reds(n_ataques)
    color = mpl.colors.to_hex(color)

    gj = folium.GeoJson(geo_json,
                        style_function=lambda feature, color=color: {
                                                                        'fillColor': color,
                                                                        'color':"black",
                                                                        'weight': 2,
                                                                        'dashArray': '5, 5',
                                                                        'fillOpacity': 0.55,
                                                                    })
    
    gj.add_child(popups[i])

    m.add_child(gj)

ano = in_ano+1

title = 'Mapa de calor com grelha {0} desde o {1}'.format('risco',ano)
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(title)

m.get_root().html.add_child(folium.Element(title_html))

m.save('aee.html')