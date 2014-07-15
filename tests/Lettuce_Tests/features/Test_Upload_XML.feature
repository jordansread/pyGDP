Feature: Upload shapefile via XML
	In order to make sure the xmlGenerator object is working
	As someone who doesn't want to actually upload an xml
	We will use local test datasets to make sure the right xml is made

	Scenario: Using the getUploadXMLtree method
		Given I have my GDP upload URLs
		And I have my own, pre-encoded, upload shapefile data
		When I use the xmlGen objects getUploadXMLtree method
		Then I see it makes the xml that will successfully upload that data