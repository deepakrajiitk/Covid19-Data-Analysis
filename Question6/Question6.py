#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


import pandas as pd
import datetime
import numpy as np
from itertools import islice


# ### Importing Datasets

# In[2]:


original_df = pd.read_csv("cowin_vaccine_data_districtwise.csv")


# ###### droppin irrelevant columns

# In[3]:


df = original_df.drop(columns=['S No','State_Code','Cowin Key'])
df.drop(0, inplace=True)


# In[4]:


df = df.reset_index(drop = True)


# ### Modifying dataset for better visualization and easy computation

# In[5]:


df1 = df.melt(id_vars=['State','District_Key','District'],var_name='Date_columns',value_name='Total_Individuals')


# In[6]:


df1['Date'] = df1.Date_columns.str[:10]
df1['Date'] = pd.to_datetime(df1['Date'],format='%d/%m/%Y')


# In[7]:


df1.drop(df1[df1['Date']>'2021-08-14'].index, inplace=True)


# In[8]:


df1.fillna(0, inplace = True)


# In[9]:


df1


# ###### In our modified dataset the entries with .5 at the end in 'Dose_Type' column represent the 'No of Females Vaccinated' and the entries with .6 in the end represent the 'No of Females Vaccinated'

# In[10]:


df1.loc[df1['Date_columns'].str[-1]=='5','Date_columns'] = 'Male'
df1.loc[df1['Date_columns'].str[-1]=='6','Date_columns'] = 'Female'


# In[12]:


df2 = df1[(df1['Date_columns']=='Female') | (df1['Date_columns']=='Male')]
df2['Total_Individuals']=df2['Total_Individuals'].astype("int")
df_Female = df2[df2['Date_columns']=='Female']
df_Male = df2[df2['Date_columns']=='Male']


# In[13]:


df3 = df_Female[['State','District_Key','District','Date']]
df3['Female_Vaccinated'] = df_Female['Total_Individuals'].values
df3['Male_Vaccinated'] = df_Male['Total_Individuals'].values


# #### Modified dataset

# In[14]:


df3


# ###### There are some districts which have more than one entries for the same district therefore merging them into single entry by taking sum

# In[16]:


df3 = df3.groupby(['Date','District_Key','District']).agg({'State':'first','Female_Vaccinated':'sum','Male_Vaccinated':'sum'}).reset_index()


# ###### Converting cummulative values to delta values

# In[17]:


for key, values in df3.groupby(['District_Key']):
    df3.loc[values.index, 'Male_Vaccinated'] = df3.loc[values.index, 'Male_Vaccinated'].diff()
    df3.loc[values.index, 'Female_Vaccinated'] = df3.loc[values.index, 'Female_Vaccinated'].diff()
df3['Female_Vaccinated'].fillna(0)
df3['Male_Vaccinated'].fillna(0)
df3['Female_Vaccinated'] = df3['Female_Vaccinated'].mask(df3['Female_Vaccinated']<0).ffill().fillna(0).convert_dtypes()
df3['Male_Vaccinated'] = df3['Male_Vaccinated'].mask(df3['Male_Vaccinated']<0).ffill().fillna(0).convert_dtypes()
df3


# #### Importing population dataset

# In[18]:


census_data = pd.read_csv("DDW_PCA0000_2011_Indiastatedist.csv")


# ###### Removing irrelevant columns

# In[19]:


census_data = census_data[['Level','Name','TRU','TOT_P','TOT_M','TOT_F']]
census_data.drop(census_data[(census_data['TRU']=='Rural') | (census_data['TRU']=='Urban')].index, inplace=True)


# In[20]:


census_data


# #### Making some changes so that vaccination data and population data can be merged

# In[21]:


census_data['State'] = census_data['Name']
census_data.loc[census_data[census_data['Level']=='DISTRICT'].index,'State'] = np.nan
census_data.ffill(axis=0, inplace=True)


# In[22]:


census_data


# ###### renaming column names

# In[23]:


census_data.drop(census_data[(census_data['Level']=='STATE') | (census_data['Level']=='India')].index, inplace=True)
census_data.drop(columns=['Level','TRU'], inplace=True)
census_data.rename(columns={'Name':'District','TOT_P':'Total_Population','TOT_M':'Total_Male_Population', 'TOT_F':'Total_Female_Population'},inplace=True)


