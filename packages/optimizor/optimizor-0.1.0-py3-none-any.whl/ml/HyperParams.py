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


from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import validation_curve


# In[ ]:


# Classifier 1: KNN
from sklearn.neighbors import KNeighborsClassifier as KNN

values = np.arange(2, 15)
train_scores, test_scores = validation_curve(
    KNN(), X_train, y_train, param_name='n_neighbors', param_range=values, cv=5, scoring='accuracy'
)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

plt.plot(values, train_mean)
plt.title("Accuracy for different k-values in training")
plt.show()

plt.plot(values, test_mean)
plt.title("Accuracy for different k-values in testing")
plt.show()


# In[ ]:


from sklearn.svm import SVC

values = [("linear", -1), ("rbf", -1), ("poly", 5), ("sigmoid", -1)]

accuracies = []

for kernel, deg in values:
    if deg == -1:
        model = SVC(kernel = kernel)
    else:
        model = SVC(kernel = kernel, degree=deg)
        
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_pred, y_test)
    accuracies.append(accuracy)

kernels = [value[0] for value in values]
plt.bar(kernels, accuracies)
plt.show()
        


# In[ ]:


import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense


# In[ ]:


# MLP Model
def create_model():
    model = Sequential([
        Dense(64, activation= 'relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation = 'relu'),
        Dense(1, activation="sigmoid")
    ])

    return model


# In[ ]:


values = []


# In[ ]:


# Full gradient Descent
model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=X_train.shape[0], validation_split=0.2) # Full Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
values.append(accuracy)
values


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
values.append(accuracy)
values


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=1, validation_split=0.2) # Stochiastic Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
values.append(accuracy)
values


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


labels = ["Full Fradient Descent", "Batch Gradient Descent", "Stochiastic Gradient Descent"]
plt.barh(labels, values)
plt.show()


# In[ ]:


# MLP Model
from tensorflow.keras.layers import LeakyReLU
def create_model():
    model = Sequential([
        Dense(64, activation= 'tanh', input_shape=(X_train.shape[1],)),
        Dense(32),
        LeakyReLU(alpha=0.05),
        Dense(1, activation="sigmoid")
    ])

    return model


# In[ ]:


values = []


# In[ ]:


model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


# Regularization!
from tensorflow.keras.layers import Dropout

def create_model():
    model = Sequential([
        Dense(64, activation= 'tanh', input_shape=(X_train.shape[1],)),
        Dropout(0.3), # Try adding dropouts
        Dense(32),
        LeakyReLU(alpha=0.05),
        Dense(1, activation="sigmoid")
    ])

    return model


# In[ ]:


model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


# Regularization using Lasso-Regulators
from tensorflow.keras.regularizers import l1_l2
def create_model():
    model = Sequential([
        Dense(64, activation= 'tanh', input_shape=(X_train.shape[1],), kernel_regularizer=l1_l2(l1=0.0001, l2=0.0001)),
        Dropout(0.3), # Try adding dropouts
        Dense(32, kernel_regularizer=l1_l2(l1=0.0001, l2=0.0001)),
        Dropout(0.3),
        LeakyReLU(alpha=0.05),
        Dense(1, activation="sigmoid")
    ])

    return model


# In[ ]:


model = create_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


labels = ["No Regularization", "With dropout Layers", "With L1-L2 and DropoutLayers"]
plt.barh(labels, values)
plt.show()


# Learning Rate

# In[ ]:


values = []


# In[ ]:


from tensorflow.keras.optimizers import Adam

optimizer = Adam(learning_rate = 1e-3)
model = create_model()
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


optimizer = Adam(learning_rate = 1e-4)
model = create_model()
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


optimizer = Adam(learning_rate = 1e-5)
model = create_model()
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2) # Batch Gradient Descent

loss, accuracy = model.evaluate(X_test, y_test)
print(accuracy)
values.append(accuracy)


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()


# In[ ]:


labels = ['1e-3', '1e-4', '1e-5']
plt.barh(labels, values)
plt.show()


# From the observations we see <br>
#  - Model with batch Gradient Descent of 32 is good (batch_size = 32) <br>
#  - Model with epochs = 30 is better (epochs = 30) <br>
#  - Model with leaky_relu and tanh seems better <br>
#  - Model with learning rat eof 1e-3 is good by the loss curve<br>

# In[ ]:


from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.layers import LeakyReLU
def create_model():
    model = Sequential([
        Dense(64, activation="tanh", input_shape=(X_train.shape[1], ), kernel_regularizer=l1_l2(l1=0.001, l2=0.001)), 
        Dropout(0.4),
        Dense(32, kernel_regularizer=l1_l2(l1=0.001, l2=0.001)),
        LeakyReLU(alpha=0.05),
        Dropout(0.3),
        Dense(1, activation="sigmoid")
    ])

    return model


# In[ ]:


from tensorflow.keras.optimizers import Adam

optimizer = Adam(learning_rate=1e-3)

model = create_model()
model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2)

loss, accuracy = model.evaluate(X_test, y_test)
print("Final Accuracy of the model:", round(accuracy, 4)*100, " %")


# In[ ]:


plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.show()

