import pyGDP
from nose.tools import assert_equal, assert_true, raises
from lettuce import *

@step(r'I am pointing to a test "prism" dataset with my URI')
def set_up_namespace(step):
    world.DATASET_URI = 'dods://cida.usgs.gov/thredds/dodsC/prism'

@step(r'I retrieve the metadata using the getDataType method')
def get_data_type(step):
    test_pyGDP = create_web_processing_object()
    world.xml_data_types = test_pyGDP.getDataType(world.DATASET_URI, False) #Boolean for verbosity    

def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I find that "(.*)" is in the big confusing xml that I get back')
def search_xml(step, keyword):
    assert(keyword in world.xml_data_types)

@step(r'Then I know that the GDP data looks good from both ends')
def check_other_datatype_properties(step):
    assert_true(len(world.xml_data_types) > 0)

@step(r'a bad OPeNDAP url')
def set_up_namespace(step):
    world.DATASET_URI = 'busted'
    
@step(r'Then I get the error I expect')
@raises(Exception)
def set_up_namespace(step):
    test_pyGDP = create_web_processing_object()
    world.xml_data_types = test_pyGDP.getDataType(world.DATASET_URI, False) #Boolean for verbosity
    
@step('I am interested in "ppt"')
def declare_variable(step):
    world.prism_variable='ppt'

@step('When I retrieve the metadata using the getTimeRange method')
def get_time_range(step):
    test_pyGDP = create_web_processing_object()
    world.prism_timeRange = test_pyGDP.getTimeRange(world.DATASET_URI, world.prism_variable)

@step('Then I find that the start date of prism is as expected.')
def test_time_range(step):
    assert('1895-01-01T00:00:00Z' in world.prism_timeRange)