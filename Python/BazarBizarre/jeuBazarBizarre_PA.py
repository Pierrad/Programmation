##########################################################
# Mini projet bazar bizarre : utilitaires sur les cartes #
##########################################################

###### Import des modules utiles
import random # module permettant de generer des nombres aleatoires
import time # module permettant de calculer le temps de réponse
import datetime # module permettant de récupérer la date et l'heure d'aujourd'hui
import dessinsBazarBizarre_PA # module contenant les foncions permettant de faire les différents dessins
from playsound import playsound # module permettant de jouer la musique
import sys # module permettant de lire les arguments passés dans la ligne de commande

###### Definition des fonctions

# fonction qui construit une carte (liste de 2 personnages) en prenant, au hasard, les formes dans f (liste des formes possibles) et les couleurs dans c (liste des couleurs possibles)
def construitCarte(f, c):
    proba = 0.3 # probabilite de generer une carte contenant un pion (plus la proba est haute et plus le jeu est facile)
    carte = [] # carte (au départ liste vide)
    pion = False # la carte ne contient pas de pion
    if random.random() < proba: # si le nombre aleatoire est inferieur a la proba predefinie (la carte contiendra un pion)
        indicePion = random.randint(0, len(f)-1) # on tire aleatoirement un indice dans la liste des formes pour determiner le pion qui sera sur la carte
        carte.append([f[indicePion], c[indicePion]]) # on ajoute le pion choisi a la carte
        pion = True # la carte contient un pion
    # ajout du deuxieme personnage (non pion) si un pion a ete ajoute sur la carte ou ajout de deux personnages (non pions) si la carte est toujours vide
    ajouteNonPion(carte, pion, f, c) # pion vaut True si la carte contient deja un pion
    return carte


# fonction qui complete une carte contenant un pion ou rien (par un ou 2 personnages non pions)
# il faut gérer la liste des indices deja utilises car il ne doit y avoir qu'une réponse juste
def ajouteNonPion(carte, pion, f, c): # pion vaut True si la carte contient deja un pion
    l=len(f)
    indices =[] # liste des indices deja utilises pour creer la carte (vide au depart)
    n = 2 # par defaut, 2 personnages a ajouter a la carte
    if pion: # s'il y a deja un pion sur la carte (pion vaut True)
        n -= 1 # plus qu'un personnage a ajouter
        indicePion = f.index(carte[0][0]) # on regarde de quel pion il s'agit (indice dans la liste f de la forme du premier personnage de la carte)
        indices.append(indicePion)
    # pour chaque personnage, on doit tirer 2 indices differents (un pour la forme et un pour la couleur) qui ne sont pas deja dans la liste des indices choisis
    while n > 0:
        ind = random.randint(0,l-1)
        if not ind in indices:
            ind2 = random.randint(0,l-1)
            if ind != ind2 and not ind2 in indices:
                carte.append([f[ind],c[ind2]])
                indices.append(ind)
                indices.append(ind2)
                n -= 1
    return carte


# procédure qui affiche les pions disponibles à partir de la liste des formes et de la liste des couleurs
def affichePions(f,c):
    print("Voici les pions disponibles: ")
    i = 0
    while i < len(c): # f et c sont de même longueur
        print(str(i+1) + ": " + f[i] + " " + c[i]) # affiche tous les pions dispos (couples couleur/objet au meme indice)
        i += 1

# procédure qui affiche la carte tirée
def afficheCarte(carteTiree):
    print("Voici la carte tirée: ")
    for perso in carteTiree:
        print("\t |" + perso[0] + " " + perso[1])

# fonction qui renvoie True si la carte contient un pion
def pion(carteTiree, f, c):
    for pers in carteTiree: # pour chaque personnage (sous-liste) de la carte
        if f.index(pers[0]) == c.index(pers[1]): # on regarde si l'indice de la forme (dans la liste des formes) est identique à l'indice de la couleur (dans la liste des couleurs)
            return True # ce qui signifie qu'il s'agit d'un pion
    return False


# fonction qui verifie si le choix de pion de l'utilisateur (entier) est correct par rapport à la carte tirée
def verifReponse(carteTiree, choix, f, c):
    pionChoisi = [f[choix-1],c[choix-1]] # convertit le choix (entier) en pion (liste forme/couleur)
    if pion(carteTiree, f, c): # si un pion se trouve dans la carte (la fonction pion renvoie True)
        return(pionChoisi in carteTiree) # le pion choisi doit être présent dans la carte
    else: # si la carte ne contient pas de pion
        for perso in carteTiree: # on vérifie que pour chaque personnage de la carte
            if perso[0] == pionChoisi[0] or perso[1] == pionChoisi[1]: # la forme du personnage n'est pas égale à celle du pion choisi et idem pour la couleur
                return False
        return True

# Fonction permettant de gérer la lecture et écriture dans un fichier
# On prend en paramètres le pseudo du joueur, son score, et si l'on veut ou pas écrire le résultat dans un fichier
# La fonction renvoit une liste contenant l'historique des joueurs et scores du fichier texte
def Fichier(nom, score, ecriture):
    # Si on veut écrire, alors on écrit le pseudo, le score et la date
    # Puis on se remet au début du fichier et on lit l'entièreté des lignes du fichier
    if ecriture == "oui":
        with open("scores.txt", "a+") as fichier:
            # On récupère la date d'aujourd'hui et l'heure actuelle mais on a pas besoin des milli secondes, donc on ne garde seulement que ce qu'il y a avant le point
            fichier.write(nom + "  " + str(score) + "    " + str(datetime.datetime.now()).split(".")[0] + "\n")
            fichier.seek(0)
            lines = fichier.readlines()
        return lines
    # Si on veut simplement lire et renvoyer la liste comportant l'historique
    else:
        with open("scores.txt", "w+") as fichier:
            lines = fichier.readlines()
        return lines


