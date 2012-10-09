import pyGDP
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
 
class TestPyGDP(object):
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
 
    def test_return_true(self):
        #pyGDP = pyGDP.pyGDPwebProcessing()
        assert_equal(1, 1)
        assert_not_equal(1, 2)

