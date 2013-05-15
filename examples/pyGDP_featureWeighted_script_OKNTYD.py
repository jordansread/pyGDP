import pyGDP
import numpy as np
import matplotlib.dates as mdates
import pprint

pyGDP = pyGDP.pyGDPwebProcessing()


filePath = 'testUpload.zip'
#upload the file to geoserver
try:
	shpfile = pyGDP.uploadShapeFile(filePath)
except Exception:
	print 'A file of this name already exists, it has not been replaced.'
else:
	print 'Shapefile Uploaded'

print 
shapefiles = pyGDP.getShapefiles()
print 'Available shapefiles: '
for shapefile in shapefiles:
    print shapefile
print
 
# Grab the file and get its attributes:
OKshapefile = shpfile
if OKshapefile not in shapefiles:
    print str(shpfile) + ' not on server.'
    exit()
print

attributes = pyGDP.getAttributes(OKshapefile)
for attr in attributes:
    print attr
print

# Grab the values from 'OBJECTID' and 'upload:OKCNTYD'
usr_attribute = 'OBJECTID'
values = pyGDP.getValues(OKshapefile, usr_attribute)
for v in values:
    print v
print

#We set our value to 13
usr_value = 13

# our shapefile = 'upload:OKCNTYD', usr_attribute = 'OBJECTID', and usr_value = 13
# We get the dataset URI that we are interested in
dataSetURIs = pyGDP.getDataSetURI(anyText='prism')
pp = pprint.PrettyPrinter(indent=5,width=60)
pp.pprint(dataSetURIs)
print

# Set our datasetURI
dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/prism'
# Get the available data types associated with the dataset
dataType = 'ppt'
# Get available time range on the dataset
timeRange = pyGDP.getTimeRange(dataSetURI, dataType)
for t in timeRange:
    print t
timeBegin = '1900-01-01T00:00:00.000Z'
timeEnd = '1901-01-01T00:00:00.000Z'
print


textFile = pyGDP.submitFeatureWeightedGridStatistics(OKshapefile, dataSetURI, dataType, timeBegin, timeEnd,usr_attribute, usr_value,verbose=True)

jd,precip=np.loadtxt(textFile,unpack=True,skiprows=3,delimiter=',', 
                     converters={0: mdates.strpdate2num('%Y-%m-%dT%H:%M:%SZ')})

print 'Some data:'
print precip[0:100]