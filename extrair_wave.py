import glob
from netCDF4 import Dataset
import pandas as pd
import numpy as np

#Record all the years of the net CDF files into a Python list
all_years = ['2010','2016','2020' ]  #uma list para guardar todos os anos na variável year

for file in glob.glob('*.nc'):  #selecionar todos os netcdf files através do *    
    print(file)                  #vai devolver os netcdf files que estão incorporados
    data = Dataset(file,'r')      #refere-se a 2019_2020 por ser o ultimo loop
    time = data.variables['time']
    year = time.units[12:16]        #selecionar apenas o ano a partir do qual começa a contar (1950)
    print(all_years)
    
        
year_start = min(all_years)
end_year = max(all_years)
date_range = pd.date_range(start = year_start + '-01-01',
                           end = end_year + '-12-31',
                           freq = 'D')                   #D é de frequência daily(diária)
df = pd.DataFrame(0.0, columns = ['Wave'], index = date_range)
   
#Definir a lat, lon e hora do ataque com base no ficheiro csv
ataques = pd.read_csv(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\base_dados_limpa.csv')
    
for index, row in ataques.iterrows():
        location = row['Bandeira']
        location_latitude = row['lat_d']
        location_longitude = row['lon_d']
    
        all_years.sort()  #para ter a certeza que começa com a ordem correta, ou seja de 2010 e crescendo até 2020
        
        for yr in all_years:
            #Reading in the data
            data = Dataset(str(yr)+'.nc', 'r')
            
            #Storing the lat and lon data of the netCDF file into variables
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
            
            #Squared Difference between the specified lat,lon and the lat,lon of the netCDF
            sq_diff_lat = (lat - location_latitude)**2
            sq_diff_lon = (lon - location_longitude)**2
            
            #Identify the index of the min value for lat and lon
            min_index_lat = sq_diff_lat.argmin()
            min_index_lon = sq_diff_lon.argmin()
            
            #Acessing the average sea surface wave significant height
            wave = data.variables['VHM0']
            
            #Creating the date range for each year during each iteration
            start = str(yr) + '-01-01'
            end = str(yr) + '-12-31'
            d_range = pd.date_range(start = start,
                                    end = end,
                                    freq = 'D')
            
            for t_index in np.arange(0,len(d_range)):
                print('Recording the value for '+location+': ' + str(d_range[t_index]))
                df.loc[d_range[t_index]]['Wave'] = wave[t_index, min_index_lat, min_index_lon]
                
        df.to_excel(location +'.xlsx')
