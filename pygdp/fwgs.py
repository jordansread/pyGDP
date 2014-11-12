from pygdp import _execute_request
from pygdp import _get_geotype
from owslib.util import log

def submitFeatureWeightedGridStatistics(geoType, dataSetURI, varID, startTime, endTime, attribute, value, gmlIDs,
                                        verbose, coverage, delim, stat, grpby, timeStep, summAttr, weighted, WFS_URL, outputfname):
    """
    Makes a featureWeightedGridStatistics algorithm call. 
    The web service interface implemented is summarized here: 
    https://my.usgs.gov/confluence/display/GeoDataPortal/Generating+Area+Weighted+Statistics+Of+A+Gridded+Dataset+For+A+Set+Of+Vector+Polygon+Features
    
    Note that varID and stat can be a list of strings.
    
    """
    # test for dods:
    dataSetURI = _execute_request.dodsReplace(dataSetURI)
    
    log.info('Generating feature collection.')
    
    featureCollection = _get_geotype._getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL)
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
    
    return _execute_request._executeRequest(processid, inputs, output, verbose, outputfname)
