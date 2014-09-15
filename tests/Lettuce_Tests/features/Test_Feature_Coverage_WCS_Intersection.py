from lettuce import *
import pyGDP
import os
from nose.tools import assert_equal

@step(r'I know my HUC_8 value') 
def define_HUC_shapefile(step):
    
    #pyGDP.WPS_URL = 'http://cida.usgs.gov/gdp/process/WebProcessingService'
    world.shapefile = 'sample:simplified_HUC8s'
    world.attribute = 'HUC_8'
    world.value = '08010211'

@step(r'I know what dataset I want to use')
def define_dataset_uri(step):
    world.dataSetURI = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer'
    world.dataType = '6'

@step(r'I run that crazy WCS insersection function')
def test_submit_WCS_Intersection(step):
    test_pyGDP = create_web_processing_object()
    world.output_file = test_pyGDP.submitFeatureCoverageWCSIntersection(world.shapefile, world.dataSetURI, world.dataType, world.attribute, world.value)

def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I see exactly the file that I expected')
def run_WCS_file_check(step):
    assert_equal(os.path.getsize(world.output_file), 1311757)
    
    
