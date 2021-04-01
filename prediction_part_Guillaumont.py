#%%
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import time
from datetime import datetime
#https://www.historique-meteo.net/site/export.php?ville_id=192
urlweather = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQX5i3DZ2AoGlj_sHXpUF3UKP9I-JaigZTdnFia60TEJdGMf6U0ta7-38bw1Txlkgy4yXIp16LpA762/pub?output=csv' 
weather = pd.read_csv(urlweather)
data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv')
#%% init data
data = data[data.columns[:4]].dropna(how = 'all') # remove empty cells and nan's cells
del data[data.columns[1]]
del data[data.columns[1]]
data['Date'] = pd.to_datetime(data['Date'])
data_day = data.drop_duplicates('Date', keep = 'last', inplace = False)
data_day[data_day["Date"] < '2021-04-02']


#%% Init weather
cPrecip = [weather.columns[0],weather.columns[7]] # keep usefull columns
weather = weather[cPrecip]
title = ['Date', 'PRECIP_TOTAL_DAY_M'] #rename columns df
weather = pd.DataFrame.drop(weather, index = [0,1,2]) 
weather.columns = title
# set_index pour virer la premiere col qui numérote les lignes
# .iloc for access to value in df
weather['Date'] = pd.to_datetime(weather['Date'], dayfirst = True)
weather = weather[weather["Date"] > np.repeat(pd.to_datetime('2020-03-11'), len(weather))]
weather['PRECIP_TOTAL_DAY_M'] = weather['PRECIP_TOTAL_DAY_M'].astype(float)
weather.loc[weather['PRECIP_TOTAL_DAY_M'] > 10,'PRECIP_TOTAL_DAY_M'] = 0 # weird values are 0
# %% make one df with weather and data_day
dataweather = pd.DataFrame()
dataweather['Rain'] = list(weather['PRECIP_TOTAL_DAY_M'])
dataweather['Daily_bikes'] = list(data_day["Vélos ce jour / Today's total"]) 
dataweather.index = weather['Date']
# %% OLS
plt.close()
X = dataweather['Rain']
X = sm.add_constant(X)
Y = dataweather['Daily_bikes']
model = sm.OLS(Y,X)
results = model.fit()
print(results.params)
plt.plot(dataweather.index, dataweather.Daily_bikes,'x')
# %% OLS only fridays
plt.close()
datafriday = dataweather[1::7]
Xf = datafriday['Rain']
Xf = sm.add_constant(Xf)
Yf = datafriday['Daily_bikes']
f_model = sm.OLS(Yf,Xf)
f_results = f_model.fit()
f_results.params
plt.plot(datafriday.index, datafriday.Daily_bikes,'x')

# %% OLS friday since Nov 2020
plt.close()
novfridaydata = datafriday[datafriday.index > '2020-11-01']

Xnovf = novfridaydata['Rain']
Xnovf = sm.add_constant(Xnovf)
Ynovf = novfridaydata['Daily_bikes']
novf_model = sm.OLS(Ynovf,Xnovf)
novf_results = novf_model.fit()
print(novf_results.params)
# polyfit only bikes, without rain
novcoef = np.polyfit(list(range(0,len(novfridaydata['Daily_bikes']))), novfridaydata['Daily_bikes'],3)
predictNov = np.polyval(novcoef,len(novfridaydata['Daily_bikes'])+1)
print(predictNov)
plt.plot(novfridaydata.index, novfridaydata['Daily_bikes'],'x')

print('La pluie est un evenement qui arrive relativement peu, la proportion de jour avec de la pluie le vendredi depuis le premier novembre est {} '.format((1-(novfridaydata['Rain'] == 0).sum()/len(novfridaydata['Rain'])).round(2)))
# %% OLS friday since Jan 2021
plt.close
janfridaydata = datafriday[datafriday.index > '2021-01-01']
plt.plot(janfridaydata.index, janfridaydata['Daily_bikes'],'x')
Xjanf = janfridaydata['Rain']
Xjanf = sm.add_constant(Xjanf)
Yjanf = janfridaydata['Daily_bikes']
janf_model = sm.OLS(Yjanf,Xjanf)
janf_results = janf_model.fit()
print(janf_results.params)
# polyfit only bikes without rain
predictJan = np.polyval(np.polyfit(list(range(0,len(janfridaydata['Daily_bikes']))), janfridaydata['Daily_bikes'],2),len(janfridaydata['Daily_bikes'])+1)
print(predictJan)
print('La pluie est un evenement qui arrive relativement peu, la proportion de jour avec de la pluie le vendredi depuis le premier janvier est {} '.format((1-(janfridaydata['Rain'] == 0).sum()/len(janfridaydata['Rain'])).round(2)))
# %% mean of two prediction from nov and jan without rain
finalPredictionDay = (predictJan + predictNov)/2
finalPrediction0to9 = finalPredictionDay * 0.21
print('My pronostic for number of bikers on 2nde April 2021 between midnight and 9AM is {}'.format(int(finalPrediction0to9.round())))