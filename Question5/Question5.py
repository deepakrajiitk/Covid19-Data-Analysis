#!/usr/bin/env python
# coding: utf-8

# ### Importing libraries

# In[1]:


import pandas as pd
import json
import datetime
from itertools import islice


# ### Importing datasets

# In[2]:


df = pd.read_csv("cowin_vaccine_data_districtwise.csv")
df.head()


# ###### droppin irrelevant columns

# In[3]:


df.drop(columns=['S No','State_Code','Cowin Key'],inplace=True)
df.drop(0, inplace=True)


# In[4]:


df = df.reset_index(drop = True)


# In[5]:


df.head()


# ### Reshaping dataset
# the format of dataframes given is not easy to work with and it is not clean. It is better to take the columns and turn them into rows 

# In[6]:


df1 = df.melt(id_vars=['State','District_Key','District'],var_name='Dose_Type',value_name='Total_Individuals')


# In[7]:


df1['Date'] = df1.Dose_Type.str[:10]


# In[8]:


df1['Date'] = pd.to_datetime(df1['Date'],format='%d/%m/%Y')


# ### taking data from 15 january to 14 august 2021 only

# In[9]:


df1.drop(df1[df1['Date']>'2021-08-14'].index, inplace=True)


# In[14]:


df1


# In[11]:


df1.fillna(0, inplace = True)


# ### Modifying dataset for better visualization and computablity

# #### In our modified dataset the entries with .3 at the end in 'Dose_Type' column represent the 'first dose administered value' and the entries with .4 in the end represent the 'second dose administered value'
# Ex - entry with 14/08/2021.3 in AN_Nicobar district have 0 in Total_individuals column, it measn first dose administered in this district on 14 august is zero

# In[15]:


df1.loc[df1['Dose_Type'].str[-1]=='3','Dose_Type'] = 'First_Dose'
df1.loc[df1['Dose_Type'].str[-1]=='4','Dose_Type'] = 'Second_Dose'


# In[16]:


df2 = df1[(df1['Dose_Type']=='First_Dose') | (df1['Dose_Type']=='Second_Dose')]


# In[17]:


df2['Total_Individuals']=df2['Total_Individuals'].astype("int")


# In[18]:


df_firstDose = df2[df2['Dose_Type']=='First_Dose']
df_secondDose = df2[df2['Dose_Type']=='Second_Dose']


# In[20]:


df3 = df_firstDose[['State','District_Key','Date','District']]
df3['dose1'] = df_firstDose['Total_Individuals'].values
df3['dose2'] = df_secondDose['Total_Individuals'].values


# #### Modified dataframe

# In[21]:


df3


# #### There are some districts which have more than one entries for the same district therefore merging them into single entry by taking sum

# In[22]:


df3 = df3.groupby(['Date','District_Key','District']).agg({'State':'first','dose1':'sum','dose2':'sum'}).reset_index()


# #### Converting cummulative values to delta values

# In[23]:


for key, values in df3.groupby(['District_Key']):
    df3.loc[values.index, 'dose1'] = df3.loc[values.index, 'dose1'].diff()
    df3.loc[values.index, 'dose2'] = df3.loc[values.index, 'dose2'].diff()
df3['dose1'].fillna(0)
df3['dose2'].fillna(0)
df3['dose1'] = df3['dose1'].mask(df3['dose1']<0).ffill().fillna(0).convert_dtypes()
df3['dose2'] = df3['dose2'].mask(df3['dose2']<0).ffill().fillna(0).convert_dtypes()


# In[24]:


df3


# ###### This file is created because it will be used in upcoming question

# In[25]:


df3.to_csv("vaccination_data_dose_wise.csv",index = False)


# ### Finding no of people vaccinated in each district weekly

# In[26]:


df_week = df3.set_index('Date').groupby('District_Key').resample('w-sat').agg({'State':'first','dose1':'sum','dose2':sum}).reset_index().drop('Date',axis = 1)


# In[27]:


df_week['Week'] = 0
for key, value in df_week.groupby('District_Key'):
    index = value.index
    df_week.loc[index,'Week'] = [i for i in range(1,len(index)+1)]


# In[28]:


df_week


# ### Finding no of people vaccinated in each district monthly

# In[29]:


month_days = [30, 28, 31, 30, 31, 30, 31]
df_month = pd.DataFrame(columns=['District_Key', 'Month', 'State','dose1','dose2'])
for key, value in df3.groupby('District_Key'):
    month_count = 1
    indexes = iter(value.index)
    splitted_index = [list(islice(indexes, elem)) for elem in month_days]
    for i in splitted_index:
        s1 = int(df3.loc[i, 'dose1'].sum())
        s2 = int(df3.loc[i, 'dose2'].sum())
        df_month = df_month.append({'District_Key': key, 'State':value['State'].iloc[0], 'Month': month_count, 'dose1': s1, 'dose2':s2}, ignore_index=True)
        month_count+=1


# In[30]:


df_month


# ### Finding total no of people vaccinated in each district

# In[31]:


df_overall = df3.groupby('District_Key').agg({'State':'first','dose1':'sum','dose2':'sum'}).reset_index()


# In[32]:


df_overall['dose1']=df_overall['dose1'].astype("int")
df_overall['dose2']=df_overall['dose2'].astype("int")
df_overall


# ### Finding no of people vaccinated in each state weekly

# In[33]:


df_state_week = df_week.groupby(['State','Week']).sum().reset_index()


# In[34]:


df_state_week


# ### Finding no of people vaccinated in each state monthly

# In[35]:


df_state_month = df_month.groupby(['State','Month']).sum().reset_index().drop("District_Key",axis=1)


# In[36]:


df_state_month


# In[1692]:


df_state_month


# ### Finding total no of people vaccinated in each state

# In[37]:


df_state_overall = df3.groupby('State').sum().reset_index()


# In[38]:


df_state_overall


# ### Creating csv file for each result

# In[39]:


df_week[['District_Key','dose1','dose2','Week']].to_csv("district-vaccinated-count-week.csv",header=['districtid','dose1','dose2','week'], index=False)


# In[40]:


df_month[['District_Key','Month','dose1','dose2']].to_csv("district-vaccinated-count-month.csv",header=['districtid','month','dose1','dose2'], index=False)


# In[41]:


df_overall[['District_Key','dose1','dose2']].to_csv("district-vaccinated-count-overall.csv",header=['districtid','dose1','dose2'], index=False)


# In[42]:


df_state_week.to_csv("state-vaccinated-count-week.csv",header=['state','week','dose1','dose2'], index=False)


# In[43]:


df_state_month.to_csv("state-vaccinated-count-month.csv",header=['state','month','dose1','dose2'], index=False)


# In[44]:


df_state_overall.to_csv("state-vaccinated-count-overall.csv",header=['state','dose1','dose2'], index=False)

