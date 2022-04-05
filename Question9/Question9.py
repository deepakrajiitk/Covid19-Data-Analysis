#!/usr/bin/env python
# coding: utf-8

# #### Importing libraries

# In[1]:


import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta


# #### Importing dataset

# In[3]:


# importing filtered dataset that we created in question6
census_data = pd.read_csv("filtered_census_data.csv")


# #### Dropping irrelevant columns

# In[4]:


census_data.drop(columns=['Total_Male_Population','Total_Female_Population'],inplace=True)
census_data


# In[5]:


vaccine_data = pd.read_csv("state-vaccinated-count-week.csv")
vaccine_data


# In[6]:


# using one of the output file of question no 8
state_vacine_dose_ratio = pd.read_csv("state-vaccinated-dose-ratio.csv")
state_vacine_dose_ratio


# #### finding no of doses administered in each district in last week

# In[7]:


last_week_vaccine_data = vaccine_data[vaccine_data['week']==31]
last_week_vaccine_data


# #### finding total population in each state

# In[8]:


census_state_data = census_data.groupby(['State']).sum().reset_index()
census_state_data.rename(columns={'State':'state'}, inplace=True)
census_state_data


# #### merging vaccination dataset and population dataset

# In[9]:


temp = pd.merge(state_vacine_dose_ratio, census_state_data, on=['state'])
merged_df = pd.merge(temp, last_week_vaccine_data, on=['state'])
merged_df.drop(columns=['vaccinateddose2ratio','dose2','week'], inplace=True)
merged_df


# #### finding no of people who are are not vaccinated even by first dose

# In[11]:


merged_df['rem_population'] = (merged_df['Total_Population'] - (merged_df['Total_Population']*merged_df['vaccinateddose1ratio'])).apply(np.floor)


# #### finding rate of vaccination

# In[10]:


merged_df['rate_of_vaccination'] = (merged_df['dose1']/merged_df['Total_Population'])*100


# #### findind date on which complete population of a state is expected to vaccinated at least by first dose

# In[12]:


merged_df['date'] = pd.to_datetime('2021-08-14') + pd.to_timedelta(((merged_df['Total_Population']/merged_df['dose1'])*7).apply(np.floor), unit = 'D')


# In[13]:


merged_df['rem_population'] = merged_df['rem_population'].astype('int')
merged_df


# #### creating csv file for result

# In[14]:


merged_df[['state','rem_population','rate_of_vaccination','date']].to_csv("complete-vaccination.csv", header=['stateid','populationleft','rateofvaccination','date'], index=False)

