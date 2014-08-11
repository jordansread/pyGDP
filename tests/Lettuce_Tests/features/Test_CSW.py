from lettuce import *
from nose.tools import assert_equal, assert_true
import pyGDP
import warnings

@step(r'I define the keyword as "(.*)"')
def define_keyword(step, keyword):
    world.my_keyword = keyword

@step(r'I invoke the pyGDP.getDataSetURI method')
def invoke_getDataSetURI(step):
    test_pyGDP = create_web_processing_object()
    warnings.filterwarnings("ignore")#Ignore a user warning thrown by an \
                                     #owslib function asking to upgrade from \
                                     #"getrecords" to "getrecords2" methods
    world.data_set_uris = test_pyGDP.getDataSetURI(anyText=world.my_keyword)

@step(r'I see the metadata and URIs of "prism" datasets')
def assert_uri_equalities(step):
    assert_true(len(world.data_set_uris) > 0)
    assert_equal(world.data_set_uris[1][2][0], 'dods://cida.usgs.gov/thredds/dodsC/prism')
   
def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I am not defining any keywords')
def undefine_keyword(step):
    world.my_keyword == ''

@step(r'I see anywhere between 1 and 1000 datasets')
def true_within_range(step):
    num_records = len(world.data_set_uris)
    assert_true(num_records > 0)
    assert_true(num_records < 1000)
