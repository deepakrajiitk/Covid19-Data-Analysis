#!/usr/bin/env python
# coding: utf-8

# ### Importing libraries

# In[22]:


import pandas as pd
import json
from itertools import islice


# ### Importing datasets

# In[23]:


df = pd.read_csv("districts.csv")


# ###### dropping irrelevant columns

# In[24]:


df.drop(columns=['Recovered','Other','Tested','Deceased'], inplace = True)


# In[25]:


f = open("neighbor-districts-modified.json")
filtered_district = json.load(f)


# ###### f1 contains a file that maps state name to its (It will help to check whether a particular district is present in neighbor district modified databse or not)

# In[26]:


f1 = open("state_code_mapping.json")
state_code_mapping = json.load(f1)


# ### The following things are done here:
#     1. removing districts which are not present in district dataset we build in question 1
#     2. confirmed cases in dataset are cumulative, so converting cummulative values to delta values

# In[27]:


for key, values in df.groupby(['State', 'District']):
    if key[1]!="Unknown":
        district_name = state_code_mapping[key[0]]+"_"+key[1]
    else:
        district_name = state_code_mapping[key[0]] + "_" + key[1]
    
    if district_name not in filtered_district:
        df.drop(values.index, inplace=True)
    else:
        first_value = df.at[values.index[0],'Confirmed']
#         diff() function convert cumulative values to delta values
        df.loc[values.index, 'Confirmed'] = df.loc[values.index, 'Confirmed'].diff()
        df.at[values.index[0],'Confirmed'] = first_value
        df.loc[values.index, 'District'] = district_name


# ###### There are some wrong entries in dataset due to which we get negative test cases. Replacing negative values by nearest positive value

# In[28]:


df[df['Confirmed']<0]


# In[29]:


# ffill() function fill the negative entries with neares positive entry before it
df['Confirmed'] = df['Confirmed'].mask(df['Confirmed']<0).ffill().fillna(0).convert_dtypes()


# ###### taking data from 15 march 2020 to 14 august 2021
# ###### since entries from 15 march to 25 march, 2020 are not available, adding them by considering no of cases 0 per day

# In[30]:


df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')


# In[31]:


# dropping dates after 14 august
df.drop(df[df['Date']>'2021-08-14'].index, inplace=True)


# In[32]:


all_districts = df['District'].unique()


# In[33]:


date_range = pd.date_range('2020-04-15','2020-04-25')
for district in all_districts:
    a = pd.DataFrame({'Date': date_range, 'District':district, 'Confirmed': 0,'State':df[df['District']==district]['State'].unique()[0]})
    df = pd.concat([a,df])


# In[34]:


df


# In[35]:


df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')


# In[36]:


df.sort_values(['Date','District'],ignore_index=True, inplace=True)
df


# ### Findig Weekly cases
# Resample function divides the dataset into weeks starting from sunday and ending at saturday.
# To calculate df_week we take sum of every week for every district in database

# In[37]:


df_week = df.set_index('Date').groupby('District').resample('w-sat').agg({'Confirmed':'sum','State':'first'}).reset_index().drop('Date',axis = 1)


# ###### df_week we calculated above does not have column which tells the week number, so creating one

# In[38]:


df_week['Week'] = 0
for key, value in df_week.groupby('District'):
    index = value.index
    df_week.loc[index,'Week'] = [i for i in range(1,len(index)+1)]


# In[39]:


df_week


# ###### this file is created because it will be used in coming questions

# In[208]:


df_week.to_csv('weekly-cases.csv',index=False)


# ###### creating output1 csv file

# In[166]:


df_week[['District','Confirmed','Week']].to_csv("cases-week.csv", index = False, header=['District Id','Cases','Week'])


# ### Finding Monthly cases

# ###### Since month starts from 15 and ends at 14, we have to define length of each month manually, this part of program is quite time taking because it iterate over every district in database and calculate total cases of that district for each month

# In[40]:


month_days = [30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31]
df_month = pd.DataFrame(columns=['State','District','Month','Cases'])
for key, value in df.groupby(['State','District']):
    month_count = 1
    indexes = iter(value.index)
    splitted_index = [list(islice(indexes, elem)) for elem in month_days]
    for i in splitted_index:
        s = df.loc[i, 'Confirmed'].sum()
        df_month = df_month.append({'State':key[0],'District': key[1], 'Month': month_count, 'Cases':s}, ignore_index=True)
        month_count+=1


# ###### this file is created because it will be used in coming questions

# In[41]:


df_month.to_csv("monthly-cases.csv",index = False)


# ###### creating output2 csv file

# In[42]:


df_month[['District','Month','Cases']].to_csv("cases-month.csv", index = False, header=['District Id','Month','Cases'])


# ### Finding overall cases

# In[43]:


df_overall = df.groupby('District').sum().reset_index()


# ###### creating output3 csv file

# In[45]:


df_overall.to_csv("cases-overall.csv", index = False, header=['District Id','Cases'])

