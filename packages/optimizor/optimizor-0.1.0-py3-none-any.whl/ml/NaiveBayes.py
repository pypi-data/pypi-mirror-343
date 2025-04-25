#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:


df = pd.read_csv("World Energy Consumption.csv")
df


# Use One Feature (i.e) only population to classsify the uage of electricity high or low based on median electricty.

# In[ ]:


df["Total Electricity"] = (
    df["biofuel_electricity"] +
    df["electricity_generation"] +
    df["fossil_electricity"] +
    df["gas_electricity"] +
    df["hydro_electricity"]
)

df_1 = df[df['year'] == 2000] # Let's take for the year 2000.
df_1 = df_1[['population', 'Total Electricity']]

df_cleaned = df_1.dropna()
df_cleaned


# In[ ]:


median_electricity = df_cleaned['Total Electricity'].median()

df_cleaned['class'] = df_cleaned['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df_cleaned


# In[ ]:


class NaiveBayes:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = {}
        self.means = {}
        self.variances = {}

        print(self.classes)
        
        for c in self.classes:
            curr_class = X[y == c]
            self.means[c] = np.mean(curr_class, axis = 0)
            self.variances[c] = np.var(curr_class, axis = 0)
            self.priors[c] = curr_class.shape[0] / X.shape[0]

    def _gaussian_probability(self, x, mean, var):
        eps = 1e-6
        coeff = 1 / np.sqrt(2 * np.pi * var + eps)
        exponent = np.exp(-((x - mean) ** 2) / (2 * var + eps))
        return coeff * exponent

    def predict(self, X):
        predictions = [self._predict_sample(x) for x in X]
        return np.array(predictions)

    def _predict_sample(self, x):
        posteriors = []

        for c in self.classes:
            prior = np.log(self.priors[c])
            likelihoods = np.sum(np.log(self._gaussian_probability(x, self.means[c], self.variances[c])))
            posterior = prior + likelihoods
            posteriors.append(posterior)

        return self.classes[np.argmax(posteriors)]
            


# In[ ]:


from sklearn.model_selection import train_test_split

X = df_cleaned["population"]
y = df_cleaned["class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


X_train, X_test = X_train.to_numpy().reshape(-1, 1), X_test.to_numpy().reshape(-1, 1)
y_train, y_test = y_train.to_numpy().reshape(-1, 1), y_test.to_numpy().reshape(-1, 1)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# In[ ]:


model = NaiveBayes()
model.fit(X_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score, classification_report

y_pred = [model.predict(x) for x in X_test]
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


# In[ ]:


print(classification_report(y_test, y_pred))


# In[ ]:


df_2 = df[df['year'] == 2000]
df_2 = df_2[['population', 'gdp', 'Total Electricity']]
df_2


# Using Two features for X and trying to classify (i.e) use Both Population and GDP

# In[ ]:


df_2 = df[df['year'] == 2000]
df_2 = df_2[['population', 'gdp', 'Total Electricity']]
df_2


# In[ ]:


df_cleaned = df_2.dropna()
df_cleaned


# In[ ]:


median_electricity = df_cleaned['Total Electricity'].median()
df_cleaned['class'] = df_cleaned['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df_cleaned


# In[ ]:


X = df_cleaned[["population", "gdp"]]
y = df_cleaned["class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


# In[ ]:


from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# In[ ]:


model = NaiveBayes()
model.fit(X_train, y_train)


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


print(f"Accuracy :{accuracy_score(y_test, y_pred) * 100:.2f}%")

