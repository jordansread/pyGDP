import pyGDP

pyGDP = pyGDP.pyGDPwebProcessing()


shapefile = 'sample:CONUS_States'
attribute = 'STATE'
value = 'Alabama'

dataSetURI = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer'

dataType = '1'
file_handle = pyGDP.submitFeatureCategoricalGridCoverage(shapefile, dataSetURI, dataType, attribute, value, verbose=True)