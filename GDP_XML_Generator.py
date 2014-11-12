from owslib.etree import etree
import owslib.util as util

#Import the appropriate namespace variables.
from pygdp.namespaces import WPS_DEFAULT_VERSION, WPS_DEFAULT_SCHEMA_LOCATION, GML_SCHEMA_LOCATION
from pygdp.namespaces import namespaces

class gdpXMLGenerator():
    """
    This class is responsible for generating the upload XML tree template
    as well as the xml post request tree template.
    This class serves no other functions.
    """
    
    def _init_(self):
        pass
    
    def _subElement(self, root, elementName):
        return etree.SubElement(root, util.nspath_eval(elementName, namespaces))
    
    def getUploadXMLtree(self, filename, wfsUrl, filedata):
        
        # generate the POST XML request
        #<wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0" 
        #             xmlns:ows="http://www.opengis.net/ows/1.1" 
        #             xmlns:xlink="http://www.w3.org/1999/xlink" 
        #             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        #             service="WPS" 
        #             version="1.0.0" 
        #             xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">       
        root = etree.Element(util.nspath_eval('wps:Execute', namespaces), nsmap=namespaces)
        root.set('service', 'WPS')
        root.set('version', WPS_DEFAULT_VERSION)
        root.set(util.nspath_eval('xsi:schemaLocation', namespaces), '%s %s' % (namespaces['wps'], WPS_DEFAULT_SCHEMA_LOCATION) )
        
        # <ows:Identifier>gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids</ows:Identifier>
        identifierElement = self._subElement(root, 'ows:Identifier')
        identifierElement.text = 'gov.usgs.cida.gdp.wps.algorithm.filemanagement.ReceiveFiles'
        
        # <wps:DataInputs>
        #    <wps:Input>
        #        <ows:Identifier>filename</ows:Identifier>
        #        <wps:Data>
        #            <wps:LiteralData>FILENAME</wps:LiteralData>
        #        </wps:Data>
        #    <wps:Input>
        #        <wps:Identifier>wfs-url</wps:Identifier>
        #            <wps:Data>
        #                <wps:LiteralData>false</wps:LiteralData>
        #            </wps:Data>
        # </wps:DataInputs>
        dataInputsElement = self._subElement(root,'wps:DataInputs')
        inputElements = self._subElement(dataInputsElement, 'wps:Input')
        identifierElement = self._subElement(inputElements, 'ows:Identifier')
        identifierElement.text = 'filename'
        
        dataElement = self._subElement(inputElements,'wps:Data')
        literalElement = self._subElement(dataElement, 'wps:LiteralData')
        literalElement.text = filename
        
        inputElements = self._subElement(dataInputsElement, 'wps:Input')
        identifierElement = self._subElement(inputElements, 'ows:Identifier')
        identifierElement.text = 'wfs-url'
        dataElement = self._subElement(inputElements,'wps:Data')
        literalElement = self._subElement(dataElement,'wps:LiteralData')
        literalElement.text = wfsUrl
    
        # adding complex information
        inputElements = self._subElement(dataInputsElement, 'wps:Input')
        identifierElement = self._subElement(inputElements, 'ows:Identifier')
        identifierElement.text = 'file'
        dataElement = self._subElement(inputElements, 'wps:Data')
        complexDataElement = etree.SubElement(dataElement, util.nspath_eval('wps:ComplexData', namespaces),
                                                  attrib={"mimeType":"application/x-zipped-shp", "encoding":"Base64"} )
        # sets filedata
        complexDataElement.text = filedata
        
        # <wps:ResponseForm>
        #    <wps:ResponseDocument>
        #        <ows:Output>
        #            <ows:Identifier>result</ows:Identifier>
        #        </ows:Output>
        #    </wps:ResponseDocument>
        # </wps:ResponseForm>
        responseFormElement = self._subElement(root, 'wps:ResponseForm')
        responseDocElement = self._subElement(responseFormElement, 'wps:ResponseDocument')
        outputElement = self._subElement(responseDocElement, 'wps:Output')
        identifierElement = self._subElement(outputElement, 'ows:Identifier')
        identifierElement.text = 'result'
        outputElement = self._subElement(responseDocElement, 'wps:Output')
        identifierElement = self._subElement(outputElement, 'ows:Identifier')
        identifierElement.text = 'wfs-url'
        outputElement = self._subElement(responseDocElement, 'wps:Output')
        identifierElement = self._subElement(outputElement,'ows:Identifier')
        identifierElement.text = 'featuretype'
        
        return root

    def getXMLRequestTree(self, dataSetURI, algorithm, method, varID=None, verbose=False):
        
        #<wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0" 
        #             xmlns:ows="http://www.opengis.net/ows/1.1" 
        #             xmlns:xlink="http://www.w3.org/1999/xlink" 
        #             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        #             service="WPS" 
        #             version="1.0.0" 
        #             xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd">       
        root = etree.Element(util.nspath_eval('wps:Execute', namespaces), nsmap=namespaces)
        root.set('service', 'WPS')
        root.set('version', WPS_DEFAULT_VERSION)
        root.set(util.nspath_eval('xsi:schemaLocation', namespaces), '%s %s' % (namespaces['wps'], WPS_DEFAULT_SCHEMA_LOCATION) )
        
        # <ows:Identifier>gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids</ows:Identifier>
        identifierElement = etree.SubElement(root, util.nspath_eval('ows:Identifier', namespaces))
        identifierElement.text = algorithm
        
        # <wps:DataInputs>
        #    <wps:Input>
        #        <ows:Identifier>catalog-url</ows:Identifier>
        #        <wps:Data>
        #            <wps:LiteralData>'dataSetURI</wps:LiteralData>
        #        </wps:Data>
        #    <wps:Input>
        #        <wps:Identifier>allow-cached-response</wps:Identifier>
        #            <wps:Data>
        #                <wps:LiteralData>false</wps:LiteralData>
        #            </wps:Data>
        # </wps:DataInputs>
        dataInputsElement = etree.SubElement(root, util.nspath_eval('wps:DataInputs', namespaces))
        inputElements = etree.SubElement(dataInputsElement, util.nspath_eval('wps:Input', namespaces))
        identifierElement = etree.SubElement(inputElements, util.nspath_eval('ows:Identifier', namespaces))
        identifierElement.text = 'catalog-url'
        dataElement = etree.SubElement(inputElements, util.nspath_eval('wps:Data', namespaces))
        literalElement = etree.SubElement(dataElement, util.nspath_eval('wps:LiteralData', namespaces))
        literalElement.text = dataSetURI
        
        if method == 'getDataSetTime':
            inputElements = etree.SubElement(dataInputsElement, util.nspath_eval('wps:Input', namespaces))
            identifierElement = etree.SubElement(inputElements, util.nspath_eval('ows:Identifier', namespaces))
            identifierElement.text = 'grid'
            dataElement = etree.SubElement(inputElements, util.nspath_eval('wps:Data', namespaces))
            literalElement = etree.SubElement(dataElement, util.nspath_eval('wps:LiteralData', namespaces))
            literalElement.text = varID
        
        inputElements = etree.SubElement(dataInputsElement, util.nspath_eval('wps:Input', namespaces))
        identifierElement = etree.SubElement(inputElements, util.nspath_eval('ows:Identifier', namespaces))
        identifierElement.text = 'allow-cached-response'
        dataElement = etree.SubElement(inputElements, util.nspath_eval('wps:Data', namespaces))
        literalElement = etree.SubElement(dataElement, util.nspath_eval('wps:LiteralData', namespaces))
        literalElement.text = 'false'
        
        # <wps:ResponseForm storeExecuteResponse=true status=true>
        #    <wps:ResponseDocument>
        #        <ows:Output asReference=true>
        #            <ows:Identifier>result</ows:Identifier>
        #        </ows:Output>
        #    </wps:ResponseDocument>
        # </wps:ResponseForm>
        responseFormElement = etree.SubElement(root, util.nspath_eval('wps:ResponseForm', namespaces), attrib={'storeExecuteResponse': 'true', 'status' : 'true'})
        responseDocElement = etree.SubElement(responseFormElement, util.nspath_eval('wps:ResponseDocument', namespaces))
        outputElement = etree.SubElement(responseDocElement, util.nspath_eval('wps:Output', namespaces), attrib={'asReference': 'false'})
        identifierElement = etree.SubElement(outputElement, util.nspath_eval('ows:Identifier', namespaces))
        identifierElement.text = 'result_as_xml'
        
        return root
    
