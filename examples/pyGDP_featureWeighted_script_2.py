import pyGDP
'''
Shows GDP workflow in using specific values of attributes from a shapefile
that already exists on the GDP server.
'''


pyGDP = pyGDP.pyGDPwebProcessing()
shapefiles = pyGDP.getShapefiles()
print 'Available shapefiles: '
for shapefile in shapefiles:
    print shapefile

# Grab the file and get its attributes:
shapefile = 'sample:CSC_Boundaries'
attributes = pyGDP.getAttributes(shapefile)
for attr in attributes:
    print attr

# Grab the values from 'area_name' and 'sample:CSC_Boundaries'
usr_attribute = 'area_name'
values = pyGDP.getValues(shapefile, usr_attribute)
for v in values:
    print v

usr_value = 'Southwest'

dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml'
dataTypes = pyGDP.getDataType(dataSetURI)
for d in dataTypes:
    print d

dataType = 'Prcp'
# Get available time range on the dataset
timeRange = pyGDP.getTimeRange(dataSetURI, dataType)
for t in timeRange:
    print t

timeBegin = '1960-01-01T00:00:00.000Z'
timeEnd = '1960-01-21T00:00:00.000Z'
outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeBegin, timeEnd, usr_attribute, usr_value, gmlIDs=None, verbose=True)

