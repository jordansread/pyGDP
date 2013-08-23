# dependencies: lxml.etree, owslib
# =============================================================================
# Authors : Xao Yang, Jordan Walker, Jordan Read, Curtis Price, David Blodgett
#
# Contact email: jread@usgs.gov
# =============================================================================
from owslib.wps import WebProcessingService, WFSFeatureCollection, WFSQuery, GMLMultiPolygonFeatureCollection, monitorExecution
from owslib.ows import DEFAULT_OWS_NAMESPACE, XSI_NAMESPACE, XLINK_NAMESPACE
from owslib.wfs import WebFeatureService
from owslib.csw import CatalogueServiceWeb
from owslib.etree import etree
from StringIO import StringIO
from urllib import urlencode
from urllib2 import urlopen
from time import sleep
import owslib.util as util
import base64
import cgi
import sys
import os
import zipfile

__version__ = '1.2.2'

#global urls for GDP and services
WFS_URL    = 'http://cida.usgs.gov/gdp/geoserver/wfs'
upload_URL = 'http://cida.usgs.gov/gdp/geoserver'
WPS_URL    = 'http://cida.usgs.gov/gdp/process/WebProcessingService'
WPS_Service= 'http://cida.usgs.gov/gdp/utility/WebProcessingService'
CSWURL='http://cida.usgs.gov/gdp/geonetwork/srv/en/csw'

# namespace definition
WPS_DEFAULT_NAMESPACE="http://www.opengis.net/wps/1.0.0"
WPS_DEFAULT_SCHEMA_LOCATION = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd'
WPS_DEFAULT_VERSION = '1.0.0'
WFS_NAMESPACE = 'http://www.opengis.net/wfs'
OGC_NAMESPACE = 'http://www.opengis.net/ogc'
GML_NAMESPACE = 'http://www.opengis.net/gml'
GML_SCHEMA_LOCATION = "http://schemas.opengis.net/gml/3.1.1/base/feature.xsd"
DRAW_NAMESPACE = 'gov.usgs.cida.gdp.draw'
SMPL_NAMESPACE = 'gov.usgs.cida.gdp.sample'
UPLD_NAMESPACE = 'gov.usgs.cida.gdp.upload'
CSW_NAMESPACE = 'http://www.opengis.net/cat/csw/2.0.2'

# misc variables
URL_timeout = 60		# seconds
WPS_attempts= 10		# tries with null response before failing

# list of namespaces used by this module
namespaces = {
     None  	: WPS_DEFAULT_NAMESPACE,
    'wps'  	: WPS_DEFAULT_NAMESPACE,
    'ows'  	: DEFAULT_OWS_NAMESPACE,
    'xlink'	: XLINK_NAMESPACE,
    'xsi'  	: XSI_NAMESPACE,
    'wfs'  	: WFS_NAMESPACE,
    'ogc'  	: OGC_NAMESPACE,
    'gml'  	: GML_NAMESPACE,
    'sample': SMPL_NAMESPACE,
    'upload': UPLD_NAMESPACE,
    'csw'	: CSW_NAMESPACE
}

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
        outputElement = etree.SubElement(responseDocElement, util.nspath_eval('wps:Output', namespaces), attrib={'asReference': 'true'})
        identifierElement = etree.SubElement(outputElement, util.nspath_eval('ows:Identifier', namespaces))
        identifierElement.text = 'result'
        
        return root
    
