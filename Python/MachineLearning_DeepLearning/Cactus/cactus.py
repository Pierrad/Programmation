# -*- coding: utf-8 -*-
import pandas as pd
# Print all DataFrame
'''
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199
'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Conv2D, MaxPooling2D, Flatten
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
# Plus l'erreur de librairie et plus le warning sur le fait que TensorFlow n'a pas été compilé pour mon type de processeur
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# Plus l'erreur par rapport à l'assignation d'une dataframe à une autre pas forcément voulue (pandas)
pd.options.mode.chained_assignment = None
# On configure le nombre de CPU par type de threads pour maximiser les performances
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto(device_count={"CPU":2},
						inter_op_parallelism_threads=2,
						intra_op_parallelism_threads=2)
session = tf.Session(config=config)
K.set_session(session)


class Data():
    def __init__(self):
        self.train_values = pd.read_csv("train.csv")
        self.nameList = os.listdir("test/test/")

    def printData(self):
        #print(self.Xtrain)
        #print(self.Ytrain)
        print(self.nameList)
        print(self.test)

    def setTrainData(self):
        self.imageTrain = []
        self.hasCactus = []
        for i in range(len(self.train_values)):
            self.imageTrain.append(cv2.imread("train/train/" + str(self.train_values["id"][i])))
            self.hasCactus.append(self.train_values["has_cactus"][i])
        print(self.imageTrain[0])
        #self.Xtrain = pd.DataFrame({'Image': self.imageTrain})
        #self.Ytrain = pd.DataFrame({'Has_Cactus': self.hasCactus})

    def setTestData(self):
        self.imageTest = []
        for i in range(len(self.nameList)):
            self.imageTest.append(cv2.imread("test/test/" + str(self.nameList[i])))
        self.test = pd.DataFrame({'id': self.imageTest})

    def AugmentedData(self):
        self.datagen = ImageDataGenerator(rescale=1./255., horizontal_flip = True, width_shift_range = 0.2, height_shift_range = 0.2, validation_split = 0.25)
        self.Testdatagen = ImageDataGenerator(rescale=1./255.)
        self.train_generator= self.datagen.flow_from_dataframe(
                                                        dataframe = self.train_values,
                                                        directory="train/train/",
                                                        x_col="id",
                                                        y_col="has_cactus",
                                                        subset="training",
                                                        batch_size=32,
                                                        seed=42,
                                                        shuffle=False,
                                                        class_mode="other",
                                                        target_size=(32,32))
        self.valid_generator= self.datagen.flow_from_dataframe(
                                                        dataframe=self.train_values,
                                                        directory="train/train/",
                                                        x_col="id",
                                                        y_col="has_cactus",
                                                        subset="validation",
                                                        batch_size=32,
                                                        seed=42,
                                                        shuffle=False,
                                                        class_mode="other",
                                                        target_size=(32,32))
        self.test_generator = self.Testdatagen.flow_from_directory(
                                                        directory="test/",
                                                        target_size=(32, 32),
                                                        color_mode="rgb",
                                                        batch_size=1,
                                                        class_mode=None,
                                                        shuffle=False,
                                                        seed=42)


class TheModel():
    def __init__(self, data):
        self.STEP_SIZE_TRAIN = data.train_generator.n // data.train_generator.batch_size
        self.STEP_SIZE_VALID = data.valid_generator.n // data.valid_generator.batch_size
        self.STEP_SIZE_TEST = data.test_generator.n // data.test_generator.batch_size

    def Model(self, data):
        self.model = Sequential()
        # Convotional layers + pooling pour se concentrer sur les éléments importants et Dropout pour éviter l'overfitting
        self.model.add(Conv2D(filters=16, kernel_size=(3,3), activation='relu', padding='same', input_shape=(32,32,3)))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        self.model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        self.model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        self.model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'))
        self.model.add(MaxPooling2D(pool_size=(2,2)))
        self.model.add(Dropout(0.2))
        # Conv2D et MaxPooling sont des tableaux de plusieurs dimensions, on doit les transformer en 1 dimension pour le réseau de neurones Dense d'où Flatten()
        self.model.add(Flatten())
        # Dense, un réseau de neurones classique
        self.model.add(Dense(256, activation='relu'))
        # Output layer
        self.model.add(Dense(1, activation='relu'))
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        self.model.fit_generator(generator = data.train_generator, epochs=1, steps_per_epoch= self.STEP_SIZE_TRAIN, validation_data= data.valid_generator, validation_steps= self.STEP_SIZE_VALID)
        self.model.evaluate_generator(generator = data.valid_generator, steps = self.STEP_SIZE_TEST)

    def predict(self, data):
        data.test_generator.reset()
        self.prediction = self.model.predict_generator(data.test_generator, steps=self.STEP_SIZE_TEST, verbose=2)
        self.prediction = self.prediction.round().astype(int)

data = Data()
#data.setTrainData()
#data.setTestData()
data.AugmentedData()
#data.printData()
model = TheModel(data)
model.Model(data)
model.predict(data)

predictions = []
for i in range(len(model.prediction)):
    predictions.append(model.prediction[i][0])

submission = pd.DataFrame({
        "id": data.nameList,
        "has_cactus": predictions
    })

submission.to_csv('submission.csv', index=False)


