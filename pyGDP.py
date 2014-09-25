# dependencies: lxml.etree, owslib
# =============================================================================
# Authors : Xao Yang, Jordan Walker, Jordan Read, Curtis Price, David Blodgett
#
# Contact email: jread@usgs.gov
# =============================================================================
from pyGDP_WFS_Utilities import shapefile_value_handle, shapefile_id_handle, _get_geotype
from pyGDP_WebData_Utilities import webdata_handle, _webdata_xml_generate
from pyGDP_Submit_Feature import fwgs, _execute_request, feature_coverage
from pyGDP_File_Utilities import upload_shapefile, shape_to_zip
from GDP_XML_Generator import gdpXMLGenerator
from owslib.wps import WebProcessingService, monitorExecution
from StringIO import StringIO
from urllib import urlencode
from time import sleep
import cgi
import sys

__version__ = '1.3.0-dev'

#This series of import functions brings in the namespaces, url, and pyGDP utility
#variables from the pyGDP_Namespaces file, as well as owslib's own namespaces
#Check out the pyGDP_Namespaces file to see precisely how things are
#what URLs pyGDP is pointing to. It's good to be aware.
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE
from pyGDP_Namespaces.pyGDP_Namespaces import WFS_URL, upload_URL, WPS_URL, WPS_Service, CSWURL
from pyGDP_Namespaces.pyGDP_Namespaces import WPS_DEFAULT_VERSION, WPS_DEFAULT_SCHEMA_LOCATION, GML_SCHEMA_LOCATION
from pyGDP_Namespaces.pyGDP_Namespaces import WPS_DEFAULT_NAMESPACE, CSW_NAMESPACE, WPS_DEFAULT_NAMESPACE, WFS_NAMESPACE, OGC_NAMESPACE, GML_NAMESPACE
from pyGDP_Namespaces.pyGDP_Namespaces import DRAW_NAMESPACE, SMPL_NAMESPACE, UPLD_NAMESPACE
from pyGDP_Namespaces.pyGDP_Namespaces import URL_timeout, WPS_attempts
from pyGDP_Namespaces.pyGDP_Namespaces import namespaces

class pyGDPwebProcessing():
    """
    This class allows interactive calls to be made into the GDP.
    """

    def __init__(self, wfsUrl=WFS_URL, wpsUrl=WPS_URL, version='1.1.0'):
        self.wfsUrl = wfsUrl
        self.wpsUrl = wpsUrl
        self.version = version
        self.wps = WebProcessingService(wpsUrl)
        
    def WPSgetCapbilities(self, xml=None):
        """
        Returns a list of capabilities.
        """
        self.wps.getcapabilities(xml)
        
    def WPSdescribeprocess(self, identifier, xml=None):
        """
        Returns a list describing a specific identifier/process.
        """
        self.wps.describeprocess(identifier, xml)
    
    #pyGDP Submit Feature	
    def dodsReplace(self, dataSetURI, verbose=False):
		return _execute_request.dodsReplace(dataSetURI, verbose)
    
    def submitFeatureCoverageOPenDAP(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None, gmlIDs=None, 
                                     verbose=False, coverage='true'):      
        return feature_coverage.submitFeatureCoverageOPenDAP(geoType, dataSetURI, varID, startTime, endTime, attribute, value, gmlIDs, verbose, coverage)    
    
    def submitFeatureCoverageWCSIntersection(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                             coverage='true'):
        return feature_coverage.submitFeatureCoverageWCSIntersection(geoType, dataSetURI, varID, attribute, value, gmlIDs, verbose, coverage)
    
    def submitFeatureCategoricalGridCoverage(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                             coverage='true', delim='COMMA'):
        return feature_coverage.submitFeatureCategoricalGridCoverage(geoType, dataSetURI, varID, attribute, value, gmlIDs, verbose, coverage, delim)

    def submitFeatureWeightedGridStatistics(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None,
                                            gmlIDs=None, verbose=None, coverage=True, delim='COMMA', stat='MEAN', grpby='STATISTIC', 
                                            timeStep=False, summAttr=False, weighted=True):
        return fwgs.submitFeatureWeightedGridStatistics(geoType, dataSetURI, varID, startTime, endTime, attribute, value, gmlIDs,
                                                        verbose, coverage, delim, stat, grpby, timeStep, summAttr, weighted)

    #pyGDP File Utilities
    def shapeToZip(self, inShape, outZip=None, allFiles=True):
        return shape_to_zip.shapeToZip(inShape, outZip=None, allFiles=True)

    def uploadShapeFile(self, filePath):
        value, ntuple = upload_shapefile.uploadShapefile(filePath)
        return value, ntuple

    #pyGDP WFS Utilities
    def getTuples(self, shapefile, attribute):
        return shapefile_id_handle.getTuples(shapefile, attribute)
     
    def getShapefiles(self):
        return shapefile_value_handle.getShapefiles()
    
    def getAttributes(self, shapefile):
        return shapefile_value_handle.getAttributes(shapefile)
    
    def getValues(self, shapefile, attribute, getTuples='false', limitFeatures=None):
        return shapefile_value_handle.getValues(shapefile, attribute, getTuples, limitFeatures)
    
    def getGMLIDs(self, shapefile, attribute, value):
        return shapefile_id_handle.getGMLIDs(shapefile, attribute, value)
    
    def _getFilterID(self, tuples, value):
        return shapefile_id_handle._getFilterID(tuples, value)
    
    def _getFeatureCollectionGeoType(self, geoType, attribute='the_geom', value=None, gmlIDs=None):
        return _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)

    def _generateRequest(self, dataSetURI, algorithm, method, varID=None, verbose=False):
        return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method, varID, verbose)

    #pyGDP WebData Utilities
    def getDataLongName(self, dataSetURI, verbose=False):
        return webdata_handle.getDataLongName(dataSetURI, verbose)
    
    def getDataType(self, dataSetURI, verbose=False):
        return webdata_handle.getDataType(dataSetURI, verbose)

    def getDataUnits(self, dataSetURI, verbose=False):
        return webdata_handle.getDataUnits(dataSetURI, verbose)
    
    def getDataSetURI(self, anyText='',CSWURL=CSWURL,BBox=None):
        return  webdata_handle.getDataSetURI(anyText, CSWURL, BBox)

    def getTimeRange(self, dataSetURI, varID, verbose=False):
        return webdata_handle.getTimeRange(ddataSetURI, varID, verbose)




