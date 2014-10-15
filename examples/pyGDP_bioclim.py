"""
This example shows the basic usage of the submitCustomBioclim method of pyGDP.
"""
import os
import tempfile
tempdir = tempfile.gettempdir()
import pyGDP as _pyGDP
pyGDP = _pyGDP.pyGDPwebProcessing()
extent = [-80.0, 35.0, -81.0, 36.0]
temp_output1 = os.path.join(tempdir, "testout1.zip")
request1_args ={'OPeNDAP_URI': 'http://cida.usgs.gov/thredds/dodsC/new_gmo', 
                'end': 2009, 
                'prcp_var': 'pr', 
                'tave_var': 'tas', 
                'bbox_in': extent, 
                'start': 2009, 
                'tmax_var': 'tasmax', 
                'tmin_var': 'tasmin', 
                'bioclims': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
                'outputfname': temp_output1}
                
path=pyGDP.submitCustomBioclim(verbose=False, **request1_args)
print path 