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
                           freq = 'D')                   #D é de frequência daily(diária)
df = pd.DataFrame(0.0, columns = ['Wind'], index = date_range)
   
#Definir a lat, lon e hora do ataque com base no ficheiro csv
ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_2.xlsx')

data1 = Dataset(all_years[0]+'.nc','r')
data2 = Dataset(all_years[1]+'.nc','r')
data3 = Dataset(all_years[2]+'.nc','r')
data4 = Dataset(all_years[3]+'.nc','r')
data5 = Dataset(all_years[4]+'.nc','r')
data6 = Dataset(all_years[5]+'.nc','r')
data7 = Dataset(all_years[6]+'.nc','r')
data8 = Dataset(all_years[7]+'.nc','r')
data9 = Dataset(all_years[8]+'.nc','r')
data10 = Dataset(all_years[9]+'.nc','r')
data11 = Dataset(all_years[10]+'.nc','r')



time1 = data1.variables['time'][:].data # saber de todas as datas do respetivo ano (cada ficheiro 1 ano)
time2 = data2.variables['time'][:].data # saber de todas as datas
time3 = data3.variables['time'][:].data # saber de todas as datas
time4 = data4.variables['time'][:].data # saber de todas as datas
time5 = data5.variables['time'][:].data # saber de todas as datas
time6 = data6.variables['time'][:].data # saber de todas as datas
time7 = data7.variables['time'][:].data # saber de todas as datas
time8 = data8.variables['time'][:].data # saber de todas as datas
time9 = data9.variables['time'][:].data # saber de todas as datas
time10 = data10.variables['time'][:].data # saber de todas as datas
time11 = data11.variables['time'][:].data # saber de todas as datas


units1 = data1.variables['time'].units
units2 = data2.variables['time'].units
units3 = data3.variables['time'].units
units4 = data4.variables['time'].units
units5 = data5.variables['time'].units
units6 = data6.variables['time'].units
units7 = data7.variables['time'].units
units8 = data8.variables['time'].units
units9 = data9.variables['time'].units
units10 = data10.variables['time'].units
units11 = data11.variables['time'].units


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

time_modif4 = num2date(time4,
                        units = units4,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date4 = []


for i in range(len(time_modif4)): # mudar para datetime
    b = time_modif4[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date4.append(reg)

time_modif5 = num2date(time5,
                        units = units5,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date5 = []


for i in range(len(time_modif5)): # mudar para datetime
    b = time_modif5[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date5.append(reg)

time_modif6 = num2date(time6,
                        units = units6,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date6 = []


for i in range(len(time_modif6)): # mudar para datetime
    b = time_modif6[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date6.append(reg)

time_modif7 = num2date(time7,
                        units = units7,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date7 = []


for i in range(len(time_modif7)): # mudar para datetime
    b = time_modif7[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date7.append(reg)

time_modif8 = num2date(time8,
                        units = units8,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date8 = []


for i in range(len(time_modif8)): # mudar para datetime
    b = time_modif8[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date8.append(reg)

time_modif9 = num2date(time9,
                        units = units9,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date9 = []


for i in range(len(time_modif9)): # mudar para datetime
    b = time_modif9[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date9.append(reg)

time_modif10 = num2date(time10,
                        units = units10,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date10 = []


for i in range(len(time_modif10)): # mudar para datetime
    b = time_modif10[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date10.append(reg)
    
time_modif11 = num2date(time11,
                        units = units11,
                        calendar = 'gregorian') # como modificar de numérico para data gregorian
date11 = []


for i in range(len(time_modif11)): # mudar para datetime
    b = time_modif11[i]
    reg = datetime(b.year,b.month,b.day,b.hour)
    date11.append(reg)


wind = []

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
    
    
    if year<2011:
        data = Dataset(all_years[0]+'.nc','r')
        date_ = date1
    elif year<2012:
        data = Dataset(all_years[1]+'.nc','r')
        date_ = date2
    elif year<2013:
        data = Dataset(all_years[2]+'.nc','r')
        date_ = date3
    elif year<2014:
        data = Dataset(all_years[3]+'.nc','r')
        date_ = date4
    elif year<2015:
        data = Dataset(all_years[4]+'.nc','r')
        date_ = date5
    elif year<2016:
        data = Dataset(all_years[5]+'.nc','r')
        date_ = date6
    elif year<2017:
        data = Dataset(all_years[6]+'.nc','r')
        date_ = date7
    elif year<2018:
        data = Dataset(all_years[7]+'.nc','r')
        date_ = date8
    elif year<2019:
        data = Dataset(all_years[8]+'.nc','r')
        date_ = date9
    elif year<2020:
        data = Dataset(all_years[9]+'.nc','r')
        date_ = date10
    else:
        data = Dataset(all_years[10]+'.nc','r')
        date_ = date11
               
    #Storing the lat and lon data of the netCDF file into variables
    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]
    
    
    
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
    
    Data_conv_wind = np.int(round((hour+minutes/60)/6)*6)
    
    if Data_conv_wind==24:
        Data_conv_wind=0
        new_date = date(year,month,day)+timedelta(days=1)
        year = new_date.year
        month = new_date.month
        day = new_date.day
        
    
    index_time = np.where(np.array(date_)==datetime.combine(date(year,month,day),time(Data_conv_wind)))[0][0]
    print(index_time)
    wind_val = data.variables['wind_speed'][index_time][min_index_lat][min_index_lon]
    
    if np.ma.is_masked(wind_val):
        print(index)
        print(np.mean(data.variables['wind_speed'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5]))
        wind_val = np.mean(data.variables['wind_speed'][index_time-0:index_time+1,min_index_lat-4:min_index_lat+5,min_index_lon-4:min_index_lon+5])
        
    wind.append(wind_val)


ataques_new = ataques.copy()

ataques_new['vento']=wind

ataques_new.to_excel('novo_com_wind.xlsx')
    
    #Acessing the average sea surface wave significant height
    #wave = data.variables['VHM0']
    