from pygdp import _execute_request
from pygdp import _get_geotype

def submitFeatureCategoricalGridCoverage(geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False,
                                         coverage='true', delim='COMMA', WFS_URL=None, outputfname=None, sleepSecs=10):
    """
    Makes a featureCategoricalGridCoverage algorithm call. 
    """
    
    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL)
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
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs)

def submitFeatureCoverageWCSIntersection(geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False, coverage='true', WFS_URL=None, outputfname=None, sleepSecs=10):
    """
    Makes a featureCoverageWCSIntersection algorithm call. 
    """
    
    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL)
    if featureCollection is None:
        return
    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageIntersectionAlgorithm'
    inputs = [("DATASET_URI", dataSetURI),
              ("DATASET_ID", varID),
              ("REQUIRE_FULL_COVERAGE",coverage), 
              ("FEATURE_COLLECTION", featureCollection)]
    output = "OUTPUT"
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs)

def submitFeatureCoverageOPenDAP(geoType, dataSetURI, varID, startTime, endTime, attribute='the_geom', value=None, gmlIDs=None, verbose=False, coverage='true', WFS_URL=None, outputfname=None, sleepSecs=10):
    """
    Makes a featureCoverageOPenDAP algorithm call. 
    """
    
    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL)
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
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs)    

def submitFeatureCoverageWCSIntersection(geoType, dataSetURI, varID, attribute='the_geom', value=None, gmlIDs=None, verbose=False, coverage='true', WFS_URL=None, outputfname=None, sleepSecs=10):
    """
    Makes a featureCoverageWCSIntersection algorithm call. 
    """
    
    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL)
    if featureCollection is None:
        return
    processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureCoverageIntersectionAlgorithm'
    inputs = [("DATASET_URI", dataSetURI),
              ("DATASET_ID", varID),
              ("REQUIRE_FULL_COVERAGE",coverage), 
              ("FEATURE_COLLECTION", featureCollection)]
    output = "OUTPUT"
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname, sleepSecs)
