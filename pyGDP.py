# dependencies: lxml.etree, owslib
# =============================================================================
# Authors : Xao Yang, Jordan Walker, Jordan Read, Curtis Price, David Blodgett
#
# Contact email: jread@usgs.gov
# =============================================================================
from pygdp import shapefile_value_handle, shapefile_id_handle, _get_geotype
from pygdp import webdata_handle, _webdata_xml_generate
from pygdp import fwgs, _execute_request, feature_coverage, bioclim
from pygdp import upload_shapefile, shape_to_zip
from GDP_XML_Generator import gdpXMLGenerator
from owslib.wps import WebProcessingService, monitorExecution
from StringIO import StringIO
from urllib import urlencode
from time import sleep
import cgi
import sys
import logging

__version__ = '1.3.1-dev'

#This series of import functions brings in the namespaces, url, and pyGDP utility
#variables from the pyGDP_Namespaces file, as well as owslib's own namespaces
#Check out the pyGDP_Namespaces file to see precisely how things are
#what URLs pyGDP is pointing to. It's good to be aware.
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE
from pygdp.namespaces import upload_URL, WPS_URL, WPS_Service, CSWURL
from pygdp.namespaces import WPS_DEFAULT_VERSION, WPS_DEFAULT_SCHEMA_LOCATION, GML_SCHEMA_LOCATION
from pygdp.namespaces import WPS_DEFAULT_NAMESPACE, CSW_NAMESPACE, WPS_DEFAULT_NAMESPACE, WFS_NAMESPACE, OGC_NAMESPACE, GML_NAMESPACE
from pygdp.namespaces import DRAW_NAMESPACE, SMPL_NAMESPACE, UPLD_NAMESPACE
from pygdp.namespaces import URL_timeout, WPS_attempts
from pygdp.namespaces import namespaces

#Get OWSLib Logger
logger = logging.getLogger('owslib')
logger.setLevel(logging.DEBUG)
# create file handler which logs debug messages to a file.
fh = logging.FileHandler('owslib.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class pyGDPwebProcessing():
    """
    This class allows interactive calls to be made into the GDP.
    """
    
    def __init__(self, WFS_URL=None):
        if WFS_URL==None:
            from pygdp.namespaces import WFS_URL
        wfsUrl=WFS_URL
        self.wfsUrl = wfsUrl
        self.wpsUrl = WPS_URL
        self.version = '1.1.0'
        self.wps = WebProcessingService(WPS_URL)
        
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
        if verbose:
            ch.setLevel(logging.INFO)
        return _execute_request.dodsReplace(dataSetURI, verbose)
    
    def submitFeatureCoverageOPenDAP(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None, gmlIDs=None, 
                                     verbose=False, coverage='true', outputfname=None, sleepSecs=10):
        if verbose:
            ch.setLevel(logging.INFO)
        return feature_coverage.submitFeatureCoverageOPenDAP(geoType, dataSetURI, varID, startTime, endTime, attribute, value, gmlIDs, verbose, coverage, self.wfsUrl, outputfname, sleepSecs)    
    
    def submitFeatureCoverageWCSIntersection(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                             coverage='true', outputfname=None, sleepSecs=10):
        if verbose:
            ch.setLevel(logging.INFO)
        return feature_coverage.submitFeatureCoverageWCSIntersection(geoType, dataSetURI, varID, attribute, value, gmlIDs, verbose, coverage, self.wfsUrl, outputfname, sleepSecs)
    
    def submitFeatureCategoricalGridCoverage(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                             coverage='true', delim='COMMA', outputfname=None, sleepSecs=10):
        if verbose:
            ch.setLevel(logging.INFO)
        return feature_coverage.submitFeatureCategoricalGridCoverage(geoType, dataSetURI, varID, attribute, value, gmlIDs, verbose, coverage, delim, self.wfsUrl, outputfname, sleepSecs)

    def submitFeatureWeightedGridStatistics(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None,
                                            gmlIDs=None, verbose=None, coverage=True, delim='COMMA', stat='MEAN', grpby='STATISTIC', 
                                            timeStep=False, summAttr=False, weighted=True, outputfname=None, sleepSecs=10):
        if verbose:
            ch.setLevel(logging.INFO)
        return fwgs.submitFeatureWeightedGridStatistics(geoType, dataSetURI, varID, startTime, endTime, attribute, value, gmlIDs,
                                                        verbose, coverage, delim, stat, grpby, timeStep, summAttr, weighted, self.wfsUrl, outputfname, sleepSecs)

    def submitCustomBioclim(processid="org.n52.wps.server.r.gridded_bioclim", outputfname=None, verbose=False, **kwargs):
        if verbose:
            ch.setLevel(logging.INFO)
        return bioclim.submitCustomBioclim(processid="org.n52.wps.server.r.gridded_bioclim", outputfname=outputfname, verbose=verbose, **kwargs)

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
        return shapefile_value_handle.getShapefiles(self.wfsUrl)
    
    def getAttributes(self, shapefile):
        return shapefile_value_handle.getAttributes(shapefile, self.wfsUrl)
    
    def getValues(self, shapefile, attribute, getTuples='false', limitFeatures=None):
        return shapefile_value_handle.getValues(shapefile, attribute, getTuples, limitFeatures, self.wfsUrl)
    
    def getGMLIDs(self, shapefile, attribute, value):
        return shapefile_id_handle.getGMLIDs(shapefile, attribute, value, WFS_URL=self.wfsUrl)
    
    def _getFilterID(self, tuples, value):
        return shapefile_id_handle._getFilterID(tuples, value)
    
    def _getFeatureCollectionGeoType(self, geoType, attribute='the_geom', value=None, gmlIDs=None):
        return _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, self.wfsUrl)

    def _generateRequest(self, dataSetURI, algorithm, method, varID=None, verbose=False):
        return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method, varID, verbose)

    #pyGDP WebData Utilities
    def getDataLongName(self, dataSetURI, verbose=False):
        if verbose:
            ch.setLevel(logging.INFO)
        return webdata_handle.getDataLongName(dataSetURI, verbose)
    
    def getDataType(self, dataSetURI, verbose=False):
        if verbose:
            ch.setLevel(logging.INFO)
        return webdata_handle.getDataType(dataSetURI, verbose)

    def getDataUnits(self, dataSetURI, verbose=False):
        if verbose:
            ch.setLevel(logging.INFO)
        return webdata_handle.getDataUnits(dataSetURI, verbose)
    
    def getDataSetURI(self, anyText='',CSWURL=CSWURL,BBox=None):
        return  webdata_handle.getDataSetURI(anyText, CSWURL, BBox)

    def getTimeRange(self, dataSetURI, varID, verbose=False):
        if verbose:
            ch.setLevel(logging.INFO)
        return webdata_handle.getTimeRange(dataSetURI, varID, verbose)




