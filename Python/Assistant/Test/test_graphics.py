from tkinter import *

#creer une fenetre
fenetre = Tk()

#creation variable tkinter
var_texte = StringVar()

#label = ligne de texte
champ_label = Label(fenetre, text="yo")

#création bouton quitter avec commande de quit
bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)

#creation ligne de texte 
ligne_texte = Entry(fenetre, textvariable=var_texte, width=30)

#affiche le label dans la fenetre
champ_label.pack()

#afficher le bouton quitter
bouton_quitter.pack()

#affichage ligne de texte 
ligne_texte.pack()

#boucle tkinter
fenetre.mainloop()
