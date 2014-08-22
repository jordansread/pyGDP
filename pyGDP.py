# dependencies: lxml.etree, owslib
# =============================================================================
# Authors : Xao Yang, Jordan Walker, Jordan Read, Curtis Price, David Blodgett
#
# Contact email: jread@usgs.gov
# =============================================================================
from owslib.wps import WebProcessingService, WFSFeatureCollection, WFSQuery, GMLMultiPolygonFeatureCollection, monitorExecution
from owslib.wfs import WebFeatureService
from owslib.csw import CatalogueServiceWeb
from owslib.etree import etree
from StringIO import StringIO
from urllib import urlencode
from urllib2 import urlopen
from time import sleep
from GDP_XML_Generator import gdpXMLGenerator
from pyGDP_File_Utilities import upload_shapefile, shape_to_zip
from pyGDP_WebData_Utilities import webdata_handle, _webdata_xml_generate
from pyGDP_WFS_Utilities import shapefile_value_handle, shapefile_id_handle, _get_geotype
import owslib.util as util
import base64
import cgi
import sys
import os
import zipfile

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

__version__ = '1.2.2'

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

    def shapeToZip(self, inShape, outZip=None, allFiles=True):
        outZip = shape_to_zip.shapeToZip(inShape, outZip=None, allFiles=True)
        return outZip

    def uploadShapeFile(self, filePath):
        value, ntuple = upload_shapefile.uploadShapefile(filePath)
        return value, ntuple

    def getTuples(self, shapefile, attribute):
        return shapefile_id_handle.getTuples(shapefile, attribute)
    
    def _getFilterID(self, tuples, value):
        return shapefile_id_handle._getFilterID(tuples, value)
    
    def _generateRequest(self, dataSetURI, algorithm, method, varID=None, verbose=False):
        return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method, varID, verbose)
    
    def _generateFeatureRequest(self, typename, attribute=None):
        """
        This function, given a attribute and a typename or filename will return a list of values associated
        with the file and the attribute chosen.
        """
        
        service_url = WFS_URL
        qs = []
        if service_url.find('?') != -1:
                qs = cgi.parse_qsl(service_url.split('?')[1])
    
        params = [x[0] for x in qs]
    
        if 'service' not in params:
            qs.append(('service', 'WFS'))
        if 'request' not in params:
            if attribute is None:
                qs.append(('request', 'DescribeFeatureType'))
            else:
                qs.append(('request', 'GetFeature'))
        if 'version' not in params:
            qs.append(('version', '1.1.0'))
        if 'typename' not in params:
            qs.append(('typename', typename))
        if attribute is not None:
            if 'propertyname' not in params:
                qs.append(('propertyname', attribute))
            
        urlqs = urlencode(tuple(qs))
        return service_url.split('?')[0] + '?' + urlqs

    def getShapefiles(self):
        return shapefile_value_handle.getShapefiles()
    
    def getAttributes(self, shapefile):
        return shapefile_value_handle.getAttributes(shapefile)
    
    def getValues(self, shapefile, attribute, getTuples='false', limitFeatures=None):
        return shapefile_value_handle.getValues(shapefile, attribute, getTuples, limitFeatures)
    
    def getDataType(self, dataSetURI, verbose=False):
        return webdata_handle.getDataType(dataSetURI, verbose)
    
    def getDataLongName(self, dataSetURI, verbose=False):
        return webdata_handle.getDataLongName(dataSetURI, verbose)

    def getDataUnits(self, dataSetURI, verbose=False):
        return webdata_handle.getDataUnits(dataSetURI, verbose)
	
    def dodsReplace(self, dataSetURI, verbose=False):
		if "/dodsC" in dataSetURI:
			dataSetURI= dataSetURI.replace("http", "dods")
		return dataSetURI
        
    def getDataSetURI(self, anyText='',CSWURL=CSWURL,BBox=None):
        return  webdata_handle.getDataSetURI(anyText, CSWURL, BBox)
    
    def getGMLIDs(self, shapefile, attribute, value):
        return shapefile_id_handle.getGMLIDs(shapefile, attribute, value)
    
    def getTimeRange(self, dataSetURI, varID, verbose=False):
        """
        Set up a get dataset time range request given a datatype and dataset uri. Returns the range
        of the earliest and latest time.
        If verbose = True, will print on screen the waiting seq. for response document.
        """
        
        algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.GetGridTimeRange'
        return self._generateRequest(dataSetURI, algorithm, method='getDataSetTime', varID=varID, verbose=verbose)
    
    
    def _getFeatureCollectionGeoType(self, geoType, attribute='the_geom', value=None, gmlIDs=None):
        return _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)
    
    def _executeRequest(self, processid, inputs, output, verbose):
        """
        This function makes a call to the Web Processing Service with
        the specified user inputs.
        """
        wps = WebProcessingService(WPS_URL)

        old_stdout = sys.stdout
        # create StringIO() for listening to print
        result = StringIO()
        if not verbose: # redirect standard output
            sys.stdout = result
        
        execution = wps.execute(processid, inputs, output)
        
        sleepSecs=10
        err_count=1
        
        while execution.isComplete()==False:
            try:
                monitorExecution(execution, sleepSecs, download=False) # monitors for success
                err_count=1
            except Exception:
                print 'An error occurred while checking status, checking again.'
                print 'Sleeping %d seconds...' % sleepSecs
                err_count+=1
                if err_count > WPS_attempts:
                    raise Exception('The status document failed to return, status checking has aborted. There has been a network or server issue preventing the status document from being retrieved, the request may still be running. For more information, check the status url %s' % execution.statusLocation)
                sleep(sleepSecs)
    
        # redirect standard output after successful execution
        sys.stdout = result
        done=False
        err_count=1
        while done==False:
            try: 
                monitorExecution(execution, download=True)
                done=True
            except Exception:
                print 'An error occurred while trying to download the result file, trying again.'
                err_count+=1
            if err_count > WPS_attempts:        
                raise Exception("The process completed successfully, but an error occurred while downloading the result. You may be able to download the file using the link at the bottom of the status document: %s" % execution.statusLocation)
            sleep(sleepSecs)
            
        result_string = result.getvalue()
        output = result_string.split('\n')
        tmp = output[len(output) - 2].split(' ')  
        sys.stdout = old_stdout
        return tmp[len(tmp)-1]

    
    def submitFeatureWeightedGridStatistics(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None,
                                            gmlIDs=None, verbose=None, coverage=True, delim='COMMA', stat='MEAN', grpby='STATISTIC', 
                                            timeStep=False, summAttr=False, weighted=True):
        """
        Makes a featureWeightedGridStatistics algorithm call. 
        The web service interface implemented is summarized here: 
        https://my.usgs.gov/confluence/display/GeoDataPortal/Generating+Area+Weighted+Statistics+Of+A+Gridded+Dataset+For+A+Set+Of+Vector+Polygon+Features
        
        Note that varID and stat can be a list of strings.
        
        """
        # test for dods:
        dataSetURI = self.dodsReplace(dataSetURI)
        
        if verbose == True:
            print 'Generating feature collection.'
        
        featureCollection = self._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)
        if featureCollection is None:
            return
        
        processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureWeightedGridStatisticsAlgorithm'
        if weighted==False:
            processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureGridStatisticsAlgorithm'
        
        solo_inputs = [("FEATURE_ATTRIBUTE_NAME",attribute), 
                  ("DATASET_URI", dataSetURI),  
                  ("TIME_START",startTime),
                  ("TIME_END",endTime), 
                  ("REQUIRE_FULL_COVERAGE",str(coverage).lower()), 
                  ("DELIMITER",delim), 
                  ("GROUP_BY", grpby),
                  ("SUMMARIZE_TIMESTEP", str(timeStep).lower()), 
                  ("SUMMARIZE_FEATURE_ATTRIBUTE",str(summAttr).lower()), 
                  ("FEATURE_COLLECTION", featureCollection)]
                  
        if isinstance(stat, list):
            num_stats=len(stat)
            if num_stats > 7:
                raise Exception('Too many statistics were submitted.')
        else:
            num_stats=1
                  
        if isinstance(varID, list):
            num_varIDs=len(varID)
        else:
            num_varIDs=1
        
        inputs = [('','')]*(len(solo_inputs)+num_varIDs+num_stats)
        
        count=0
        rmvCnt=0
        
        for solo_input in solo_inputs:
			if solo_input[1]!=None:
				inputs[count] = solo_input
				count+=1
			else: 
				rmvCnt+=1
		
        del inputs[count:count+rmvCnt]
			
        if num_stats > 1:
            for stat_in in stat:
                if stat_in not in ["MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"]:
                    raise Exception('The statistic %s is not in the allowed list: "MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"' % stat_in)
                inputs[count] = ("STATISTICS",stat_in)
                count+=1
        elif num_stats == 1:
            if stat not in ["MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"]:
                raise Exception('The statistic %s is not in the allowed list: "MEAN", "MINIMUM", "MAXIMUM", "VARIANCE", "STD_DEV", "SUM", "COUNT"' % stat)
            inputs[count] = ("STATISTICS",stat)
            count+=1
                 
        if num_varIDs > 1:
            for var in varID:
                inputs[count] = ("DATASET_ID",var)
                count+=1
        elif num_varIDs == 1:
            inputs[count] = ("DATASET_ID",varID)
        
        output = "OUTPUT"
        
        return self._executeRequest(processid, inputs, output, verbose)
    
    def submitFeatureCoverageOPenDAP(self, geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None, gmlIDs=None, 
                                     verbose=False, coverage='true'):
        """
        Makes a featureCoverageOPenDAP algorithm call. 
        """
        
        featureCollection = self._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)
        if featureCollection is None:
            return
        processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageOPeNDAPIntersectionAlgorithm'
        inputs = [ ("DATASET_URI", dataSetURI),
                   ("DATASET_ID", varID), 
                   ("TIME_START",startTime), 
                   ("TIME_END",endTime),
                   ("REQUIRE_FULL_COVERAGE",coverage),
                   ("FEATURE_COLLECTION", featureCollection)]
        output = "OUTPUT"
        return self._executeRequest(processid, inputs, output, verbose)    

    def submitFeatureCoverageWCSIntersection(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False, coverage='true'):
        """
        Makes a featureCoverageWCSIntersection algorithm call. 
        """
        
        featureCollection = self._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)
        if featureCollection is None:
            return
        processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageIntersectionAlgorithm'
        inputs = [("DATASET_URI", dataSetURI),
                  ("DATASET_ID", varID),
                  ("REQUIRE_FULL_COVERAGE",coverage), 
                  ("FEATURE_COLLECTION", featureCollection)]
        output = "OUTPUT"
        return self._executeRequest(processid, inputs, output, verbose)
    
    def submitFeatureCategoricalGridCoverage(self, geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                             coverage='true', delim='COMMA'):
        """
        Makes a featureCategoricalGridCoverage algorithm call. 
        """
        
        featureCollection = self._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs)
        if featureCollection is None:
            return
        processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCategoricalGridCoverageAlgorithm'
        inputs = [ ("FEATURE_ATTRIBUTE_NAME",attribute),
               ("DATASET_URI", dataSetURI),
               ("DATASET_ID", varID),         
               ("DELIMITER", delim),
               ("REQUIRE_FULL_COVERAGE",coverage),
               ("FEATURE_COLLECTION", featureCollection)]
        output = "OUTPUT"
        return self._executeRequest(processid, inputs, output, verbose)
