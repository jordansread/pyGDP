import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
 
class TestProcessRequestUsingPolygon(object):
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
 
    def test_submit_FWGS(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
	shapefile  = 'sample:CONUS_States'
	attribute  = 'STATE'
	value 	   = 'Wisconsin'
	userPoly   = [(-102.8184, 39.5273), (-102.8184, 37.418), (-101.2363, 37.418), (-101.2363,39.5273), (-102.8184, 39.5273)]
	datasetURI = 'dods://cida.usgs.gov/qa/thredds/dodsC/prism'
	dataType   = 'ppt'
	timeStart  = '1900-01-01T00:00:00.000Z'
	timeEnd    = '1950-01-01T00:00:00.000Z'
	 
	outputFile_handle = testPyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value)
  
	# ALERT: Fragile Test :)
	print os.path.getsize(outputFile_handle, 18416)
