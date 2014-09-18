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
    name = 'pyGDP',
    version = __version__,
    description = 'Interface to the USGS GeoData Portal',
    long_description = open('README.txt').read(),
    license='Public Domain',
    maintainer='Jordan Read',  # Originally Xao Yang
    maintainer_email='jread@usgs.gov',
    py_modules=['pyGDP','GDP_XML_Generator'],
    packages=find_packages(),
    install_requires=['setuptools'],
    url='https://github.com/USGS-CIDA/pyGDP',
    test_suite='tests',
)
