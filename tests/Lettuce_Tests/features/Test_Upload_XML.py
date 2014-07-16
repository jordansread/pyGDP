from pyGDP import gdpXMLGenerator
from owslib.etree import etree
from nose.tools import assert_equal
from lettuce import *
import os, sys

@step(r'I have my GDP upload URLs')
def got_those_urls(step):
    world.upload_URL = 'http://cida.usgs.gov/gdp/geoserver'
    world.filename = 'CIDA_TEST_'

@step(r'I have my own, pre-encoded, upload shapefile data')
def read_in_the_data(step):
    test_file = os.path.join(os.getcwd(), 'testEncodeData.txt')
    encode_data = open(test_file, 'r')
    world.file_data = encode_data.read()
    encode_data.close()
    
@step(r'I use the xmlGen objects getUploadXMLtree method')
def upload_xml_tree(step):
    xml_gen = gdpXMLGenerator()
    world.test_xml = xml_gen.getUploadXMLtree(world.filename, world.upload_URL, world.file_data)

@step(r'I see it makes the xml that will successfully upload that data')
def will_upload_that_data(step):
    assert_equal(len(etree.tostring(world.test_xml)), 6217)
