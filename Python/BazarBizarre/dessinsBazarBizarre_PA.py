from turtle import Screen, Turtle
import time

# Fonction permettant de dessiner la lettre A au coordonnées actuelles
def dessineA():
    turtle.seth(0)
    turtle.left(73.5)
    turtle.forward(103)
    turtle.right(147)
    turtle.forward(103)
    turtle.backward(40)
    turtle.right(106.5)
    turtle.forward(37)

# Fonction permettant de dessiner la lettre R au coordonnées actuelles
def dessineR():
    turtle.seth(0)
    turtle.left(90)
    turtle.forward(100)
    turtle.right(90)
    turtle.forward(30)
    for ra in range(18):
        turtle.forward(4.5)
        turtle.right(10)
    turtle.forward(33)
    turtle.backward(15)
    turtle.left(132)
    turtle.forward(65)

# Fonction permettant de dessiner la lettre S au coordonnées actuelles
def dessineS():
    turtle.seth(0)
    turtle.up()
    turtle.left(90)
    turtle.forward(100)
    turtle.right(90)
    turtle.forward(56)
    turtle.right(90)
    turtle.forward(5)
    turtle.right(180)
    turtle.down()
    # Début
    turtle.left(40)
    for sa in range(5):
        turtle.forward(2)
        turtle.left(10)
    turtle.forward(29)
    # Bas
    for sa in range(9):
        turtle.forward(3)
        turtle.left(10)
    turtle.forward(15)
    # Droite
    for sa in range(9):
        turtle.forward(3)
        turtle.left(10)
    turtle.forward(26)
    # Bas
    for sa in range(9):
        turtle.forward(3)
        turtle.right(10)
    turtle.forward(16)
    # Gauche
    for sa in range(9):
        turtle.forward(3)
        turtle.right(10)
    turtle.forward(26)
    # Haut
    for sa in range(9):
        turtle.forward(3)
        turtle.right(10)

# Fonction permettant de dessiner la lettre T au coordonnées actuelles
def dessineT():
    turtle.seth(0)
    turtle.left(90)
    turtle.up()
    turtle.forward(100)
    turtle.down()
    turtle.right(90)
    turtle.forward(60)
    turtle.backward(30)
    turtle.right(90)
    turtle.forward(100)

# Fonction permettant de dessiner la lettre W au coordonnées actuelles
def dessineW():
    turtle.seth(0)
    turtle.up()
    turtle.forward(-10)
    turtle.right(90)
    turtle.backward(100)
    turtle.down()
    # Début
    turtle.left(14)
    turtle.forward(103)
    # Haut
    turtle.left(152)
    turtle.forward(103)
    # Bas
    turtle.right(152)
    turtle.forward(103)
    # Haut
    turtle.left(152)
    turtle.forward(104)

# Fonction permettant de dessiner la lettre X au coordonnées actuelles
def dessineX():
    turtle.up()
    turtle.forward(10)
    x, y = turtle.position()
    turtle.goto(x, y+4)
    turtle.down()
    turtle.left(59)
    turtle.forward(116.5)
    turtle.left(121)
    turtle.up()
    turtle.forward(58)
    turtle.down()
    turtle.left(121)
    turtle.forward(116.5)

# Fonction permettant de dessiner le chiffre 1 au coordonnées actuelles
def dessine1(l):
    turtle.seth(0)
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.up()
    turtle.left(90)
    turtle.forward(l)
    turtle.right(90)
    turtle.forward(l/10)
    turtle.right(90)
    turtle.down()
    turtle.forward(l)

# Fonction permettant de dessiner le chiffre 2 au coordonnées actuelles
def dessine2(l):
    turtle.seth(0)
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.left(90)
    turtle.up()
    turtle.forward(l)
    turtle.down()
    turtle.right(90)
    turtle.forward(l/1.5)
    turtle.right(90)
    turtle.forward(l/2)
    turtle.right(90)
    turtle.forward(l/1.5)
    turtle.left(90)
    turtle.forward(l/2)
    turtle.left(90)
    turtle.forward(l/1.5)

