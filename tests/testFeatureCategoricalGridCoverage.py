import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCategoricalGridCoverage(object):
 
    def test_submit_FCGC(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
	shapefile = 'sample:CONUS_States'
	attribute = 'STATE'
	value = 'Rhode Island'
	dataSetURI = 'http://cida.usgs.gov/ArcGIS/services/statsgo_numid/MapServer/WCSServer'
	dataType = '1'

	outputFile_handle = testPyGDP.submitFeatureCategoricalGridCoverage(shapefile, dataSetURI, dataType, attribute, value, verbose=True)
  
	# This test is not currently working because what comes from
	# testPyGDP.submitFeatureCategoricalGridCoverage() is a NoneType
	# even through I've verified that it consistently writes a file
	# of the size below. I expect a string to come back from this
	# function
	assert_equal(os.path.getsize(outputFile_handle), 650)
