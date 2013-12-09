import matplotlib.dates as mdates
import numpy
import pylab
from pylab import plot, show
import pyGDP
import array
import os

pyGDP = pyGDP.pyGDPwebProcessing()

# using the default WFS, specify the shapefile to use.
# Used http://cida.usgs.gov/gdp/client/?development=true to identify the next three values.
shapefile='sample:simplified_HUC8s'
attribute='SUBBASIN'
value='Au Sable'

### Hourly Precip
# This dataset URI is available here: http://cida.usgs.gov/thredds/rfc_qpe/
# OPeNDAP html page is: http://cida.usgs.gov/thredds/rfc_qpe/dodsC/RFC/QPE/KMSR.html
datasetURI='dods://cida.usgs.gov/thredds/rfc_qpe/dodsC/RFC/QPE/KMSR'

# Note that pyGDP offers convenience functions to determine what these options are.
# These were derived from the thredds server housing the data.
dataType = '1-hour_Quantitative_Precip_Estimate_surface_1_Hour_Accumulation'
timeStart = '2000-01-01T00:00:00.000Z'
timeEnd   = '2010-01-01T00:00:00.000Z'

outputFileName = 'AuSableRadarPrcp2000-2010.csv'

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
fig.suptitle('Radar Indicated Rainfall, Au Sable Watershed',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Precipitation (mm)', fontsize=18)
ax.plot_date(dates,vals,'b-')
ax.xaxis.set_major_locator(mdates.YearLocator(1,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

show()

### Daily Precip
# This daymet service is internal USGS only.
datasetURI='dods://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet'
dataType = 'prcp'

outputFileName = 'AuSableDaymetPrcp2000-2010.csv'

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
fig.suptitle('DayMet Rainfall, Au Sable Watershed',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Precipitation (mm)', fontsize=18)
ax.plot_date(dates,vals,'b-')
ax.xaxis.set_major_locator(mdates.YearLocator(1,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

show()

### Monthly Precip
# This daymet service is internal USGS only.
datasetURI='http://cida.usgs.gov/thredds/dodsC/prism'
dataType = 'ppt'

outputFileName = 'AuSablePrismPrcp2000-2010.csv'

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
fig.suptitle('PRISM Rainfall, Au Sable Watershed',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Precipitation (mm)', fontsize=18)
ax.plot_date(dates,vals,'b-')
ax.xaxis.set_major_locator(mdates.YearLocator(1,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

show()