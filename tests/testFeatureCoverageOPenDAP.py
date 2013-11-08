import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCoverageOPenDAP(object):
 
    def test_submit_FCOD(self):
        pyGDP.WPS_URL='http://cida.usgs.gov/gdp/process/WebProcessingService'
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
    	shapefile = 'sample:CONUS_States'
    	attribute = 'STATE'
    	value = 'Alabama'
    	dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml'
    	dataType = 'Prcp'
    	timeStart = '1950-01-01T00:00:00.000Z'
    	timeEnd = '1950-01-02T00:00:00.000Z'

    	outputFile_handle = testPyGDP.submitFeatureCoverageOPenDAP(shapefile, dataSetURI, dataType, timeStart, timeEnd, attribute, value)

    	# This test is not currently working because what comes from 
    	# testPyGDP.submitFeatureCoverageOPenDAP() is a NoneType
    	# even though I've verified that it constistently writes a 
    	# file of the size below. I expect a string to come back from 
    	# this function
    	assert_equal(os.path.getsize(outputFile_handle), 14312)
