compteur = 0
'''
with open("message.html") as fichier:
    for line in fichier:
        if " 2015 " in line:
            compteur = compteur + 1

print(compteur)

'''
file = open("message.txt", "r")
message = file.read()
print(message.count("2018"))