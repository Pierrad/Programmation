Stock_Prediction
================
Projet ayant pour but de prédire les valeurs d'une action dans le futur pour une certaine entreprise. <br/>
L'API AlphaVantage (https://www.alphavantage.co/) a était utilisé pour récupérer la totalité des valeurs d'une action depuis sa mise en bourse. <br/>
Ensuite il a fallu clarifier les données reçus afin de les rendre utilisables. <br/>
Un modèle Long short-term memory a était utilisé afin de prendre en compte les valeurs précédentes lors du calcul d'une prédiction. <br/>
L'algorithme permet de prédire X jours.
Il est possible d'afficher toutes sortes de graphiques (toutes les valeurs, quelques mois, quelques jours...). <br/>
A la fin du projet, on retrouve un Grid Classifier qui permet de déterminer les meilleurs paramètres du modèle parmi une séléction. <br/>

Il est plutôt efficace pour les actions relativement linéaire. Il aurait été mauvais à prédire la brutale hausse du CAC40 en 2019 par exemple. 

Installation
============
- Pandas
- Numpy 
- TensorFlow / Keras
- Matplotlib
- Scipy
- Sklearn
