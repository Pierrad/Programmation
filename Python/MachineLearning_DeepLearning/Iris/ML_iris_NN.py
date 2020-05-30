from matplotlib import pyplot as plt
import numpy as np 
import os 

fichier = open("iris_data.txt", "r")
lecture = fichier.readlines()

# Network
# The lengh and the width are inputs
# The w1, w2, b are parameters
# The flower type is output


# Parametres de début sont randoms
w1 = np.random.randn()
w2 = np.random.randn()
w3 = np.random.randn()
w4 = np.random.randn()
b = np.random.randn()

# Fonction sigmoid
def sigmoid(x):
    return 1/(1+ np.exp(-x))

# Dériver de la fonction sigmoid
def sigmoid_d(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Scatter data, observer la dispersion des données 
for i in range(len(lecture)):
    point = lecture[i].split(',')
    if point[4] == "Iris-setosa\n":
        color = "r"
    if point[4] == "Iris-versicolor\n":
        color = "b"
    if point[4] == "Iris-virginica\n":
        color = "g"
    plt.scatter(float(point[0]), float(point[1]), c = color)
    plt.scatter(float(point[2]), float(point[3]), c = color)
# Affiche le graph après la boucle for pour avoir tous les points sur le même graph
plt.show(block = True)

# Training loop

learning_rate = 0.2
costs = []

for i in range(50000):
    # Permet de train plusieurs fois sur les mêmes data 

    # Random point in 0 to 7 because len(data)=8 
    ri = np.random.randint(len(lecture))
    # Random point of data
    point = lecture[ri].split(',')
    
    # La prediction de l'ordinateur 
    z  = float(point[0]) * w1 + float(point[1]) * w2 + float(point[2]) * w3 + float(point[3]) * w4 + b
    # Le calcul de la prediction entre 0 et 1
    pred = sigmoid(z)
    # Le vrai type de fleur 
    if point[4] == "Iris-setosa\n":
        target = 0
    if point[4] == "Iris-versicolor\n":
        target = 0.5
    if point[4] == "Iris-virginica\n":
        target = 1
    # La fonction cost pour déterminer le taux d'erreur (doit se rapprocher de 0)
    cost = np.square(pred - target) # np.square permet la mise au carré

    # Ajouter 'cost' à la liste costs
    costs.append(cost)

    # Derivée du cout en fonction de la prediction
    dcost_pred = 2 * (pred - target)
    # Derivée de la prediction en fonction de z
    dpred_dz = sigmoid_d(z)
    # Derivée de z en fonction de w1
    dz_dw1 = float(point[0])
    # Derivée de z en fonction de w2
    dz_dw2 = float(point[1])
    # Derivée de z en fonction de w3
    dz_dw3 = float(point[2])
    # Derivée de z en fonction de w4
    dz_dw4 = float(point[3])
    # Derivée de z en fonction de b
    dz_db = 1

    # Derivée du cout en fonction de w1
    dcost_dw1 = dcost_pred * dpred_dz * dz_dw1 # On peut y voir une sorte de relation de chasles
    # Derivée du cout en fonction de w2
    dcost_dw2 = dcost_pred * dpred_dz * dz_dw2
    # Derivée du cout en fonction de w3
    dcost_dw3 = dcost_pred * dpred_dz * dz_dw3
    # Derivée du cout en fonction de w4
    dcost_dw4 = dcost_pred * dpred_dz * dz_dw4
    # Derivée du cout en fonction de b 
    dcost_db = dcost_pred * dpred_dz * dz_db

    # Nouveaux paramètres de w1, w2, b
    w1 = w1 - learning_rate * dcost_dw1
    w2 = w2 - learning_rate * dcost_dw2
    w3 = w3 - learning_rate * dcost_dw3
    w4 = w4 - learning_rate * dcost_dw4
    b = b - learning_rate * dcost_db

# Maintenant les paramètres de liaisons w1, w2, b sont correctement évalués
# Observer les prédictions du modèle pour chaque donnée
for i in range(len(lecture)):
    point = lecture[i].split(',')
    print(point)
    # La prédiction de l'ordinateur
    z = float(point[0]) * w1 + float(point[1]) * w2 + float(point[2]) * w3 + float(point[3]) * w4 + b
    # La prediction entre 0 et 1
    pred = sigmoid(z)
    print("prediction : {}".format(pred))

def pred_fleur(lengh_s, width_s, lengh_p, width_p):
    if lengh_s < 0 or width_s < 0 or lengh_p < 0 or width_p < 0:
        os.system("Say Impossible")
    z = lengh_s * w1 + width_s * w2 + lengh_p * w3 + width_p * w4 + b
    pred = sigmoid(z)
    if pred > 0 and pred < 0.4:
        os.system("say Setosa")
    if pred > 0.4 and pred < 0.6:
        os.system("say Versicolor")
    if pred > 0.8:
        os.system("Say Virginica")

pred_fleur(2, 1.2, 4, 1.4)


fichier.close()