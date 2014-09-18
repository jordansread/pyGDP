import os
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE
#Global URLs for GDP and services


#URLs are read out from the dictionary.
#Here they are prepared to be sent to pyGDP.
def get_URLs(environ_name):
    if environ_name == 'production':
    
        urls        = {  'WFS_URL'	        :	'http://cida.usgs.gov/gdp/geoserver/wfs',
                        'upload_URL'	        :	'http://cida.usgs.gov/gdp/geoserver',
                        'WPS_URL'	        :	'http://cida.usgs.gov/gdp/process/WebProcessingService',
                        'WPS_Service'	        :	'http://cida.usgs.gov/gdp/utility/WebProcessingService',
                        'CSWURL'	        :	'http://cida.usgs.gov/gdp/geonetwork/srv/en/csw'
                      }
        
    if environ_name == 'development':
        
        urls        = { 'WFS_URL'	        :	'http://cida-eros-gdpdev.er.usgs.gov:8082/geoserver/wfs',
                        'upload_URL'        	:	'http://cida-eros-gdpdev.er.usgs.gov:8082/geoserver/',
                        'WPS_URL'	        :	'http://cida-eros-gdpdev.er.usgs.gov:8080/gdp-process-wps/WebProcessingService',
                        'WPS_Service'	        :	'http://cida-eros-gdpdev.er.usgs.gov:8080/gdp-utility-wps/WebProcessingService?Service=WPS&Request=GetCapabilities',	
                        'CSWURL'	        :	'http://cida-test.er.usgs.gov/gdp/geonetwork/srv/en/csw'
                      }
        
    if environ_name == 'testing':
        
        urls    =     { 'WFS_URL'	        :	'http://cida-test.er.usgs.gov/geoserver/',
                        'upload_URL'	        :	'http://cida-eros-gdpdev.er.usgs.gov:8082/geoserver/',
                        'WPS_URL'	        :	'http://cida-test.er.usgs.gov/gdp-process-wps/WebProcessingService',
                        'WPS_Service'	        :	'http://cida-test.er.usgs.gov/gdp-utility-wps/WebProcessingService?Service=WPS&Request=GetCapabilities',	
                        'CSWURL'	        :	'http://cida-test.er.usgs.gov/gdp/geonetwork/srv/en/csw'
                      }
        
    if environ_name == 'custom':
        
        urls    =      { 'WFS_URL'	        :	'your input here',	
                        'upload_URL'	        :	'your input here',
                        'WPS_URL'	        :	'your input here',
                        'WPS_Service'	:       	'your input here',	
                        'CSWURL'	        :	'your input here'
                       }
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
