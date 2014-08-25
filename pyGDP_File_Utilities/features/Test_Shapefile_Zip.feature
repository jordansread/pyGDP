Feature: Zipping up shapefiles
	In order to make sure all the parts of a shapefile zip correctly
	As a person who tends to break everything unintentionally
	We will make sure that those files get zipped

	Scenario: Zipping the files
		Given I have a test shapefile and all its associated components
		When I run the shapeToZip function
		Then I am returned a pyGDP viable output