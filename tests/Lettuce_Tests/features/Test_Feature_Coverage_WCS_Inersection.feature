Feature: Feature Coverage WCS Intersection
	In order to make sure our high order pyGDP functions are working
	As an extremely paranoid pyGDP user
	We are going to run a test on the submitFeatureCoverageWCSIntersection method
	
	@not_working
	Scenario: Submit Feature Coverage WCS Intersection
		Given I know my HUC_8 value (Hydrologic Unit Code for a subbasin shapefile)
		And I know what dataset I want to use (because this is a very realistic test)
		When I run that crazy WCS insersection function
		Then I see exactly the file that I expected (by running it before)