import pyGDP

pyGDP = pyGDP.pyGDPwebProcessing()
"""
This example script calls into the geoserver to obtain
the name of the shapefile 'sample:CONUS_States' sets up the
proper inputs and submits a request into GDP.
"""

shapefiles = pyGDP.getShapefiles()
print 'Available shapefiles: '
for shapefile in shapefiles:
    print shapefile


# Grab the attributes for sample:CONUS_States
shapefile = 'sample:CONUS_states'
attributes = pyGDP.getAttributes(shapefile)
for attr in attributes:
    print attr


# Grab the values from the STATE attribute of sample:CONUS_States
usr_attribute = 'STATE'
values = pyGDP.getValues(shapefile, usr_attribute)
for v in values:
    print v

# Choose Colorado
value = ['Colorado']

# Search for datasets
dataSetURIs = pyGDP.getDataSetURI(anyText='prism')
for dataset in dataSetURIs:
	print dataset

# Set our datasetURI to the OPeNDAP/dods response for the prism dataset.
dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/prism'

# Get the available data types associated with the dataset
dataTypes = pyGDP.getDataType(dataSetURI)
for dataType in dataTypes:
	print dataType

dataType = 'ppt'

# Get available time range for the dataset.
timeRange = pyGDP.getTimeRange(dataSetURI, dataType)
for t in timeRange:
    print t

# Execute a GeatureWeightedGridStatistics request and return the path to the output file. 
# Note that this is for one time step but could be for multiple.
outputfile = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeRange[0], timeRange[0], usr_attribute, value, verbose=True)
print outputfile
