from owslib.csw import CatalogueServiceWeb
from pyGDP_WebData_Utilities import _webdata_xml_generate

def getDataSetURI(anyText, CSWURL, BBox):
                            """

                            Searches a given CSW server and returns metadata content for the datasets found.

                            Arguments
                            ---------

                            - anyText - A string that will be submitted to the CSW search. (Optional, default is empty which will return all records.)
                            - CSWURL - A base URL for the CSW server to be searched. (Optional, defaults to the CDIA/GDP CSW server.)
                            - BBox - A lat/lon bounding box in [minx,miny,maxx,maxy] that will be used to limit results to datasets that atleast partially intersect. (Optional)

                            """

                            csw = CatalogueServiceWeb(CSWURL, skip_caps=True)
                            #Works with owslib version 0.8.6.
                            csw.getrecords(keywords=[anyText], outputschema='http://www.isotc211.org/2005/gmd', esn='full', maxrecords=100)
                            dataSetURIs = [['title','abstract',['urls']]]
                            for rec in csw.records:
                                    title=csw.records[rec].identification.title
                                    abstract=csw.records[rec].identification.abstract
                                    urls=[]
                                    try:
                                            for onlineresource in range(len(csw.records[rec].distribution.online)):
                                                    urls.append(csw.records[rec].distribution.online[onlineresource].url)
                                    except AttributeError:
                                            print#pass
                                    else:
                                            print#pass
                                    for ident in range(len(csw.records[rec].identificationinfo)):
                                            try:
                                                    for operation in range(len(csw.records[rec].identificationinfo[ident].operations)):
                                                            urls.append(csw.records[rec].identificationinfo[ident].operations[0]['connectpoint'][0].url)
                                            except AttributeError:
                                                    print#pass
                                            else:
                                                    print#pass
                                    entry=[title,abstract,urls]
                                    dataSetURIs.append(entry)
                            for i,dataset in enumerate(dataSetURIs):
                                    dataSetURIs[i][2]=[uri.replace("http", "dods") if "/dodsC/" in uri else uri for uri in dataset[2]]
                            return dataSetURIs
                        
def getDataType(dataSetURI, verbose):
    """
    Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
    If verbose = True, will print on screen the waiting seq. for response document.
    """
        
    algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
    return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method='getDataType', varID=None, verbose=verbose)

def getDataLongName(dataSetURI, verbose):
    """
        Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
        If verbose = True, will print on screen the waiting seq. for response document.
        """
    
    algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
    return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method='getDataLongName', varID=None, verbose=verbose)

def getDataUnits(dataSetURI, verbose):
    """
        Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
        If verbose = True, will print on screen the waiting seq. for response document.
        """
    
    algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
    return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method='getDataUnits', varID=None, verbose=verbose)

def getTimeRange(dataSetURI, varID, verbose):
    """
    Set up a get dataset time range request given a datatype and dataset uri. Returns the range
    of the earliest and latest time.
    If verbose = True, will print on screen the waiting seq. for response document.
    """
    
    algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.GetGridTimeRange'
    return _webdata_xml_generate._generateRequest(dataSetURI, algorithm, method='getDataSetTime', varID=varID, verbose=verbose)
