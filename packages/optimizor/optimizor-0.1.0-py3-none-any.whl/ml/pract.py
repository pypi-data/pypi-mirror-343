#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y = True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def initialize_weights(dim):
    weights = np.zeros(dim)
    bias = 0
    return weights, bias

def predict(X, weights, bias):
    y_pred = np.dot(X, weights) + bias
    return y_pred

def get_loss(y_pred, y_true):
    m = len(y_true)
    loss = (1 / 2*m) * np.sum((y_pred - y_true) ** 2)
    return loss

def get_gradients(X, y_true, y_pred):
    m = len(y_true)
    dw = (1/m) * np.dot(X.T, (y_pred - y_true))
    db = (1/m) * np.sum(y_pred - y_true)
    return dw, db

def adjust(weights, bias, dw, db, lr):
    weights -= lr * dw
    bias -= lr * db
    return weights, bias

def linear_regression(X, y, epochs, lr):
    weights, bias = initialize_weights(X.shape[1])
    for i in range(epochs):
        y_pred = predict(X, weights, bias)
        loss = get_loss(y_pred, y)
        dw, db = get_gradients(X, y, y_pred)
        weights, bias = adjust(weights, bias, dw, db, lr)

        if i % 100 == 0:
            print(loss)
    return weights, bias


# In[ ]:


m, c = linear_regression(X_train, y_train, 1000, 1e-3)


# In[ ]:




