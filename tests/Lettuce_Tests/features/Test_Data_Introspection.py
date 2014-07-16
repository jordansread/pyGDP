import pyGDP
from nose.tools import assert_equal
from lettuce import *

@step(r'I am pointing to a test "prism" dataset with my URI')
def set_up_namespace(step):

    pyGDP.WPS_Service= 'http://cida.usgs.gov/gdp/utility/WebProcessingService'
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
    assert_equal(len(world.xml_data_types), 3)
