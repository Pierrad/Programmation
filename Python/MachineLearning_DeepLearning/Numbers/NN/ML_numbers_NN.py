# coding=utf-8
import numpy as np
import os
from PIL.Image import *
import random as rand

# Renvoi le maximum d'une liste
def Maximum(liste):
    max_ = liste[0]
    for item in liste:
        if item > max_:
            max_ = item
    return max_

# Renvoi la liste avec des valeurs dont la somme atteint 1, permet de faire des prédictions
def softmax(liste):
    z = [0 for x in range(len(liste))]
    for i in range(len(liste)):
        z[i] = liste[i] - Maximum(liste)
    numerator = np.exp(z)
    denominator = np.sum(numerator)
    softmax = numerator/denominator
    return softmax

# Dérivée de la softmax nécessaire pour la backpropagation
def softmax_d(liste):
    return softmax(liste) * (1 - softmax(liste))

# Fonction de coût adapté à la soft max, renvoie une liste
def cross_entropy_loss(list_target, list_pred):
        result = -sum(list_target * np.log(list_pred))
        return result

# Dérivée de la fonction de coût nécéssaire à la backpropagation
def cross_entropy_loss_d(list_target, list_pred):
        result = list_pred - list_target
        return result

def normalization(z):
    z = (z-0) / (255 - 0)
    return z

def initialisation():
    # Initialise les valeurs
    global a
    global e
    global z
    global y
    a = 0.0
    e = 0.0
    b = 0.0
    z = []
    y = 0.0

    # Network
    # Parametres des liaisons du début sont tous randoms
    w = [[0 for x in range(784)] for y in range(10)]
    for i in range(10):
        for j in range(784):
            random = np.random.randn()
            w[i][j] = random

    # Parametres de début sont randoms
    b = np.random.randn()
    return w, b

# La boucle d'entrainement
def training_loop(repet, learning_rate):
    w, b = initialisation()
    global z
    global y
    y = 0.0
    costs = []
    for i in range(repet):
        # Création de 10 neurones
        z = [0 for x in range(10)]
        # Création de la list pour contenir les 10 predictions
        pred = []
        # Genere un nombre aléatoire entre 0 et 9 pour dire dans quel dossier d'image aller
        img_random = rand.randint(0,9)
        # Genere la target en fonction du nombre random pour que cela corresponde
        target = [0 for x in range(10)]
        target[img_random] = 1
        # Permet de train plusieurs fois sur les mêmes data
        # Random point entre 0 et 59
        ri = np.random.randint(len(images_pixel_all[img_random]))

        # Fully connected layer pour 10 neurones
        for j in range(10):
            for i in range(784):
                y = float(images_pixel_all[img_random][ri][i]) * w[j][i]
                z[j] = z[j] + y
            z[j] = z[j] + b

        # Fonction softmax pour donner une prédiction selon les 10 neurones (10 chiffres)
        pred = softmax(z)
        # On arrondit à 5 chiffres après la virgule
        pred = pred.round(5)
        # Transforme numpy array en list normale
        pred = pred.tolist()

        # Cout et backpropagation en fonction de la pred pour chaque neurones
        for j in range(10):
            # La fonction cost pour déterminer le taux d'erreur
            cost = cross_entropy_loss(target, pred)
            # Ajouter 'cost' à la liste costs
            costs.append(cost)
            # Derivée partielle du cout en fonction de la prediction
            dcost_pred = cross_entropy_loss_d(target[j], pred[j])
            # Derivée partielle de la prediction en fonction de z
            dpred_dz = softmax_d(z)
            # Transforme numpy array en list normale
            dpred_dz = dpred_dz.tolist()
            # Derivée partielle de z en fonction de w[i]
            # Derivée partielle du cout en fonction de w[i]
            dz_dw = []
            dcost_dw = []
            # Calculs des nouveaux paramètres de w[i]
            for i in range(784):
                derivee = float(images_pixel_all[img_random][ri][i])
                dz_dw.append(derivee)
                somme = dcost_pred * dpred_dz[j] * dz_dw[i]
                dcost_dw.append(somme)
                w[j][i] = w[j][i] - learning_rate * dcost_dw[i]
            # Derivée partielle de z en fonction de b
            dz_db = 1
            # Derivée partielle du cout en fonction de b
            dcost_db = dcost_pred * dpred_dz[j] * dz_db
            # Calcul des nouveauxparamètres de b
            b = b - learning_rate * dcost_db
    return w, b

