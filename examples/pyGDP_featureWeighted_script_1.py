import pyGDP
import pprint
"""
This example script calls into the geoserver to obtain
the name of the shapefile 'sample:CONUS_States' searches for PRISM data 
and submits a featureWeightedGridStatistics request into GDP.
"""

pyGDP = pyGDP.pyGDPwebProcessing()

shapefiles = pyGDP.getShapefiles()
print 'Available shapefiles: '
for shapefile in shapefiles:
    print shapefile

# Grab the file and get its attributes:
shapefile = 'sample:CONUS_states'
attributes = pyGDP.getAttributes(shapefile)
for attr in attributes:
    print attr

# Grab the values from the 'STATE' attribute:
usr_attribute = 'STATE'
values = pyGDP.getValues(shapefile, usr_attribute)
for v in values:
    print v

# Instead of specifically specifying a value, we get request to get
# the gmlID of these values and append them to a gmlID to be used
# as an input instead of value.
michGMLID = pyGDP.getGMLIDs(shapefile, usr_attribute, 'Michigan')
gmlIDs = michGMLID

# We get the dataset URI that we are interested in by searching for prism:
dataSetURIs = pyGDP.getDataSetURI(anyText='prism')
pp = pprint.PrettyPrinter(indent=5,width=60)
pp.pprint(dataSetURIs)

# Set our datasetURI
dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/prism'
# Get the available data types associated with the dataset
datatypes = pyGDP.getDataType(dataSetURI)
for dt in datatypes:
	print dt

# Set the dataType. Note that leaving dataType out below will select all.
dataType = 'ppt'
# Get available time range on the dataset
timeRange = pyGDP.getTimeRange(dataSetURI, dataType)
for t in timeRange:
    print t


# Instead of submitting in a value, we submit a list of gmlIDs associated
# with either a small portion of that value, or multiple values.

value = None
path = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeRange[0], timeRange[0], usr_attribute, value, gmlIDs, verbose=True)
print path
