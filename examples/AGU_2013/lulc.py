import matplotlib.dates as mdates
from matplotlib.ticker import LinearLocator
import numpy
import pylab
from pylab import plot, show
import pyGDP
import array
import os
from datetime import datetime

pyGDP = pyGDP.pyGDPwebProcessing()

# using the default WFS, specify the shapefile to use.
# Used http://cida.usgs.gov/gdp/client/?development=true to identify the next three values.
shapefile='sample:simplified_HUC8s'
attribute='SUBBASIN'
value='Au Sable'

### Land Use Land Cover
# This dataset URI is available here: http://cida.usgs.gov/thredds/
# OPeNDAP html page is: http://cida.usgs.gov/thredds/dodsC/iclus/hd_is.html
datasetURI='dods://cida.usgs.gov/thredds/dodsC/iclus/hd_is'

# Note that pyGDP offers convenience functions to determine what these options are.
# These were derived from the thredds server housing the data.
dataType = 'housing_density_hd_iclus_a2'
timeStart = '2000-01-01T00:00:00.000Z'
timeEnd   = '2100-01-01T00:00:00.000Z'

outputFileName = 'HousingDensityAuSable2000-2100.csv'
# 
# outputFile_handle = pyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value,verbose=True)
# os.rename(outputFile_handle,outputFileName)

dates = []
vals  = []
datesT,valsT = numpy.loadtxt(outputFileName,unpack=True,skiprows=3,delimiter=',',
        converters={0: mdates.strpdate2num("%Y-%m-%dT%H:%M:%SZ")})

for v in valsT:
    vals.append(v)

for d in datesT:
    dates.append(d)

fig = pylab.figure(figsize=(12,6),facecolor='w')
fig.suptitle('ICLUS A2 Housing Density, Au Sable Watershed',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Housing Density (Housing Units Per Hectare)', fontsize=18)
ax.plot_date(dates,vals,'b-')
ax.xaxis.set_major_locator(mdates.YearLocator(10,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

ax.set_ylim([70,73])
majorLocator   = LinearLocator(numticks=5)
ax.yaxis.set_major_locator(majorLocator)

show()

### Downscaled Climate
# This dataset URI is available here: http://cida.usgs.gov/thredds/
# OPeNDAP html page is: http://cida.usgs.gov/thredds/dodsC/iclus/hd_is.html
datasetURI='dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml'

# Note that pyGDP offers convenience functions to determine what these options are.
# These were derived from the thredds server housing the data.
dataType = ['sresa2_inmcm3-0_1_Prcp','sresa2_inmcm3-0_1_Tavg','sresa1b_inmcm3-0_1_Prcp','sresa1b_inmcm3-0_1_Tavg']
timeStart = '2000-01-01T00:00:00.000Z'
timeEnd   = '2100-01-01T00:00:00.000Z'

outputFileName = 'ClimateProjectionAuSable2000-2100.csv'

# outputFile_handle = pyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value,verbose=True)
# os.rename(outputFile_handle,outputFileName)

var_list  = []
dates = []
vals = []
header=True
dataFile=open(outputFileName)
for line in dataFile:
    if line[0] == '#':
        var_list.append(line[2:len(line)-1])
        vals.append([])
        dates.append([])
    elif line[0] == ',':
        if header == True:
            feature_ids = line[1:len(line)-1].split(',')
    elif line[0:4] == 'TIME':
        if header == True:
            stats_units = line[9:len(line)-1].split(',')
            header=False
    else:
        data = line.split(',') #(line,unpack=True,delimiter=',',converters={0: mdates.strpdate2num("%Y-%m-%dT%H:%M:%SZ")})
        date = datetime.strptime(data[0],"%Y-%m-%dT%H:%M:%SZ")
        dates[len(var_list)-1].append(mdates.date2num(date))
        vals[len(var_list)-1].append(map(float,data[1:len(data)]))

fig = pylab.figure(figsize=(12,6),facecolor='w')
fig.suptitle('CMIP3 A2 Climate Projections (INCMCM3 GCM)',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Monthly Precipitation (mm)', fontsize=18)
ax.plot_date(dates[0],vals[0],'b-')
ax.xaxis.set_major_locator(mdates.YearLocator(10,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

#ax.set_ylim([185.5,187.5])
majorLocator   = LinearLocator(numticks=5)
ax.yaxis.set_major_locator(majorLocator)

show()

fig = pylab.figure(figsize=(12,6),facecolor='w')
fig.suptitle('CMIP3 A2 Climate Projections (INCMCM3 GCM)',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Monthly Average Temperature (C)', fontsize=18)
ax.plot_date(dates[1],vals[1],'r-')
ax.xaxis.set_major_locator(mdates.YearLocator(10,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

#ax.set_ylim([185.5,187.5])
majorLocator   = LinearLocator(numticks=5)
ax.yaxis.set_major_locator(majorLocator)

show()