# Fonction permettant de dessiner le chiffre 3 au coordonnées actuelles
def dessine3(l):
    turtle.seth(0)
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.left(90)
    turtle.up()
    turtle.forward(l)
    turtle.right(90)
    turtle.down()
    turtle.forward(l/1.5)
    turtle.right(90)
    turtle.forward(l/2)
    turtle.right(90)
    turtle.forward(l/2)
    turtle.backward(l/2)
    turtle.left(90)
    turtle.forward(l/2)
    turtle.right(90)
    turtle.forward(l/1.5)

# Fonction permettant de dessiner le chiffre 4 au coordonnées actuelles
def dessine4(l):
    turtle.seth(0)
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.left(90)
    turtle.up()
    turtle.forward(l)
    turtle.down()
    turtle.backward(l/2)
    turtle.right(90)
    turtle.forward(l/1.5)
    turtle.left(90)
    turtle.forward(l/2)
    turtle.backward(l)

# Fonction permettant de dessiner le chiffre 5 au coordonnées actuelles
def dessine5(l):
    turtle.seth(0)
    turtle.up()
    turtle.forward(10)
    turtle.down()
    turtle.left(90)
    turtle.up()
    turtle.forward(l)
    turtle.right(90)
    turtle.forward(l/1.5)
    turtle.down()
    turtle.backward(l/1.5)
    turtle.right(90)
    turtle.forward(l/2)
    turtle.left(90)
    turtle.forward(l/1.5)
    turtle.right(90)
    turtle.forward(l/2)
    turtle.right(90)
    turtle.forward(l/1.5)

# Fonction permettant de dessiner l'étoile de la mort
# On prend en paramètres 2 radius, les coordonnées et la couleur
def EtoileDeLaMort(r1, r2, x, y, c):
    turtle.color(c)
    turtle.seth(0)
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    turtle.circle(r1)
    turtle.up()
    turtle.goto(x,y+r1)
    turtle.forward(-r1)
    turtle.down()
    turtle.forward(r1*2)
    turtle.up()
    turtle.goto(x, y+r1+r2)
    turtle.down()
    turtle.circle(r2)

# Fonction permettant de dessiner les "cornes" du Faucon Millénium
# Cela correspond à des triangles sans le dernier côté
# On prend en paramètres une longueur et un string afin de définir si la corne est celle de droite ou de gauche
def CorneFaucon(l, d):
    if d == "droit":
        angle = [150,130]
        L = [-l, -l*2]
    if d == "gauche":
        angle = [285,50]
        L = [l, -l*2]
    for i in range(2):
            turtle.right(angle[i])
            turtle.forward(L[i])

# Fonction permettant de dessiner le rectangle à l'avant du Faucon Millénium.
# On prend en paramètre une longueur
def RectFaucon(l):
    L = [l, l*2, l, l*2]
    for i in range(4):
        turtle.left(90)
        turtle.forward(L[i])

# Fonction permettant de dessiner le Faucon Millénium
# On prend en paramètres 2 radius, une longueur, les coordonnées et la couleur
def FauconMillenium(r1, r2, l, x, y, c):
    turtle.color(c)
    turtle.seth(0)
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    turtle.circle(r1)
    turtle.up()
    turtle.goto(x, y+r1-r2)
    turtle.down()
    turtle.circle(r2)
    turtle.up()
    turtle.goto(x+r2,y)
    turtle.down()
    CorneFaucon(l, "droit")
    turtle.goto(x+r2,y)
    turtle.up()
    turtle.goto(x-r2,y)
    turtle.down()
    CorneFaucon(l, "gauche")
    turtle.goto(x-r2,y)
    turtle.seth(0)
    RectFaucon(-l/2)

