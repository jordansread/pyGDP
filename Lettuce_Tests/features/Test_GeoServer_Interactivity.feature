Feature: GeoServer Interactivity
	In order to test pyGDP's ability to communicate with GeoServer
	As someone who is doing a lot of stuff "under the hood"
	We will run through all the GeoSever call scenarios

	Scenario: Get Shapefile List
		Given I know there are shapefiles on our GeoServer
		When I use the getShapefiles method and I get a list of those files
		Then I get a non-zero response
	
	Scenario: Get List of Shapefile Attributes
		Given I already know a shapefile (sample:CONUS_states) that has attributes and values
		When I use the getAttributes method and I get a list of those attributes
		Then I should see an expected number of attributes

	Scenario: Get List of Shapefile Values
		Given I already know a shapefile (sample:CONUS_states) that has attributes and values 
		And I know that one of those attributes is "STATE"
		When I ask for a list of values in the STATE
		Then I should see the number of states
	
	Scenario: Get Single Feature Collection GeoType
		Given I already know a shapefile (sample:CONUS_states) that has attributes
		And I know that one of those attributes is "STATE"
		And I know that one of those states is "Wisconsin"
		When I ask for the Feature Collection GeoType of Wisconsin in CONUS
		Then I am given a single expected output from the Feature Collection

	@not_working
	Scenario: Get All Feature Collection GeoTypes
		Given I already know a shapefile (sample:CONUS_states) that has attributes
		And I know that one of those attributes is "STATE"
		When I ask for the Feature Collection GeoType of all the states in CONUS
		Then I am given multiple expected outputs from Feature Collection