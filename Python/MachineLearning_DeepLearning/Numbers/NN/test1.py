# coding=utf-8
import numpy as np
import os
from PIL import Image
import random as rand


# Fonction pour le produit matriciel de deux matrices
def produitMatriciel(A,B):
	result = [[0 for x in range(len(A))] for y in range(len(A))]
	for i in range(len(A)):
		for j in range(len(A)):
			result[i][j] = A[i][j] * B[i][j]
	return result

# Fonction pour la somme matricielle de deux matrices
def sommeMatricielle(A,B):
	result = [[0 for x in range(len(A))] for y in range(len(A))]
	for i in range(len(A)):
		for j in range(len(B)):
				result[i][j] = A[i][j] + B[i][j]
	return result

# Renvoie une valeur égale à 0
def reLU_function(pixel):
	pixel = 0
	return pixel

# Renvoie la valeur max de la matrice
def max_nbr_matrice(mat, nrb_pool):
	max_value = mat[0][0]
	for i in range(nrb_pool):
		for j in range(nrb_pool):
			if mat[i][j] > max_value:
				max_value = mat[i][j]
	return max_value

# Renvoie une liste double
def define_list(h, l):
	new_list = [[0 for x in range(h)] for y in range(l)]
	return new_list

# Transforme une liste double à un élément en liste double à multiple élément
def change(my_liste, new_liste):
    k = 0
    for l in range(28):
        for j in range(28):
            new_liste[0+l][j] = my_liste[0][j+k]
        k = k + 28
    return new_liste


# ConvLayer en fonction de la matrice de filtre
def conv_layer(h, l, filter_size, matrice, basic_image, new_image, stride):
	mat = define_list(filter_size, filter_size)
	for i in range(h-filter_size -1):
		for j in range(l-filter_size - 1):
			for a in range(filter_size):
				for b in range(filter_size):
					# On créer une matrice de transition
					mat[a][b] = basic_image[i+a][j+b]
			# Le produit
			pixel_mat = produitMatriciel(mat, matrice)
			# La somme
			for c in range(filter_size):
				for d in range(filter_size):
					new_image[i][j] = new_image[i][j] + pixel_mat[c][d]
			# Une Moyenne
			new_image[i][j] = new_image[i][j] / 9
			# Passe les valeurs négative en 0, reLU fonction
			if new_image[i][j] < 0:
				new_image[i][j] = reLU_function(new_image[i][j])
				# On applique le stride
			j = j + stride - 1
		i = i + stride - 1
	return new_image

# Pooling de type max, garde la plus grande valeur parmi toutes celles de la matrice de taille pool_nbr
def max_pooling(h, l, pool_nbr, new_image):
	mat = define_list(pool_nbr, pool_nbr)
	for i in range(h-pool_nbr):
		for j in range(l-pool_nbr):
			for a in range(pool_nbr):
				for b in range(pool_nbr):
					# On créer une matrice de transition
					mat[a][b] = new_image[i+a][j+b]
			new_image[i][j] = max_nbr_matrice(mat, pool_nbr)
			# Passe les valeurs négative en 0, reLU fonction
			if new_image[i][j] < 0:
				new_image[i][j] = reLU_function(new_image[i][j])
	return new_image


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

# La matrice
matrice = []

# Matrice 3*3 pour ressortir les contours
matrice_all_edge = [[-1, -1, -1],
		   			[-1,  8,  -1],
		   			[-1, -1, -1]]

# Matrice 3*3 pour ressortir certain contours
matrice_edge_1 = [[0, 1, 0],
		 		[1, -4, 1],
		 		[0, 1, 0]]

# On choisit la taille du filtre et définit son carré
filter_size = 3
filter_size_pow = filter_size * filter_size

# On attribut la matrice nécéssaire
if filter_size == 3:
	matrice = matrice_all_edge


# Chargement de toutes les images et tout les pixels parmi tous les dossiers dans images_pixel_all
images_pixel_all = []

