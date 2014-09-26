from pyGDP_WFS_Utilities import shapefile_id_handle, shapefile_value_handle

#Use the import chunks from pyGDP.py to bring in the necessary namespace definitions
from pyGDP_Namespaces.pyGDP_Namespaces import WFS_URL
from owslib.wps import WebProcessingService, WFSFeatureCollection, WFSQuery, GMLMultiPolygonFeatureCollection, monitorExecution

def _getFeatureCollectionGeoType(geoType, attribute, value, gmlIDs, WFS_URL):
    """
    This function returns a featurecollection. It takes a geotype and determines if
    the geotype is a shapfile or polygon. 
    
    If value is set to None, a FeatureCollection with all features will be returned.
    
    """
    
    # This is a polygon
    if isinstance(geoType, list):
        return GMLMultiPolygonFeatureCollection( [geoType] )
    elif isinstance(geoType, str):
        if value==None:
            # Using an empty gmlIDs element results in all features being returned to the constructed WFS query.
            if gmlIDs is None:
                gmlIDs=[]
                print 'All shapefile attributes will be used.'
        tmpID = []
        if gmlIDs is None:
            if type(value) == type(tmpID):
                gmlIDs = []
                for v in value:
                    tuples = shapefile_id_handle.getTuples(geoType, attribute)
                    tmpID = shapefile_id_handle._getFilterID(tuples, v)
                    gmlIDs = gmlIDs + tmpID
                print tmpID
                if tmpID == []:
                    raise Exception("Didn't find any features matching given attribute values.")
            else:
                tuples = shapefile_id_handle.getTuples(geoType, attribute, WFS_URL)
                gmlIDs = shapefile_id_handle._getFilterID(tuples, value)
                if gmlIDs==[]:
                    raise Exception("Didn't find any features matching given attribute value.")
        
        geometry_attribute='the_geom'
        if 'arcgis' in WFS_URL.lower():
            geometry_attribute='Shape'
        
        query = WFSQuery(geoType, propertyNames=[geometry_attribute, attribute], filters=gmlIDs)
        
        return WFSFeatureCollection(WFS_URL, query)
    else:
        raise Exception('Geotype is not a shapefile or a recognizable polygon.')
