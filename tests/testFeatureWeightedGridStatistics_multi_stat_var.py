import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class testFeatureWeightedGridStatistics_multi_stat_var(object):
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
 
    def test_submit_FWGS_multi_stat_var(self):
        testPyGDP = pyGDP.pyGDPwebProcessing()

        shapefile  = 'sample:CONUS_States'
        attribute  = 'STATE'
        value 	   = 'Wisconsin'
        datasetURI = 'dods://cida.usgs.gov/thredds/dodsC/prism'
        dataType   = ['ppt','tmx']
        gmlIDs=None
        verbose=False
        coverage='true'
        delim='COMMA'
        stats      = ['MEAN','STD_DEV']
        timeStart  = '1900-01-01T00:00:00.000Z'
        timeEnd    = '1900-03-01T00:00:00.000Z'

        outputFile_handle = testPyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value, gmlIDs, verbose, coverage, delim, stats)

        assert_equal(os.path.getsize(outputFile_handle), 375)