import pyGDP
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
 
class TestCSWreturnsurl(object):

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
 
    def test_get_uri(self):
	testPyGDP = pyGDP.pyGDPwebProcessing()
	dataseturis=testPyGDP.getDataSetURI(anyText='prism')
	uris=[]
	for dat in dataseturis:
	    for uri in dat[2]:
	        uris.append(uri)
	
	assert_equal(len(dataseturis), 3)
	assert_equal('dods://cida.usgs.gov/thredds/dodsC/prism' in uris, True)


	
