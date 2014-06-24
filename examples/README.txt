pyGDP_client.py                                : Main example to showcase pyGDP workflow and pyGDP.webProcessingObject functions. Uses pyGDP's main 
                                                 tool the submitFeatureWeightedGrid statistics algorithm. (Note: this example is not how production
                                                 pyGDP should actually be implemented).

pyGDP_featureCategoricalGridCoverage.py        : A short example to request a file using the submitfeatureCategoricalGridCoverage algorithm.

pyGDP_featureCoverageOPenDAP_script.py         : A similarly short example making a request and downloading an example file using the 
						 submitFeatureCoverageOPenDAP algorithm.

pyGDP_featureCoverageWCSintersection_script.py : Another example of the submitFeatureCoverageWCSintersection function.

pyGDP_featureWeighted_multi_vars_stats.py      : Another example using the FWGS (FeatureWeightedGridStatistics algorithm) this time utilizing 
                                                 multiple data types and statistics.

pyGDP_featureWeighted_script_1.py              : An example of choosing datasets through pyGDP, then selecting a data type from that
                                                 dataset for FWGS calculations. Text listings of both the datasets and datatypes can be generated
                                                 with pyGDP to make things easier on the user.

pyGDP_featureWeighted_script_2.py              : An example using specific values of attributes from a shapefile that already exists on the GDP server.

pyGDP_featureWeighted_script_3.py              : An example of some of the other user-friendly listing that can be completed by pyGDP; including
                                                 values, data types, and time ranges; all of which eventually define the FWGS request.

pyGDP_featureWeighted_script_4.py              : An example showing a call being made without any listing or searching of FWGS variables.

pyGDP_featureWeighted_script_NTYD.py           : An example utilizing the uploadShapefile function to upload a test file to GDP before submitting
						 a request of FWGS using that file.

pyGDP_wicci_featureWeighted_example_script.py  : An example to show  how to search for a particular dataset and loop through a list of OPeNDAP 
						 resources associated with it.