from math import isnan
import pyreadr
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#RED IS D70040
#RED IS ALSO GOING TO BE SPEI

#BLUE IS 1434A4
#BLUE IS ALSO GOING TO BE scPDSI

#WHITE IS FFFFFF
#WHITE IS GOING TO BE FILL IN EMPTY

def mix_colors(hex_code_1, hex_code_2, percent_1, percent_2):
    if hex_code_2 == -1:
        return hex_code_1
    elif hex_code_1 == -1:
        return hex_code_2
    # Convert hex codes to RGB tuples
    elif not isnan(percent_1):
        try:
            hex_code_1 = hex_code_1.strip("#")
            hex_code_2 = hex_code_2.strip("#")
            r1, g1, b1 = tuple(int(hex_code_1[i:i+2], 16) for i in (0, 2, 4))
            r2, g2, b2 = tuple(int(hex_code_2[i:i+2], 16) for i in (0, 2, 4))
            
            # Calculate mixed RGB values
            r = int((r1 * percent_1) + (r2 * percent_2))
            g = int((g1 * percent_1) + (g2 * percent_2))
            b = int((b1 * percent_1) + (b2 * percent_2))
            
            # Convert mixed RGB values to hex format
            hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
            return hex_code
        except:
            print(f'error found, {hex_code_1}, {hex_code_2}, {percent_1}, {percent_2}')
    return -1

#1950 to 2020
#1950, 1962, 1974, 1986, 1998, 2010, 2020
#Other is monthly, jan, feb, etc

scPDSI = pyreadr.read_r('C:/Users/pasca/Desktop/Research/Step3/pdsi_1950-2021.rds')
scPDSI = scPDSI[None]

spei = pyreadr.read_r('C:/Users/pasca/Desktop/Research/Step3/spei_1950-2020.rds')
spei = spei[None]

scPDSI['Date'] = pd.to_datetime(dict(year=scPDSI.Year, month=scPDSI.Month, day=scPDSI.Day))
#                       scPDSI['Year'] = pd.DatetimeIndex(scPDSI['Date']).year
scPDSI['Month'] = pd.DatetimeIndex(scPDSI['Date']).month

print(type(scPDSI))

spei['Date'] = pd.to_datetime(dict(year=spei.Year, month=spei.Month, day=spei.Day))
#                           spei['Year'] = pd.DatetimeIndex(spei['Date']).year
spei['Month'] = pd.DatetimeIndex(spei['Date']).month

spei['scPDSI'] = ''
scPDSI['spei'] = ''

combined = scPDSI.append(spei)
combined_1962 = combined.loc[combined['Month'] == 12].reset_index(drop=True)
print(combined_1962)

combined_1962 = combined_1962.drop(columns=['Date'])
replace_scPDSI = pd.to_numeric(combined_1962['scPDSI'], errors='coerce')
replace_spei = pd.to_numeric(combined_1962['spei'], errors='coerce')

combined_1962['scPDSI'] = replace_scPDSI
combined_1962['spei'] = replace_spei

combined_1962_scPDSI = combined_1962.groupby(['x','y'], as_index = False)['scPDSI'].mean()
print(combined_1962_scPDSI)
combined_1962_spei = combined_1962.groupby(['x','y'], as_index = False)['spei'].mean()
print(combined_1962_spei)

print(type(combined_1962_scPDSI))
print(type(combined_1962_spei))

combined_1962_spei['scPDSI'] = combined_1962_scPDSI['scPDSI']

print(combined_1962_spei)

min_spei = combined_1962_spei['spei'].min()
max_spei = combined_1962_spei['spei'].max()

min_scPDSI = combined_1962_spei['scPDSI'].min()
max_scPDSI = combined_1962_spei['scPDSI'].max()

combined_1962_spei['perSPEI'] = (combined_1962_spei['spei'] - min_spei) / (max_spei - min_spei)
combined_1962_spei['perscPDSI'] = (combined_1962_spei['scPDSI'] - min_scPDSI) / (max_scPDSI - min_scPDSI)

print(combined_1962_spei)

#LEFT OFF DOING RED AND WHITE MIX, BLUE AND WHITE MIX
#THEN MIX THOSE 2 COLORS

speiHeatUsing = combined_1962_spei['perSPEI'].values.tolist()
seconadrySpeiUsing = [1 - x for x in speiHeatUsing]
redRepeat = ['#D70040']*len(speiHeatUsing)
whiteRepeat = ['#FFFFFF']*len(speiHeatUsing)

speiHeat = list(map(mix_colors, redRepeat, whiteRepeat, speiHeatUsing, seconadrySpeiUsing))

scPDSIHeatUsing = combined_1962_spei['perscPDSI'].values.tolist()
seconadryScPDSIUsing = [1 - x for x in scPDSIHeatUsing]
blueRepeat = ['#1434A4']*len(scPDSIHeatUsing)
whiteRepeat = ['#FFFFFF']*len(scPDSIHeatUsing)

print('testing')
print(combined_1962_spei['perscPDSI'].isna().sum())

scPDSIHeat = list(map(mix_colors, blueRepeat, whiteRepeat, scPDSIHeatUsing, seconadryScPDSIUsing))

print('len speiHeat', len(speiHeat))
print('len scPDSIHeat', len(scPDSIHeat))

halfPer = [0.5]*len(scPDSIHeatUsing)
finalMix = list(map(mix_colors, speiHeat, scPDSIHeat, halfPer, halfPer))
print(finalMix)

combined_1962_spei['colors'] = finalMix
print(combined_1962_spei)

m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
x, y = m(combined_1962_spei['x'].values, combined_1962_spei['y'].values)

plt.figure(figsize=(10,8))
plt.scatter(x, y, c=combined_1962_spei['colors'], s=20, alpha=0.5)
#xmin = 1.562e+07, ymin = 1.00e+07, xmax = 2.600e+07, ymax = 1.910e+07
#plt.axis([1.562e+07, 2.600e+07, 1.00e+07, 1.910e+07])
plt.xlim(1.562e+07, 2.600e+07)
plt.ylim(1.00e+07, 1.910e+07)

m.drawcoastlines()
plt.colorbar()
plt.show()