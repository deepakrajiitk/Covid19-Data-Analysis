#!/usr/bin/env python
# coding: utf-8

# #### Importing libraries

# In[96]:


import pandas as pd
import json
from itertools import islice


# #### Importing datasets

# In[97]:


df = pd.read_csv("districts.csv")


# #### dropping irrelevent columns

# In[98]:


df.drop(columns=['Recovered','Other','Tested','Deceased'], inplace = True)


# In[99]:


f = open("neighbor-districts-modified.json")
filtered_district = json.load(f)


# In[100]:


f1 = open("state_code_mapping.json")
state_code_mapping = json.load(f1)


# #### 
# 1. converting cummulative values to delta values
# 2. findig intersection of covid database and neighbors district database

# In[101]:


for key, values in df.groupby(['State', 'District']):
    if key[1]!="Unknown":
        district_name = state_code_mapping[key[0]]+"_"+key[1]
    else:
        district_name = state_code_mapping[key[0]] + "_" + key[1]
    
    if district_name not in filtered_district:
        df.drop(values.index, inplace=True)
    else:
        first_value = df.at[values.index[0],'Confirmed']
        df.loc[values.index, 'Confirmed'] = df.loc[values.index, 'Confirmed'].diff()
        df.at[values.index[0],'Confirmed'] = first_value
        df.loc[values.index, 'District'] = district_name


# In[102]:


df['Confirmed'] = df['Confirmed'].mask(df['Confirmed']<0).ffill().fillna(0).convert_dtypes()


# In[103]:


df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')


# In[104]:


df.drop(df[df['Date']>'2021-08-14'].index, inplace=True)


# In[105]:


all_districts = df['District'].unique()


# #### Taking dataset from 15-04-2020 to 14-08-201

# In[106]:


date_range = pd.date_range('2020-04-16','2020-04-25')
for district in all_districts:
    a = pd.DataFrame({'Date': date_range, 'District':district, 'Confirmed': 0,'State':df[df['District']==district]['State'].unique()[0]})
    df = pd.concat([a,df])


# In[107]:


df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')


# In[108]:


df.sort_values(['Date','District'],ignore_index=True, inplace=True)
df


# In[109]:


df['Week']=0
df


# #### finding no of cases per week starting from sunday

# In[110]:


x=-1
def myfunc(Series):
    global x
    x+=2
    if(x==141):
        x=1
    return x
    
df1 = df.set_index('Date').groupby('District').resample('w-sat').agg({'Confirmed':'sum','Week':myfunc})


# #### finding no of cases per week starting from thursday

# In[111]:


y=0
def myfunc2(Series):
    global y
    y+=2
    if(y==142):
        y=2
    return y
    
df2 = df.set_index('Date').groupby('District').resample('w-wed').agg({'Confirmed':'sum','Week':myfunc2})


# In[112]:


df1.reset_index(inplace=True)
df2.reset_index(inplace = True)
df_week = pd.concat([df1,df2])


# In[113]:


df_week.sort_values(['District','Date','Week'],inplace=True)
df_week


# #### finding monthtly cases of each district

# In[114]:


month_days = [30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31]
df_month = pd.DataFrame(columns=['District','Month','Cases'])
for key, value in df.groupby('District'):
    month_count = 1
    indexes = iter(value.index)
    splitted_index = [list(islice(indexes, elem)) for elem in month_days]
    for i in splitted_index:
        s = df.loc[i, 'Confirmed'].sum()
        df_month = df_month.append({'District': key, 'Month': month_count, 'Cases':s}, ignore_index=True)
        month_count+=1
df_month


# #### Dividing dataset into two parts (one contain year 2020 data and another contain year 2021 data)

# In[115]:


df1  = df_week[df_week['Week']<=70]
df2  = df_week[df_week['Week']>70]


# #### finding weeks in year 2020 dataset where each district has maximum cases

# In[116]:


df1_max = pd.DataFrame(columns={'District','Week','Max_Cases'})
for key, value in df1.groupby(['District']):
    max_cases = value['Confirmed'].max()
    week = value[value['Confirmed']==max_cases]['Week'].values[0]
    df1_max = df1_max.append({'District':key,'Week':week,'Max_Cases':max_cases},ignore_index=True)
