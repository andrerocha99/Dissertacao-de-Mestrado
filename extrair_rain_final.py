from netCDF4 import Dataset, num2date
from datetime import datetime,date,time, timedelta
import pandas as pd
import numpy as np

#Record all the years of the net CDF files into a Python list
all_years = ['2010','2011','2012','2013', '2014','2015','2016', '2017','2018','2019','2020']
        
year_start = min(all_years)
end_year = max(all_years)
date_range = pd.date_range(start = year_start + '-01-01',
                           end = end_year + '-12-31',
                           freq = 'M')                   #D é de frequência daily(diária)
df = pd.DataFrame(0.0, columns = ['Wind'], index = date_range)
   
#Definir a lat, lon e hora do ataque com base no ficheiro csv
ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_Limpa_Sem2021.xlsx')



rain = []

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
    if month<10:
        anomes = str(year)+'0'+str(month)
    else:
        anomes = str(year)+str(month)
    if year==2020:
        data = Dataset('2020_rain.nc')
    else:
        data = Dataset('Rainf_WFDE5_CRU+GPCC_{0}_v2.0.nc'.format(anomes))
    
     
    #Storing the lat and lon data of the netCDF file into variables
    if year==2020:
        lat = data.variables['latitude'][:]
        lon = data.variables['longitude'][:]
    else:
        lat = data.variables['lat'][:]
        lon = data.variables['lon'][:]
    
    
    
    time1 = data.variables['time'][:].data # saber de todas as datas
    
    units = data.variables['time'].units
    
    time_modif = num2date(time1,
                             units = units,
                             calendar = 'gregorian') # como modificar de numérico para data gregorian
    date_ = []
    
    
    for i in range(len(time_modif)): # mudar para datetime
        b = time_modif[i]
        reg = datetime(b.year,b.month,b.day,b.hour)
        date_.append(reg)

    
    #Squared Difference between the specified lat,lon and the lat,lon of the netCDF
    sq_diff_lat = (lat - location_latitude)**2
    sq_diff_lon = (lon - location_longitude)**2
    
    #Identify the index of the min value for lat and lon
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()
    
    Data_conv_rain = np.int(round((hour+minutes/60)))
    
    if Data_conv_rain==24:
        Data_conv_rain=0
        new_date = date(year,month,day)+timedelta(days=1)
        year = new_date.year
        month = new_date.month
        day = new_date.day
        if month<10:
            anomes = str(year)+'0'+str(month)
        else:
            anomes = str(year)+str(month)
        if year==2020:
            data = Dataset('2020_rain.nc')
        else:
            data = Dataset('Rainf_WFDE5_CRU+GPCC_{0}_v2.0.nc'.format(anomes))
        time1 = data.variables['time'][:].data # saber de todas as datas
    
        units = data.variables['time'].units
        
        time_modif = num2date(time1,
                                 units = units,
                                 calendar = 'gregorian') # como modificar de numérico para data gregorian
        date_ = []
        
        
        for i in range(len(time_modif)): # mudar para datetime
            b = time_modif[i]
            reg = datetime(b.year,b.month,b.day,b.hour)
            date_.append(reg)
        
        if year == 2020:
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
        else:
            lat = data.variables['lat'][:]
            lon = data.variables['lon'][:]
        
        #Squared Difference between the specified lat,lon and the lat,lon of the netCDF
        sq_diff_lat = (lat - location_latitude)**2
        sq_diff_lon = (lon - location_longitude)**2
    
        #Identify the index of the min value for lat and lon
        min_index_lat = sq_diff_lat.argmin()
        min_index_lon = sq_diff_lon.argmin()

            
    
    if year==2020:
        index_time = np.where(np.array(date_)==datetime.combine(date(year,month,day),time(Data_conv_rain)))[0][0]
        print(index_time)
        rain_val = data.variables['crr'][index_time][min_index_lat][min_index_lon]
        
        if np.ma.is_masked(rain_val):
            print(index)
            print(np.mean(data.variables['crr'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5]))
            rain_val = np.mean(data.variables['crr'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5])
    else:
        index_time = np.where(np.array(date_)==datetime.combine(date(year,month,day),time(Data_conv_rain)))[0][0]
        print(index_time)
        rain_val = data.variables['Rainf'][index_time][min_index_lat][min_index_lon]
    
        if np.ma.is_masked(rain_val):
            print(index)
            print(np.mean(data.variables['Rainf'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5]))
            rain_val = np.mean(data.variables['Rainf'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5])
    rain.append(rain_val)


ataques_new = ataques.copy()

ataques_new['chuva']=rain

ataques_new.to_excel('novo_com_chuva.xlsx')
    
    #Acessing the average sea surface wave significant height
    #wave = data.variables['VHM0']