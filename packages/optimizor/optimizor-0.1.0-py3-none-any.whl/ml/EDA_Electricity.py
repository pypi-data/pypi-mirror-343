#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


# In[ ]:


data = pd.read_csv("World Energy Consumption.csv")
data


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


data["Total Electricity"] = (
    data["biofuel_electricity"] +
    data["electricity_generation"] +
    data["fossil_electricity"] +
    data["gas_electricity"] +
    data["hydro_electricity"]
)
data = data[['country', 'year', 'Total Electricity']]

df_cleaned = data.dropna()
df_cleaned


# In[ ]:


set(df_cleaned['country'])


# In[ ]:


# Lets Analyse for all countries and specific countries too!

# First lets see for all countries in a specific year
data_2000 = df_cleaned[df_cleaned['year'] == 2000]
print(data_2000.head())
print(data_2000.shape)
data_2000 = data_2000.iloc[:30]

sb.barplot(x = data_2000['country'], y = data_2000['Total Electricity'])
plt.title("Energy Consumption for 30 countries on the year 2000")
plt.xticks(rotation=90)
plt.show()

# Now lets see for a specific country !
data_india = df_cleaned[df_cleaned['country'] == "India"]
print(data_india)
plt.scatter(x = data_india['year'], y = data_india['Total Electricity'])
plt.title("Energy Consumption for India over the years")
plt.show()


# In[ ]:


# Suppose we want to predict the data for India then we must check the correlation
df_num = data_india[['year', 'Total Electricity']]
print(df_num.head())

sb.heatmap(df_num.corr())


# We can see there a 99% correleation between the year and the total electricity!

# In[ ]:


# We check for outliers on the data for india
sb.boxplot(df_num['Total Electricity'])
plt.show() # Good data will have less outliers!


# In[ ]:


sb.histplot(df_num['Total Electricity'], kde = True)

