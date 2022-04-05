# Covid19 Data Analysis
## About This Project
The pandemic has already taken grip over peoples’ life. Since the start of the pandemic, India is facing problem of ever-increasing cases.Through the data analysis of cases one  can  analyse  how  states/districts  all  over  the  country are  doing  in  terms  of  controlling  the pandemic. Analysing data leads to adapt the prevention model of the states/districts that are doing great in  terms of  lowering the  graph.
The aim of the  project  is  to  provide data analysis of covid-19  (a pandemic started in December 2019) in India. Through plotting of data, various cases have been studied like most affected state/district due to this pandemic. Study of data from various states/districts is combined to show the growth of cases and recovery graph.

## Libraries required
- [Numpy] - For performing arithmetic operations
- [Pandas] - For Datasets handling
- [Matplotlib] - For plotting graphs and visualizations
- [itertools] - used to iterate over data structures
- [fuzzywuzzy] - used for matching strings
- [datetime] - used to work with dates and times

## Code Files
| File Name | Description |
| ------ | ------ |
|Question1.ipynb|preprocess and merge datasets to calculate needed measures and prepare them for an Analysis.|
|Question2.ipynb|construct an undirected graph of districts|
|Question3.ipynb| For every district i, it finds the number of cases from the Covid-19 portal.|
|Question4.ipynb|for every district, state and overall, find the week and month having peak (highest) number of active cases for wave-1 and wave-2.|
|Question5.ipynb|find the number of people vaccinated with 1 or 2 doses of any vaccine, and sort the output file with district id and state id|
|Question6.ipynb|find the number of people vaccinated with 1 or 2 doses of any vaccine, and sort the output file with district id and state id.| |Question6.ipynb|for each state, district and overall, it finds the following ratios: total number of females vaccinated (either 1 or 2 doses) to total number of males vaccinated (same). For that district/state/country, it finds the ratio of population of females to males. At last it finds the ratio of the two ratios, i.e., vaccination ratio to population ratio|
|Question7.ipynb| For each state, district and overall, it finds the following ratios: total number of Covishield vaccinated persons (either 1 or 2 doses) to total number of Covaxin vaccinated persons(same).|
|Question8.ipynb| for each state, district and overall, it finds the following ratio: total number of persons vaccinated (both 1 and 2 doses) to total population.|
|Question9.ipynb|for every state, find the date on which the entire population will get at least one does of vaccination.|

Note:  If a district is absent in 2011 census, we have dropped it from analysis.

.sh files are also provided in each folder.

[Numpy]: <https://numpy.org/>
[Pandas]: <https://pandas.pydata.org/>
[Matplotlib]: <https://matplotlib.org/>
[itertools]: <https://docs.python.org/3/library/itertools.html/>
[fuzzywuzzy]: <https://pypi.org/project/fuzzywuzzy/>
[datetime]: <https://docs.python.org/3/library/datetime.html/>
