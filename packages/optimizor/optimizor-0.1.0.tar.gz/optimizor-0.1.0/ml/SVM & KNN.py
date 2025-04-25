#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv("World Energy Consumption.csv")
df


# In[ ]:


df["Total Electricity"] = (
    df["biofuel_electricity"] +
    df["electricity_generation"] +
    df["fossil_electricity"] +
    df["gas_electricity"] +
    df["hydro_electricity"]
)

df = df[df["year"] == 2000]
df = df[['population', 'gdp', 'Total Electricity']]
df.dropna(inplace = True)
df


# In[ ]:


median_electricity = df['Total Electricity'].mean()
df['class'] = df['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df


# In[ ]:


from sklearn.model_selection import train_test_split

X = df[["population", "gdp"]]
y = df["class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# y_train, y_test = y_train.to_numpy().reshape(-1, 1), y_test.to_numpy().reshape(-1, 1)

# print(X_train.shape, y_train.shape)
# print(X_test.shape, y_test.shape)


# In[ ]:


sb.countplot(x = y)
plt.show()


# In[ ]:


plt.scatter(X["gdp"][50:100], y[50:100])
plt.show()


# In[ ]:


sb.heatmap(df.corr(), annot=True)
plt.show()


# In[ ]:


# Using KNN
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

model = KNN(n_neighbors = 3)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))


# In[ ]:


# Using KNN for 5 neighbors

model = KNN(n_neighbors = 5)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))


# In[ ]:


from sklearn.svm import SVC

# Linear Kernel
model1 = SVC(kernel='linear')
model1.fit(X_train, y_train)

y_pred = model1.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")


# In[ ]:


# Polynomial Kernel
model2 = SVC(kernel='poly', degree=5)
model2.fit(X_train, y_train)

y_pred = model2.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")


# In[ ]:


# RBF Kernel
model3 = SVC(kernel='rbf', gamma='scale')
model3.fit(X_train, y_train)

y_pred = model3.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")


# In[ ]:


# Sigmoid Kernel
model4 = SVC(kernel='sigmoid')
model4.fit(X_train, y_train)

y_pred = model4.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

