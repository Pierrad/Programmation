import pygame
from pygame.locals import *
import math


nombre_sprite_cote = 21
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite
coordonnee_mur = []
coordonnee_arrivee = []

def generer(path):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""
		#On ouvre le fichier
		with open(path, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			structure = structure_niveau
			return structure


def afficher(structure, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load("mur.png").convert()
		depart = pygame.image.load("depart.png").convert()
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'd':
					fenetre.blit(mur, (x,y))
					coordonnee_mur.append((x,y))
				elif sprite == 'a':
					fenetre.blit(depart, (x,y))
					coordonnee_arrivee.append((x,y))
				num_case += 1
			num_ligne += 1


def from_coord_to_grid(pos):
    """Retourne la position dans le niveau en indice (i, j)

    `pos` est un tuple contenant la position (x, y) du coin supérieur gauche.
    On limite i et j à être positif.
    """
    x, y = pos
    i = max(0, int(x / 30))
    j = max(0, int(y / 30))
    return i, j

def get_neighbour_blocks(structure, i_start, j_start, what, k):
    """Retourne la liste des rectangles autour de la position (i_start, j_start).

    Vu que le personnage est dans le carré (i_start, j_start), il ne peut
    entrer en collision qu'avec des blocks dans sa case, la case en-dessous,
    la case à droite ou celle en bas et à droite.
    """
    blocks = list()
    for j in range(j_start, j_start+k):
        for i in range(i_start, i_start+k):
            if structure[j][i] == what:
                topleft = i*30, j*30
                blocks.append(pygame.Rect((topleft), (30, 30)))
    return blocks

# Gère les collisions
def collision(structure, pos, what):
    rect = pygame.Rect(pos, (30, 30))
    i, j = from_coord_to_grid(pos)
    for block in get_neighbour_blocks(structure, i, j, what, 2):
        if rect.colliderect(block):
            return True
    return False

'''
def distance (structure, pos, what):
	i, j = from_coord_to_grid(pos)
	blocks = get_neighbour_blocks(structure, i, j, what, 4)
	block_1 = min(blocks, key=lambda c: (c[0]- pos[0])**2 + (c[1]-pos[1])**2)
	blocks.remove(block_1)
	for i in blocks:
		if block_1[0] == blocks[i][0]:
			block_2 = block
		if block_1[1] == blocks[i][1]:
			block_2 = block

	# Position des deux blocs obtenus

	# Savoir si c'est celui de droite ou de gauche ?


	# Pour coté gauche, mur a gauche si valeur mur x est inférieur a celle de valeur x voiture
	# Pour coté haut, mur a gauche si valeur mur y est inférieur a celle de valeur y voiture
	# Pour coté droit, mur a gauche si valeur mur x est supérieur a celle de valeur x voiture
	# Pour coté bas, mur a gauche si valeur mur y est supérieur a celle de valeur y voiture

'''

# On initialise pygame et tout ses modules et on utilise pas pygame.init() car il plante
pygame.init()

# On définit une fenetre de 640*480 qui peut être resizé
fenetre = pygame.display.set_mode((cote_fenetre,cote_fenetre), RESIZABLE)

# Permet de rester appuyer, il attend 400ms avant de continuer si la touche reste enfoncée et 30 ms entre chaque déplacement
pygame.key.set_repeat(400, 30)

# On enregistre les états des touches
keystates = {'up':False, 'down':False, 'left':False, 'right':False}

live_states = True

# Boucle infinie pour garder la fenetre ouverte
continuer = 1
speed = 5


while continuer:
	# On charge une image et l'a convertit direct pour être utilisable par pygame
	fond = pygame.image.load("background.jpg").convert()
	# On applique le fond à la fenêtre à 0,0
	fenetre.blit(fond, (0,0))
	# On genère la structure
	structure = generer("map.txt")
	# On affiche la structure par rapport à la fenêtre
	afficher(structure, fenetre)
	# La police
	myfont = pygame.font.SysFont("monospace", 20)
	# render text
	i = 0
	label = myfont.render("Nombre de tour:" + str(i), 1, (0,0,0))
	fenetre.blit(label, (0, 0))
	proche = 0.0
	label1 = myfont.render("Distance:" + str(proche), 1, (0,0,0))
	fenetre.blit(label1, (0, 600))
	borne = 0
	# On récupère les coordonnée des images "départ"
	(o,p) = coordonnee_arrivee[1]
	# On load le perso en avant
	perso = pygame.image.load("Car_haut.png").convert_alpha()
	# On récupère sa position
	position_perso = perso.get_rect()
	# On update sa position sur les carrés de départ
	position_perso = position_perso.move(o,p)
	continuer_jeu = 1
	degree = 0
	# Le jeu démarre
	while continuer_jeu:
		# On parcours la liste de tous les événements reçus
		for event in pygame.event.get():
			# Si un de ces événements est de type QUIT
			if event.type == QUIT:
				# On arrête la boucle
				continuer = 0
				continuer_jeu = 0
			# On vérifie pour les events de types touches enfoncées
			if event.type == KEYDOWN:
				# Touche du haut
				if event.key == K_UP:
					keystates['up']=True
				# Touche du bas
				if event.key == K_DOWN:
					keystates['down']=True
				# Touche de gauche
				if event.key == K_LEFT:
					keystates['left']=True
				# Touche de droite
				if event.key == K_RIGHT:
					keystates['right']=True

			# On vérifie pour les events de types touches relachées
			if event.type == KEYUP:
				# Touche du haut
				if event.key == K_UP:
					keystates['up']=False
				# Touche du bas
				if event.key == K_DOWN:
					keystates['down']=False
				# Touche de gauche
				if event.key == K_LEFT:
					keystates['left']=False
				# Touche de droite
				if event.key == K_RIGHT:
					keystates['right']=False

		if keystates['left']:
			degree = degree + 5
			while degree > 359:
				degree -= 360

		if keystates['right']:
			degree = degree - 5
			while degree < 0:
				degree += 360

		dx = math.cos(math.radians(degree))
		dy = math.sin(math.radians(degree))

		# On sauvegarde l'ancienne position
		old_pos = position_perso

		if keystates['up']:
			# Nouvelle position
			position_perso = (position_perso[0] - int(speed * dy), position_perso[1] - int(speed * dx))

		if keystates['down']:
			# Nouvelle position
			position_perso = (position_perso[0] + int(speed * dy), position_perso[1] + int(speed * dx))

		# Si il y a collision on redonne les anciennes valeurs
		if collision(structure, (position_perso[0], position_perso[1]), 'd'):
			# position_perso = old_pos
			live_states = False
		# Si il y a collision avec les images d'arrivée
		if collision(structure, (position_perso[0], position_perso[1]), 'b'):
			borne = 1
		if collision(structure, (position_perso[0], position_perso[1]), 'c') and borne == 1:
			borne = 2
		if collision(structure, (position_perso[0], position_perso[1]), 'e') and borne == 2:
			borne = 3
		if collision(structure, (position_perso[0], position_perso[1]), 'a') and borne == 3:
			i = i + 1
			borne = 0


		# On colle les images à la fenetre
		fenetre.blit(fond, (0,0))
		afficher(structure, fenetre)
		perso2 = pygame.transform.rotate(perso, degree)
		if live_states == True:
			fenetre.blit(perso2, position_perso)
		else:
			label = myfont.render("Game Over! Restart ? Press 'R' ", 1, (0,0,0))
			fenetre.blit(label, (145, 350))
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_r:
						live_states = True
						continuer_jeu = 0

		#proche = distance(coordonnee_mur, (position_perso[0], position_perso[1]), 'a')
		label1 = myfont.render("Distance:" + str(proche), 1, (0,0,0))
		fenetre.blit(label1, (0, 600))
		label = myfont.render("Nombre de tour:" + str(i), 1, (0,0,0))
		fenetre.blit(label, (0, 0))
		# On met à jour la fenêtre
		pygame.display.flip()
