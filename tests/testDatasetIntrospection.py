import pyGDP
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
 
class TestDatasetIntrospection(object):

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
 
    def test_get_dataset_parameters(self):
	DATASET_URI = 'dods://cida.usgs.gov/qa/thredds/dodsC/prism'
        testPyGDP = pyGDP.pyGDPwebProcessing()

	datatypes = testPyGDP.getDataType(DATASET_URI, True)

	assert_equal(len(datatypes), 3)

	assert('ppt' in datatypes)
