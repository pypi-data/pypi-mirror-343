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

df = df[df["year"] >= 2000]
df = df[['population', 'gdp', 'Total Electricity']]
df.dropna(inplace = True)
df


# In[ ]:


median_electricity = df['Total Electricity'].mean()
df['class'] = df['Total Electricity'].apply(lambda x : 0 if x < median_electricity else 1)
df


# In[ ]:


X = df[["population", "Total Electricity"]]
X = X.to_numpy()
y = df["class"]
X


# In[ ]:


from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score


# In[ ]:


k = 2 # 2 Classes
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)


# In[ ]:


labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print(labels, centroids)


# In[ ]:


plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], label='Data Points')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', label='Centroids')
plt.xlabel('Population')
plt.ylabel('Total Electricity')
plt.title('K-Means Clustering on the Iris Dataset')
plt.legend()
plt.show()
# A prediction Dataset so classification not so good.


# In[ ]:


mat = confusion_matrix(y, labels)
sb.heatmap(mat, annot=True)
plt.xlabel('K-Means Cluster')
plt.ylabel('True Species')
plt.show()


# In[ ]:


print("Accuracy :", round(accuracy_score(y, labels)*100, 2))

