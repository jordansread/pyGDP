Feature: Execute BioClim
	In order to test pyGDP's ability to execute the bioClim algorithm
	As someone needing bioClim indices
	We will run some bioClim related scenarios
		
	Scenario: A simple complete bioClim run
		Given a bunch of inputs for prism
		When I execute the bioclim algorithm
		Then I want to make sure the file is what I expect from before