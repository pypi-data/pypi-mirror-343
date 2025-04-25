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


# In[ ]:


print(df.columns)
df.info()


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


df_cleaned['class'] = df_cleaned['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df_cleaned


# In[ ]:


class SLP:
    def __init__(self, input_size, lr = 1e-4, epochs = 100):
        self.weights = np.zeros(input_size)
        self.bias = 0
        self.lr = lr
        self.epochs = epochs

    def sigmoid(self, x):
        return 1 if x>=0 else 0

    def predict(self, x):
        # X is a vector!
        z = np.dot(x, self.weights) + self.bias
        return self.sigmoid(z)

    def train(self, X, y):
        for _ in range(self.epochs):
            for i in range(len(X)):
                prediction = self.predict(X[i])
                error = y[i] - prediction
                self.weights += (self.lr * error * X[i])
                self.bias += (self.lr * error)


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


model = SLP(X_train.shape[1], 0.01, 100)
model.train(X_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score

y_pred = [model.predict(x) for x in X_test]
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


# In[ ]:


import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


# In[ ]:


model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# In[ ]:


history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)


# In[ ]:


loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

