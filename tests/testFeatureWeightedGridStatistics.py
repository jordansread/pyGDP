import pyGDP
import os
from nose.tools import assert_equal
from nose.tools import assert_not_equal
 
class TestFeatureWeightedGridStatistics(object):
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
        pyGDP.WPS_URL='http://cida.usgs.gov/qa/climate/gdp/process/WebProcessingService'
        testPyGDP = pyGDP.pyGDPwebProcessing()

        shapefile  = 'sample:CONUS_States'
        attribute  = 'STATE'
        value 	   = 'Wisconsin'
        userPoly   = [(-102.8184, 39.5273), (-102.8184, 37.418), (-101.2363, 37.418), (-101.2363,39.5273), (-102.8184, 39.5273)]
        datasetURI = 'dods://cida.usgs.gov/thredds/dodsC/prism'
        dataType   = 'ppt'
        timeStart  = '1900-01-01T00:00:00.000Z'
        timeEnd    = '1900-03-01T00:00:00.000Z'

        outputFile_handle = testPyGDP.submitFeatureWeightedGridStatistics(shapefile, datasetURI, dataType, timeStart, timeEnd, attribute, value)

        assert_equal(os.path.getsize(outputFile_handle), 133)

    def test_submit_FWGS_multi_stat_var(self):
        pyGDP.WPS_URL='http://cida.usgs.gov/qa/climate/gdp/process/WebProcessingService'
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

    def test_submit_FWGS_multi_stat_var_named(self):
        pyGDP.WPS_URL='http://cida.usgs.gov/qa/climate/gdp/process/WebProcessingService'
        testPyGDP = pyGDP.pyGDPwebProcessing()

        shapefile  = 'sample:CONUS_States'
        shapefileAttribute  = 'STATE'
        attributeValue 	   = 'Wisconsin'
        datasetURI = 'http://cida.usgs.gov/thredds/dodsC/prism' # Note that this test also tests the http to dods conversion for urls.
        dataType   = ['ppt','tmx']
        Coverage='true'
        Delim='COMMA'
        stats      = ['MEAN','STD_DEV']
        timeStart  = '1900-01-01T00:00:00.000Z'
        timeEnd    = '1900-03-01T00:00:00.000Z'

        outputFile_handle = testPyGDP.submitFeatureWeightedGridStatistics(geoType=shapefile, dataSetURI=datasetURI, varID=dataType, startTime=timeStart, endTime=timeEnd, attribute=shapefileAttribute, value=attributeValue, gmlIDs=None, verbose=False, coverage=Coverage, delim=Delim, stat=stats, grpby='STATISTIC', timeStep='false', summAttr='false')

        assert_equal(os.path.getsize(outputFile_handle), 375)
        
    def test_submit_FWGS_no_time(self):
        pyGDP.WPS_URL='http://cida.usgs.gov/qa/climate/gdp/process/WebProcessingService'
        testPyGDP = pyGDP.pyGDPwebProcessing()

        shapefile  = 'sample:simplified_HUC8s'
        shapefileAttribute  = 'HUC_8'
        attributeValue 	   = '08010211'
        datasetURI = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer' # Note that this test also tests the http to dods conversion for urls.
        dataType   = '6'
        Coverage='true'
        Delim='COMMA'
        stats      = ['MEAN','STD_DEV']
        timeStart  = None
        timeEnd    = None

        outputFile_handle = testPyGDP.submitFeatureWeightedGridStatistics(geoType=shapefile, dataSetURI=datasetURI, varID=dataType, startTime=timeStart, endTime=timeEnd, attribute=shapefileAttribute, value=attributeValue, gmlIDs=None, verbose=False, coverage=Coverage, delim=Delim, stat=stats, grpby='STATISTIC', timeStep='false', summAttr='false')

        assert_equal(os.path.getsize(outputFile_handle), 57)
