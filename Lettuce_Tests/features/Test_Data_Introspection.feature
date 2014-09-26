Feature: Test Data Introspection
	In order to make sure pyGDP is able to look at metadata in CSW datasets
	As a person who really likes the "prism" data
	We will run through  some pyGDP introspection commands

	Scenario: Looking for "ppt" in dataset parameters.
		Given I am pointing to a test "prism" dataset with my URI
		When I retrieve the metadata using the getDataType method
		Then I find that "ppt" is in the big confusing xml that I get back
		Then I know that the GDP data looks good from both ends
		
	Scenario: I made a mistake
		Given a bad OPeNDAP url
		Then I get the error I expect