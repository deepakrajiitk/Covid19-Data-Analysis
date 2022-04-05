#!/usr/bin/env python
# coding: utf-8

# #### Importing Libraries

# In[1]:


import pandas as pd


# #### Importing Dataset

# In[4]:


# importing filtered dataset we created in question 6
census_data = pd.read_csv("filtered_census_data.csv")


# #### droppin irrelevant columns

# In[5]:


census_data.drop(columns=['Total_Male_Population','Total_Female_Population'],inplace=True)
census_data


# In[6]:


vaccine_data = pd.read_csv("vaccination_data_dose_wise.csv")


# In[7]:


vaccine_data


# ### Merging vaccination dataset and population dataset

# In[8]:


merged_df = pd.merge(vaccine_data, census_data, on=['District','State'])


# In[9]:


merged_df


# In[10]:


merged_df['dose1'] = merged_df['dose1'].astype('float')
merged_df['dose2'] = merged_df['dose2'].astype('float')
merged_df['Total_Population'] = merged_df['Total_Population'].astype('float')
merged_df


# #### Findig required ratio for each district

# In[11]:


df_district = merged_df.groupby('District_Key').agg({'State':'first','dose1':'sum', 'dose2':'sum','Total_Population':'first'}).reset_index()


# In[12]:


df_district['ratio1'] = df_district['dose1']/df_district['Total_Population']
df_district['ratio2'] = df_district['dose2']/df_district['Total_Population']
df_district.sort_values(['ratio1'],inplace=True)
df_district


# #### Finding required ratio for each state

# In[13]:


df_state = df_district.groupby('State').agg({'dose1':'sum', 'dose2':'sum','Total_Population':'sum'}).reset_index()


# In[14]:


df_state['ratio1'] = df_state['dose1']/df_state['Total_Population']
df_state['ratio2'] = df_state['dose2']/df_state['Total_Population']
df_state.sort_values(['ratio1'],inplace=True)
df_state


# #### Finding required ratio for whole country

# In[15]:


df_overall = pd.DataFrame(columns=['Country','dose1','dose2','Total_Population','ratio1','ratio2'])
a=df_state['dose1'].sum(axis=0)
b=df_state['dose2'].sum(axis=0)
x=df_state['Total_Population'].sum(axis=0)
df_overall.loc[0,'Country'] = 'India'
df_overall.loc[0,'dose1'] = a
df_overall.loc[0,'dose2'] = b
df_overall.loc[0,'Total_Population'] = x
df_overall.loc[0,'ratio1'] = a/x
df_overall.loc[0,'ratio2'] = b/x


# In[16]:


df_overall


# #### Creating csv file for each result

# In[17]:


df_district[['District_Key','ratio1','ratio2']].to_csv("district-vaccinated-dose-ratio.csv",header=['districtid', 'vaccinateddose1ratio', 'vaccinateddose2ratio'], index=False)


# In[18]:


df_state[['State','ratio1','ratio2']].to_csv("state-vaccinated-dose-ratio.csv",header=['state', 'vaccinateddose1ratio', 'vaccinateddose2ratio'], index=False)


# In[19]:


df_overall[['Country','ratio1','ratio2']].to_csv("overall-vaccinated-dose-ratio.csv",header=['country', 'vaccinateddose1ratio', 'vaccinateddose2ratio'], index=False)