class pyGDPwebProcessing():
    """
    This class allows interactive calls to be made into the GDP.
    """
    
    def _init_(self, wfsUrl=WFS_URL, wpsUrl=WPS_URL, version='1.1.0'):
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

    def _encodeZipFolder(self, filename):
        """
        This function will encode a zipfile and return the filename.
        """
        #check extension
        if not filename.endswith('.zip'):
            raise Exception('Wrong filetype.')
        
        #encode the file
        with open(filename, 'rb') as fin:
            bytesRead = fin.read()
            encode= base64.b64encode(bytesRead)
    
        #renames the file and saves it onto local drive
        filename = filename.split('.')
        filename = str(filename[0]) + '_copy.' + str(filename[-1])
        
        fout = open(filename, "w")
        fout.write(encode)
        fout.close()
        return filename

    def shapeToZip(self,inShape, outZip=None, allFiles=True):
        """Packs a shapefile to ZIP format.
        
        arguments
        -inShape -  input shape file
        
        -outZip -   output ZIP file (optional)
          default: <inShapeName>.zip in same folder as inShape
          (If full path not specified, output is written to
          to same folder as inShape)
        
        -allFiles - Include all files? (optional)
          True (default) - all shape file components
          False - just .shp,.shx,.dbf,.prj,shp.xml files
        
        reference: Esri, Inc, 1998, Esri Shapefile Technical Description
          http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
        
        author: Curtis Price, cprice@usgs.gov"""
    
        if not os.path.splitext(inShape)[1] == ".shp":
            raise Exception, "inShape must be a *.shp"
    
        if not os.path.exists(inShape):
            raise Exception, "%s not found" % inShape
    
        # get shapefile root name "path/file.shp" -> "file"
        # and shapefile path
        rootName = os.path.splitext(os.path.basename(inShape))[0]
        inShape = os.path.realpath(inShape)
        inDir = os.path.dirname(inShape)
    
        # output zip file path
        if outZip in [None,""]:
            # default output: shapefilepath/shapefilename.zip
            outDir = inDir
            outZip = os.path.join(outDir,rootName) + ".zip"
        else:
            outDir = os.path.dirname(outZip)
            if outDir.strip() in ["","."]:
                # if full path not specified, use input shapefile folder
                outDir = os.path.dirname(os.path.realpath(inShape))
            else:
                # if output path does exist, raise an exception
                if not os.path.exists(outDir):
                    raise Exception, "Output folder %s not found" % outDir
            outZip = os.path.join(outDir,outZip)
            # enforce .zip extension
            outZip = os.path.splitext(outZip)[0] + ".zip"

        if not os.access(outDir, os.W_OK):
            raise Exception, "Output directory %s not writeable" % outDir

        if os.path.exists(outZip):
            os.unlink(outZip)

        try:
            # open zipfile
            zf = zipfile.ZipFile(outZip, 'w', zipfile.ZIP_DEFLATED)
            # write shapefile parts to zipfile
            ShapeExt = ["shp","shx","dbf","prj","shp.xml"]
            if allFiles: ShapeExt += ["sbn","sbx","fbn","fbx",
                                  "ain","aih","isx","mxs","atx","cpg"]
            for f in ["%s.%s" % (os.path.join(inDir,rootName),ext)
                  for ext in ShapeExt]:
                if os.path.exists(f):
                    zf.write(f)
                    ##print f # debug print
            return outZip
        except Exception, msg:
            raise Exception, \
                "Could not write zipfile " + outZip + "\n" + str(msg)
        finally:
            try:
                # close the output file
                zf.close()
            except:
                pass

    def uploadShapeFile(self, filePath):
        """
        Given a file, this function encodes the file and uploads it onto geoserver.
        """
        
        # encodes the file, opens it, reads it, and closes it
        # returns a filename in form of: filename_copy.zip
        filePath = self._encodeZipFolder(filePath)
        if filePath is None:
            return
        
        filehandle = open(filePath, 'r')
        filedata = filehandle.read()
        filehandle.close()
        os.remove(filePath)  # deletes the encoded file
        
        # this if for naming the file on geoServer
        filename = filePath.split("/")
        # gets rid of filepath, keeps only filename eg: file.zip
        filename = filename[len(filename) - 1]
        filename = filename.replace("_copy.zip", "")
        
        
        # check to make sure a file with the same name does not exist
        fileCheckString = "upload:" + filename
        shapefiles = self.getShapefiles()
        if fileCheckString in shapefiles:
            raise Exception('File exists already.')
        
        xmlGen = gdpXMLGenerator()
        root = xmlGen.getUploadXMLtree(filename, upload_URL, filedata)
        
        # now we have a complete XML upload request
        uploadRequest = etree.tostring(root)
        POST = WebProcessingService(WPS_Service)
        execution = POST.execute(None, [], request=uploadRequest)
        monitorExecution(execution)
        return "upload:"+filename
    
    def getTuples(self, shapefile, attribute):
        """
        Will return the dictionary tuples only.
        """
        return self.getValues(shapefile, attribute, getTuples='only')
    
    def _getGMLIDString(self, GMLbeginterm, line, GMLstopterm, valBeginTerm, valStopTerm):
        """
        This function is specific to the output documents from the GDP. This
        function parses the XML document, to find the correct GMLID associated
        with a feature. Returns the list of values, and a dictionary [feature:id].
        """
        
        # we are searching for attr-value, gml:id pair
        value = []
        ntuple = []
        begin_index = 0
        end_index = len(line)
        tmpline = line
        # start at the beginning
        while begin_index < len(line):
            begin_index = tmpline.find(GMLbeginterm)
            if begin_index != -1:
                end_index = tmpline.find(GMLstopterm, begin_index)
                # we get the gml term
                gmlterm = tmpline[begin_index + len(GMLbeginterm) : end_index ]
                
                # now we get the attribute value
                begin_index2 = tmpline.find(valBeginTerm)
                end_index2   = tmpline.find(valStopTerm, begin_index2)    
                
                valTerm = tmpline[begin_index2 + len(valBeginTerm) : end_index2 ]
                #tuple: attr-value, gml:id
                tmpTuple = valTerm, gmlterm
                ntuple.append(tmpTuple)
                
                tmpline = tmpline[end_index2 :]
                
                if valTerm not in value:
                    value.append(valTerm)
                begin_index = end_index
            else:
                break
        return value, ntuple
    
    def _getFilterID(self,tuples, value):
        """
        Given a the tuples generated by getTuples and a value, will return a list of gmlIDs
        associated with the value specified.
        """
        value = str(value)
        filterID = []
        for item in tuples:
            if item[0] == value:
                filterID.append(item[1])
        if filterID==[]:
            raise Exception('Feature attribute value %s was not found in the feature collection.' % value)
        return filterID
    
    def _parseXMLNodesForTagText(self, xml, tag):
        """
        Parses through a XML tree for text associated with specified tag.
        Returns a list of the text.
        """
        
        tag_text = []
        for node in xml.iter():
            if node.tag == tag:
                tag_text.append(node.text)
        return tag_text
    
    def _generateRequest(self, dataSetURI, algorithm, method, varID=None, verbose=False):
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
        if method == 'getDataSetTime':
            seekterm = 'time'
        elif method == 'getDataType':
            seekterm = 'name'
        elif method == 'getDataLongName':
            seekterm = 'description'
        elif method == 'getDataUnits':
            seekterm = 'unitsstring'
        if not verbose:
            sys.stdout = old_stdout
    
        return self._parseXMLNodesForTagText(execution.response, seekterm)
    
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
    
    def getAttributes(self, shapefile):
        """
        Given a valid shapefile(WFS Featuretype as returned by getShapefiles), this function will 
        make a request for one feature from the featureType and parse out the attributes that come from
        a namespace not associated with the normal GML schema. There may be a better way to determine 
        which are shapefile dbf attributes, but this should work pretty well.
        """
        wfs = WebFeatureService(WFS_URL, version='1.1.0')
        feature = wfs.getfeature(typename=shapefile, maxfeatures=1, propertyname=None)
        gml = etree.parse(feature)
        gml_root=gml.getroot()
        name_spaces = gml_root.nsmap
        
        attributes = []
        
        for namespace in name_spaces.values():
            if namespace not in ['http://www.opengis.net/wfs',
                                 'http://www.w3.org/2001/XMLSchema-instance',
                                 'http://www.w3.org/1999/xlink',
                                 'http://www.opengis.net/gml',
                                 'http://www.opengis.net/ogc',
                                 'http://www.opengis.net/ows']:
                custom_namespace = namespace
                
                for element in gml.iter('{'+custom_namespace+'}*'):
                    if etree.QName(element).localname not in ['the_geom', 'Shape', shapefile.split(':')[1]]:
                        attributes.append(etree.QName(element).localname)
        return attributes
    
    def getShapefiles(self):
        """
        Returns a list of available files currently on geoserver.
        """
        wfs = WebFeatureService(WFS_URL)
        shapefiles = wfs.contents.keys()
        return shapefiles
    
    def getValues(self, shapefile, attribute, getTuples='false', limitFeatures=None):
        """
        Similar to get attributes, given a shapefile and a valid attribute this function
        will make a call to the Web Feature Services returning a list of values associated
        with the shapefile and attribute.
        
        If getTuples = True, will also return the tuples of [feature:id]  along with values [feature]
        """
        
        wfs = WebFeatureService(WFS_URL, version='1.1.0')
        
        feature = wfs.getfeature(typename=shapefile, maxfeatures=limitFeatures, propertyname=[attribute])

        gml = etree.parse(feature)

        values= []

        for el in gml.iter():
            if attribute in el.tag:
                if el.text not in values:
                    values.append(el.text)

        if getTuples == 'true' or getTuples == 'only':
            tuples = []
            # If features are encoded as a list of featureMember elements.
            gmlid_found=False
            for featureMember in gml.iter('{'+GML_NAMESPACE+'}featureMember'):
                for el in featureMember.iter():
                    if el.get('{'+GML_NAMESPACE+'}id'):
                        gmlid = el.get('{'+GML_NAMESPACE+'}id')
                        att=True
                        gmlid_found=True
                    if attribute in el.tag and att==True:
                        value=el.text
                        tuples.append((value,gmlid))
                        att=False
                if gmlid_found==False:
                    raise Exception('No gml:id found in source feature service. This form of GML is not supported.')
            # If features are encoded as a featureMembers element.
            for featureMember in gml.iter('{'+GML_NAMESPACE+'}featureMembers'):
                for el in featureMember.iter():
                    gmlid = el.get('{'+GML_NAMESPACE+'}id')
                    for feat in el.getchildren():
                        if attribute in feat.tag:
                            value=feat.text
                            tuples.append((value,gmlid))

        if getTuples=='true':
            return sorted(values), sorted(tuples)
        elif getTuples=='only':
            return sorted(tuples)
        else:
            return sorted(values)
    
    def getDataType(self, dataSetURI, verbose=False):
        """
        Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
        If verbose = True, will print on screen the waiting seq. for response document.
        """
            
        algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
        return self._generateRequest(dataSetURI, algorithm, method='getDataType', varID=None, verbose=verbose)
    
    def getDataLongName(self, dataSetURI, verbose=False):
        """
            Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
            If verbose = True, will print on screen the waiting seq. for response document.
            """
        
        algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
        return self._generateRequest(dataSetURI, algorithm, method='getDataLongName', varID=None, verbose=verbose)

    def getDataUnits(self, dataSetURI, verbose=False):
        """
            Set up a get Data type request given a dataSetURI. Returns a list of all available data types.
            If verbose = True, will print on screen the waiting seq. for response document.
            """
        
        algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.ListOpendapGrids'
        return self._generateRequest(dataSetURI, algorithm, method='getDataUnits', varID=None, verbose=verbose)
	
    def dodsReplace(self, dataSetURI, verbose=False):
		if "/dodsC" in dataSetURI:
			dataSetURI= dataSetURI.replace("http", "dods")
		return dataSetURI
        
    def getDataSetURI(self, anyText='',CSWURL=CSWURL,BBox=None):
				"""

				Searches a given CSW server and returns metadata content for the datasets found.

				Arguments
				---------

				- anyText - A string that will be submitted to the CSW search. (Optional, default is empty which will return all records.)
				- CSWURL - A base URL for the CSW server to be searched. (Optional, defaults to the CDIA/GDP CSW server.)
				- BBox - A lat/lon bounding box in [minx,miny,maxx,maxy] that will be used to limit results to datasets that atleast partially intersect. (Optional)

				"""

				csw = CatalogueServiceWeb(CSWURL, skip_caps=True)
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
						pass
					else:
						pass
					for ident in range(len(csw.records[rec].identificationinfo)):
						try:
							for operation in range(len(csw.records[rec].identificationinfo[ident].operations)):
								urls.append(csw.records[rec].identificationinfo[ident].operations[0]['connectpoint'][0].url)
						except AttributeError:
							pass
						else:
							pass
					entry=[title,abstract,urls]
					dataSetURIs.append(entry)
				for i,dataset in enumerate(dataSetURIs):
					dataSetURIs[i][2]=[uri.replace("http", "dods") if "/dodsC/" in uri else uri for uri in dataset[2]]
				return dataSetURIs
    
    def getGMLIDs(self, shapefile, attribute, value):
        """
        This function returns the gmlID associated with a particular attribute value.
        """
        tuples = self.getTuples(shapefile, attribute)
        return self._getFilterID(tuples, value)
    
    def getTimeRange(self, dataSetURI, varID, verbose=False):
        """
        Set up a get dataset time range request given a datatype and dataset uri. Returns the range
        of the earliest and latest time.
        If verbose = True, will print on screen the waiting seq. for response document.
        """
        
        algorithm = 'gov.usgs.cida.gdp.wps.algorithm.discovery.GetGridTimeRange'
        return self._generateRequest(dataSetURI, algorithm, method='getDataSetTime', varID=varID, verbose=verbose)
    
    
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
