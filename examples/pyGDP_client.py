import pyGDP

def getInput(listInput):
    
    for i in listInput:
        print i
    
    print '\n' + 'Choose from the list above:'
    usrinput = str(raw_input())
    while usrinput not in listInput:
        print 'not a valid input'
        usrinput = str(raw_input())
    return usrinput

def getInput_2(listInput):

    for i in listInput:
        print i

    print '\n' + 'Choose from the list above or press enter to chose all:'
    usrinput = str(raw_input())
    while usrinput not in listInput:
        if usrinput =='':
            break
        print 'Not a valid input, please try again.'
        usrinput = str(raw_input())
    print usrinput
    return usrinput

def getInput_3(listInput):

    for i in listInput:
        print i

    print '\n' + 'Choose an OPeNDAP url from the list above:'
    usrinput = str(raw_input())
    while 'dods' not in userinput:
        print "This doesn't appear to be a valid dods url. Please enter an OPeNDAP url."
        usrinput = str(raw_input())
    return usrinput

def getInput_4():

    print 'Enter a search term or press enter to return all datasets in catalog.'
    usrinput = str(raw_input())
    return usrinput

def main():
    gdp = pyGDP.pyGDPwebProcessing()
    sfiles = gdp.getShapefiles()
    for s in sfiles:
        print s
    
    shapefile = getInput(sfiles)
    
    print
    print 'Get Attributes:'
    attributes = gdp.getAttributes(shapefile)
    attribute = getInput(attributes)
	
    print
    print 'Get values:'
    values = gdp.getValues(shapefile, attribute)    
    value = getInput_2(values)

    print
    print 'Enter a search term or press enter to return all datasets in catalog.'
    searchString = getInput_4()
    datasetURIs = gdp.getDataSetURI()
    dataSetURI = getInput(datasetURIs)
    
    print ''
    print 'Getting available dataTypes'
    dataTypes = gdp.getDataType(dataSetURI)
    dataType = getInput(dataTypes)
    
    print 
    print 'Getting time range from dataset'
    
    timeRange = gdp.getTimeRange(dataSetURI, dataType)
    for i in timeRange:
        print i
    
    print
    print 'Submitting request'
    output = gdp.submitFeatureWeightedGridStatistics(shapefile, dataSetURI, dataType, timeRange[0], timeRange[0], 'STATE', 'Wisconsin')
    print output
    
if __name__=="__main__":
    main()