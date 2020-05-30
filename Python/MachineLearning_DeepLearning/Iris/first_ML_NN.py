from matplotlib import pyplot as plt
import numpy as np 
import os 


# The lengh, the width, the type (0 blue, 1 red)
data =  [[3, 1.5, 1],
        [2, 1, 0], 
        [4, 1.5, 1], 
        [3, 1, 0], 
        [3.5, 0.5, 1], 
        [2, 0.5, 0], 
        [5.5, 1, 1], 
        [1, 1, 0]]

mystery_flower = [4.5, 1]

# Network
# The lengh and the width are inputs
# The w1, w2, b are parameters
# The flower type is output


# Paramètres de début sont randoms
w1 = np.random.randn()
w2 = np.random.randn()
b = np.random.randn()

# Fonction sigmoid
def sigmoid(x):
    return 1/(1+ np.exp(-x))

# Dériver de la fonction sigmoid
def sigmoid_d(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Scatter data, observer la dispersion des données 
for i in range(len(data)):
    point = data[i]
    color = "r"
    if point[2] == 0:
        color = "b"
    plt.scatter(point[0], point[1], c = color)
# Affiche le graph après la boucle for pour avoir tous les points sur le même graph
#plt.show(block = True)


# Training loop

learning_rate = 0.2
costs = []

for i in range(50000):
    # Permet de train plusieurs fois sur les mêmes data 

    # Random point in 0 to 7 because len(data)=8 
    ri = np.random.randint(len(data))
    # Random point of data
    point = data[ri]
    
    # La prediction de l'ordinateur 
    z  = point[0] * w1 + point[1] * w2 + b
    # Le calcul de la prediction entre 0 et 1
    pred = sigmoid(z)
    # Le vrai type de fleur 
    target = point[2]
    # La fonction cost pour déterminer le taux d'erreur (doit se rapprocher de 0)
    cost = np.square(pred - target) # np.square permet la mise au carré

    # Ajouter 'cost' à la liste costs
    costs.append(cost)

    # Derivée du cout en fonction de la prediction
    dcost_pred = 2 * (pred - target)
    # Derivée de la prediction en fonction de z
    dpred_dz = sigmoid_d(z)
    # Derivée de z en fonction de w1
    dz_dw1 = point[0]
    # Derivée de z en fonction de w2
    dz_dw2 = point[1]
    # Derivée de z en fonction de b
    dz_db = 1

    # Derivée du cout en fonction de w1
    dcost_dw1 = dcost_pred * dpred_dz * dz_dw1 # On peut y voir une sorte de relation de chasles
    # Derivée du cout en fonction de w2
    dcost_dw2 = dcost_pred * dpred_dz * dz_dw2
    # Derivée du cout en fonction de b 
    dcost_db = dcost_pred * dpred_dz * dz_db

    # Nouveaux paramètres de w1, w2, b
    w1 = w1 - learning_rate * dcost_dw1
    w2 = w2 - learning_rate * dcost_dw2
    b = b - learning_rate * dcost_db

# Maintenant les paramètres de liaisons w1, w2, b sont correctement évalués
# Observer les prédictions du modèle pour chaque donnée
for i in range(len(data)):
    point = data[i]
    print(point)
    # La prédiction de l'ordinateur
    z = point[0] * w1 + point[1] * w2 + b
    # La prediction entre 0 et 1
    pred = sigmoid(z)
    print("prediction : {}".format(pred))

def pred_fleur(lengh, width):
    if lengh and width < 0 or lengh <0 or width < 0:
        os.system("Say Impossible")
    z = lengh * w1 + width * w2 + b
    pred = sigmoid(z)
    if pred < 0.5:
        os.system("say Fleur bleue")
    else:
        os.system("Say Fleur rouge")

pred_fleur(4.5, 1)



