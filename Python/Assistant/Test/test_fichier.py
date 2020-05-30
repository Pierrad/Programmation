import re
from os import system
import os
'''
# Chercher exactement un mot dans le fichier
fichier = open("world-cities.csv", "r")
for word in fichier:
    if re.match("est,", word):
        print (word)

fichier.close()
'''
'''
#Chercher tout les mots qui contiennent 'paris' dans le fichier
fichier = open("world-cities.csv", "r")
for word in fichier:
    if 'est,' in word:
        print (word)
fichier.close()
'''


chaine = "souviens-toi des cours demain" 
if chaine.find('souviens-toi') != -1 or chaine.find('rappelle-toi') != -1 or chaine.find('rappelle-moi') != -1:
    fichier = open("Souvenir.txt", "a")
    if chaine.find('souviens-toi') != -1:
        chaine = chaine.replace('souviens-toi ', '')
    if chaine.find('rappele-toi') != -1:
        chaine = chaine.replace('rappelle-toi ', '')
    if chaine.find('rappele-moi') != -1:
        chaine = chaine.replace('rappelle-moi ', '')
    if os.path.getsize("Souvenir.txt") == 0:
        fichier.write(chaine + "\n")
    else:
        fichier.write("\n" + chaine + "\n")
    fichier.close()



chaine1 = "De quoi dois-je me souvenir ou me rappeler ?"
chaine2 = "oui"
if chaine1.find('souvenir') != -1 or chaine1.find('rappeler') != -1:
        fichier = open("Souvenir.txt", "r")
        lectures = fichier.readlines()
        system("Say Je me rappelle : ")
        for lecture in lectures:
                var = "Say " + lecture
                system(var)
        fichier.close()
        #tout supprimer
        if chaine2.find("oui") != -1:
                guess = start()
                i = char_to_int(guess["transcription"])
                lectures.remove(lectures[i])
                with open("Souvenir.txt", "w") as fichier:
                        for lecture in lectures:        
                                fichier.write(lecture)
        fichier.close()

def char_to_int(chiffre_char):

        if chiffre_char.find('un') != -1:
                chiffre_char = 0
        if chiffre_char.find('deux') != -1:
                chiffre_char = 1
        if chiffre_char.find('trois') != -1:
                chiffre_char = 2
        if chiffre_char.find('quatre') != -1:
                chiffre_char = 3
        if chiffre_char.find('cinq') != -1:
                chiffre_char = 4
        if chiffre_char.find('six') != -1:
                chiffre_char = 5
        if chiffre_char.find('sept') != -1:
                chiffre_char = 6
        if chiffre_char.find('huit') != -1:
                chiffre_char = 7
        if chiffre_char.find('neuf') != -1:
                chiffre_char = 8
        if chiffre_char.find('dix') != -1:
                chiffre_char = 9

return chiffre_char