import pyGDP

"""
This simple client script demonstrates the basic workflow of the Geo Data Portal in python. 

Shapefile upload has not been implemented here.

The CSW Client is very rudimentary, copy and paste of the "dods" url is required.

The client requests only the first time step of a dataset to minimize processing overhead of the demonstration.

"""

def getInput(listInput):
    
    for i in listInput:
        print i
    
    print '\n' + 'Choose from the list above (hit ENTER for a default):'
    usrinput = str(raw_input())

    if usrinput == "":
        usrinput = "sample:CONUS_states"
        print usrinput
    else:
        while usrinput not in listInput:
            print 'not a valid input'
            usrinput = str(raw_input())
    return usrinput

def getInput_1(listInput):
    
    for i in listInput:
        print i
    
    print '\n' + 'Choose from the list above (hit ENTER for a default):'
    usrinput = str(raw_input())

    if usrinput == "":
        usrinput = "STATE"
        print usrinput
    else:
        while usrinput not in listInput:
            print 'not a valid input'
            usrinput = str(raw_input())
    return usrinput

def getInput_2(listInput):

    for i in listInput:
        print i

    print '\n' + 'Choose from the list above or use "++" to choose all (hit ENTER for a default):'
    usrinput = str(raw_input())

    if usrinput == "":
        usrinput = "Wisconsin"
        print usrinput
    else:
        while usrinput not in listInput:
            if usrinput =='++':
                print "All values selected"
                return listInput
                break
            print 'Not a valid input, please try again.'
            usrinput = str(raw_input())
        print usrinput
    return usrinput

def getInput_3(listInput):

    for i in listInput:
        print i

    print '\n' + 'Choose an OPeNDAP url from the list above (hit ENTER for a default):'
    usrinput = str(raw_input())
    if usrinput == "":
        usrinput = "dods://cida.usgs.gov/thredds/dodsC/UofIMETDATA"
        print usrinput
    else:
        while 'dods' not in usrinput:
            print "This doesn't appear to be a valid dods url. Please enter an OPeNDAP url."
            usrinput = str(raw_input())
    return usrinput

def getInput_4():

    print 'Enter a search term or press ENTER to return all datasets in catalog.'
    usrinput = str(raw_input())
    return usrinput

def getInput_5(listInput):
    
    for i in listInput:
        print i
    
    print '\n' + 'Choose from the list above (hit ENTER for a default):'
    usrinput = str(raw_input())

    if usrinput == "":
        usrinput = "surface_downwelling_shortwave_flux_in_air"
        print usrinput
    else:
        while usrinput not in listInput:
            print 'not a valid input'
            usrinput = str(raw_input())
    return usrinput


def main():

    #This instantiates a pyGDP web processing object. All other processes are done through the web processing
    #object.
    gdp = pyGDP.pyGDPwebProcessing()

    #Returns a list of shapefiles that are currently sitting on the GDP server.
    #It's possible to upload your own shapefile using the .uploadShapefile function.
    sfiles = gdp.getShapefiles()
    for s in sfiles:
        print s
    shapefile = getInput(sfiles)
    
    print
    print 'Get Attributes:'
    #Gets shapefile dbf attributes of the file you chose from the previous selection process.
    #A good example of levels of detail processed by on GDP.
    attributes = gdp.getAttributes(shapefile)
    attribute = getInput_1(attributes)
	
    print
    print 'Get values:'
    #Yet another level of detail down on the shapefile. This time it is values of an attribute or shapefile.
    #Does all the web processing necessary to show the user what they are working with.
    values = gdp.getValues(shapefile, attribute)    
    value = getInput_2(values)

    print
    #Allows the user to select a dods dataset for processing. The getDataSetURI function returns a lot of
    #metadata making it helpful to narrow down the search with anyText.
    searchString = getInput_4()
    datasetURIs = gdp.getDataSetURI(anyText=searchString)
    dataSetURI = getInput_3(datasetURIs)
    
    print 
    print 'Getting available dataTypes... \n'
    #Gives a list of the available data types within the dods dataset for processing.
    dataTypes = gdp.getDataType(dataSetURI)
    dataType = getInput_5(dataTypes)
    
    print 
    print 'Getting time range from dataset...'
    #This example only uses the first time range (see submitFeatureWeightedGridStatistics execution)
    timeRange = gdp.getTimeRange(dataSetURI, dataType)
    for i in timeRange:
        print i
    
    print
    print 'Submitting request...'
    #Time for some heavy web services processing. The submitFeatureWeightedGridStaistics is the end product of
    #all the variable choosing we have done up until this point. It takes a lot of inputs and sends them all
    #through a remote processing algorithm associated with GDP. The result is a file downloaded to the location
    #of the executing script, also returned is the URL associated with the download (it usually gives a csv file).
    output = gdp.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeRange[0], timeRange[0], attribute, value, verbose=True)
    print
    print output
    print

    print "The resulting ouput file (which should now exist in the folder where this example was executed) holds the", \
        "Feature Weighted Grid Statistics (just the mean value if you did the default options) of the area chose from the", \
        "the 'value' shapefile (from GDP). \nFor more details refer to comments in the main method of this example script."
    
if __name__=="__main__":
    main()
