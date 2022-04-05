#!/usr/bin/env python
# coding: utf-8

# ## This file is used to find common districts between covid dataset and cowin dataset

# #### Importing libraries

# In[22]:


import pandas as pd
import numpy as np
import json
from fuzzywuzzy import process
from collections import OrderedDict
import bisect 


# #### Importing dataset

# In[23]:


df = pd.read_csv("cowin_vaccine_data_districtwise.csv")
df.head()


# In[24]:


df2 = pd.read_csv("districts.csv")
df2.head()


# #### finding no of unique districts in 'districts.csv' dataset

# In[25]:


districts1 = df2['District'].dropna().values
districts1 = set(districts1)
len(districts1)


# #### finding no of unique districts in 'cowin' dataset

# In[26]:


cowin_districts = df['District'].dropna().values
# converting to set to remove duplicates
cowin_districts = set(cowin_districts)
# print(cowin_districts)
print(len(cowin_districts))


# #### dropping irrelevant rows or columns

# In[27]:


districts_to_avoid=['Chengalpattu', 'Gaurela Pendra Marwahi', 'Nicobars', 'North and Middle Andaman', 'Saraikela-Kharsawan', 'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']
for i in districts_to_avoid:
    cowin_districts.remove(i)
print(len(cowin_districts))


# In[28]:


# intersection of districts from districts.csv and from cowin database
len(cowin_districts.intersection(districts1))


# #### importing modified neighbor file

# In[29]:


f = open('neighbors_modified.json')
data = json.load(f)
neighbors_districts = {key for key in data}
# print(neighbors_districts)
print(len(neighbors_districts))


# #### finding common districts and uncommon districts in cowin and ditricts database

# In[30]:


matching_dict = {}
unmatched_districts=set()
rem_cowin_districts = cowin_districts.copy()
for district in neighbors_districts:
    if district in cowin_districts:
        matching_dict[district]=district
        rem_cowin_districts.remove(district)
    else:
        unmatched_districts.add(district)
# print(matching_dict)
print("total matched districts are",len(matching_dict))
print('toal unmatched districts are',len(unmatched_districts))


# #### for every unmatched district in cowin dataset, finding its closest district in 'district' dataset using fuzzywuzzy

# In[31]:


similar=[]
for district in unmatched_districts:
    temp = process.extractOne(district,rem_cowin_districts)
    similar.append([district,temp[0]])
print(len(similar))
similar


# #### manually found districts for which fuzzywuzzy process gave wrong result

# In[32]:


dissimilar_districts = [['Ysr', 'Balasore'],
 ['Jyotiba Phule Nagar', 'S.A.S. Nagar'],
 ['Pashchim Champaran', 'East Champaran'],
 ['Mumbai Suburban', 'Mumbai'],
 ['Sri Potti Sriramulu Nellore', 'Sri Muktsar Sahib'],
 ['Purbi Singhbhum', 'West Singhbhum'],
 ['Sant Ravidas Nagar', 'S.A.S. Nagar'],
 ['Seraikela Kharsawan', 'Maharajganj'],
 ['Baleshwar', 'Ballari'],
 ['Hugli', 'Lahaul and Spiti'],
 ['Palghat', 'Parbhani'],
 ['Mumbai City', 'Mumbai'],
 ['Bid', 'Karbi Anglong'],]


# #### removing all wrong predicted districts from 'similar' set

# In[33]:


for district in dissimilar_districts:
    if district in similar:
        similar.remove(district)
    else:
        print(district)
print("found correct district names using fuzzywuzzy of total "+str(len(similar))+" districts")


# #### manually corrected some districts name

# In[34]:


# not found mumbai suburban, mumbai city and narsimhapur
correct_districts = [
['Seraikela Kharsawan', 'Saraikela-Kharsawan'],
['Pashchim Champaran', 'West Champaran'],
['Hugli', 'Hooghly'],
['Sri Potti Sriramulu Nellore', 'S.P.S. Nellore'],
['Purbi Singhbhum', 'East Singhbhum'],
['Palghat', 'Palakkad'],
['Ysr', 'Y.S.R. Kadapa'],
['Baleshwar', 'Balasore'],
['Bid', 'Beed'],
['Sant Ravidas Nagar', 'Bhadohi'],
['Jyotiba Phule Nagar', 'Amroha']]


# In[35]:


for district in correct_districts:
    if district not in similar:
        similar.append(district)
print(len(similar))
# similar


# In[36]:


# finally adding similar districts to our matching district dictionary
for item in similar:
    matching_dict[item[0]]=item[1]
# print(matching_dict)
print(len(matching_dict))
print("out of "+str(len(neighbors_districts))+" districts in neigbors_district, total "+str(len(matching_dict))+" districts matching found in cowin database")


# In[37]:


for key in matching_dict:
    temp = df.loc[df['District'] == matching_dict[key], 'District_Key']
    if(len(temp)==0):
        print("district not found in cowin database",matching_dict[key])
    else:
        matching_dict[key]=[matching_dict[key], temp.iloc[0]]
matching_dict


# #### getting all neighbors of matching districts

# In[38]:


f = open("neighbors_modified.json")
districts_json = json.load(f)
final_dict = {}
for district in districts_json:
    if district in matching_dict:
        key = matching_dict[district][1]
        values = []
        for neighbor in districts_json[district]:
            if neighbor in matching_dict:
                bisect.insort(values,matching_dict[neighbor][1])
            else:
                print("district not found",neighbor)
        final_dict[key]=values
    else:
        print("district not found",district)
final_dict


# #### adding some more districts which were corrected manually

# In[39]:


f1 = open("duplicate_districts.json")
duplicate_districts = json.load(f1)
for district in duplicate_districts:
    final_dict[district] = duplicate_districts[district]
for district in duplicate_districts:
    for value in duplicate_districts[district]:
        if district not in final_dict[value]:
            bisect.insort(final_dict[value],district)


# In[40]:


print("Total districts in final neighbor district file are",len(final_dict))


# In[42]:


final_dict = OrderedDict(sorted(final_dict.items()))
with open("cowin_district_intersection.json", "w") as file:
    json.dump(final_dict, file, indent=4)

