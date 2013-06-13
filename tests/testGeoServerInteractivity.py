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
        
    def test_get_shapefile_attributes_arc(self):
        pyGDP.WFS_URL = 'http://www.sciencebase.gov/arcgis/services/GeospatialFabric/mows_mapping/MapServer/WFSServer'
        
        testPyGDP = pyGDP.pyGDPwebProcessing()

        shapefile  = 'GeospatialFabric_mows_mapping:NHDPlus_Catchment'

        attributes = testPyGDP.getAttributes(shapefile)

        assert_equal(len(attributes), 7)

        assert('hru_id' in attributes)
        
    def test_get_shapefile_values(self):
        pyGDP.WFS_URL = 'http://cida.usgs.gov/gdp/geoserver/wfs'
        
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
        shapefile  = 'sample:CONUS_States'  
	
        attribute = 'STATE'
	
        values    = testPyGDP.getValues(shapefile,attribute)
	
        assert_equal(len(values), 49)
        
        assert('Wisconsin' in values)
	
    def test_getFeatureCollectionGeoType_single(self):
        testpyGDP = pyGDP.pyGDPwebProcessing()
        
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
        shapefile  = 'sample:CONUS_States'  
        
        attribute = 'STATE'
        
        value = 'Wisconsin'
        
        testFeatureCollection = testPyGDP._getFeatureCollectionGeoType(shapefile,attribute,value)
        
        assert_equal(len(testFeatureCollection.query.filters), 36)
        
    def test_getFeatureCollectionGeoType_all(self):
        testpyGDP = pyGDP.pyGDPwebProcessing()
        
        testPyGDP = pyGDP.pyGDPwebProcessing()
        
        shapefile  = 'sample:CONUS_States'  
        
        attribute = 'STATE'
        
        value = None
        
        testFeatureCollection = testPyGDP._getFeatureCollectionGeoType(shapefile,attribute,value)
        
        assert_equal(testFeatureCollection.query.filters, [])