from owslib.wps import WebProcessingService, monitorExecution
from pyGDP_Namespaces.pyGDP_Namespaces import upload_URL, WPS_URL, WPS_Service, CSWURL
from pyGDP_Namespaces.pyGDP_Namespaces import URL_timeout, WPS_attempts
from time import strftime, sleep
import sys
from os import devnull 

def dodsReplace(dataSetURI, verbose=False):
    if "/dodsC" in dataSetURI:
        dataSetURI= dataSetURI.replace("http", "dods")
    return dataSetURI

def _executeRequest(processid, inputs, output, verbose=True, outputFilePath=None):
    """
    This function makes a call to the Web Processing Service with
    the specified user inputs.
    """
    wps = WebProcessingService(WPS_URL)
    
    execution = wps.execute(processid, inputs, output)
    
    sleepSecs=10
    err_count=1
    
    while execution.isComplete()==False:
        # try:
        monitorExecution(execution, sleepSecs, download=False) # monitors for success
        err_count=1
        # except Exception:
        #     print 'An error occurred while checking status, checking again.'
        #     print 'Sleeping %d seconds...' % sleepSecs
        #     err_count+=1
        #     if err_count > WPS_attempts:
        #         raise Exception('The status document failed to return, status checking has aborted. There has been a network or server issue preventing the status document from being retrieved, the request may still be running. For more information, check the status url %s' % execution.statusLocation)
        #     sleep(sleepSecs)
    
    if outputFilePath==None:
        outputFilePath='gdp_'+processid.replace('.','-')+'_'+strftime("%Y-%m-%dT%H-%M-%S-%Z")
        
    done=False
    err_count=1
    while done==False:
        # try: 
        monitorExecution(execution, download=True,filepath=outputFilePath)
        done=True
        # except Exception:
        #             print 'An error occurred while trying to download the result file, trying again.'
        #             err_count+=1
        #             sleep(sleepSecs)
        #         if err_count > WPS_attempts:        
        #             raise Exception("The process completed successfully, but an error occurred while downloading the result. You may be able to download the file using the link at the bottom of the status document: %s" % execution.statusLocation)
    
    _check_for_execution_errors(execution)
        
    return outputFilePath
    
def _check_for_execution_errors(execution):
    '''wps does not raise python errors if something goes wrong on the server side
    we will check for errors, and the succeded status and raise python
    Exceptions as needed 
    '''
    errmsg = ""
    
    if execution.status == "ProcessFailed":
        errmsg = "The remote process failed!\n"
    
    if execution.errors:
        #something went wrong, it would be a shame to pass silently
        errmsg += "\n".join([err.text for err in execution.errors])
    
    if errmsg:
        raise Exception(errmsg)
