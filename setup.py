import ast
import sys
from pyGDP import __version__

try:
    from setuptools import setup
except:
    sys.exit('Requires distribute or setuptools')

from setuptools import find_packages

# TODO: include the examples in the sdist
setup(
    name = 'gdp',
    version = __version__,
    description = 'Interface to the USGS GeoData Portal',
    long_description = open('README.txt').read(),
    license='Public Domain',  # Authors are US Govt, so this should be okay.
    maintainer='Jordan Read',  # Originally Xao Yang
    maintainer_email='jread@usgs.gov',
    packages=find_packages(),
    install_requires=['setuptools'],
    url='https://github.com/USGS-CIDA/pyGDP',
    test_suite='tests',
)
