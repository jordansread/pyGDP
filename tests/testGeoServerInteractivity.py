import pyGDP
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
 
class TestGeoServerInteractivity(object):
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
 
    def test_get_shapefile_list(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()

	shapefiles = testPyGDP.getShapefiles()

	assert_not_equal(len(shapefiles), 0)

    def test_get_shapefile_attributes(self):
	testPyGDP = pyGDP.pyGDPwebProcessing()
	
	shapefile  = 'sample:CONUS_States'

	attributes = testPyGDP.getAttributes(shapefile)

	assert_equal(len(attributes), 9)
	
	assert('STATE' in attributes)

    def test_get_shapefile_values(self):
	testPyGDP = pyGDP.pyGDPwebProcessing()
	
	shapefile  = 'sample:CONUS_States'  
	
	attribute = 'STATE'
	
	values    = testPyGDP.getValues(shapefile,attribute)
	
	assert_equal(len(values), 49)

	assert('Wisconsin' in values)
