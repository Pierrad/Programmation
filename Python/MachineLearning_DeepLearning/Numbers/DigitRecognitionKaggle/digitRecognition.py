# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Conv2D, Flatten, MaxPooling2D
from keras.utils import to_categorical

# Plus l'erreur de librairie et plus le warning sur le fait que TensorFlow n'a pas été compilé pour mon type de processeur
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# Plus l'erreur par rapport à l'assignation d'une dataframe à une autre pas forcément voulue (pandas)
pd.options.mode.chained_assignment = None
# On configure le nombre de CPU par type de threads pour maximiser les performances
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto(device_count = {"CPU":2},
						inter_op_parallelism_threads = 2,
						intra_op_parallelism_threads = 2)
session = tf.Session(config = config)
K.set_session(session)
img_rows, img_cols = 28, 28
num_classes = 10

class Data():
    def __init__(self):
        self.train = pd.read_csv("train.csv")
        self.test = pd.read_csv("test.csv")

    def readData(self):
        # Affiche le nombre de "nan" dans la dataFrame
        print("Nombre de 'nan' dans la DataFrame : ", self.test.isnull().sum().sum())
        # On remarque qu'il n'y a aucun "nan" donc pas besoin de compléter nos DataFrame

class Model():
    def __init__(self, data):
        self.X_train = data.train.drop("label", axis = 1)
        self.Y_train = data.train["label"]
        self.X_test = data.test
        # On redéfinit les dimensions de nos données
        self.X_train = self.X_train.values.reshape(self.X_train.shape[0], img_rows, img_cols, 1)
        self.X_test = self.X_test.values.reshape(self.X_test.shape[0], img_rows, img_cols, 1)
        self.input_shape = (img_rows, img_cols, 1)
        # Permet de catégoriser les données, il n'y a que des chiffres de 0 à 9 dans les données
        # Permet de transformer un 4 en [0,0,0,0,1,0,0,0,0,0]
        self.Y_train = to_categorical(self.Y_train, num_classes)
        # On normalise nos données même celle de test pour que la prediction soit adaptée
        self.X_train = self.X_train.astype('float32')
        self.X_test = self.X_test.astype('float32')
        self.X_train /= 255
        self.X_test /= 255
        # On coupe nos données en 70/30 pour l'entrainement puis la validation
        self.x_train, self.x_valid, self.y_train, self.y_valid = train_test_split(self.X_train, self.Y_train, test_size = 0.33, shuffle = True)

    def CreateModel(self):
        self.model = Sequential()
        # Convotional layers + pooling pour se concentrer sur les éléments importants et Dropout pour éviter l'overfitting
        self.model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same', input_shape=self.input_shape))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        self.model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        self.model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        # Conv2D et MaxPooling sont des tableaux de plusieurs dimensions, on doit les transformer en 1 dimension pour le réseau de neurones Dense d'où Flatten()
        self.model.add(Flatten())
        # Dense, un réseau de neurones classique
        self.model.add(Dense(128, activation='relu'))
        # Output layer
        self.model.add(Dense(num_classes, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, batch_size = 64, epochs = 18, verbose = 1)

    def Predict(self):
        self.prediction = self.model.predict(self.X_test)
        self.score, self.accuracy = self.model.evaluate(self.x_valid, self.y_valid)

# Les données
data = Data()
data.readData()
# Le modèle
model = Model(data)
model.CreateModel()
model.Predict()

print(model.prediction)
print("Loss (near 0) : ", model.score, " // Accuracy (near 1) : ", model.accuracy)

prediction = []
label = []
for i in range(len(model.prediction)):
    prediction.append(np.where(model.prediction[i] == np.amax(model.prediction[i]))[0][0])
    label.append(i+1)

submission = pd.DataFrame({
        "ImageId": label,
        "Label": prediction
    })

submission.to_csv('submission.csv', index=False)