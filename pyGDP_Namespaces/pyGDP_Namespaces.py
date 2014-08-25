import os
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE
import _read_config_text
#Global URLs for GDP and services

#The environ_name can be either production, development, testing, or a custom
#set of URLs that can be adjusted in the pyGDP_URLs.txt file.
#The .txt path is currently set to point wherever this script is executed from.

URL_file = os.path.join(os.path.split(_read_config_text.__file__)[0], 'pyGDP_URLs.txt')

#URLs are read out from the dictionary created from the .txt file.
#Here they are prepared to be sent to pyGDP.
def get_URLs(environ_name):
    urls = _read_config_text.get_urls(URL_file, environ_name)
    return urls

urls=get_URLs(environ_name = 'production')

WFS_URL    = urls['WFS_URL']
upload_URL = urls['upload_URL']
WPS_URL    = urls['WPS_URL']
WPS_Service= urls['WPS_Service']
CSWURL     = urls['CSWURL']

#These are the schema locations for pyGDP XML validation.
WPS_DEFAULT_VERSION = '1.0.0'
WPS_DEFAULT_SCHEMA_LOCATION = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd'
GML_SCHEMA_LOCATION = "http://schemas.opengis.net/gml/3.1.1/base/feature.xsd"

#These namespaces are subject to change in version number. They will change
#with pyGDP versions here if necessary.
WPS_DEFAULT_NAMESPACE="http://www.opengis.net/wps/1.0.0"
CSW_NAMESPACE = 'http://www.opengis.net/cat/csw/2.0.2'
WPS_DEFAULT_NAMESPACE="http://www.opengis.net/wps/1.0.0"

WFS_NAMESPACE = 'http://www.opengis.net/wfs'
OGC_NAMESPACE = 'http://www.opengis.net/ogc'
GML_NAMESPACE = 'http://www.opengis.net/gml'

#These are geoserver specific namespaces for different work environments.
#These will probably never change.
DRAW_NAMESPACE = 'gov.usgs.cida.gdp.draw'
SMPL_NAMESPACE = 'gov.usgs.cida.gdp.sample'
UPLD_NAMESPACE = 'gov.usgs.cida.gdp.upload'

#Variables used for internal pyGDP purposes
URL_timeout = 60		# seconds
WPS_attempts= 10		# tries with null response before failing

#Here is a dictionary of all the namespaces used in pyGDP. Expect to see
#both calls to this dictionary and references to the full namespace variable
#depending on the the nature of the function in pyGDP.
namespaces = {
     None  	: WPS_DEFAULT_NAMESPACE,
    'wps'  	: WPS_DEFAULT_NAMESPACE,
    'ows'  	: DEFAULT_OWS_NAMESPACE,
    'xlink'	: XLINK_NAMESPACE,
    'xsi'  	: XSI_NAMESPACE,
    'wfs'  	: WFS_NAMESPACE,
    'ogc'  	: OGC_NAMESPACE,
    'gml'  	: GML_NAMESPACE,
    'sample'    : SMPL_NAMESPACE,
    'upload'    : UPLD_NAMESPACE,
    'csw'	: CSW_NAMESPACE
}
