import pyGDP
from lettuce import *
from nose.tools import assert_equal
from nose.tools import assert_not_equal
import os

@step(r'I know there are shapefiles on our GeoServer')
def point_to_geoserver(step):
    pyGDP.WFS_URL = 'http://cida.usgs.gov/gdp/geoserver/wfs'

@step(r'I use the getShapefiles method and I get a list of those files')
def get_shapefiles(step):
    test_pyGDP = create_web_processing_object()
    world.shapefiles = test_pyGDP.getShapefiles()
    
def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I get a non-zero response')
def assert_num_shapefiles(step):
    assert_not_equal(len(world.shapefiles), 0)

@step(r'I already know a shapefile')
def define_the_conus(step):
    world.shapefile = 'sample:CONUS_states'

@step(r'I use the getAttributes method and I get a list of those attributes')
def get_the_attributes(step):
      test_pyGDP = create_web_processing_object()
      world.attributes = test_pyGDP.getAttributes(world.shapefile)

@step(r'I should see an expected number of attributes')
def check_the_attributes(step):
      assert_equal(len(world.attributes), 10)
      assert('STATE' in world.attributes)

@step(r'I know that one of those attributes is "STATE"')
def that_attribute_is_state(step):
    world.attribute = 'STATE'

@step(r'I ask for a list of values in the STATE')
def get_the_values(step):
    test_pyGDP = create_web_processing_object()
    world.values = test_pyGDP.getValues(world.shapefile, world.attribute)

@step(r'I should see the number of states')
def wisconsin_is_a_state(step):
    assert_equal(len(world.values), 49)
    assert('Wisconsin' in world.values)

@step(r'I know that one of those states is "Wisconsin"')
def on_wisconsin(step):
    world.value ='Wisconsin'
      
@step(r'I ask for the Feature Collection GeoType of Wisconsin in CONUS')
def ask_and_you_shall_recieve(step):
    test_pyGDP = create_web_processing_object()
    world.feature_collection = test_pyGDP._getFeatureCollectionGeoType(world.shapefile, world.attribute, world.value, 'http://cida.usgs.gov/gdp/geoserver/wfs')

@step(r'Then I am given a single expected output from the Feature Collection')
def feature_collection(step):
    assert_not_equal(len(world.feature_collection.query.filters), 0)

@step(r'I ask for the Feature Collection GeoType of all the states in CONUS')
def every_of_the_conus(step):
    test_pyGDP = create_web_processing_object()
    value = None
    world.feature_collection = test_pyGDP._getFeatureCollectionGeoType(world.shapefile, world.attribute, value, 'http://cida.usgs.gov/gdp/geoserver/wfs')

@step(r'I am given multiple expected outputs from Feature Collection')
def all_feature_collection(step):
    assert_not_equal(len(world.feature_collection.query.filters), 0)
    
