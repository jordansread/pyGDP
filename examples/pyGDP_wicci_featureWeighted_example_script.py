import pyGDP

"""
This script demonstrates how to search for a particular dataset and loop through a list of OPeNDAP resources associated with it. 

This runs a very small subset of the dataset for example purposes. See notes for how to expand the scope of processing.

"""
pyGDP = pyGDP.pyGDPwebProcessing()

shapefiles = pyGDP.getShapefiles()
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

# Choose Delaware
# Note that removing "value" in the main request below will run all values in the shapefile.
value = ['Delaware']

# Search for datasets
dataSetURIs = pyGDP.getDataSetURI(anyText='wicci')
for dataset in dataSetURIs:
	print dataset

# Loop through datasets of interest, in this case the first three OPeNDAP urls. 
for dataSetURI in dataSetURIs[1][2][0:3]:
	# Get the available data types associated with the dataSetURI
	dataTypes = pyGDP.getDataType(dataSetURI)
	print dataTypes
	# For this example just run the first dataType. This dataType list should be modified if multiple datatypes are required.
	dataType = dataTypes[0]
	print dataType
	# Get available time range for the dataset.
	timeRange = pyGDP.getTimeRange(dataSetURI, dataType)
	print timeRange
	# Execute a GeatureWeightedGridStatistics request and return the path to the output file. 
	# Note that this is for one time step but could be for multiple. Please test on very short time periods to minimize impacts on system resources.
	outputfile = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeRange[0], timeRange[0], usr_attribute, value)
	print outputfile
