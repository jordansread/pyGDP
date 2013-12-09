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
# This dataset URI will be available here: http://cida.usgs.gov/thredds/
# At the time of creation, this dataset was internal USGS only.
datasetURI='http://cida-eros-thredds1.er.usgs.gov:8081/qa/thredds/dodsC/ssebopeta/monthly'

# Note that pyGDP offers convenience functions to determine what these options are.
# These were derived from the thredds server housing the data.
dataType = 'et'
timeStart = '2000-01-01T00:00:00.000Z'
timeEnd   = '2010-01-01T00:00:00.000Z'

outputFileName = 'ETAuSable2000-2010.csv'

outputFile_handle = pyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value,verbose=True)
os.rename(outputFile_handle,outputFileName)

dates = []
vals  = []
datesT,valsT = numpy.loadtxt(outputFileName,unpack=True,skiprows=3,delimiter=',',
        converters={0: mdates.strpdate2num("%Y-%m-%dT%H:%M:%SZ")})

for v in valsT:
    vals.append(v)

for d in datesT:
    dates.append(d)

fig = pylab.figure(figsize=(12,6),facecolor='w')
fig.suptitle('SSEBop Actual Evapotranspiration, Au Sable Watershed',fontsize=26)
ax = fig.gca()
ax.set_ylabel('Monthly Actual Evapotranspiration (mm)', fontsize=18)
ax.plot_date(dates,vals,'g-')
ax.xaxis.set_major_locator(mdates.YearLocator(10,month=1,day =1))
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %Y'))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(18)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(18)

#ax.set_ylim([182,192])
majorLocator   = LinearLocator(numticks=5)
ax.yaxis.set_major_locator(majorLocator)

show()


