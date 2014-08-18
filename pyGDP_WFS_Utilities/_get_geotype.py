def _getFeatureCollectionGeoType(self, geoType, attribute='the_geom', value=None, gmlIDs=None):
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
                    tuples = self.getTuples(geoType, attribute)
                    tmpID = self._getFilterID(tuples, v)
                    gmlIDs = gmlIDs + tmpID
                print tmpID
                if tmpID == []:
                    raise Exception("Didn't find any features matching given attribute values.")
            else:
                tuples = self.getTuples(geoType, attribute)
                gmlIDs = self._getFilterID(tuples, value)
                if gmlIDs==[]:
                    raise Exception("Didn't find any features matching given attribute value.")
        
        geometry_attribute='the_geom'
        if 'arcgis' in WFS_URL.lower():
            geometry_attribute='Shape'
        
        query = WFSQuery(geoType, propertyNames=[geometry_attribute, attribute], filters=gmlIDs)
        
        return WFSFeatureCollection(WFS_URL, query)
    else:
        raise Exception('Geotype is not a shapefile or a recognizable polygon.')