# Fonction permettant de dessiner le cockpit du X-Wing qui correspond à un carré
# On prend en paramètre une longueur
def CockpitXwing(l):
    for i in range(4):
        turtle.forward(l)
        turtle.left(90)

# Fonction permettant de dessiner les ailes du X-Wing
# On prend en paramètres un longueur, un angle, un radius, les coordonnées et un string afin de définir si ce sont les ailes de droites ou de gauche
def AileXwing(l, angle, r, x, y, d):
    if d == "droit":
        turtle.up()
        turtle.goto(x+(l/6)+l,y+(l/2))
        turtle.down()
    if d == "gauche":
        turtle.up()
        turtle.goto(x+(l/6),y+(-l/2))
        turtle.down()
    turtle.left(angle)
    turtle.circle(r/2)
    turtle.forward(l*1.5)
    turtle.circle(r)

# Fonction permettant de dessiner un X-Wing
# On prend en paramètres une longueur, un radius, les coordonnées et la couleur
def XWing(l, r, x, y, c):
    turtle.color(c)
    turtle.seth(0)
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    CockpitXwing(l)
    AileXwing(l, 30, 10, x, y, "droit")
    AileXwing(l, -60, -10, x, y, "droit")
    turtle.seth(0)
    AileXwing(-l, 30, -10, x, y, "gauche")
    AileXwing(-l, -60, 10, x, y, "gauche")

# Focntion permettant de dessiner les ailes du Chasseur Stellaire
# On prend en paramètres une longueur, un angle, une orientation (une liste constitué d'angles), les coordonnées et un string afin de savoir si ce sont les ailes de droite ou de gauche
def AileChasseur(l, angle, orientation, x, y, d):
    turtle.seth(0)
    if d == "droit":
        turtle.up()
        turtle.goto(x+l,y+l)
        turtle.down()
        turtle.left(angle)
    if d == "gauche":
        turtle.up()
        turtle.goto(x+l,y-l)
        turtle.down()
        turtle.left(angle)
    turtle.forward(l*1.5)
    turtle.seth(orientation[0])
    turtle.forward(l/2)
    turtle.seth(orientation[1])
    turtle.forward(l)
    turtle.seth(orientation[2])
    turtle.forward(l/2)

# Fonction permettant de dessiner un chasseur Stellaire
# On prend en paramètres une longueur, 2 radius, les coordonnées et la couleur
def ChasseurStellaire(l, r1, r2, x, y, c):
    turtle.color(c)
    turtle.seth(0)
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    turtle.circle(r1)
    turtle.up()
    turtle.goto(x,y+r1-r2)
    turtle.down()
    turtle.circle(r2)
    orientationHaut = [270, 90, 150]
    orientationBas = [90, 270, 220]
    AileChasseur(r1, 15, orientationHaut, x, y, "droit")
    AileChasseur(r1, -15, orientationBas, x, y, "droit")
    AileChasseur(-r1, 15, orientationHaut, x, y, "gauche")
    AileChasseur(-r1, -15, orientationBas, x, y, "gauche")

# Fonction permettant de dessiner les pattes du TB-TT
# On prend en paramètres une longueur et un radius
def patteTBTT(l, r):
    turtle.seth(0)
    turtle.right(90)
    turtle.forward(l)
    turtle.right(90)
    turtle.circle(r,90) # Permet de faire un ovale
    turtle.left(90)
    turtle.forward(l-50)
    turtle.left(90)
    turtle.circle(r,90) # Permet de faire un ovale
    turtle.right(90)
    turtle.forward(l)

