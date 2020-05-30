import sqlite3

import sqlite3

#Connexion
connexion = sqlite3.connect('basededonnees.db')

#Récupération d'un curseur
curseur = connexion.cursor()

#Création de la table mots
curseur.execute("""
    CREATE TABLE IF NOT EXISTS mots(
    mot TEXT,
    nbr INTEGER);
    """)

#Suppression des éléments de mots
curseur.execute("""DELETE FROM mots""")

#Préparation des données à ajouter
donnees = [
    ("Bonjour", 1),
    ("Coucou", 2),
    ("Salut", 3),
    ("Hola", 4),
    ("Hello", 5),
    ("Yo", 6)
    ]

#Insertion des données
curseur.executemany('''INSERT INTO mots (mot, nbr) VALUES (?, ?)''', donnees)

#Validation
connexion.commit()


#On affiche une données
mot1 = "Test"
curseur.execute("SELECT mot FROM mots WHERE mot = ?", [mot1])
print(curseur.fetchmany())

Lecture de nos données
curseur.execute("SELECT * FROM mots")
for resultat in curseur:
    print(resultat)

#Validation des donnees / envoi
connexion.commit()

curseur.close()
connexion.close()  #Déconnexion

