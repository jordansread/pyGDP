Feature: Feature Weighted Grid Statistics
	In order to thorougly test pyGDPs "bread and butter"
	As the kind of person that would describe a feature as "bread and butter"
	We will make a series of requests through pyGP

	Scenario: Submit basic FWGS
		Given I have defined my CONUS shapefile to be Wisconsin
		And I will be using "ppt" in my favorite "prism" dataset
		And I have even defined my own start and stop times
		When I submit my FWGS
		Then I should get the basic output that I expect

	Scenario: Submit multi-stat variable FWGS
		Given I have defined my CONUS shapefile to be Wisconsin
		And I will be using "ppt" and "tmx" in my favorite "prism" datatset
		And I have even defined my own start and stop times
		And I will be searching for the "MEAN" and "STD_DEV" statistics
		When I submit my multi-stat FWGS
		Then I should get the multi-stat output that I expect

	Scenario: Submit multi-stat variable FWGS Fully Named
		Given I have defined my CONUS shapefile to be Wisconsin
		And I will be using "ppt" and "tmx" in my favorite "prism" datatset
		And I have even defined my own start and stop times
		And I will be searching for the "MEAN" and "STD_DEV" statistics
		When I fill out every variable and submit my FWGS call
		Then I should get the multi-stat output that I expect

	@not_working
	Scenario: Submit FWGS without time
		Given I will be using a HUC 8 Shapefile
		And I will be searching in a Landcover Dataset
		And I will be searching for the "MEAN" and "STD_DEV" statistics
		When I submit my FWGS without a time variable
		Then I should get a timeless output that I expect

	@not_working
	Scenario: Submit FWGS with Arc Shapefile
		Given I have already uploaded the shapefile I want to sceincebase
		And I will be using "ppt" in my favorite "prism" dataset
		And I have even defined my own start and stop times
		When I submit my timestamped FWGS
		Then I should get a custom output that I expect