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

pyGDP request lxml.etree and owslib

Usage
=================

You can find example usages and scripts in the examples folder.

Installation
==================
In your pyGDP directory, run python setup.py install
This should install pyGDP onto your current Python version site-packages.

To install owslib, you can find installation here:
http://pypi.python.org/pypi/OWSLib/#downloads
Or install with pip
    pip install owslib
Or on their github page:
https://github.com/geopython/OWSLib

For lxml, window users can find unofficial window binaries of lxml
and other interesting packages here:
http://www.lfd.uci.edu/~gohlke/pythonlibs/ 

OWSlib and lxml are included in the Enthought Python Distribution (EPD).

For OSX users, you can installation instructions here:
http://lxml.de/installation.html
or use macports
or install with homebrew (http://brew.sh/) and pip:
    brew install libxml2
    pip install lxml


Support
=================
Contact jread@usgs.gov for questions, issues.

Thanks
=================
1. Dave Blodgett
2. Jordan I Walker
3. Jordan Read
