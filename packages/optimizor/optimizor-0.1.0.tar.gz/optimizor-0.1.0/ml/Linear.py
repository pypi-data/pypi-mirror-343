#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


# In[ ]:


data = pd.read_csv("World Energy Consumption.csv")
data


# In[ ]:


data.describe()


# In[ ]:


data.info()


# In[ ]:


data.columns


# In[ ]:


data["Total Electricity"] = (
    data["biofuel_electricity"] +
    data["electricity_generation"] +
    data["fossil_electricity"] +
    data["gas_electricity"] +
    data["hydro_electricity"]
)
new_data = data[['country', 'year', 'Total Electricity']]

df_cleaned = new_data.dropna()
df_cleaned


# In[ ]:


# Lets do a prediction for India
data_india = df_cleaned[df_cleaned['country'] == "India"]
print(data_india.info())
data_india.head()


# In[ ]:


df_num = data_india[['year', 'Total Electricity']]
sb.heatmap(df_num.corr())
plt.show() # Shows Strong correlation


# In[ ]:


plt.scatter(x = data_india['year'], y = data_india['Total Electricity'])
plt.show()


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X_train, X_test, y_train, y_test = train_test_split(data_india['year'], data_india['Total Electricity'], test_size = 0.2, random_state = 42)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


X_train = X_train.to_numpy().reshape(-1, 1)
y_train = y_train.to_numpy().reshape(-1, 1)
X_test = X_test.to_numpy().reshape(-1, 1)
y_test = y_test.to_numpy().reshape(-1, 1)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[ ]:


model = LinearRegression()
model.fit(X_train, y_train)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)


# In[ ]:


y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(mse, r2)


# In[ ]:


plt.scatter(X_test, y_test)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs Predicted")
plt.plot(X_test, y_pred)
plt.show()

