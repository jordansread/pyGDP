Feature: Feature Coverage OPenDAP
	In order to test the higher functions of pyGDP
	As a climatologist in Alabama
	We will run through some climate data in Alabama!

	Scenario: Submit Feature Coverage OPenDAP
		Given I already have my boundary shapefile call from GDP
		And I have set up my precipitaion data call from GDP
		When I run submitFeatureCoverageOPenDAP in pyGDP
		Then I know my output is something I expect
	