# Fonction permettant de dessiner un TB-TT
# On prend en paramètres une longueur, 2 angles (un plus grand que l'autre afin de dessiner les ovales), les coordonnées et la couleur
def TBTT(l, angleG, angleP, x, y, c):
    turtle.color(c)
    turtle.seth(0)
    turtle.up()
    turtle.goto(x,y)
    turtle.down()
    turtle.forward(l)
    turtle.seth(45)
    turtle.circle(angleP,90) # Permet de faire un ovale
    turtle.circle(angleG,90) # Permet de faire un ovale
    turtle.seth(180)
    turtle.circle(41,90)
    turtle.seth(180)
    turtle.forward(l/4)
    turtle.seth(0)
    turtle.forward(l-20)
    turtle.left(90)
    turtle.forward(l/2)
    turtle.seth(270)
    turtle.forward(l/2)
    patteTBTT(80, 10)
    turtle.up()
    turtle.goto(x+75,y)
    turtle.down()
    patteTBTT(80, 10)

# Fonction permettant de dessiner les pions
def dessinePions():
    color = ["white","red","orange", "blue", "green"]
    # On appelle la fonction dessinant l'étoile de la mort
    EtoileDeLaMort(50, 10, -450, 200, color[0])
    turtle.up()
    turtle.goto(-500, 297)
    turtle.down()
    dessine1(10)
    # On appelle la fonction dessinant le Faucon Millénium
    FauconMillenium(50, 10, 20, -275, 200, color[1])
    turtle.up()
    turtle.goto(-328, 297)
    turtle.down()
    dessine2(10)
    # On appelle la fonction dessinant un X-Wing
    XWing(40, 10, -100, 225, color[2])
    turtle.up()
    turtle.goto(-183, 297)
    turtle.down()
    dessine3(10)
    # On appelle la fonction dessinant un chasseur stellaire
    ChasseurStellaire(20, 30, 5, 150, 220, color[3])
    turtle.up()
    turtle.goto(63, 297)
    turtle.down()
    dessine4(10)
    # On appelle la fonction dessinant un TB-TT
    TBTT(85, 60, 30, 350, 260, color[4])
    turtle.up()
    turtle.goto(303, 297)
    turtle.down()
    dessine5(10)


# Permet de dessiner un rectangle
# On prend en paramètres une longueur, une hauteur et la couleur
def dessineRect(l, h, c):
    turtle.seth(0)
    turtle.color(c)
    turtle.down()
    value = [l,h,l,h]
    for i in value:
        turtle.forward(i)
        turtle.left(90)

# Permet de dessiner une carte vide avec un trait au milieu
# On prend en paramètres une longueur, un hauteur et les coordonnées
def dessineCarteVide(l, h, x, y):
    turtle.seth(0)
    # Dessin d'une carte vide que l'on remplit en noir pour remplacer le contenu précédent
    turtle.color("black")
    turtle.up()
    turtle.goto(x,y)
    turtle.begin_fill()
    dessineRect(l,h,"black")
    turtle.end_fill()
    # Dessin de la carte
    turtle.color("white")
    turtle.up()
    turtle.sety(y)
    dessineRect(l,h,"white")
    turtle.up()
    turtle.sety(y+200)
    turtle.down()
    turtle.forward(l)

# Fonction permettant de dessiner la carte avec les pions à l'intérieur
# On prend en paramètre la carte créée
def dessineCarte(carte):
    dessineCarteVide(250, 400, -500, -300)
    x = -400
    y = [-50, -220]
    for i in range(2):
        if carte[i][0] == "Etoile de la mort":
            EtoileDeLaMort(50, 10, x+10, y[i]-10, carte[i][1])
        elif carte[i][0] == "Faucon Millenium":
            FauconMillenium(50, 10, 20, x+10, y[i]-10, carte[i][1])
        elif carte[i][0] == "X-Wing":
            XWing(40, 10, x+10, y[i], carte[i][1])
        elif carte[i][0] == "Chasseur Stellaire":
            ChasseurStellaire(20, 30, 5, x+20, y[i]-20, carte[i][1])
        elif carte[i][0] == "TB-TT":
            TBTT(85, 60, 30, x, y[i]+50, carte[i][1])

