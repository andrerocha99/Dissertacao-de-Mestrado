from netCDF4 import Dataset, num2date
from datetime import datetime,date,time, timedelta
import pandas as pd
import numpy as np

#Record all the years of the net CDF files into a Python list
all_years = ['2010','2016','2020' ]  #uma list para guardar todos os anos na variável year

    
        
year_start = min(all_years)
end_year = max(all_years)
date_range = pd.date_range(start = year_start + '-01-01',
                           end = end_year + '-12-31',
                           freq = 'D')                   #D é de frequência daily(diária)
df = pd.DataFrame(0.0, columns = ['Wave'], index = date_range)
   
#Definir a lat, lon e hora do ataque com base no ficheiro csv
ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\base_dados_limpa_sem2021.xlsx')

data1 = Dataset(all_years[0]+'.nc','r')
data2 = Dataset(all_years[1]+'.nc','r')
data3 = Dataset(all_years[2]+'.nc','r')



time1 = data1.variables['time'][:].data # saber de todas as datas
time2 = data2.variables['time'][:].data # saber de todas as datas
time3 = data3.variables['time'][:].data # saber de todas as datas

units1 = data1.variables['time'].units
units2 = data2.variables['time'].units
units3 = data3.variables['time'].units
 

time_modif1 = num2date(time1,
                        units = units1,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date1 = []


for i in range(len(time_modif1)): # mudar para datetime
    b = time_modif1[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date1.append(reg)

time_modif2 = num2date(time2,
                        units = units2,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date2 = []


for i in range(len(time_modif2)): # mudar para datetime
    b = time_modif2[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date2.append(reg)


time_modif3 = num2date(time3,
                        units = units3,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date3 = []


for i in range(len(time_modif3)): # mudar para datetime
    b = time_modif3[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date3.append(reg)




wave = []

for index, row in ataques.iterrows():
    location = row['Bandeira']
    location_latitude = row['lat_d']
    location_longitude = row['lon_d']
    day_and_hour = row['Data_hora']
    year = day_and_hour.year
    month = day_and_hour.month
    day = day_and_hour.day
    hour = day_and_hour.hour
    minutes = day_and_hour.minute
    
    
    if year<2016:
        data = Dataset(all_years[0]+'.nc','r')
        date_ = date1
    elif year<2020:
        data = Dataset(all_years[1]+'.nc','r')
        date_ = date2
    elif year<2021:
        data = Dataset(all_years[2]+'.nc','r')
        date_ = date3
    else:
        wave.append('to complete')
               
    #Storing the lat and lon data of the netCDF file into variables
    lat = data.variables['latitude'][:]
    lon = data.variables['longitude'][:]
    
    
    
    # time = data.variables['time'][:].data # saber de todas as datas

 
    
    # time_modif = num2date(time,
    #                         units = 'hours since 1900-01-01 00:00:00.0 00:00',
    #                         calendar = 'gregorian') # como modificar de numérico para data gregorian
    # date = []
    
    
    # for i in range(len(time_modif)): # mudar para datetime
    #     b = time_modif[i]
    #     reg = datetime(b.year,b.month,b.day,b.hour)
    #     date.append(reg)

    
    #Squared Difference between the specified lat,lon and the lat,lon of the netCDF
    sq_diff_lat = (lat - location_latitude)**2
    sq_diff_lon = (lon - location_longitude)**2
    
    #Identify the index of the min value for lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    
    Data_conv_wave = np.int(round((hour+minutes/60)/6)*6)
    
    if Data_conv_wave==24:
        Data_conv_wave=0
        new_date = date(year,month,day)+timedelta(days=1)
        year = new_date.year
        month = new_date.month
        day = new_date.day
        
    
    
    
    index_time = np.where(np.array(date_)==datetime.combine(date(year,month,day),time(Data_conv_wave)))[0][0]
    
    wave_val = data.variables['VHM0'][index_time][min_index_lat][min_index_lon]
    
    if np.ma.is_masked(wave_val):
        print(index)
        print(np.mean(data.variables['VHM0'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5]))
        wave_val = np.mean(data.variables['VHM0'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5])
        
    wave.append(wave_val)


ataques_new = ataques.copy()

ataques_new['onda']=wave

ataques_new.to_excel('novo_com_wave_falsooooo.xlsx')
    
    #Acessing the average sea surface wave significant height
    #wave = data.variables['VHM0']
    
    