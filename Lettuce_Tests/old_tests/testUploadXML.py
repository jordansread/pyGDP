import os
from pyGDP import gdpXMLGenerator
from owslib.etree import etree
from nose.tools import assert_equal

class TestUploadXMLGeneration(object):

    def test_gdpXMLGenerator(self):
        #Define test environment variables (they are forom production GDP; no actual web calls will be made)
        upload_URL = 'http://cida.usgs.gov/gdp/geoserver'
        filename = 'CIDA_TEST_'

        #Read in encoded shapefile data from associated test encode file.
        #This is how it's done in full pyGDP so we'll do the same thing here
        testfile = os.path.join(os.getcwd(), 'testEncodeData.txt')
        encodeData = open(testfile, 'r')
        filedata =encodeData.read()
        encodeData.close()

        #Instantiate an XMLGenerator object and create the xml.etree_Element upload object
        xmlGen = gdpXMLGenerator()
        testXML = xmlGen.getUploadXMLtree(filename, upload_URL, filedata)

        #Assert that the new XML is equal to same XML under working pyGDP conditions
        assert_equal(len(etree.tostring(testXML)), 6217)
