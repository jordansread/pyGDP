import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureCoverageWCSIntersection(object):
 
    def test_submit_WCSIntersection(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
	shapefile = 'sample:CONUS_States'
	attribute = 'STATE'
	value = 'Alabama'
	dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml'
	dataType = 'Prcp'
	timeStart = '1950-01-01T00:00:00.000Z'
	timeEnd = '1951-01-31T00:00:00.000Z'

	outputFile_handle = testPyGDP.submitFeatureCoverageWCSIntersection(shapefile, dataSetURI, dataType, timeStart, timeEnd, attribute, value, verbose=True)

	assert_equal(os.path.getsize(outputFile_handle), 18416)
