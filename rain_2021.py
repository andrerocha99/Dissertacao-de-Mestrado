from netCDF4 import Dataset, num2date
from datetime import datetime,date,time, timedelta
import pandas as pd
import numpy as np


#load 2021 wind

data1 = Dataset('precipitation_2021.nc','r')
        

time1 = data1.variables['time'][:].data


units1 = data1.variables['time'].units


time_modif1 = num2date(time1,
                        units = units1,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date1 = []


#Storing the lat and lon data of the netCDF file into variables
lat = data1.variables['lat'][:]
lon = data1.variables['lon'][:]


for i in range(len(time_modif1)): # mudar para datetime
    b = time_modif1[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date1.append(reg)
   
#carregar ataques 2021
ataques_2021 = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD_2021.xlsx')


rain = []

for index, row in ataques_2021.iterrows():
    location = row['Bandeira']
    location_latitude = row['lat_d']
    location_longitude = row['lon_d']
    day_and_hour = row['Data_hora']
    year = day_and_hour.year
    month = day_and_hour.month
    day = day_and_hour.day
    hour = day_and_hour.hour
    minutes = day_and_hour.minute
    print(index)
    
    
    #Squared Difference between the specified lat,lon and the lat,lon of the netCDF
    sq_diff_lat = (lat - location_latitude)**2
    sq_diff_lon = (lon - location_longitude)**2
    #print(sq_diff_lat)
    #print(sq_diff_lon)
    
    #Identify the index of the min value for lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    #print(min_index_lat)
    #print(min_index_lon)
    
    Data_conv_rain = np.int(round((hour+minutes/60)))
    
    if Data_conv_rain==24:
        Data_conv_rain=0
        new_date = date(year,month,day)+timedelta(days=1)
        year = new_date.year
        month = new_date.month
        day = new_date.day
        
        
    index_time = np.where(np.array(date1)==datetime.combine(date(year,month,day),time(12)))[0][0]
    print(index_time)
    rain_val = data1.variables['pr'][index_time][min_index_lat][min_index_lon]
    print(rain_val)
    if np.ma.is_masked(rain_val):
        #print(index)
        print(np.mean(data1.variables['pr'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5]))
        rain_val = np.mean(data1.variables['pr'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5])
        
    rain.append(rain_val)


ataques_new_2021 = ataques_2021.copy()

ataques_new_2021['chuva']=rain

ataques_new_2021.to_excel('novo_com_rain_21.xlsx')
    
    #Acessing the average sea surface wave significant height
    #wave = data.variables['VHM0']