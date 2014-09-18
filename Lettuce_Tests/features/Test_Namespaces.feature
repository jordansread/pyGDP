Feature: Namespace Conformation
	In order to validate all of my pyGDP Namespace Variables
	As a person with the power of the internet at thier disposal
	We will check to make sure all of the namespaces are up

	Scenario: Checking the sever status
	Given I have all my namespaces defined in pyGDP
	And that each namespace points to a working URL or part of an XML
	When I check the http response from each url
	Then I get a working response for each one