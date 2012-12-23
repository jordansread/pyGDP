import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCoverageWCSIntersection(object):
 
    def test_submit_WCSIntersection(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
	shapefile = 'sample:simplified_HUC8s'
	attribute = 'SUBBASIN'
	value = 'Alafia'
	dataSetURI = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer'
	dataType = '6'

	outputFile_handle = testPyGDP.submitFeatureCoverageWCSIntersection(shapefile, dataSetURI, dataType, attribute, value, verbose=True)

	assert_equal(os.path.getsize(outputFile_handle), 1918261)
