Feature: Change URLs to pyGDP resources
	In order to test pyGDP's ability to communicate with GeoServer
	As someone who is doing a lot of stuff "under the hood"
	We will run through all the GeoSever call scenarios
		
	Scenario: Change wfs url the old way.
		Given I want to access shapefiles on some bogus server
		Then I want to make sure that bogus server is actually getting set