#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sb


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


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier as RFS

model = RFS(n_estimators = 100, random_state = 42)

model.fit(X_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score, classification_report

y_pred = model.predict(X_test)
print(f"Bagging Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(classification_report(y_test, y_pred))


# In[ ]:


# Boosting
from xgboost import XGBClassifier

# Train XGBoost model
model = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print(f"Boosting Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(classification_report(y_test, y_pred))


# In[ ]:


# Stacking
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.tree import DecisionTreeClassifier

base_models = [
    ('knn', KNN(n_neighbors=5)),
    ('svm', SVC(kernel='linear')),
    ('dt', DecisionTreeClassifier(max_depth=5))
]

meta_model = LogisticRegression()

model = StackingClassifier(estimators=base_models, final_estimator=meta_model)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Stacking Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print(classification_report(y_test, y_pred))

