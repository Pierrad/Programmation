# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
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
        # Lecture de nos fichiers .csv
        self.train = pd.read_csv("train.csv")
        self.test = pd.read_csv("test.csv")
        # On créer un liste avec train et test
        self.all = [self.train, self.test]

    def removeData(self):
        # On supprime certaines colonnes de nos données
        DataToRemoveTrain = ["PassengerId", "Name", "SibSp", "Parch", "Ticket", "Cabin", "FamilySize"]
        DataToRemoveTest = ["Name", "SibSp", "Parch", "Ticket", "Cabin", "FamilySize"]
        self.train = self.train.drop(DataToRemoveTrain, axis = 1)
        self.test = self.test.drop(DataToRemoveTest, axis = 1)

    def readData(self,column):
        # Affiche le nombre de valeurs totales de la colonne
        print(len(self.train[column]))
        # Affiche les valeurs possibles d'une certaine colonne
        print(self.train[column].unique())
        # Affiche le nombre de valeurs disponible selon la catégorie
        print(self.train[column].value_counts())

    def modifyData(self):
        # On modifie l'entiereté de nos valeurs (d'un coup "train" et d'un coup "test") pour qu'elles soient efficace et lisible par le modèle
        for dataSet in self.all:
            # On remplace les valeurs "nan" de la colonne "Embarked" par "S" car c'est le plus courant
            dataSet['Embarked'] = dataSet['Embarked'].fillna('S')
            # On convertit les caractères en nombre pour que ce soit compréhensible pour le modèle et on transforme bien en int
            dataSet['Embarked'] = dataSet['Embarked'].map( {'S': 0, 'C': 1, 'Q':2} ).astype(int)
            ###########################################################################################################################################
            # On convertit avec la fonction map qui applique "female" en 1 et "male" en 0 puis on transforme bien en int
            dataSet['Sex'] = dataSet['Sex'].map( {'female': 1, 'male': 0} ).astype(int)
            ###########################################################################################################################################
            # On calcule la moyenne et l'écart-type, on créer une liste de nombre random en fonction du nombre de "nan"
            # On attribut un nombre moyen random à un élement "nan" de la colonne puis on transforme bien en int
            ageAvg = dataSet['Age'].mean()
            ageStd = dataSet['Age'].std()
            ageNullCount = dataSet['Age'].isnull().sum()
            ageNullRandomList = np.random.randint(ageAvg - ageStd, ageAvg + ageStd, size = ageNullCount)
            dataSet['Age'][np.isnan(dataSet['Age'])] = ageNullRandomList
            dataSet['Age'] = dataSet['Age'].astype(int)
            # On attribut un nombre (transforme bien en int) selon la catégorie d'age pour faciliter l'extraction au modèle
            # Loc permet d'accéder à un groupe de colonne ou ligne par leurs noms et ensuite on leur attribut une valeur
            dataSet.loc[(dataSet['Age'] <= 16), 'Age'] = 0
            dataSet.loc[(dataSet['Age'] > 16) & (dataSet['Age'] <= 32), 'Age'] = 1
            dataSet.loc[(dataSet['Age'] > 32) & (dataSet['Age'] <= 48), 'Age'] = 2
            dataSet.loc[(dataSet['Age'] > 48) & (dataSet['Age'] <= 64), 'Age'] = 3
            dataSet.loc[(dataSet['Age'] > 64), 'Age'] = 4
            dataSet['Age'] = dataSet['Age'].astype(int)
            ###########################################################################################################################################
            # On remplace les valeurs "nan" de la colonne "Fare" (tarif) par la valeur médiane de cette colonne (valeur qui sépare le groupe en deux)
            dataSet['Fare'] = dataSet['Fare'].fillna(self.train['Fare'].median())
            # On attribut un nombre (transforme bien en int) selon la catégorie de tarif pour faciliter l'extraction au modèle
            # Loc permet d'accéder à un groupe de colonne ou ligne par leurs noms et ensuite on leur attribut une valeur
            dataSet.loc[(dataSet['Fare'] <= 8), 'Fare'] = 0
            dataSet.loc[(dataSet['Fare'] > 8) & (dataSet['Fare'] <= 15), 'Fare'] = 1
            dataSet.loc[(dataSet['Fare'] > 15) & (dataSet['Fare'] <= 31), 'Fare']   = 2
            dataSet.loc[(dataSet['Fare'] > 31), 'Fare'] = 3
            dataSet['Fare'] = dataSet['Fare'].astype(int)
            ###########################################################################################################################################
            # On créer une nouvelle colonne comprenant la taille de la famille (+1 pour nous-même)
            dataSet['FamilySize'] = dataSet['SibSp'] + dataSet['Parch'] + 1
            # De base IsAlone = 0 mais si on est tout seul alors IsAlone = 1
            # Cette variable est nécessaire car selon si l'on est seul ou pas les chances de survit augmente ou pas
            dataSet['IsAlone'] = 0
            dataSet.loc[dataSet['FamilySize'] == 1, 'IsAlone'] = 1
            ###########################################################################################################################################
            # On extrait les noms en créant une nouvelle colonne
            # On remplace des noms par d'autres pour que ca s'accorde
            # On convertit les noms en nombre pour que cela soit compréhensible pour le modèle
            dataSet['Title'] = dataSet.Name.str.extract(' ([A-Za-z]+)\.')
            dataSet['Title'] = dataSet['Title'].replace(['Lady', 'Countess','Capt', 'Col', \
 	        'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Other')
            dataSet['Title'] = dataSet['Title'].replace('Mlle', 'Miss')
            dataSet['Title'] = dataSet['Title'].replace('Ms', 'Miss')
            dataSet['Title'] = dataSet['Title'].replace('Mme', 'Mrs')
            dataSet['Title'] = dataSet['Title'].map({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Other": 5})
            dataSet['Title'] = dataSet['Title'].fillna(0)
            ###########################################################################################################################################

class Model():
    def __init__(self, data):
        # On enlève la colonne "Survived" pour X_train mais on créer Y_train qui contient seulement cela (donc les bonnes réponses)
        self.X_train = data.train.drop('Survived', axis=1)
        self.Y_train = data.train['Survived']
        # On créer une copie X_test sans l'Id des passagers à partir des données de test
        self.X_test = data.test.drop("PassengerId", axis=1).copy()
        self.x_train, self.x_valid, self.y_train, self.y_valid = train_test_split(self.X_train, self.Y_train, test_size=0.33, shuffle= True)

    def TheModel(self):
        '''
        self.mdl = LogisticRegression()
        self.mdl.fit(self.X_train, self.Y_train)
        '''
        self.mdl = Sequential()
        self.mdl.add(Dense(200, input_dim = (self.X_train.shape[1]), activation = "relu"))
        self.mdl.add(Dropout(0.2))
        self.mdl.add(Dense(100, activation = "relu"))
        self.mdl.add(Dropout(0.2))
        self.mdl.add(Dense(1, activation = "sigmoid"))
        self.mdl.compile(optimizer = "adam", loss = "mean_squared_error", metrics = ["accuracy"])
        self.mdl.fit(self.x_train, self.y_train, epochs = 200, batch_size = 500, verbose = 2)
        self.mdl.summary()

    def Predict(self):
        self.prediction = self.mdl.predict(self.X_test)
        self.prediction = np.around(self.prediction)
        # Renvoit la loss value (plus c'est près de 0 mieux c'est là car MeanSquaredError) et la metrics value sur les données d'entrainements
        self.score, self.accuracy = self.mdl.evaluate(self.x_valid, self.y_valid)
        print(str(self.score) + ' %')

data = Data()
data.modifyData()
data.removeData()

model = Model(data)
model.TheModel()
model.Predict()

prediction = []
for i in range(len(data.test)):
    if int(model.prediction[i]) == -1:
        prediction.append(int(0))
    else:
        prediction.append(int(model.prediction[i]))

submission = pd.DataFrame({
        "PassengerId": data.test["PassengerId"],
        "Survived": prediction
    })

submission.to_csv('submission.csv', index=False)