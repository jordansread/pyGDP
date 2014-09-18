Feature: Feature Categorical Grid Coverage
	In order to test pyGDPs main functionality against a test dataset
	As a person who is worried about eveything falling apart
	We will set up and run a FCGC call
	
	@not_working
	Scenario: Running a sample in Rhode Island
		Given I already know how to get my shapefile boundary from GDP
		Given I can call a working dataset from GDP
		When I make a Feature Categorical Grid Coverage call
		Then I can see the returned file is exactly what I would expect