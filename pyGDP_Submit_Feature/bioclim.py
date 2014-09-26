from pyGDP_Submit_Feature import _execute_request
from pyGDP_WebData_Utilities import webdata_handle
import datetime
import os
import dateutil.parser
import urllib2
import shutil

def submitCustomBioclim(processid="org.n52.wps.server.r.gridded_bioclim", 
                        outputfname=None, verbose=False, **kwargs):
    '''Makes a call to the WPS algorithm wrapping an R script which generates 
    custom Bioclim variables. The processid is the locator of our R script.
        defaults to: org.n52.wps.server.r.gridded_bioclim
    outputfname is the path to save the returned zip to
    the remaining argumnets are:
        OPeNDAP_URI: A locator of a valid OPenDAP dataset
            defaults to: http://cida.usgs.gov/thredds/dodsC/prism
        tmax_var: the name of the max temp variable
            defaults to 
        tmin_var: the name of the min temp variable
        prcp_var: the name of the prcp vaiable,
        tave_var: the name of the tave_var
            defaults to "Null"
        bioclims: A list of integers (1-19) of the bioclim vars to return
        start: The year to begin with
        end: The year to end with
        bbox_in:  The bounding box to use
                    four item tuple (max long, min lat, min long, max lat) 
    '''
    _validate_bioclim_inputs(outputfname, verbose=verbose, **kwargs)
    inputs = _parse_bioclim_inputs(**kwargs)
    output=_execute_request._executeRequest(processid, inputs, "name", verbose, outputfname)
    return output

    
def _validate_bioclim_inputs(outputfname, verbose, **kwargs):
    '''Checks that the arguments submitted to submitCustomBioclim are 
    reasonable
    '''
    # first check that the URI is a valid url
    # May want to have this try a few times to be safe, 
    # some datasets take a long time and can time out once or twice
    try:
        urllib2.urlopen(kwargs["OPeNDAP_URI"] + ".html")
    except:
        raise Exception("Invalid or unresponsive OPeNDAP_URI provided:  " + kwargs["OPeNDAP_URI"])
    
    #Check that the passed variable names exist
    datatypes = webdata_handle.getDataType(kwargs["OPeNDAP_URI"], verbose=verbose)
    for var in ['prcp_var', 'tmax_var', 'tmin_var']: #Note tave_var is not required, not checked here.
        if not kwargs[var] is None:
            if kwargs[var] not in datatypes:
                msg = "Specified '" + var + "' (" + kwargs[var] 
                msg += ") not a datatype in specified OPeNDAP_URI ("
                msg += kwargs["OPeNDAP_URI"] + ")"
                msg += "\n existing variables:"
                msg += "\t" + ", ".join(datatypes[:(min(10, len(datatypes)))])
                raise Exception(msg)        
    
    #Check that the start and end times will work
    timerange = webdata_handle.getTimeRange(kwargs["OPeNDAP_URI"], 
                                  varID=kwargs["prcp_var"], verbose=verbose)
    uri_start = dateutil.parser.parse(timerange[0]).replace(tzinfo=None)
    uri_end = dateutil.parser.parse(timerange[1]).replace(tzinfo=None)
    arg_start = datetime.datetime(int(kwargs['start']), 1, 1)
    arg_end = datetime.datetime(int(kwargs['end']), 1, 1)
    if not uri_start <= arg_start <= uri_end:
        msg = "Specified start " + str(kwargs['start']) + " not between the "
        msg += "start and end dates of the OPeNDAP_URI dataset\n\t"
        msg += str(uri_start) + " !<= " + str(arg_start) + " !<= " + str(uri_end)
        raise Exception(msg) 
    if not uri_start <= arg_end <= uri_end:
        msg = "Specified end " + str(kwargs['end']) + " not between the "
        msg += "start and end dates of the OPeNDAP_URI dataset\n\t"
        msg += str(uri_start) + " !<= " + str(arg_end) + " !<= " + str(uri_end)
        raise Exception(msg) 
    
    #check that the folder of the output dataset exists and the output zip does not
    if not os.path.exists(os.path.split(outputfname)[0]):
        raise Exception("Folder of output file does not exist:\n " 
                    + os.path.split(outputfname)[0])
    if os.path.exists(outputfname):
        try:
            os.remove(outputfname)
        except:
            raise Exception("Could not delete existing output file:\n " 
                    + os.path.split(outputfname))
    
    #check that the bioclims are legit
    for bioclim in kwargs['bioclims']:
        if (not str(bioclim).isdigit() or bioclim < 1 or bioclim > 19):
            raise Exception ("The bioclim specified (" + str(bioclim) + ") is not between 1 and 19 inclusive" )
    
def _parse_bioclim_inputs(**kwargs):
    '''return an inputs list formated like _executeRequest needs
    Allows the submitCustomBioclim function to accept parameters in a
    more pythonic format None object instead of the string "NULL",
    lists and integers instead of their string equivelent, etc
    '''
    inputs = []
    for var in ["start", "end", "OPeNDAP_URI"]:
        inputs.append((var,str(kwargs[var])))
        
    for var in ["tmax_var", "tmin_var", "prcp_var", "tave_var"]:
        if kwargs[var] is None:
            inputs.append((var, "NULL"))
        else:
            inputs.append((var,str(kwargs[var])))
        
    inputs.append(("bbox_in", ",".join([str(i) for i in kwargs['bbox_in']]))) 
    inputs.append(("bioclims", ",".join([str(i) for i in kwargs['bioclims']])))
    return inputs
