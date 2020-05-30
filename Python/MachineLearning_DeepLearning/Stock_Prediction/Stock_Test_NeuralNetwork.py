import requests
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.wrappers.scikit_learn import KerasClassifier
from statsmodels.tsa.stattools import adfuller
from scipy.ndimage.interpolation import shift
import datetime
from scipy import stats
import matplotlib
# Pour éviter "Abort trap 6"
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# Plus l'erreur de librairie et plus le warning sur le fait que TensorFlow n'a pas été compilé pour mon type de processeur
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
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

# Création du modèle
def CreateModel(x_train, y_train, epoch, batch_size):
	# Création du model
	model = Sequential()
	# Ajout d'un layer au réseau de neurones LSTM (long short-term memory) avec comme format d'input x_train et 50 neurones et qui retourne la séquence pour pas renvoyer du random au prochain layer
	model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1],1)))
	# Ajout d'un layer Dropout pour éviter l'overfitting
	model.add(Dropout(0.2))
	# On ajoute encore 3 layers
	model.add(LSTM(units = 50, return_sequences = True))
	model.add(Dropout(0.2))
	model.add(LSTM(units = 50, return_sequences = True))
	model.add(Dropout(0.2))
	model.add(LSTM(units = 50))
	model.add(Dropout(0.2))
	# Ajout d'un layer Dense qui prend un seul neurone pour l'output
	model.add(Dense(1))
	# On ajoute une fonction d'erreur pour la backpropagation
	model.compile(loss = 'mean_squared_error', optimizer='adam')
	# On entraine le réseau avec les données plus des paramètres
	# Epoch = passage de toutes les données pour l'entraînement
	# Batch_Size nombre de données qu'il prend pour chaque entrainement plus le batch_size est grand plus l'entrainement est long mais plus précis mais plus couteux
	model.fit(x_train, y_train, epochs = epoch, batch_size = batch_size, verbose = 2)
	return model

# Permet de créer un modèle pour le Grid Search
def CreateModelGrid(activation = 'relu'):
	# Création du model
	model = Sequential()
	# Ajout d'un layer au réseau de neurones LSTM (long short-term memory) avec comme input x_train
	model.add(LSTM(units = 50, return_sequences = True, input_shape = (60,1), activation = 'relu'))
	# Ajout d'un autre layer
	model.add(LSTM(units = 50, activation = activation))
	# Ajout d'un layer Dense
	model.add(Dense(1))
	# On ajoute une fonction d'erreur pour la backpropagation
	model.compile(loss = 'mean_squared_error', optimizer = 'adam', metrics = ['accuracy'])
	return model

# On récupère les données sur le site
API_URL = "https://www.alphavantage.co/query"
data = { "function": "TIME_SERIES_DAILY",
		"symbol": "ORA.PA",
		"outputsize": "full",
		"datatype": "json",
		"apikey": "20M98U0442RX494K" }
response = requests.get(API_URL, data)
data = response.json()

# Globalement les actions suivantes réduisent de plus en plus le dictionnaire pour ne donner qu'une liste de liste
# Convertit le dictionnaire en list
data = list(data.values())
# On récupère et isole les informations de base de nos données
data_information = data[0]
# On convertit la dict globale des dates en list en gardant les dates (les keys) (intérieur est toujours dict comme ca on peut supprimer plus facilement)
data = list(data[1].items())

# On a donc une list de list de tuple
# On créer une double liste pour stocker nos valeurs sous la forme [[date, valeur], ...]
data_f = [[0 for x in range(2)] for y in range(len(data))]

for i in range(len(data)):
	# On ne garde que la valeur de la fin de journée de l'action (close)
	del data[i][1]['1. open']
	del data[i][1]['2. high']
	del data[i][1]['3. low']
	del data[i][1]['5. volume']
	# On remplit data_f avec toutes les dates et les valeurs qui correspondent (d'abord en list puis tranformé en float)
	data_f[i][0] = data[i][0]
	data_f[i][1] = list(data[i][1].values())
	data_f[i][1] = float(data_f[i][1][0])

# On inverse la list pour l'avoir dans l'ordre chronologique (plus ancien au plus récent)
data_f.reverse()
# Tranforme notre list en Pandas DataFrame
df = pd.DataFrame(data_f)
# On renomme les colonnes pour avoir une colonne "Date" et une colonne "Close Values"
df = df.rename(columns = {0 : "Date", 1 : "Close values"})
# On définit la colonne date avec une mise en forme particulière
df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
# On définit la colonne Date comme étant l'index de notre dataframe
df.set_index("Date")
# On supprime la colonne date pour ne plus avoir les dates comme index mais seulement des nombres
df.drop("Date", axis=1, inplace=True)
# Dataset ne contient que les valeurs de df (colonne Close Values)
dataset = df.values
'''
# Voir s'il y a pas d'outlier dans nos données (valeurs aberrantes)
plt.boxplot(dataset, vert=False)
plt.title("Visualisation des valeurs pour trouver des Outliers")
plt.show()
'''
# Supprimer les Outliers
z = np.abs(stats.zscore(dataset))
threshold = 3
datasetNew = dataset[(z < 3).all(axis=1)]

# Des datas d'entraînement et des datas de validation
train = datasetNew[0:3900,:]
valid = datasetNew[3900:,:]

# On test les données, si p-values est proche de 1 alors on a bcp de chance que ce soit non-stationnaire et donc une random walk (mais pas forcément)
data = pd.DataFrame(datasetNew)
data1 = data.iloc[:,0].values
result = adfuller(data1)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1]) #p-value > 0.05: is non-stationary == Random walk // p-value <= 0.05: is stationary.
print('Critical Values:')
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))