# Chargement de toutes les images et tout les pixels parmi tous les dossiers dans images_pixel_all
images_pixel_all = []
# Boucle pour les 10 dossiers
for j in range(10):
    # Création des différentes listes
    images = []
    pixel = []
    images_pixel = []
    # Boucle pour les X images qu'il y a dans chaque dossier
    for i in range(5000):
        # Ouverture de fichier
        var = "trainingSample/"+ str(j)+ "/" + str(i) + ".jpg"
        files = open(var, "r")
        images.append(files)
        # On récupère la taille de chaque image
        point = images[i]
        (l, h) = point.size
        # On récupère chaque pixel que l'on normalise pour pas atteindre de trop grandes valeurs que l'on place dans images_pixel
        for y in range(h):
            for x in range(l):
                c = Image.getpixel(point, (x, y))
                #c = normalization(c)
                pixel.append(c)
        images_pixel.append(pixel)
        print("Ok image", i)
        # On ferme le fichier
        files.close()

    # On place images_pixel dans images_pixel_all
    images_pixel_all.append(images_pixel)


# Maintenant les paramètres de liaisons w[i], b sont correctement évalués

# Observer les prédictions du modèle pour chaque images de chaque dossiers
# Chaque dossier
'''
for e in range(10):
    print("----------------------------------- {}".format(e))
    # Chaque images du dossier
    for i in range(60):
        # Fully connected layer
        # Initialise valeurs
        z = [0 for x in range(10)]
        y = 0
        # Pour chacun des 10 neurones (car 10 images)
        for k in range(10):
            # Pour chaque pixels (h*l)
            for j in range(784):
                y = float(images_pixel_all[e][i][j]) * w[k][j]
                z[k] = z[k] + y
            z[k] = z[k] + b
        # Le calcul de la prediction avec la fonction softmax
        pred = softmax(z)
        # On affiche la prédiction
        print("prediction : {}".format(pred))
'''

# On test le réseau de neurones
def pred_number(path, real, w, b):
    # Initialise les valeurs
    global a
    a = [0 for x in range(10)]
    global e
    e = 0
    pixel = []
    images_pixel = []
    # Ouverture du fichier
    files = open(path, "r")
    # On récupère la taille
    (l, h) = files.size
    # On récupère les pixels et on les places dans images_pixels
    for y in range(h):
        for x in range(l):
            c = Image.getpixel(files, (x, y))
            c = c / 255
            pixel.append(c)
    images_pixel.append(pixel)
    # On ferme le fichier
    files.close()
    # Fully connected layer pour 10 neurones et 784 liaisons par neurones
    for j in range(10):
        for i in range(784):
            e = float(images_pixel[0][i]) * w[j][i]
            a[j] = a[j] + e
        a[j] = a[j] + b
    # Le calcul de la prediction par la fonction softmax (Avoir une prediction pour 10 chiffres qui atteint 1)
    pred = softmax(a)
    # On arrondit à 5 chiffres après la virgule
    pred = pred.round(5)
    # Transforme numpy array en list normale
    pred = pred.tolist()
    # On récupère l'indice du max de la liste qui correspond à la prédiction du chiffre
    valeurs_images = pred.index(Maximum(pred))
    result = 0
    if valeurs_images == real:
        result = 1
    else:
        result = 0
    # On affiche cette prédiction
    #print("C'est un {}".format(valeurs_images))
    return result

# Entrainement pour toutes les données avec tout les paramètres
epoch = [100,500,1000, 5000, 10000, 15000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
nbrLearn = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
maxT = 0
bestEpoch = 0
bestNbr = 0
for k in range(len(epoch)):
    for l in range(len(nbrLearn)):
        w, b = training_loop(epoch[k], nbrLearn[l])
        print("/////////////////////////////////////////////////////////////////////////////////////////")
        print("Avec les paramètres suivants : ", epoch[k], " et ", nbrLearn[l], " on a : ")
        # Prédictions par rapport aux dossiers d'images de test
        nbrInDossier = 29
        nbrAll = 349
        resultF = 0
        for i in range(10):
            result = 0
            for j in range(30):
                path = "testSample/" + str(i) + "/" + str(j) + ".jpg"
                res = pred_number(path, i, w, b)
                result += res
            resultF += result
            result = round(((result / nbrInDossier)*100),2)
            print("Pour le chiffre " + str(i) + " la réussite est de : ", result, "%")
        resultF = round(((resultF/nbrAll)*100),2)
        print("Le total de réussite est de : ", resultF, "%")
        if resultF > maxT:
            maxT = resultF
            bestEpoch = epoch[k]
            bestNbr = nbrLearn[l]

print("Avec un score de : ", maxT, " %, les meilleures paramètres sont : ", bestEpoch, " et ", bestNbr)