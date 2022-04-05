#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[5]:


import pandas as pd
import json
import datetime
from itertools import islice


# ### Importing Datasets

# In[6]:


df = pd.read_csv("cowin_vaccine_data_districtwise.csv")
df.head()


# #### dropping irrelevant rows and columns

# In[7]:


df.drop(columns=['S No','State_Code','Cowin Key','District'],inplace=True)
df.drop(0, inplace=True)


# In[8]:


df = df.reset_index(drop = True)


# In[9]:


df.head()


# #### Reshaping dataset
# the format of dataframes given is not easy to work with and it is not clean. It is better to take the columns and turn them into rows 

# In[10]:


df1 = df.melt(id_vars=['State','District_Key'],var_name='Date_columns',value_name='Total_Individuals')


# In[11]:


df1['Date'] = df1.Date_columns.str[:10]
df1['Date'] = pd.to_datetime(df1['Date'],format='%d/%m/%Y')


# In[12]:


df1.drop(df1[df1['Date']>'2021-08-14'].index, inplace=True)


# In[13]:


df1.fillna(0, inplace = True)


# In[14]:


df1


# #### In our modified dataset the entries with .8 at the end in 'Dose_Type' column represent the 'Covaxin dose administered value' and the entries with .9 at the end represent the 'covishield dose administered value'

# In[16]:


df1.loc[df1['Date_columns'].str[-1]=='8','Date_columns'] = 'Covaxin'
df1.loc[df1['Date_columns'].str[-1]=='9','Date_columns'] = 'Covishield'


# In[17]:


df2 = df1[(df1['Date_columns']=='Covaxin') | (df1['Date_columns']=='Covishield')]
df2['Total_Individuals']=df2['Total_Individuals'].astype("int")
df_Covaxin = df2[df2['Date_columns']=='Covaxin']
df_Covishield = df2[df2['Date_columns']=='Covishield']


# In[19]:


df3 = df_Covaxin[['State','District_Key','Date']]
df3['Covaxin_Dose'] = df_Covaxin['Total_Individuals'].values
df3['Covishield_Dose'] = df_Covishield['Total_Individuals'].values


# #### modified dataset

# In[20]:


df3


# #### There are some districts which have more than one entries for the same district therefore merging them into single entry by taking sum

# In[21]:


df3 = df3.groupby(['Date','District_Key']).agg({'State':'first','Covaxin_Dose':'sum','Covishield_Dose':'sum'}).reset_index()


# #### Converting cummulative values to delta values

# In[22]:


for key, values in df3.groupby(['District_Key']):
    df3.loc[values.index, 'Covishield_Dose'] = df3.loc[values.index, 'Covishield_Dose'].diff()
    df3.loc[values.index, 'Covaxin_Dose'] = df3.loc[values.index, 'Covaxin_Dose'].diff()
df3['Covaxin_Dose'].fillna(0)
df3['Covishield_Dose'].fillna(0)
df3['Covaxin_Dose'] = df3['Covaxin_Dose'].mask(df3['Covaxin_Dose']<0).ffill().fillna(0).convert_dtypes()
df3['Covishield_Dose'] = df3['Covishield_Dose'].mask(df3['Covishield_Dose']<0).ffill().fillna(0).convert_dtypes()
df3


# #### Finding required ration for each district

# In[23]:


df_district_overall = df3.groupby('District_Key').agg({'State':'first','Covaxin_Dose':'sum','Covishield_Dose':'sum'}).reset_index()


# In[24]:


df_district_overall['Covaxin_Dose'] = df_district_overall['Covaxin_Dose'].astype('float')
df_district_overall['Covishield_Dose'] = df_district_overall['Covishield_Dose'].astype('float')
df_district_overall['Ratio'] = df_district_overall.Covishield_Dose.divide(df_district_overall.Covaxin_Dose)
df_district_overall.fillna(0)
df_district_overall.sort_values(['Ratio'], inplace=True)
df_district_overall


# ### Finding required ratio for each state

# In[25]:


df_state_overall = df3.groupby('State').sum().reset_index()


# In[26]:


df_state_overall['Covaxin_Dose'] = df_state_overall['Covaxin_Dose'].astype('float')
df_state_overall['Covishield_Dose'] = df_state_overall['Covishield_Dose'].astype('float')
df_state_overall['Ratio'] = df_state_overall.Covishield_Dose.divide(df_state_overall.Covaxin_Dose)
df_state_overall.fillna(0)
df_state_overall.sort_values(['Ratio'], inplace=True)
df_state_overall


# #### Finding required ratio for whole country

# In[27]:


df_overall = pd.DataFrame(columns=['Country','Covaxin_Dose','Covishield_Dose','Ratio'])
a=df_state_overall['Covaxin_Dose'].sum(axis=0)
b=df_state_overall['Covishield_Dose'].sum(axis=0)
df_overall.loc[0,'Country'] = 'India'
df_overall.loc[0,'Covaxin_Dose'] = a
df_overall.loc[0,'Covishield_Dose'] = b
df_overall.loc[0,'Ratio'] = a/b
df_overall


# #### Creating csv file for each result

# In[28]:


df_district_overall[['District_Key','Ratio']].to_csv("vaccine-district-ratio.csv.csv",header=['districtid','vaccinationratio'], index=False)


# In[29]:


df_state_overall[['State','Ratio']].to_csv("vaccine-state-ratio.csv.csv",header=['state','vaccinationratio'], index=False)


# In[30]:


df_overall[['Country','Ratio']].to_csv("vaccine-overall-ratio.csv.csv",header=['Country','vaccinationratio'], index=False)

