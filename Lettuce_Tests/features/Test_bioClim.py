import pyGDP
from pyGDP_Submit_Feature import bioclim
from lettuce import *
from nose.tools import assert_equal
import os

@step(r'a bunch of inputs for prism')
def bioclim_constants(step):
    world.start = "1950"
    world.end = "1951"
    world.bbox_in=[-87,41,-89,43]
    world.bioclims=[1,2,3,4,5,6,7]
    world.OPeNDAP_URI="http://cida.usgs.gov/thredds/dodsC/prism"
    world.tmax_var  = "tmx"
    world.tmin_var = "tmn"
    world.prcp_var = "ppt"
    world.tave_var = "NULL"
    world.output="./test_bioclim.zip"
    

@step(r'I execute the bioclim algorithm')
def run_bioclim(step):
    world.outputfname=bioclim.submitCustomBioclim(outputfname=world.output, 
        OPeNDAP_URI=world.OPeNDAP_URI, 
        start=world.start, 
        end=world.end,
        bbox_in=world.bbox_in,
        bioclims=world.bioclims,
        tmax_var=world.tmax_var,
        tmin_var=world.tmin_var,
        prcp_var=world.prcp_var,
        tave_var=world.tave_var,
        verbose=False
        )
        
@step(r'I want to make sure the file is what I expect from before')
def check_file_size(step):
    assert_equal(os.path.getsize(world.outputfname), 69776)