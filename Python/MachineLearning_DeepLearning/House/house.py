# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
# Un arbre de décision
from sklearn.tree import DecisionTreeClassifier
# Ensemble methods -> Bagging (random forest or multiple decision tree)
# XGBoosting (on utilise le modele entrainer pour en creer un autre et ainsi de suite)
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor

# One Hot Encoding necessaire

class Data():
    def __init__(self):
        self.train = pd.read_csv("train.csv")
        self.test = pd.read_csv("test.csv")
        # On créer une liste avec train et test
        self.all = [self.train, self.test]

    def readData(self):
        column = "BsmtUnfSF"
        for dataSet in self.all:
            # Affiche le nombre de valeurs totales de la colonne
            print(len(dataSet[column]))
            # Affiche les valeurs possibles d'une certaine colonne
            print(dataSet[column].sort_values().unique())
            # Affiche le nombre de valeurs disponible selon la catégorie
            print(dataSet[column].value_counts())

    def modifyData(self):
        for dataSet in self.all:
            # Transforme chaque type de valeurs de la catégorie en variable numérique int
            dataSet['LotArea'] = dataSet['LotArea'].fillna(self.train['LotArea'].median())
            dataSet.loc[(dataSet['LotArea'] >= 0) & (dataSet["LotArea"] <= 5000), 'LotArea'] = 0
            dataSet.loc[(dataSet['LotArea'] >= 5000) & (dataSet["LotArea"] <= 10000), 'LotArea'] = 1
            dataSet.loc[(dataSet['LotArea'] >= 10000) & (dataSet["LotArea"] <= 20000), 'LotArea'] = 2
            dataSet.loc[(dataSet['LotArea'] >= 20000) & (dataSet["LotArea"] <= 30000), 'LotArea'] = 3
            dataSet.loc[(dataSet['LotArea'] >= 30000) , 'LotArea'] = 4
            dataSet['LotArea'] = dataSet['LotArea'].astype(int)
            dataSet.loc[(dataSet['YearRemodAdd'] >= 1950) & (dataSet["YearRemodAdd"] <= 1980), 'YearRemodAdd'] = 0
            dataSet.loc[(dataSet['YearRemodAdd'] >= 1980) & (dataSet["YearRemodAdd"] <= 1990), 'YearRemodAdd'] = 1
            dataSet.loc[(dataSet['YearRemodAdd'] >= 1990) & (dataSet["YearRemodAdd"] <= 2020), 'YearRemodAdd'] = 2
            dataSet['YearRemodAdd'] = dataSet['YearRemodAdd'].astype(int)
            dataSet["ExterQual"] = dataSet["ExterQual"].map({"Ex": 4, "Gd": 3, "TA": 2, "Fa": 1, "Po": 0}).astype(int)
            dataSet["BsmtQual"] = dataSet["BsmtQual"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "NA": 0}).fillna(0).astype(int)
            dataSet["BsmtCond"] = dataSet["BsmtCond"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "NA": 0}).fillna(0).astype(int)
            dataSet["BsmtExposure"] = dataSet["BsmtExposure"].map({"Gd": 4, "Av": 3, "Mn": 2, "No": 1, "NA": 0}).fillna(0).astype(int)
            dataSet.loc[(dataSet['1stFlrSF'] >= 0) & (dataSet["1stFlrSF"] <= 500), '1stFlrSF'] = 0
            dataSet.loc[(dataSet['1stFlrSF'] >= 500) & (dataSet["1stFlrSF"] <= 1000), '1stFlrSF'] = 1
            dataSet.loc[(dataSet['1stFlrSF'] >= 1000) & (dataSet["1stFlrSF"] <= 1500), '1stFlrSF'] = 2
            dataSet.loc[(dataSet['1stFlrSF'] >= 1500) & (dataSet["1stFlrSF"] <= 2000), '1stFlrSF'] = 3
            dataSet.loc[(dataSet['1stFlrSF'] >= 2000) , '1stFlrSF'] = 4
            dataSet['1stFlrSF'] = dataSet['1stFlrSF'].fillna(0).astype(int)
            dataSet.loc[(dataSet['TotalBsmtSF'] >= 0) & (dataSet["TotalBsmtSF"] <= 500), 'TotalBsmtSF'] = 0
            dataSet.loc[(dataSet['TotalBsmtSF'] >= 500) & (dataSet["TotalBsmtSF"] <= 1000), 'TotalBsmtSF'] = 1
            dataSet.loc[(dataSet['TotalBsmtSF'] >= 1000) & (dataSet["TotalBsmtSF"] <= 1500), 'TotalBsmtSF'] = 2
            dataSet.loc[(dataSet['TotalBsmtSF'] >= 1500) & (dataSet["TotalBsmtSF"] <= 2000), 'TotalBsmtSF'] = 3
            dataSet.loc[(dataSet['TotalBsmtSF'] >= 2000) , 'TotalBsmtSF'] = 4
            dataSet['TotalBsmtSF'] = dataSet['TotalBsmtSF'].fillna(0).astype(int)
            dataSet["HeatingQC"] = dataSet["HeatingQC"].map({"Ex": 4, "Gd": 3, "TA": 2, "Fa": 1, "Po": 0}).fillna(4).astype(int)
            dataSet["CentralAir"] = dataSet["CentralAir"].map({"N": 0, "Y": 1}).astype(int)
            dataSet.loc[(dataSet['GrLivArea'] >= 0) & (dataSet["GrLivArea"] <= 1000), 'GrLivArea'] = 0
            dataSet.loc[(dataSet['GrLivArea'] >= 1000) & (dataSet["GrLivArea"] <= 1500), 'GrLivArea'] = 1
            dataSet.loc[(dataSet['GrLivArea'] >= 1500) & (dataSet["GrLivArea"] <= 2000), 'GrLivArea'] = 2
            dataSet.loc[(dataSet['GrLivArea'] >= 2500) & (dataSet["GrLivArea"] <= 3000), 'GrLivArea'] = 3
            dataSet.loc[(dataSet['GrLivArea'] >= 3000) , 'GrLivArea'] = 4
            dataSet['GrLivArea'] = dataSet['GrLivArea'].fillna(0).astype(int)
            dataSet["KitchenQual"] = dataSet["KitchenQual"].map({"Ex": 4, "Gd": 3, "TA": 2, "Fa": 1, "Po": 0}).fillna(2).astype(int)
            dataSet["GarageType"] = dataSet["GarageType"].map({"2Types": 6, "Attchd": 5, "Basment": 4, "BuiltIn": 3, "CarPort": 2, "Detchd": 1, "NA": 0}).fillna(0).astype(int)
            dataSet["GarageFinish"] = dataSet["GarageFinish"].map({"Fin": 3, "RFn": 2, "Unf": 1, "NA": 0}).fillna(0).astype(int)
            dataSet.loc[(dataSet['GarageArea'] >= 0) & (dataSet["GarageArea"] <= 250), 'GarageArea'] = 0
            dataSet.loc[(dataSet['GarageArea'] >= 250) & (dataSet["GarageArea"] <= 500), 'GarageArea'] = 1
            dataSet.loc[(dataSet['GarageArea'] >= 500) & (dataSet["GarageArea"] <= 750), 'GarageArea'] = 2
            dataSet.loc[(dataSet['GarageArea'] >= 750) , 'GarageArea'] = 3
            dataSet['GarageArea'] = dataSet['GarageArea'].fillna(0).astype(int)
            dataSet["GarageQual"] = dataSet["GarageQual"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "NA": 0}).fillna(0).astype(int)
            dataSet["GarageCond"] = dataSet["GarageCond"].map({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "NA": 0}).fillna(0).astype(int)
            dataSet["PavedDrive"] = dataSet["PavedDrive"].map({"Y": 2, "P": 1, "N": 0}).astype(int)
            dataSet['GarageCars'] = dataSet['GarageCars'].fillna(2).astype(int)
            dataSet.loc[(dataSet['FullBath'] == 4) , 'FullBath'] = 2
            dataSet["FullBath"] = dataSet["FullBath"].astype(int)
            dataSet.loc[(dataSet['YearBuilt'] >= 1870) & (dataSet["YearBuilt"] <= 1980), 'YearBuilt'] = 0
            dataSet.loc[(dataSet['YearBuilt'] >= 1980) & (dataSet["YearBuilt"] <= 1990), 'YearBuilt'] = 1
            dataSet.loc[(dataSet['YearBuilt'] >= 1990) & (dataSet["YearBuilt"] <= 2010), 'YearBuilt'] = 2
            dataSet['YearBuilt'] = dataSet['YearBuilt'].astype(int)
            dataSet.loc[(dataSet['Fireplaces'] >= 3) , 'Fireplaces'] = 2
            dataSet["Fireplaces"] = dataSet["Fireplaces"].astype(int)
            dataSet.loc[(dataSet['BsmtFinSF1'] >= 0) & (dataSet["BsmtFinSF1"] <= 750), 'BsmtFinSF1'] = 0
            dataSet.loc[(dataSet['BsmtFinSF1'] >= 750) & (dataSet["BsmtFinSF1"] <= 6000), 'BsmtFinSF1'] = 1
            dataSet['BsmtFinSF1'] = dataSet['BsmtFinSF1'].fillna(0).astype(int)
            dataSet.loc[(dataSet['WoodDeckSF'] >= 0) & (dataSet["WoodDeckSF"] <= 100), 'WoodDeckSF'] = 0
            dataSet.loc[(dataSet['WoodDeckSF'] >= 100) & (dataSet["WoodDeckSF"] <= 1000), 'WoodDeckSF'] = 1
            dataSet['WoodDeckSF'] = dataSet['WoodDeckSF'].astype(int)
            dataSet.loc[(dataSet['2ndFlrSF'] >= 0) & (dataSet["2ndFlrSF"] <= 500), '2ndFlrSF'] = 0
            dataSet.loc[(dataSet['2ndFlrSF'] >= 500) & (dataSet["2ndFlrSF"] <= 1000), '2ndFlrSF'] = 1
            dataSet.loc[(dataSet['2ndFlrSF'] >= 1000) & (dataSet["2ndFlrSF"] <= 2100), '2ndFlrSF'] = 2
            dataSet['2ndFlrSF'] = dataSet['2ndFlrSF'].astype(int)
            dataSet.loc[(dataSet['OpenPorchSF'] >= 0) & (dataSet["OpenPorchSF"] <= 50), 'OpenPorchSF'] = 0
            dataSet.loc[(dataSet['OpenPorchSF'] >= 50) & (dataSet["OpenPorchSF"] <= 800), 'OpenPorchSF'] = 1
            dataSet['OpenPorchSF'] = dataSet['OpenPorchSF'].astype(int)
            dataSet.loc[(dataSet['BsmtFullBath'] >= 3) , 'BsmtFullBath'] = 2
            dataSet["BsmtFullBath"] = dataSet["BsmtFullBath"].fillna(0).astype(int)

    def removeData(self):
        # Correlation en dessous de 0.2
        removelist = ["LotShape", "MSZoning", "Fence", "KitchenAbvGr", "EnclosedPorch", "LotConfig", "MSSubClass", "SaleType", "OverallCond", "LandContour", "LandSlope",
        "LowQualFinSF", "MiscVal", "BsmtHalfBath", "BsmtFinSF2", "SaleCondition", "Utilities", "ExterCond", "LotFrontage", "Street", "3SsnPorch", "MoSold", "PoolArea", "HouseStyle",
        "ScreenPorch", "Exterior1st", "BedroomAbvGr", "YrSold", "Alley", "Neighborhood", "Condition1", "Condition2", "BldgType", "RoofStyle", "RoofMatl", "Exterior2nd", "MasVnrType", "Foundation",
        "BsmtFinType1", "BsmtFinType2", "Heating", "Electrical", "Functional", "FireplaceQu", "PoolQC", "MiscFeature"]
        self.train = self.train.drop(removelist, axis = 1)
        self.train = self.train.drop("Id", axis = 1)
        self.test = self.test.drop(removelist, axis = 1)

    def plotData(self):
        print(self.train[self.train.columns[1:]].corr()['SalePrice'][:].sort_values())
        #self.corrTrain = self.train.corr()
        #sns.heatmap(self.corrTrain[['SalePrice']].sort_values(by=['SalePrice'],ascending=False), cmap='coolwarm', annot=True)
        #plt.show()

class Model():
    def __init__(self, data):
        self.X_train = data.train.drop("SalePrice", axis = 1)
        self.Y_train = data.train['SalePrice']
        self.X_test = data.test.drop("Id", axis = 1).copy()
        self.x_train, self.x_valid, self.y_train, self.y_valid = train_test_split(self.X_train, self.Y_train, test_size=0.33, shuffle= True)

    def TheModel(self):
        self.mdl = XGBRegressor()
        self.mdl.fit(self.X_train, self.Y_train, eval_set=[(self.x_valid, self.y_valid)], verbose = False)

    def Predict(self):
        self.prediction = self.mdl.predict(self.X_test)
        self.prediction = np.around(self.prediction).astype(int)
        self.accuracy = self.mdl.score(self.x_valid, self.y_valid, sample_weight=None)
        print(str(self.accuracy) + ' %')

data = Data()
data.modifyData()
#data.readData()
data.removeData()
#data.plotData()

model = Model(data)
model.TheModel()
model.Predict()

submission = pd.DataFrame({
        "Id": data.test["Id"],
        "SalePrice": model.prediction
    })

submission.to_csv('submission.csv', index=False)
