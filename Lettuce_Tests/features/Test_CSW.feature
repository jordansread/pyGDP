Feature: Get Dataset URI from Catalogue Web Service
	In order to make sure the CSW calls are working
	As savvy pyGDP users
	We will make a search for datasets
	
	Scenario: Search for "prism" data
		Given I define the keyword as "prism"
		When I invoke the pyGDP.getDataSetURI method
		Then I see the metadata and URIs of "prism" datasets

	Scenario: Search for all datasets
		Given I am not defining any keywords
		When I invoke the pyGDP.getDataSetURI method
		Then I see anywhere between 1 and 1000 datasets