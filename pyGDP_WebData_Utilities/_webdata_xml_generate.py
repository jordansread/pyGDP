from owslib.wps import WebProcessingService
from StringIO import StringIO
from owslib.etree import etree
from GDP_XML_Generator import gdpXMLGenerator
from pyGDP_Submit_Feature import _execute_request
import sys

from pyGDP_Namespaces.pyGDP_Namespaces import WPS_Service

def _generateRequest(dataSetURI, algorithm, method, varID, verbose):
    """
    Takes a dataset uri, algorithm, method, and datatype. This function will generate a simple XML document
    to make the request specified. (Only works for ListOpendapGrids and GetGridTimeRange). 
    
    Will return a list containing the info requested for (either data types or time range).
    """
    
    POST = WebProcessingService(WPS_Service, verbose=verbose)
    
    xmlGen = gdpXMLGenerator()
    root = xmlGen.getXMLRequestTree(dataSetURI, algorithm, method, varID, verbose)           
    
    # change standard output to not display waiting status
    if not verbose:
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result   
    request = etree.tostring(root)
    
    execution = POST.execute(None, [], request=request)
    
    _execute_request._check_for_execution_errors(execution)
    
    if method == 'getDataSetTime':
        seekterm = '{xsd/gdptime-1.0.xsd}time'
    elif method == 'getDataType':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}name'
    elif method == 'getDataLongName':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}description'
    elif method == 'getDataUnits':
        seekterm = '{xsd/gdpdatatypecollection-1.0.xsd}unitsstring'
    if not verbose:
        sys.stdout = old_stdout

    return _parseXMLNodesForTagText(execution.response, seekterm)

def _parseXMLNodesForTagText(xml, tag):
    """
    Parses through a XML tree for text associated with specified tag.
    Returns a list of the text.
    """
    
    tag_text = []
    for node in xml.iter():
        if node.tag == tag:
            tag_text.append(node.text)
    return tag_text


