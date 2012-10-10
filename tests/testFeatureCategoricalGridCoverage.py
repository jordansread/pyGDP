import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCategoricalGridCoverage(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
 
    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""
 
    def setUp(self):
        """This method is run once before _each_ test method is executed"""
 
    def teardown(self):
        """This method is run once after _each_ test method is executed"""
 
    def test_submit_FCGC(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
	shapefile = 'sample:CONUS_States'
	attribute = 'STATE'
	value = 'Alabama'
	dataSetURI = 'http://cida.usgs.gov/ArcGIS/services/statsgo_numid/MapServer/WCSServer'
	dataType = '1'

	outputFile_handle = testPyGDP.submitFeatureCategoricalGridCoverage(shapefile, dataSetURI, dataType, attribute, value, verbose=True)
  
	print outputFile_handle

	assert_equal(os.path.getsize(outputFile_handle), 18416)
