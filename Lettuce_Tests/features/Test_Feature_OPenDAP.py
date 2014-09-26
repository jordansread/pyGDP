import pyGDP
import os
from lettuce import *
from nose.tools import assert_equal

@step(r'I already have my boundary shapefile call from GDP')
def alabama_conus_area(step):
    world.shapefile = 'sample:CONUS_states'
    world.attribute = 'STATE'
    world.value = 'Alabama'

@step(r'I have set up my precipitaion data call from GDP')
def dataset_call(step):
    world.dataSetURI = 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml'
    world.dataType = 'Prcp'
    world.timeStart = '1950-01-01T00:00:00.000Z'
    world.timeEnd = '1950-01-02T00:00:00.000Z'

@step(r'I run submitFeatureCoverageOPenDAP in pyGDP')
def test_FCO(step):
    test_pyGDP = create_web_processing_object()
    world.output_file = test_pyGDP.submitFeatureCoverageOPenDAP(world.shapefile, world.dataSetURI, world.dataType, world.timeStart, world.timeEnd, world.attribute, world.value, verbose=False)


def create_web_processing_object():
    new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I know my output is something I expect')
def check_FCO_output(step):
    assert_equal(os.path.getsize(world.output_file), 14312)
