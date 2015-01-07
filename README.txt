pyGDP
=================

pyGDP provides a fast and efficient way of making calls to the USGS GeoData Portal.

pyGDP has the following algorithms: 
	- FeatureCategoricalGridCoverage
	- FeatureWeightedGridStatistics
	- FeatureCoverageOPenDap
	- FeatureCoverageWCSIntersection

Additional documentation can be found at the Geo Data Portal wiki. 
https://my.usgs.gov/confluence/pages/viewpage.action?pageId=250937417

Dependencies
=================

pyGDP request owslib and lxml.etree (which, in turn, uses libxml2 and libxslt)

Usage
=================

You can find example usages and scripts in the examples folder.

Installation
==================
1.) Use of virtualenv and pip is highly recommended. Sample commands to install pyGDP as a virtual env on a mac/unix operating system are given below. Similar commands can be used on windows. 

>> git clone https://github.com/USGS-CIDA/pyGDP.git
>> virtualenv -p /usr/bin/python2.7 pyGDP/venv
>> source pyGDP/venv/bin/activate
>> pip install -r pyGDP/requirements.txt
>> pip install -r pyGDP/testing-requirements.txt
>> cd pyGDP
>> python setup.py install
>> lettuce pyGDP/Lettuce_Tests/features/ --tag=-not_working

OR
2.) Install using pip (first install or --upgrade dependencies):

	pip install owslib --upgrade

	pip install lxml --upgrade

You can find libxml2 and libxlst with:
	
	pip install libxml2-python

You can install the pyGDP git master branch (with python v.3.0 or greater):
	
	pip install git+https://github.com/USGS-CIDA/pyGDP.git@v1.3.1#egg=pyGDP (for the lastest stable version)

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
