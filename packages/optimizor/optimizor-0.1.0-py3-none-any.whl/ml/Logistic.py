#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


df = pd.read_csv("World Energy Consumption.csv")
df.tail()


# In[ ]:


print(df.columns)
df.info()


# In[ ]:


df['year']


# # Task = Logistic Regression!
# 
# Let's try to classify consumption of electricty as high consumption or low consumption based on population on a particular year
# 

# In[ ]:


df["Total Electricity"] = (
    df["biofuel_electricity"] +
    df["electricity_generation"] +
    df["fossil_electricity"] +
    df["gas_electricity"] +
    df["hydro_electricity"]
)

df = df[df['year'] == 2000] # Let's take for the year 2000.
df = df[['population', 'Total Electricity']]

df_cleaned = df.dropna()
df_cleaned


# In[ ]:


# Lets take average electricity
median_electricity = df_cleaned['Total Electricity'].median()
median_electricity


# In[ ]:


df_cleaned['consumption_class'] = df_cleaned['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df_cleaned


# In[ ]:


sb.heatmap(df_cleaned.corr()) # Bad correlation! so Expected accuracy is low for this task :(
plt.show()


# In[ ]:


plt.scatter(y = df_cleaned['Total Electricity'], x = df_cleaned['population'])
plt.show()


# In[ ]:


plt.scatter(y = df_cleaned['consumption_class'], x = df_cleaned['population'])
plt.show()


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

X = df_cleaned['population']
y = df_cleaned['consumption_class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


# Reshape for fitting sinze 1d- feature
X_train, X_test = X_train.to_numpy().reshape(-1, 1), X_test.to_numpy().reshape(-1, 1)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


model = LogisticRegression()
model.fit(X_train, y_train)


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


print("Accuracy:", accuracy_score(y_test, y_pred)) # Pretty good accuracy!
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix\n:", confusion_matrix(y_test, y_pred))

