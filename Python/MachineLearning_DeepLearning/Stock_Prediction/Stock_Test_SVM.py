import requests
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
import datetime
import matplotlib.pyplot as plt
# On récupère les données sur le site
API_URL = "https://www.alphavantage.co/query"
data = { "function": "TIME_SERIES_DAILY",
        "symbol": "AMZN",
        "outputsize": "full",
        "datatype": "json",
        "apikey": "" }
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
# Transforme chaque élement pour en faire un index dans une liste
dates = df.index.tolist()

# Conversion vers un array d'une dimension
dates = np.reshape(dates, (len(dates), 1))

# Définition d'un modèle SVR - Radial basis function
svr_rbf = svm.SVR(kernel= 'rbf', C= 1e3, gamma= 0.1)

# On définit des valeurs de test et de train (30-70)
xtrain, xtest, ytrain, ytest = train_test_split(dates, df["Close values"], test_size=0.33)
# On entraine les modèles
svr_rbf.fit(xtrain, ytrain)

# On affiche les données initiales
plt.scatter(dates, df["Close values"], color= 'blue', label= 'Data')
# On affiche les prédictions avec les différents modèles
plt.plot(dates, svr_rbf.predict(dates), color='red', label = 'RBF model')
# On créer un titre
plt.title('SVR')
# On l'affiche en tant que légende
plt.legend()
# On créer un label pour les x
plt.xlabel('Date')
plt.ylabel('Price')
# Affichage du graphique
plt.show()

print ("Score:", svr_rbf.score(xtest, ytest))
# Date de demain
print(svr_rbf.predict(np.array(dates[-1]+1).reshape(-1,1))[0])


'''
plt.plot(df_date["Date"], df_values["Close values"], label = 'Valeurs Réelles')
plt.plot(df_date["Date"], forecast_prediction, label = 'Prédiction')
plt.legend(loc='upper right')
plt.show()
'''