# In[24]:


census_data['State'] = census_data['State'].str.lower()
census_data['State'] = census_data['State'].str.title()
census_data.replace("&", "and", regex = True, inplace = True)


# In[327]:


census_data


# ###### this file is created because it will be used in coming questions

# In[25]:


census_data.to_csv("filtered_census_data.csv",index = False)


# #### Merging Population dataset and Vaccination dataset

# In[26]:


merged_df = pd.merge(df3, census_data, on=['District','State'])
merged_df['Male_Vaccinated'] = merged_df['Male_Vaccinated'].astype('float')
merged_df['Female_Vaccinated'] = merged_df['Female_Vaccinated'].astype('float')
merged_df['Total_Male_Population'] = merged_df['Total_Male_Population'].astype('float')
merged_df['Total_Female_Population'] = merged_df['Total_Female_Population'].astype('float')
merged_df


# ### Finding the required ratio for each district

# In[27]:


df_district = merged_df.groupby('District_Key').agg({'State':'first','Female_Vaccinated':'sum','Male_Vaccinated':'sum','Total_Male_Population':'first','Total_Female_Population':'first','District':'first'}).reset_index().drop('District',axis=1)


# In[28]:


df_district['Vaccination_Ratio'] = df_district.Female_Vaccinated.divide(df_district.Male_Vaccinated)
df_district['Population_Ratio'] = df_district.Total_Female_Population.divide(df_district.Total_Male_Population)
df_district['Ratio_of_Ratio'] = df_district.Vaccination_Ratio.divide(df_district.Population_Ratio)


# In[29]:


df_district.sort_values(['Ratio_of_Ratio'],inplace=True)
df_district


# ### Finding the required ratio for each state

# In[30]:


df_state = df_district.groupby('State').agg({'Female_Vaccinated':'sum','Male_Vaccinated':'sum','Total_Male_Population':'sum','Total_Female_Population':'sum'}).reset_index()


# In[31]:


df_state['Vaccination_Ratio'] = df_state.Female_Vaccinated.divide(df_state.Male_Vaccinated)
df_state['Population_Ratio'] = df_state.Total_Female_Population.divide(df_state.Total_Male_Population)
df_state['Ratio_of_Ratio'] = df_state.Vaccination_Ratio.divide(df_state.Population_Ratio)


# In[32]:


df_state.sort_values(['Ratio_of_Ratio'],inplace=True)
df_state


# ### Finding required ration for whole country

# In[33]:


df_overall = pd.DataFrame(columns=['Country','Female_Vaccinated','Male_Vaccinated','Total_Male_Population','Total_Female_Population','Vaccination_Ratio','Population_Ratio'])
a=df_state['Female_Vaccinated'].sum(axis=0)
b=df_state['Male_Vaccinated'].sum(axis=0)
x=df_state['Total_Female_Population'].sum(axis=0)
y=df_state['Total_Male_Population'].sum(axis=0)
df_overall.loc[0,'Country'] = 'India'
df_overall.loc[0,'Female_Vaccinated'] = a
df_overall.loc[0,'Male_Vaccinated'] = b
df_overall.loc[0,'Total_Female_Population'] = x
df_overall.loc[0,'Total_Male_Population'] = y
df_overall.loc[0,'Vaccination_Ratio'] = a/b
df_overall.loc[0,'Population_Ratio'] = a/b
df_overall.loc[0,'Ratio_of_Ratio'] = x/y


# In[34]:


df_overall


# ### Creating csv file for each result

# In[35]:


df_district[['District_Key','Vaccination_Ratio','Population_Ratio','Ratio_of_Ratio']].to_csv("district-vaccination-population-ratio.csv",header=['districtid', 'vaccinationratio', 'populationratio', 'ratioofratios'], index=False)


# In[36]:


df_state[['State','Vaccination_Ratio','Population_Ratio','Ratio_of_Ratio']].to_csv("state-vaccination-population-ratio.csv",header=['state', 'vaccinationratio', 'populationratio', 'ratioofratios'], index=False)


# In[37]:


df_overall[['Country','Vaccination_Ratio','Population_Ratio','Ratio_of_Ratio']].to_csv("overall-vaccination-population-ratio.csv",header=['country', 'vaccinationratio', 'populationratio', 'ratioofratios'], index=False)

