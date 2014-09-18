from GDP_XML_Generator import gdpXMLGenerator
from owslib.wps import WebProcessingService, monitorExecution 
from pyGDP_Namespaces.pyGDP_Namespaces import WFS_URL, upload_URL, WPS_URL, WPS_Service, CSWURL

#This file contains a function to encode a zipped shapefile (probably from
#the shapeToZip function) then include that function 
def uploadShapeFile(filePath):
    """
    Given a file, this function encodes the file and uploads it onto geoserver.
    """
    
    # encodes the file, opens it, reads it, and closes it
    # returns a filename in form of: filename_copy.zip
    filePath = _encodeZipFolder(filePath)
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

def _encodeZipFolder(filename):
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
