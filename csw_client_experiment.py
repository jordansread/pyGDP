from owslib.csw import CatalogueServiceWeb

def getDataSetURI(anyText='gmo',CSWURL='http://cida.usgs.gov/gdp/geonetwork/srv/en/csw',BBox=None):
		"""
		
		Searches a given CSW server and returns metadata content for the datasets found.
		
		Arguments
		---------
		
		- CSWURL - A base URL for the CSW server to be searched. (Optional, defaults to the CDIA/GDP CSW server.)
		- anyText - A string that will be submitted to the CSW search. (Optional, deafualt is empty which will return all records.)
		- BBox - A bounding box in WGS84 lat/lon that will be used to limit results to datasets that atleast partially intersect. (Optional)
		
		"""
		
		csw = CatalogueServiceWeb(CSWURL)
		csw.getrecords(keywords=[anyText], outputschema='http://www.isotc211.org/2005/gmd', esn='full')
		dataSetURIs = [['title','abstract',['urls']]]
		for rec in csw.records:
			title=csw.records[rec].identification.title
			abstract=csw.records[rec].identification.abstract
			urls=[]
			for onlineresource in range(len(csw.records[rec].distribution.online)):
					urls.append(csw.records[rec].distribution.online[onlineresource].url)
			# Should be another loop here that goes through all urls in the serviceidentification section of a metadata record as well.
			entry=[title,abstract,urls]
			dataSetURIs.append(entry)
		return dataSetURIs


dataseturis=getDataSetURI(anyText='gmo')
dataseturis
