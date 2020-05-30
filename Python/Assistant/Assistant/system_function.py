import socket
import os 
import pyttsx3 

def Check_connexion(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


def wifi_on(): 
    os.system("networksetup -setairportpower airport on")

def wifi_off():
    os.system("networksetup -setairportpower airport off")


def open_app(guess):
    #J'enlève le mot 'ouvre' 
    guess["transcription"] = guess["transcription"].replace('ouvre ','')
    #Concatene un bout de commande avec 'guess' qui contient le nom de l'app
    # " \"" permet de ne mettre qu'un ' " ',  pareil pour celui de la fin
    # on a donc "mes mots" considérées comme une seule chaine de caractère et pas deux chaines
    # \ est un caractère d'échappement, il permet de ne pas prendre en compte le caractère qui suit pour faire une certaine action
    # exemple : \n 
    Command = "open -a " + " \"" + guess["transcription"] + "\""
    print (guess["transcription"])
    os.system(Command)
    if guess["transcription"].find('Firefox') != -1:
        engine.say("Voulez vous faire une recherche internet ?")
        engine.runAndWait() 
        print(colored('Voulez vous faire une recherche internet ?', 'red'))
        guess = start()
                            
        while guess["error"] == 'Unable to recognize speech':
            guess = erreur()
        ecriture_fichier(guess)
                            
        if guess["transcription"].find('oui') != -1:
            engine.say("Que voulez vous rechercher ?")
            engine.runAndWait() 
            print(colored('Que voulez vous rechercher ?', 'red'))
            guess = start()
                                
        while guess["error"] == 'Unable to recognize speech':
            guess = erreur()
                                
        ecriture_fichier(guess)
        url_base = "http://www.google.fr/search?hl=en&q="
        url_final = url_base + guess["transcription"]
        webbrowser.open(url_final)
