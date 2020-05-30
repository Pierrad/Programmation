from PIL import Image

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

# ConvLayer en fonction de la matrice de filtre
def conv_layer(h, l, filter_size, matrice, basic_image, new_image, stride):
	mat = define_list(filter_size, filter_size)
	for i in range(h-filter_size + 1):
		for j in range(l-filter_size + 1):
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



# Ouverture et récupération des dimensions de l'image
files = Image.open("../NN/trainingSample/0/0.jpg")
(l, h) = files.size

# Définit la taille de la liste en fonction des dimensions de l'image 
basic_image = define_list(h, l)

# Définit la nouvelle image sur la même taille que la basique pour être sûr (pas besoin normalement d'aussi grand)
new_image = define_list(h, l)

# Remplit la liste avec tous les pixels de l'image
for a in range(h):
	for b in range(l):
		d = Image.Image.getpixel(files, (a, b))
		basic_image[a][b] = d

# On choisit la taille du filtre et définit son carré
filter_size = 3
filter_size_pow = filter_size * filter_size

# On attribut la matrice nécéssaire 
if filter_size == 3:
	matrice = matrice_all_edge

#if filter_size == 4:
	# A définir

# On définit le stride (le décalage entre chaque calcul de matrice * filtre)
stride = 1
# Nouvelle image après passage dans un ConvLayer
new_image = conv_layer(h, l, filter_size, matrice, basic_image, new_image, stride)

# La taille de la petite matrice pour choisir la plus grande valeur, ici choix parmi 2*2
pool_nbr = 2
# Nouvelle image après passage dans un Pooling max
new_image = max_pooling(h, l, pool_nbr, new_image)

# On met tout sous une seule liste
new_image_list = []
x = 0
y = 0
for x in new_image:
	for y in x:
		new_image_list.append(y) 

# Définit la nouvelle image sur la même taille que la basique, avec une couleur blanche et en mode L (mode 8 bytes, nb)
new_files = Image.new("L", files.size, "white")

# Place la liste avec tous les pixels dans la nouvelle image
new_files.putdata(new_image_list)

# Sauvegarde l'image
new_files.save("new_image1.png")

# Fermeture du fichier
files.close()
new_files.close()
