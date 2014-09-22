import pyGDP
from lettuce import *
from nose.tools import assert_equal
import os

@step(r'I already know how to get my shapefile boundary from GDP')
def its_rhode_island(step):
    pyGDP.WPS_URL='http://cida.usgs.gov/gdp/process/WebProcessingService'
    world.shapefile = 'sample:CONUS_states'
    world.attribute = 'STATE'
    world.value = 'Rhode Island'

@step(r'I can call a working dataset from GDP')
def statsgo_dataset(step):
    world.dataSetURI = 'http://cida.usgs.gov/ArcGIS/services/statsgo_muid/MapServer/WCSServer'
    world.dataType = '1'

@step(r'When I make a Feature Categorical Grid Coverage call')
def test_FCGC(step):
    test_pyGDP = create_web_processing_object()
    world.test_output_file_handle = test_pyGDP.submitFeatureCategoricalGridCoverage(world.shapefile, world.dataSetURI, world.dataType, world.attribute, world.value, verbose=True)

def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing
    
@step(r'I can see the returned file is exactly what I would expect')
def check_test_FCGC(step):
    assert_equal(os.path.getsize(world.test_output_file_handle), 650)