# Boucle pour les 10 dossiers
for j in range(10):
    # Création des différentes listes
    images = []
    pixel = []
    images_pixel = []
    images_pixel_images = []
    # Boucle pour les X images qu'il y a dans chaque dossier
    for i in range(5000):
        # Ouverture de fichier
        var = "trainingSample/"+ str(j)+ "/" + str(i) + ".jpg"
        files = Image.open(var, "r")
        images.append(files)
        # On récupère la taille de chaque image
        point = images[i]
        (l, h) = point.size
        # On récupère chaque pixel que l'on normalise pour pas atteindre de trop grandes valeurs que l'on place dans images_pixel
        for y in range(h):
            for x in range(l):
                c = Image.Image.getpixel(point, (x, y))
                c = c / 255
                pixel.append(c)
        images_pixel.append(pixel)

        # On définit le stride (le décalage entre chaque calcul de matrice * filtre)
        stride = 1
        # Définit la nouvelle image pour le ConvLayer sur la même taille que la normale
        images_pixel_for_conv = define_list(h,l)
        # Définit la liste pour la nouvelle image
        new_image = define_list(h, l)
        # On rend compatible les deux listes (liste de liste de 784 éléments en liste de liste de 28 par 28 éléments)
        images_pixel_for_conv = change(images_pixel, images_pixel_for_conv)
        # Nouvelle image après passage dans un ConvLayer
        new_image = conv_layer(h, l, filter_size, matrice, images_pixel_for_conv, new_image, stride)
        # La taille de la petite matrice pour choisir la plus grande valeur, ici choix parmi 2*2
        pool_nbr = 2
        # Nouvelle image après passage dans un Pooling max
        new_image = max_pooling(h, l, pool_nbr, new_image)
        new_image1 = define_list(h, l)
        new_image1 = conv_layer(h, l, filter_size, matrice, new_image, new_image1, stride)
        new_image1 = max_pooling(h, l, pool_nbr, new_image1)
        # On met tout sous une seule liste
        new_image_list = []
        x = 0
        y = 0
        for x in new_image1:
            for y in x:
                new_image_list.append(y)
        # On ferme le fichier
        files.close()
        # On met chaque image dans une plus grande liste contenant toutes les images d'un dossier
        images_pixel_images.append(new_image_list)
    # On place images_pixel dans images_pixel_all
    images_pixel_all.append(images_pixel_images)
    print("Ok dossier", j)

# Maintenant les paramètres de liaisons w[i], b sont correctement évalués

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
    files = Image.open(path, "r")
    # On récupère la taille
    (l, h) = files.size
    # On récupère les pixels et on les places dans images_pixels
    for y in range(h):
        for x in range(l):
            c = Image.Image.getpixel(files, (x, y))
            c = c / 255
            pixel.append(c)
    images_pixel.append(pixel)
    # On définit le stride (le décalage entre chaque calcul de matrice * filtre)
    stride = 1
    # Définit la nouvelle image pour le ConvLayer sur la même taille que la normale
    images_pixel_for_conv = define_list(h,l)
    # Définit la liste pour la nouvelle image
    new_image = define_list(h, l)
    # On rend compatible les deux listes (liste de liste de 784 éléments en liste de liste de 28 par 28 éléments)
    images_pixel_for_conv = change(images_pixel, images_pixel_for_conv)
    # Nouvelle image après passage dans un ConvLayer
    new_image = conv_layer(h, l, filter_size, matrice, images_pixel_for_conv, new_image, stride)
    # La taille de la petite matrice pour choisir la plus grande valeur, ici choix parmi 2*2
    pool_nbr = 2
    # Nouvelle image après passage dans un Pooling max
    new_image = max_pooling(h, l, pool_nbr, new_image)
    new_image1 = define_list(h, l)
    new_image1 = conv_layer(h, l, filter_size, matrice, new_image, new_image1, stride)
    new_image1 = max_pooling(h, l, pool_nbr, new_image1)
    # On met tout sous une seule liste
    new_image_list = []
    x = 0
    y = 0
    for x in new_image1:
        for y in x:
            new_image_list.append(y)
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