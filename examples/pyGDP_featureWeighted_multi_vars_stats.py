import pyGDP

pyGDP = pyGDP.pyGDPwebProcessing()

"""
This example shows how to use multiple dataTypes and Statistics.

"""

shapefile = 'sample:simplified_HUC8s'
user_attribute = 'SUBBASIN'
user_value = 'Baraboo'
dataSet = 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml'
dataType = ['Prcp','Tavg','Tmax','Tmin']
timeBegin = '1970-01-24T00:00:00.000Z'
timeEnd = '1970-01-25T00:00:00.000Z'
gmlIDs=None
verbose=True
coverage='true'
delim='COMMA'
stats=['MEAN','STD_DEV']

print 'Processing request.'
outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)