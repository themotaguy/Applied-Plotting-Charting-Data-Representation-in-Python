
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[2]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[3]:

get_ipython().magic('matplotlib notebook')
get_ipython().magic('matplotlib inline')

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

import pandas as pd
import numpy as np


# In[9]:

data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

data['Data_Value'] = data['Data_Value']*0.1
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month_Day'] = data['Date'].dt.strftime('%m-%d')

data = data[data['Month_Day'] != '02-29']

max_temp = data[(data.Year >= 2005) & (data.Year < 2015) & (data['Element'] == 'TMAX')].groupby(['Month_Day'])['Data_Value'].max()
min_temp = data[(data.Year >= 2005) & (data.Year < 2015) & (data['Element'] == 'TMIN')].groupby(['Month_Day'])['Data_Value'].min()

data = data.merge(max_temp.reset_index(drop = False).rename(columns = {'Data_Value':'Max_Temp'}), on = 'Month_Day', how = 'left')
data = data.merge(min_temp.reset_index(drop = False).rename(columns = {'Data_Value':'Min_Temp'}), on = 'Month_Day', how = 'left')

record_high = data[(data.Year == 2015) & (data.Data_Value > data.Max_Temp)]
record_low = data[(data.Year == 2015) & (data.Data_Value < data.Min_Temp)]

date_index = np.arange('2015-01-01', '2016-01-01', dtype = 'datetime64[D]')

plt.figure()

plt.plot(date_index, max_temp, color = 'lightcoral', linewidth = 1)
plt.plot(date_index, min_temp, color = 'skyblue', linewidth = 1)

plt.scatter(record_high.Date.values, record_high.Data_Value.values, color = 'red', s = 8)
plt.scatter(record_low.Date.values, record_low.Data_Value.values, color = 'blue', s = 8)

ax = plt.gca()
ax.axis(['2015/01/01', '2015/12/31', -50,50])

plt.xlabel('Date', fontsize = 10)
plt.ylabel('℃elsius', fontsize = 10)
plt.title('Temperature in Ann Arbour, Michigan, United States(2005-2015)', fontsize = 12)

plt.legend(['Record High (2005-2015)', 'Record Low (2005-2015)', 'Record Breaking High in 2015', 'Record Breaking Low in 2015'], loc = 0, frameon = False)

ax.fill_between(date_index, max_temp, min_temp, facecolor = 'grey', alpha = 0.25)

ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday = 15))
#ax.yaxis.set_minor_locator()

ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



