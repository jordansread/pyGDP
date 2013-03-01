# Reminders for how to do tasks

default:
	@echo "    pyGDP shortcuts"
	@echo
	@echo "  build - Nothing to build for this project"
	@echo "  clean - Remove pyc files and dist directory"
	@echo "  develop - Setup for development of pyGDP"
	@echo "  sdist - Create tar.bz2 and zip in dist/"
	@echo "  test - run the unit tests"
	@echo "  virtualenv - Start you down the path to an isolated virtual environment"
	@echo
	@echo "Admin only:"
	@echo "  pypi - ONLY RUN THIS IF YOU ARE THE LEAD AUTHOR MAKING A RELEASE"

build:
	python setup.py build

clean:
	rm -f *.pyc
	rm -rf dist build

develop:
	python setup.py develop

sdist:
	python setup.py sdist --formats=bztar,zip

test:
	python setup.py test

virtualenv:
	virtualenv gdp_ve
	@echo "Please run the following:"
	@echo "source gdp_ve/bin/activate # for bash users"
	@echo "pip install gdp"

########################################
# For the package maintainer only!

# Tell http://pypi.python.org about a new release
pypi:
	python setup.py register
	python setup.py sdist --formats=bztar,zip upload
