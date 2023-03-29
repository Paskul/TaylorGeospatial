import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import pyreadr
from shapely.geometry import Point, Polygon
import math
import plotly
import plotly.express as px
from geopy.geocoders import Nominatim
import pycountry
import country_converter
import plotly.offline as py
import plotly.graph_objs as go


geolocator = Nominatim(user_agent="geoapiExercises")

africa = gpd.read_file('C:/Users/pasca/Desktop/Research/Step2/afr_g2014_2013_0.shp')

data = pyreadr.read_r('C:/Users/pasca/Desktop/Research/Step2/Pascal_data.rds') # also works for RData
data = data[None]

print(data.head())
#'ADM0_NAME'
#data = data.drop(columns=['shape_id', 'ADM0_CODE', 'CONTINENT', 'ISO3',
       #'ISO2', 'UNI', 'UNDP', 'FAOSTAT', 'GAUL', 'RIC_ISO3', 'REC_ISO3', 'AFR',
       #'CEMAC', 'CILSS', 'CRA', 'ECOWAS', 'IGAD', 'IOC', 'SADC', 'CICOS',
       #'ICPAC', 'BDMS', 'MOI'])

#data = data.drop(columns=['shape_id', 'ADM0_CODE', 'CONTINENT', 'ADM0_NAME',
       #'ISO2', 'UNI', 'UNDP', 'FAOSTAT', 'GAUL', 'RIC_ISO3', 'REC_ISO3', 'AFR',
       #'CEMAC', 'CILSS', 'CRA', 'ECOWAS', 'IGAD', 'IOC', 'SADC', 'CICOS',
       #'ICPAC', 'BDMS', 'MOI'])

data['time'] = pd.to_datetime(data['time'])
data.set_index('time', inplace=True)
data = data['2008':'2020']

print('time split break -------------------------')

print(data.head())

lonLatPairs = []
speiPairs = []
speiCount = []
countryName = []
for index, row in data.iterrows():
    lon = row['lon']
    lat = row['lat']
    spei = row['spei']
    country = row['ISO2']
    #OR country = row['ADM0_NAME']
    if [lon,lat] not in lonLatPairs:
        lonLatPairs.append([lon,lat])
        speiPairs.append(spei)
        speiCount.append(1)
        countryName.append(country)
    else:
        index = lonLatPairs.index([lon,lat])
        if math.isnan(spei):
            print('haha nan', end='')
        else:
            speiPairs[index] = speiPairs[index] + spei
        speiCount[index] += 1

for i in range(len(speiPairs)):
    speiPairs[i] = speiPairs[i] / speiCount[i]
print('done with haha')

print(len(lonLatPairs))
print(lonLatPairs)
print('break lon lat pairs')
print(len(speiPairs))
print(speiPairs)
print('break spei pairs')
print(len(countryName))
print(countryName)
print('break country name')

'''
OLD APPROACH, TRYING TO INCORPORATE Bir Tawil AND Ilemi Triangle, NOW WILL JUST REMOVE THAT DATA
newCountries=[]
for lon, lat in lonLatPairs:
    print(str(lon)+","+str(lat))
    if ((lon == -6.94607218433) and (lat == 51.5055113053)):
        newCountries.append('Seychelles')
    elif ((lon == 21.8883763834) and (lat == 33.6880375022)):
        newCountries.append('Bir Tawil')
        print(newCountries[-1], 'found at', index(lonLatPairs))
    elif ((lon == 4.76005845916) and (lat == 35.0376405729)):
        newCountries.append('Ilemi Triangle')
        print(newCountries[-1], 'found at', lonLatPairs.index())
    else:
        location = geolocator.reverse(str(lon)+","+str(lat), language='en')
        print(location)
        address = location.raw['address']
        country = address.get('country', '')
        newCountries.append(country)
        print(country)
'''

newCountries=[]
newLonLatPairs = lonLatPairs

print(len(newLonLatPairs))
#might be wrong values above, check

print(len(speiPairs))
print(len(newCountries))
#57 should be length because removing 2 from 59

del newLonLatPairs[58]
del newLonLatPairs[56]

del speiPairs[58]
del speiPairs[56]

#-------ABOVE DELETES ARE FROM BAD VALUES FOUND IN LOOP BELOW-------

del newLonLatPairs[48]
del newLonLatPairs[54]

del speiPairs[48]
del speiPairs[54]

print('break for compare--------------')
for lon, lat in lonLatPairs:
    print(str(lon)+","+str(lat))
    if ((lon == -6.94607218433) and (lat == 51.5055113053)):
        newCountries.append('Seychelles')
    elif ((lon == 21.8883763834) and (lat == 33.6880375022)):
        #newCountries.append('Bir Tawil')

        #just got error line below, swapped lat lon no
        useIndex = lonLatPairs.index([lon,lat])
        print('delete time Bir Tawil')
        print(useIndex)
    elif ((lon == 4.76005845916) and (lat == 35.0376405729)):
        #newCountries.append('Ilemi Triangle')
        useIndex = lonLatPairs.index([lon,lat])
        print('delete time Ilemi Triangle')
        #del speiPairs[useIndex]
        #del lonLatPairs[useIndex]
        #del newLonLatPairs[useIndex]
        #print(len(newLonLatPairs))
        #print(len(speiPairs))
        #print(len(newCountries))
        print(useIndex)

        #56 and 58
    else:
        location = geolocator.reverse(str(lon)+","+str(lat), language='en')
        print(location)
        address = location.raw['address']
        country = address.get('country', '')
        newCountries.append(country)
        print(country)
        useIndex = lonLatPairs.index([lon,lat])
        print('index at', useIndex)

print(len(newLonLatPairs))
#might be wrong values above, check

print(len(speiPairs))
print(len(newCountries))
#57 should be length because removing 2 from 59


newIS03 = country_converter.convert(names=newCountries, to='ISO3')
newIS03[38] = 'SOM'
newIS03[53] = 'ESH'

print(newIS03)
print('break0000-1-1-1-1-1-')
for i in range(0, len(newIS03)):    
    for j in range(i+1, len(newIS03)):    
        if(newIS03[i] == newIS03[j]):    
            print(newIS03[j]);    

#need to keep removing repeating values

newData = {'lat': [i[0] for i in newLonLatPairs],
        'lon': [i[1] for i in newLonLatPairs],
        'spei': speiPairs,
        'iso3': newIS03
        }

df = pd.DataFrame(newData)

print('break new dataframe -----------')
print(df)

layout = dict(geo={'scope': 'africa'}, title={'text': 'Average SPEI 2008-2020', 'xanchor': 'center', 'x': 0.5, 'y': 0.9, 'yanchor': 'top'})
newData2 = dict(
    type='choropleth',
    locations=df['iso3'],
    locationmode='ISO-3',
    colorscale='Viridis',
    z=df['spei'])

map = go.Figure(data=[newData2], layout=layout)
py.plot(map)
