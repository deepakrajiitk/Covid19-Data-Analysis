#!/usr/bin/env python
# coding: utf-8

# ### This program find intersection districts of cowin, covid and nieghboring datasets

# #### importing libraries

# In[2]:


import pandas as pd
import numpy as np
import json
from fuzzywuzzy import process
from collections import OrderedDict
import bisect 


# #### importing datasets

# In[4]:


df = pd.read_csv("cowin_vaccine_data_districtwise.csv")
df.head()


# In[5]:


df2 = pd.read_csv("districts.csv")
df2.head()


# In[6]:


districts1 = df2['District'].dropna().values
districts1 = set(districts1)
len(districts1)


# In[7]:


cowin_districts = df['District'].dropna().values
# converting to set to remove duplicates
cowin_districts = set(cowin_districts)
# print(cowin_districts)
print(len(cowin_districts))


# In[8]:


districts_to_avoid=['Chengalpattu', 'Gaurela Pendra Marwahi', 'Nicobars', 'North and Middle Andaman', 'Saraikela-Kharsawan', 'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']
for i in districts_to_avoid:
    cowin_districts.remove(i)
print(len(cowin_districts))


# In[9]:


# intersection of districts from districts.csv and from cowin database
len(cowin_districts.intersection(districts1))


# #### importing file we obtained in first part

# In[12]:


f = open('cowin_district_intersection.json')
data = json.load(f)
neighbors_districts = {key for key in data}
# print(neighbors_districts)
print(len(neighbors_districts))


# In[13]:


states = df[['State_Code', 'State']]
states = states.dropna().drop_duplicates()
states


# #### creating a dictionary that maps state name to its code. Saving this as a file because it will be used in coming questions

# In[17]:


state_dict={}
for index, row in states.iterrows():
    state_dict[row['State']]=row['State_Code']
print(state_dict)
with open("state_code_mapping.json", "w") as outfile:
    json.dump(state_dict, outfile, indent = 4)


# In[18]:


df3 = df2[['State','District']]
df3=df3.drop_duplicates()
df3
districts=set()
for index, row in df3.iterrows():
    districts.add(state_dict[row['State']]+"_"+row['District'])
# print(districts)
print(len(districts))


# #### finding common districts between neighbors dataset and districts.csv dataset

# In[20]:


neighbors_districts-districts


# In[21]:


districts-neighbors_districts


# #### Hadling those States which is not divided into districts in covid district dataset

# In[23]:


def check_district(district):
    state_code=district[0:2]
    if state_code=='TG':
        return 'TG_Telangana'
    elif state_code == 'SK':
        return 'SK_Sikkim'
    elif state_code == 'AS':
        return 'AS_Assam'
    elif state_code == 'DL':
        return 'DL_Delhi'
    elif state_code == 'GA':
        return "GA_Goa"
    elif state_code == 'MN':
        return "MN_Manipur"
    else:
        return district


# In[24]:


d={check_district(i):[] for i in neighbors_districts}
for district in neighbors_districts:
    key=check_district(district)
    for neighbor in data[district]:
        temp = check_district(neighbor)
        if temp not in d[key]:
            bisect.insort(d[key],temp)
d = OrderedDict(sorted(d.items()))
d


# In[25]:


d1 = {key for key in d}
d2 = districts
d1-d2


# In[26]:


d2-d1


# #### Creating json which is the intersection of all three datasets- covid, cowin and neighbors districts dataset

# In[27]:


with open("neighbor-districts-modified.json", "w") as file:
    json.dump(d, file, indent=4)

