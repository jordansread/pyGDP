pyGDP
=================

pyGDP provides a fast and efficient way of making calls to the USGS GeoData Portal.

pyGDP has the following algorithms: 
	- FeatureCategoricalGridCoverage
	- FeatureWeightedGridStatistics
	- FeatureCoverageOPenDap
	- FeatureCoverageWCSIntersection

Dependencies
=================

pyGDP request owslib and lxml.etree (which, in turn, uses libxml2 and libxslt)

Usage
=================

You can find example usages and scripts in the examples folder.

Installation
==================
1.) Install after cloning the appropriate git:

In your pyGDP-Master directory, run python:

setup.py install

This should install pyGDP into your current Python version site-packages.

Find owslib at https://github.com/geopython/OWSLib

Find lxml at https://github.com/lxml/lxml

OR
2.) Install using pip (first install or --update dependencies):

	pip install owslib --update

	pip install lxml --update

You can find libxml2 and libxlst with:
	
	pip install libxml2-python

You can install the pyGDP git master branch (with python v.3.0 or greater):
	
	pip install git+https://github.com/USGS-CIDA/pyGDP.git@424bdc2d5d#egg=pyGDP (for the recommended commit as of 7/8/2014)

	pip install git+https://github.com/USGS-CIDA/pyGDP.git@master (for the, possibly unstable, current commit)

(reference http://codeinthehole.com/writing/using-pip-and-requirementstxt-to-install-from-the-head-of-a-github-branch/)

OR
3.) Install using Enthought Canopy:

Find and install the lxml and owslib though Package Manager

(Recommended you set Canopy as your default python environment)
Install pyGDP as in 1.)


Having trouble compiling?

Windows users can find the unofficial windows binaries of lxml, owslib, and lots of other packages at:

http://www.lfd.uci.edu/~gohlke/pythonlibs/ 

For OSX users, you can find installation instructions here:

http://lxml.de/installation.html

OR use macports

OR install with homebrew (http://brew.sh/) and pip:

    brew install libxml2

    pip install lxml


Support
=================
Contact gdp@usgs.gov for questions, issues.

Thanks
=================
1. Dave Blodgett
2. Jordan I Walker
3. Jordan Read
4. Steve Kochaver