df1_max


# #### Plotting a scalar plot to know in which weeks we get most of maximum cases from most of the districts

# In[117]:


df1_max.plot.scatter(x = 'Week', y = 'Max_Cases', s = 40);


# ##### On observing plot we found out that week 30 to 55 have most of the maximum cases from most of the districts therefore our wave 1 is from week 30 to week 55

# #### finding weeks in year 2021 dataset where each district has maximum cases

# In[118]:


df2_max = pd.DataFrame(columns={'Week','Max_Cases'})
for key, value in df2.groupby(['District']):
    max_cases = value['Confirmed'].max()
    week = value[value['Confirmed']==max_cases]['Week'].values[0]
    df2_max = df2_max.append({'Week':week,'Max_Cases':max_cases},ignore_index=True)
df2_max


# #### Plotting a scalar plot to know in which weeks we get most of maximum cases from most of the districts

# In[119]:


df2_max.plot.scatter(x = 'Week', y = 'Max_Cases', s = 80);


# #### we have wave 2 from week 100 to week 120

# #### taking dataset of wave 1

# In[120]:


df_wave1_week = df1[(df1['Week']>=30) | (df1['Week']<=55)]
df_wave1_week


# #### taking dataset of wave 2

# In[121]:


df_wave2 = df2[(df2['Week']>=100) | (df2['Week']<=120)]
df_wave2


# #### finding week in which a district has maximum cases in wave1

# In[123]:


df_wave1_max = pd.DataFrame(columns={'District','Week'})
for key, value in df_wave1_week.groupby(['District']):
    max_cases = value['Confirmed'].max()
    week = value[value['Confirmed']==max_cases]['Week'].values[0]
    df_wave1_max = df_wave1_max.append({'District':key,'Week':week},ignore_index=True)
df_wave1_max


# #### finding week in which a district has maximum cases in wave1

# In[124]:


df_wave2_max = pd.DataFrame(columns={'District','Week'})
for key, value in df_wave2.groupby(['District']):
    max_cases = value['Confirmed'].max()
    week = value[value['Confirmed']==max_cases]['Week'].values[0]
    df_wave2_max = df_wave2_max.append({'District':key,'Week':week},ignore_index=True)
df_wave2_max


# In[125]:


df_week_result = pd.DataFrame()
df_week_result.insert(0, 'district_id', df_wave1_max['District'])
df_week_result.insert(1, 'wave1-weekid', df_wave1_max['Week'])
df_week_result.insert(2, 'wave2-weekid', df_wave2_max['Week'])
df_week_result


# In[126]:


df_wave1_month = df_month[(df_month['Month']>=4) & (df_month['Month']<=7)]
df_wave1_month


# In[127]:


df_wave2_month = df_month[(df_month['Month']>=13) & (df_month['Month']<=15)]
df_wave2_month


# In[128]:


df_wave1_month_max = pd.DataFrame(columns={'District','Month'})
for key, value in df_wave1_month.groupby(['District']):
    max_cases = value['Cases'].max()
    month = value[value['Cases']==max_cases]['Month'].values[0]
    df_wave1_month_max = df_wave1_month_max.append({'District':key,'Month':month},ignore_index=True)
df_wave1_month_max


# In[129]:


df_wave2_month_max = pd.DataFrame(columns={'District','Month'})
for key, value in df_wave2_month.groupby(['District']):
    max_cases = value['Cases'].max()
    month = value[value['Cases']==max_cases]['Month'].values[0]
    df_wave2_month_max = df_wave2_month_max.append({'District':key,'Month':month},ignore_index=True)
df_wave2_month_max


# ### merging all result of week

# In[131]:


df_week_result.insert(3, 'wave1-monthid', df_wave1_month_max['Month'])
df_week_result.insert(4, 'wave2-monthid', df_wave2_month_max['Month'])
df_week_result


# In[ ]:


creating csv file for result


# In[133]:


df_week_result.to_csv("district-peaks.csv")

