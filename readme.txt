Question1:
- most of the work in this is done manually
- there are two python programs in this which find the intersection ditricts of covid, cowin and neighbors-district dataset
- Libraries required:
	- pandas
	- numpy
	- json
	- fuzzywuzzy
	- bisect
	- collections

- Dataset required:
	- cowin_vaccine_data_districtwise.csv
	- districts.csv
	- duplicate_districts.json
	- neighbors_modified.json

Question 2:
- run edge-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json
	csv

Datasets required:
	neighbor-districts-modified

Question 3:
- run case-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json 
	itertools

Datasets required:
	neighbor-districts-modified.json
	state-code-mapping.json
	districts.csv

Question 4:
- run peaks-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json 
	itertools

Datasets required:
	neighbor-districts-modified.json
	state-code-mapping.json

Question 5:
- run vaccinated-count-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json 
	datetime
	itertools

Datasets required:
	cowin_vaccine_data_districtwise.csv

Question 6:
- run vaccination-population-ratio-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json 
	datetime
	itertools

Datasets required:
	cowin_vaccine_data_districtwise.csv
	DDW_PCA0000_2011_Indiastatedist.csv

Question 7:
- run vaccine-type-ratio-generator.sh file to generate all the required files
- Libraries required:
	pandas
	json 
	datetime
	itertools

Datasets required:
	cowin_vaccine_data_districtwise.csv

Question 8:
- run vaccinated-ratio-generator.sh file to generate all the required files
	pandas

Datasets required:
	filtered_census_data.csv
	vaccination_data_dose_wise.csv

Question 9:
- run complete-vaccination-generator.sh file to generate all the required files
- Libraries required:
	pandas
	numpy
	datetime
	maths
	
Datasets required:
	filtered_census_data.csv
	state-vaccinated-dose-ratio
	state-vaccinated-count-week




