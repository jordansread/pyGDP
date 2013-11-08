import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCoverageWCSIntersection(object):
 
    def test_submit_WCSIntersection(self):
        pyGDP.WPS_URL='http://cida.usgs.gov/gdp/process/WebProcessingService'
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
    	shapefile = 'sample:simplified_HUC8s'
    	attribute = 'HUC_8'
    	value = '08010211'
    	dataSetURI = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer'
    	dataType = '6'

    	outputFile_handle = testPyGDP.submitFeatureCoverageWCSIntersection(shapefile, dataSetURI, dataType, attribute, value)

    	assert_equal(os.path.getsize(outputFile_handle), 1311757)