def dessineStreak(streak, x, y):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.begin_fill()
    dessineRect(200,130, "black")
    turtle.end_fill()
    turtle.color(254, 27, 0)
    turtle.seth(0)
    turtle.width(5)
    dessineX()
    turtle.up()
    turtle.goto(x + 100, y)
    turtle.down()
    turtle.seth(0)
    if streak == 2:
        dessine2(100)
    else:
        dessine4(100)
    turtle.color("white")
    turtle.width(1)

def annuleStreak(x,y):
    turtle.up()
    turtle.goto(x, y-5)
    turtle.down()
    turtle.begin_fill()
    dessineRect(200,130, "black")
    turtle.end_fill()

# Fonction qui permet d'afficher le score
# On prend en paramètres le score, le nombre de points à ajouter et les coordonnées
def scoreUpdate(score, streak, x, y):
    score += streak
    turtle.up()
    turtle.goto(x,y)
    turtle.begin_fill()
    dessineRect(350,50, "black")
    turtle.end_fill()
    turtle.color("white")
    turtle.write("Votre score est de " + str(score) + " points", font = ("Times New Roman", 30, "italic"))
    return score

# Fonction qui permet d'afficher un texte
# On prend en paramètres un string qui correspond à une phrase et les coordonnées
def dessineTexte(texte, x, y):
    turtle.up()
    turtle.goto(x,y)
    turtle.begin_fill()
    dessineRect(400,50, "black")
    turtle.end_fill()
    turtle.color("white")
    turtle.write(texte, font = ("Times New Roman", 30, "italic"))

# Fonction permettant d'afficher une fenêtre demandant le choix du joueur
# Elle retourne le choix du joueur
def dessineChoix():
    return int(screen.numinput("Réponse", "Entre 1 et 5 (0 pour arreter)", 0, minval= 0, maxval=5))

# Fonction permettant d'afficher une fenêtre demandant le choix du joueur concernant l'écriture de son score dans un fichier
# Elle retourne le choix du joueur
def dessineChoixFichier():
    return screen.textinput("Voulez-vous enregistrer votre résultat ?", "'Oui' ou 'Non'")

# Fonction permettant d'afficher une fenêtre demandant le Pseudo du joueur
# Elle retourne le string associé
def dessineDemandeNom():
    return screen.textinput("Pseudo", "Quel est votre pseudo ?")

def dessineOutro(scores):
    turtle.clear()
    turtle.hideturtle()
    turtle.speed(0)
    y = 200
    turtle.color("white")
    for i in range(len(scores)):
        turtle.up()
        turtle.goto(int(-300*1/(len(scores)+1)), y - 30*(i+1)*2)
        turtle.down()
        turtle.write(scores[i], font = ("Times New Roman", int(60*1/(len(scores)+1)), "italic"))
        screen.update()
    time.sleep(5)

# Fonction qui permet de dessiner "Star Wars" en appelant les fonctions permettant de dessiner des lettres
# On prend un paramètres les coordonnées
def StarWars(x,y):
    turtle.width(3)
    turtle.color(229, 177, 58)
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    dessineS()
    turtle.up()
    turtle.goto(x+65, y)
    turtle.down()
    dessineT()
    turtle.up()
    turtle.goto(x+120, y)
    turtle.down()
    dessineA()
    turtle.up()
    turtle.goto(x+190, y)
    turtle.down()
    dessineR()
    turtle.up()
    turtle.goto(x, y-115)
    turtle.down()
    dessineW()
    turtle.up()
    turtle.goto(x+80, y-115)
    turtle.down()
    dessineA()
    turtle.up()
    turtle.goto(x+150, y-115)
    turtle.down()
    dessineR()
    turtle.up()
    turtle.goto(x+220, y-115)
    turtle.down()
    dessineS()
    turtle.width(1)

