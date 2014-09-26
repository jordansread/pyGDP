import pyGDP
from lettuce import *
from nose.tools import assert_equal
import os

@step(r'I have defined my CONUS shapefile to be Wisconsin')
def wisco_conus(step):
    world.shapefile  = 'sample:CONUS_states'
    world.attribute  = 'STATE'
    world.value      = 'Wisconsin'

@step(r'I will be using "ppt" in my favorite "prism" dataset')
def prism_data(step):
    world.dataset_uri = 'dods://cida.usgs.gov/thredds/dodsC/prism'
    world.data_type = "ppt"

@step(r'I have even defined my own start and stop times')
def time_stamps(step):
    world.time_start  = '1900-01-01T00:00:00.000Z'
    world.time_end    = '1900-03-01T00:00:00.000Z'

@step(r'I submit my FWGS')
def feature_weighted_grid_statistics(step):
    test_pyGDP = create_web_processing_object()
    world.output_file = test_pyGDP.submitFeatureWeightedGridStatistics(world.shapefile, \
                        world.dataset_uri, world.data_type, world.time_start, world.time_end, \
                        world.attribute, world.value, verbose=False)

def create_web_processing_object(WFS_URL=None):
    if WFS_URL!=None:
        new_web_processing = pyGDP.pyGDPwebProcessing(WFS_URL=WFS_URL)
    else:
        new_web_processing = pyGDP.pyGDPwebProcessing()
    return new_web_processing

@step(r'I should get the basic output that I expect')
def basic_tests_for_basic_outputs(step):
    assert_equal(os.path.getsize(world.output_file), 133)

@step(r'I will be using "ppt" and "tmx" in my favorite "prism" datatset')
def multi_prism_data(step):
    world.dataset_uri = 'dods://cida.usgs.gov/thredds/dodsC/prism'
    world.data_type = ['ppt','tmx']

@step(r'I will be searching for the "MEAN" and "STD_DEV" statistics')
def define_stats(step):
    world.stats = ['MEAN', 'STD_DEV']

@step(r'I submit my multi-stat FWGS')
def multi_feature_weighted_grid_statistics(step):
    gmlIDs   =  None
    verbose  =  False
    coverage =  'true'
    delim    =  'COMMA'

    test_pyGDP = create_web_processing_object()
    world.output_file = test_pyGDP.submitFeatureWeightedGridStatistics(world.shapefile, world.dataset_uri, world.data_type, world.time_start, \
                                   world.time_end, world.attribute, world.value, gmlIDs, verbose, coverage, \
                                   delim, world.stats)
    
@step(r'I should get the multi-stat output that I expect')
def tests_for_multi_outputs(step):
    assert_equal(os.path.getsize(world.output_file), 375)

@step(r'I fill out every variable and submit my FWGS call')
def full_feature_weighted_grid_statistics(step):
    
    test_pyGDP = create_web_processing_object()
    outputFile_handle = test_pyGDP.submitFeatureWeightedGridStatistics(geoType=world.shapefile, dataSetURI=world.dataset_uri, \
                    varID=world.data_type, startTime=world.time_start, endTime=world.time_end, attribute=world.attribute, \
                    value=world.value, gmlIDs=None, verbose=False, coverage='true', delim='COMMA', \
                    stat=world.stats, grpby='STATISTIC', timeStep='false', summAttr='false')

@step(r'I will be using a HUC 8 shapefile')
def huc_shapefile(step):
        world.shapefile  = 'sample:simplified_HUC8s'
        world.attribute  = 'HUC_8'
        world.value      = '08010211'

@step(r'I will be searching in a Landcover Dataset')
def set_landcover_from_nationalmap(step):
        world.dataset_uri = 'http://raster.nationalmap.gov/ArcGIS/services/TNM_LandCover/MapServer/WCSServer' # Note that this test also tests the http to dods conversion for urls.
        world.data_type   = '6'

@step(r'I submit my FWGS without a time variable')
def timeless_FWGS(step):
    time_start = None
    time_end = None
    test_pyGDP = create_web_processing_object()
    world.output_file = test_pyGDP.submitFeatureWeightedGridStatistics(geoType=world.shapefile, dataSetURI=world.dataset_uri, \
                        varID=world.data_type, startTime=time_start, endTime=time_end, attribute=world.attribute, \
                        value=world.value, gmlIDs=None, verbose=False, coverage='true', delim='COMMA', stat=world.stats, \
                        grpby='STATISTIC', timeStep='false', summAttr='false')
@step(r'I should get a timeless output that I expect')
def timeless_output_test(step):
    assert_equal(os.path.getsize(world.output_file), 58)

@step(r'I have already uploaded the shapefile I want to sceincebase')
def sciencebase_shapefile(step):
    world.WFS_URL = 'http://www.sciencebase.gov/arcgis/services/GeospatialFabric/mows_mapping/MapServer/WFSServer'
    world.shapefile  = 'GeospatialFabric_mows_mapping:NHDPlus_Catchment'
    world.attribute  = 'hru_id'
    world.value      = '99'

@step(r'I submit my timestamped FWGS')
def arc_FWGS(step):
   test_pyGDP = create_web_processing_object(WFS_URL=world.WFS_URL)
   world.output_file = test_pyGDP.submitFeatureWeightedGridStatistics(world.shapefile, world.dataset_uri, world.data_type, world.time_start, \
                                                                      world.time_end, world.attribute, world.value, coverage=False, verbose=False)

@step(r'I should get a custom output that I expect')
def test_arc_FWGS(step):
    assert_equal(os.path.getsize(world.output_file), 95)
