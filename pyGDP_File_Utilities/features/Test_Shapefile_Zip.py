from lettuce import *
from nose.tools import assert_equal
import os
import pyGDP

@step(r'I have a test shapefile and all its associated components')
def point_to_file(step):
    world.shapefile_name = 'CIDA_TEST_.shp'
    world.shapefile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), \
                                         world.shapefile_name)
    
@step(r'I run the shapeToZip function')
def shape_to_zip(step):
    test_pyGDP = create_web_processing_object()
    
    world.zip_name = test_pyGDP.shapeToZip(world.shapefile_path)
        
def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I am returned a pyGDP viable output')
def test_output(step):
    assert_equal(os.path.getsize((world.zip_name)), 4116)
    clean_up()
    
def clean_up():
    os.remove(world.zip_name)