# Fonction permettant de dessiner les éléments du décor initial
def Board(score):
    # On affiche la tortue
    turtle.showturtle()
    # On désactive les animations
    screen.tracer(1)
    # On redéfinit le trait de la tortue sur 1
    turtle.width(1)
    # On définit une vitesse de dessin plus rapide
    turtle.speed(15)
    # Permet de passer en mode couleur pour donner des valeurs (r,g,b)
    screen.colormode(255)
    # On change la couleur pour du blanc car le fond est noir
    turtle.color("white")
    # On ajoute une forme à la liste des formes possibles
    screen.register_shape("spaceship", ((-10, 15), (0, 0), (10, 15), (-15, 0), (0, 20), (20, 0)))
    # On change la forme de base de turtle pour appliquer la forme "spaceship"
    turtle.shape("spaceship")
    # On appelle la fonction dessinant les pions
    dessinePions()
    # On appelle la fonction dessinant une carte vide
    dessineCarteVide(250, 400, -500, -300)
    # On appelle la fonction d'afficher le score
    score = scoreUpdate(score, 1, 50, 0)
    # On appelle la fonction d'afficher un texte
    dessineTexte("Bienvenue !", 50, -100)
    # On appelle la fonction dessinant le titre "Star Wars"
    StarWars(300, -225)
    return score

# Fonction permettant de dessiner les éléments de l'introduction
def Intro():
    # Fonction permettant d'afficher un texte
    def dessineIntro1():
        turtle.color(75, 213, 238)
        turtle.write("Il y a bien longtemps, dans une galaxie\nlointaine, très lointaine....",align= "center", font = ("Franklin Gothic Book", 30, "bold"))
    # Fonction permettant d'afficher un texte
    def dessineIntro2():
        turtle.color(229, 177, 58)
        turtle.write("La galaxie est menacée par un danger sans précédent.\n\nL'Empire et les forces rebelles sont corrompus.\n\nVous êtes le seul espoir de la galaxie.\n\nDes vaisseaux vont apparaïtre, vous devrez les détruire\n\nseulement s'ils correspondent aux vaisseaux modèles.\n\nLa galaxie compte sur vous!",align="center",font = ("Franklin Gothic Demi", 30, "bold"))

    # Permet de calibrer la musique sur l'apparition du logo
    time.sleep(2.5)
    # Permet de cacher la tortue pour dessiner plus vite
    turtle.hideturtle()
    # Permet d'activer les animations
    screen.tracer(0)
    # Permet de mettre la vitesse à 0 pour qu'il n'y ait pas d'animation de trait lors des déplacements
    turtle.speed(0)
    # Permet de grossir le trait de la tortue
    turtle.width(3)
    # Permet de passer en mode couleur pour donner des valeurs (r,g,b)
    screen.colormode(255)
    turtle.seth(90)
    t1 = time.time()
    t2 = time.time()
    while (t2-t1) < 4:
        turtle.clear()
        StarWars(-150,25)
        screen.update()
        t2 = time.time()
    turtle.goto(0, 0)
    turtle.seth(90)
    t1 = time.time()
    t2 = time.time()
    while (t2-t1) < 4:
        turtle.clear()
        dessineIntro1()
        screen.update()
        t2 = time.time()
    turtle.goto(0, -750)
    chrono = 0.0
    x, y = turtle.position()
    t1 = time.time()
    while y < 450.00:
        turtle.clear()
        dessineIntro2()
        t2 = time.time()
        chrono += (time.time() - t1)
        while t2-t1 > 0.01:
            screen.update()
            t1 = time.time()
            turtle.forward(1)
        x, y = turtle.position()


screen = Screen()

# Permet de définir la taille de la fenêtre qui va s'ouvrir
screen.setup(width=1280, height=720)
# Permet de changer le titre de la fenêtre
screen.title("Bazar Bizarre Version Star Wars !")
# Permet de changer le fond avec l'image "space.gif"
screen.bgpic("space.gif")

turtle = Turtle()
