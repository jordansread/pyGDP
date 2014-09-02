from owslib.wps import WebProcessingService, monitorExecution
from pyGDP_Namespaces.pyGDP_Namespaces import WFS_URL, upload_URL, WPS_URL, WPS_Service, CSWURL
from pyGDP_Namespaces.pyGDP_Namespaces import URL_timeout, WPS_attempts
from StringIO import StringIO
import sys

def dodsReplace(dataSetURI, verbose=False):
    if "/dodsC" in dataSetURI:
        dataSetURI= dataSetURI.replace("http", "dods")
    return dataSetURI

def _executeRequest(processid, inputs, output, verbose=True):
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