# On définit un scaler et on scale nos data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(datasetNew)

UseValues = 120
# On créer nos x_train et y_train avec les datas adaptés
x_train, y_train = [], []
for i in range(UseValues,len(train)):
	x_train.append(scaled_data[i-UseValues:i,0])
	y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# On prépare la prédiction d'une valeur en utilisant 'UseValues' valeurs précédentes
inputs = df[len(df) - len(valid) - UseValues:].values
inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)

# X_test contient des valeurs par tranches de 'UseValues' pour donner cela au modèle afin de prédire la valeur suivante
X_test = []
for i in range(UseValues+1,inputs.shape[0]+1):
	X_test.append(inputs[i-UseValues:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Pour la création et l'entrainement du modèle avec les données d'entrainements
model = CreateModel(x_train, y_train, 1, 32)

# On affiche la prédiction du modèle sur les derniers mois pour avoir une idée du résultat de l'entrainement du modèle
PrintValid = True
Week = True
Month = False
Year = False
All = False
pastDate = []
if PrintValid == True:
	closing_price = model.predict(X_test)
	closing_price = scaler.inverse_transform(closing_price)
	# Graphique avec toutes les données disponibles plus la prédiction de 3900 à len(data_f)
	if Week == True:
		allData = df[len(df)-7:]
		prediction = df[len(df)-7:]
		prediction['Predictions'] = closing_price[-7:]
		pastDate = [str(item[0]) for item in data_f[-7:]]
	if Month == True:
		allData = df[len(df)-30:]
		prediction = df[len(df)-30:]
		prediction['Predictions'] = closing_price[-30:]
		pastDate = [str(item[0]) for item in data_f[-30:]]
	if Year == True:
		allData = df[len(df)-365:]
		prediction = df[len(df)-365:]
		prediction['Predictions'] = closing_price[-365:]
		pastDate = [str(item[0]) for item in data_f[-365:]]
	if All == True:
		allData = df
		prediction = df[3900:]
		prediction['Predictions'] = closing_price
		pastDate = [str(item[0]) for item in data_f]
	plt.plot(pastDate, allData['Close values'], label = 'Close values')
	plt.plot(pastDate, prediction[['Predictions']], label = 'Prédictions')
	plt.legend(loc='upper right')
	plt.xticks(rotation=90)
	plt.show()

# Root mean square error, permet de mesurer l'efficacité d'un NN en comparant les predictions avec les données de tests
rms = np.sqrt(np.mean(np.power((valid-closing_price),2)))
print("Résultat RMSE = ", rms, " %")

# On prédit sur DayPredict
DayPredict = 31
lastPrice = [None] * DayPredict
pastPrice = []
futurDate = []
pastDate = []
for i in range(DayPredict):
	# Prédiction
	closing_price = model.predict(X_test)
	closing_price = scaler.inverse_transform(closing_price)
	# On récupère le prix
	lastPrice[i] = float(closing_price[-1])
	# On re-prépare la prédiction d'une valeur en utilisant 'UseValues' valeurs précédentes et les prédictions faites précédemment
	inputs = df[len(df) - len(valid) - UseValues:].values
	# On roll la list vers le haut
	inputs = np.roll(inputs, -1-i)
	# On égalise la première valeur qui est devenue la dernière à la valeur prédit
	for j in range(i):
		inputs[-1-j] = lastPrice[j]
	inputs = inputs.reshape(-1,1)
	inputs = scaler.transform(inputs)
	# X_test contient des valeurs par tranches de 'UseValues' pour donner cela au modèle afin de prédire la valeur suivante en utilisant les valeurs/prédictions précédentes
	X_test = []
	for k in range(UseValues+1,inputs.shape[0]+1):
		X_test.append(inputs[k-UseValues:k,0])
	X_test = np.array(X_test)
	X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
	# On affiche le prix prédit
	print("Day ", i, " =", float(lastPrice[i]), "€")
	# On calcule le taux de variations entre le prix d'hier et d'aujourd'hui
	if i == 0:
		increase = float(lastPrice[i]) - float(datasetNew[-1])
		result = (increase/float(datasetNew[-1]))*100
	else:
		increase = float(lastPrice[i]) - float(lastPrice[i-1])
		result = (increase/float(lastPrice[i-1]))*100
	# On affiche le taux de variation
	print("On a donc ", result, " % de variation")
	# On créer deux listes de date, les 30 précédentes et les 30 suivantes
	futurDate.append(str(datetime.date.today() + datetime.timedelta(days=i+1)))
	pastDate.append(str(data_f[-1-i][0]))
	pastPrice.append(float(datasetNew[-1-i]))
pastDate.reverse()
pastPrice.reverse()
# Affichage du graphique de -30 jours à +30 jours
plt.plot(pastDate, pastPrice, label = 'Valeurs actuelles')
plt.plot(futurDate, lastPrice, label = 'Prédiction')
plt.legend(loc='upper right')
plt.xticks(rotation=90)
plt.title("Prédiction sur 30 jours")
plt.show()


# La partie suivante va permettre de déterminer les meilleurs paramètres
'''
model = KerasClassifier(build_fn = CreateModelGrid, epochs=1, batch_size=1, verbose=0)
# On définit les paramètres à tester
activation = ['softmax', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']
param_grid = dict(activation = activation)
grid = GridSearchCV(estimator = model, param_grid = param_grid, n_jobs = -1)
grid_result = grid.fit(x_train, y_train)
# Affichage des résultats
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
	print("%f (%f) with: %r" % (mean, stdev, param))
'''