###### Programme principal

# variables globales
formes = ["Etoile de la mort","Faucon Millenium","X-Wing","Chasseur Stellaire","TB-TT"]
couleurs = ["white","red","orange", "blue", "green"]

timeout = 6 # temps de reponse autorise

# Si l'argument 1 de la ligne de commande est "musique" alors on peut lancer la musique

if "musique" in sys.argv:
    # Fonction permettant de jouer en background (avec le Second paramètre "0") une musique
    # Permet de lancer la musique d'intro du jeu
    playsound("Intro.mp3", 0)
# Affichage de l'introduction
dessinsBazarBizarre_PA.Intro()
# Score
score = -1
# Streak
streak = 0
# Si l'argument 1 de la ligne de commande est "musique" alors on peut lancer la musique
if "musique" in sys.argv:
    # Permet de lancer le thème du jeu en arrière plan
    playsound('theme.mp3', 0)
# Affichage du board classique
score = dessinsBazarBizarre_PA.Board(score)
# appel des fonctions - boucle de jeu
continuer = True
while continuer: # tant que continuer vaut True (passe à False si l'utilisateur répond 0)
    carte = construitCarte(formes, couleurs) # construit une carte au hasard (liste de 2 personnages)
    # Affichage de la carte
    dessinsBazarBizarre_PA.dessineCarte(carte)
    t1 = time.time() # t1 est "l'heure" à ce moment là (avant la réponse de l'utilisateeur)
    # On récupère le choix du joueur
    i = dessinsBazarBizarre_PA.dessineChoix()
    if i == 0 : # le joueur veut arrêter
        dessinsBazarBizarre_PA.dessineTexte("Votre score est de : " + str(score), 50, -100)
        time.sleep(2)
        # On demande au joueur s'il veut enregistrer son score dans fichier
        if dessinsBazarBizarre_PA.dessineChoixFichier() == "Oui":
            # On demande son nom
            pseudo = dessinsBazarBizarre_PA.dessineDemandeNom()
            # On appelle la fonction pour enregistrer dans un fichier texte et on récupère les lignes du fichier
            historique = Fichier(pseudo, score, "oui")
        # Si le joueur ne veut pas enregistrer son score, on récupère juste les lignes avec l'historiques des joueurs et scores.
        else:
            historique = Fichier("", score, "non")
        # Si le fichier n'est pas vide
        if len(historique) > 0:
            # On appelle la fonction permettant d'afficher l'historique des joueurs et scores.
            dessinsBazarBizarre_PA.dessineOutro(historique)
        # Si le fichier est vide
        else:
            print("Pas de score enregistré")
            # On efface tout ce qu'il y a sur l'écran
            dessinsBazarBizarre_PA.turtle.clear()
            # On dessine le texte suivant
            dessinsBazarBizarre_PA.dessineTexte("Pas de score enregistré", -150, 0)
            # On met en pause le programme pour laisser un temps de lecture
            time.sleep(5)
        continuer = False
        print("----\nFin du jeu")
        print("Votre score est de : " + str(score) + "\n----")
    else: # le joueur veut continuer
        t2 = time.time() # t2 est "l'heure" à ce moment là (après la réponse de l'utilisateur
        if t2 - t1 < timeout : # t2 - t1 est le temps de réponse de l'utilisateur
            if verifReponse(carte, i, formes, couleurs): # si la fonction verifReponse renvoie True
                streak += 1
                # Si le joueur enchaine les bonnes réponses, on double puis quadruple son nombre de points reçus
                if 5 > streak >= 3:
                    # On update le score à l'écran
                    score = dessinsBazarBizarre_PA.scoreUpdate(score, 2, 50, 0)
                    # On affiche "x2" pour indiquer au joueur son streak
                    dessinsBazarBizarre_PA.dessineStreak(2, 0, -300)
                elif streak >= 5:
                    # On update le score à l'écran
                    score = dessinsBazarBizarre_PA.scoreUpdate(score, 4, 50, 0)
                    # On affiche "x4" pour indiquer au joueur son streak
                    dessinsBazarBizarre_PA.dessineStreak(4, 0, -300)
                else:
                    # On update le score à l'écran
                    score = dessinsBazarBizarre_PA.scoreUpdate(score, 1, 50, 0)
                    dessinsBazarBizarre_PA.annuleStreak(0, -300)
                # On affiche le texte suivant
                dessinsBazarBizarre_PA.dessineTexte("Bonne réponse :)", 50, -100)
            else:
                streak = 0
                dessinsBazarBizarre_PA.annuleStreak(0, -300)
                # On affiche le texte suivant
                dessinsBazarBizarre_PA.dessineTexte("Mauvaise réponse :(", 50, -100)
        else:
            streak = 0
            dessinsBazarBizarre_PA.annuleStreak(0, -300)
            # On affiche le texte suivant
            dessinsBazarBizarre_PA.dessineTexte("Vous avez trop tardé à répondre!", 50, -100)

