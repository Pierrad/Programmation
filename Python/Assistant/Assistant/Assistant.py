import random
import time
import webbrowser
import speech_recognition as sr
import subprocess
import os 
from termcolor import colored
import re
from weather import Weather, Unit
import datetime
import pyttsx3 
from system_function import *



def recognize_speech_from_mic(recognizer, microphone, connected_or_not):

    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
            successful
    "error":   `None` if no error occured, otherwise a string containing
            an error message if the API could not be reached or
            speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
            otherwise a string containing the transcribed text"""
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")


    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        #print("Je calibre le micro...")
        #recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Vous pouvez parler !")
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    try:
        if connected_or_not == True:
            response["transcription"] = recognizer.recognize_google(audio, language= 'fr-FR')
        else: 
            response["transcription"] = recognizer.recognize_sphinx(audio, language= 'fr-FR')
    except sr.RequestError:
         # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def start():
    guess = recognize_speech_from_mic(recognizer, microphone, connected_or_not)
    return guess

def erreur():
    guess = start()
    if guess["transcription"]:
        return guess
    print(colored('Pouvez-vous repéter ?', 'red'))
    engine.say('Pouvez-vous repéter ?')
    engine.runAndWait()  

def ecriture_fichier(guess):
    fichier = open("../data.txt", "a")
    fichier.write("\n" + "\"" + guess["transcription"]+ "\"")
    fichier.close()  

def proposition_mot(guess):
    fichier = open("../BD_mots.txt", "r")
    for word in fichier.read().split(): 
        if guess["transcription"] in word :
            print (word)
    fichier.close()
    return guess

def meteo(guess):
    compteur = 1
    fichier = open("../world-cities.csv", "r")
    maListe = guess["transcription"].split(" ")
    lecture = fichier.read()
    for i in maListe:
        #permet de ne trouver que la ville précisément dans le fichier
        var = "\n" + i.capitalize() + ","
        print(var)
        if var in lecture:
            weather = Weather(unit=Unit.CELSIUS)
            location = weather.lookup_by_location(var)
            condition = location.condition
            forecasts = location.forecast
            if date.hour > 20:
                guess["transcription"].replace("aujourd\'hui", "demain")
            if guess["transcription"].find("aujourd\'hui") != -1 or guess["transcription"].find("aujourd\'hui") == -1 and guess["transcription"].find('demain') == -1:
                for forecast in forecasts:
                    print(forecast.date)
                    var = "Le " + forecast.date
                    engine.say(var)
                    engine.runAndWait()  
                    print (forecast.low)
                    var = "Il va faire au minimum " +forecast.low + "degrés"
                    engine.say(var)
                    engine.runAndWait() 
                    print (forecast.high)
                    var = "Et au maximum " + forecast.high + "degrés"
                    engine.say(var)
                    engine.runAndWait() 
                    print (condition.text)
                    var = "Le temps sera " + condition.text 
                    engine.say(var)
                    engine.runAndWait() 
                    break
            if guess["transcription"].find('demain') != -1:
                for forecast in forecasts:
                    if compteur == 2:
                        print(forecast.date)
                        var = "Le " + forecast.date
                        engine.say(var)
                        engine.runAndWait() 
                        print(forecast.low)
                        var = "Il va faire au minimum " + forecast.low + "degrés"
                        engine.say(var)
                        engine.runAndWait() 
                        print(forecast.high)
                        var = "Et au maximum " + forecast.high + "degrés"
                        engine.say(var)
                        engine.runAndWait() 
                        print(forecast.text)
                        var = "Le temps sera " + forecast.text 
                        engine.say(var)
                        engine.runAndWait() 
                    compteur += 1
    fichier.close()

def souvenir(chaine):
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

def rappelle():
    fichier = open("../Souvenir.txt", "r")
    lectures = fichier.readlines()
    engine.say("Je me rappelle : ")
    engine.runAndWait() 
    for lecture in lectures:
        engine.say(lecture)
        engine.runAndWait() 
    fichier.close()
    rappelle_supp()
    

def rappelle_supp():
    
    engine.say("Voulez vous supprimer des rappels ?")
    engine.runAndWait() 
    print(colored('Voulez vous supprimer des rappels ? ', 'red'))
    guess = start()
    if guess["transcription"].find("oui") != -1:
        engine.say("Quelle ligne voulez vous supprimer ?")
        engine.runAndWait() 
        print(colored('Quelle ligne voulez vous supprimer ?', 'red'))
        guess = start()
        print(guess["transcription"])
        if guess["transcription"].find('tout') != -1:
            fichier = open("../Souvenir.txt", "w")
            fichier.close()
        else:
            fichier = open("../Souvenir.txt", "r")
            lectures = fichier.readlines()
            i = char_to_int(guess["transcription"])
            lectures.remove(lectures[i])
            with open("Souvenir.txt", "w") as fichier:
                    for lecture in lectures:        
                        fichier.write(lecture)
    fichier.close()
    


def char_to_int(chiffre_char):

    if chiffre_char.find('une') != -1:
        chiffre_char = 0
        return chiffre_char
    if chiffre_char.find('deux') != -1:
        chiffre_char = 1
        return chiffre_char
    if chiffre_char.find('trois') != -1:
        chiffre_char = 2
        return chiffre_char
    if chiffre_char.find('quatre') != -1:
        chiffre_char = 3
        return chiffre_char
    if chiffre_char.find('cinq') != -1:
        chiffre_char = 4
        return chiffre_char
    if chiffre_char.find('six') != -1:
        chiffre_char = 5
        return chiffre_char
    if chiffre_char.find('sept') != -1:
        chiffre_char = 6
        return chiffre_char
    if chiffre_char.find('huit') != -1:
        chiffre_char = 7
        return chiffre_char
    if chiffre_char.find('neuf') != -1:
        chiffre_char = 8
        return chiffre_char
    if chiffre_char.find('dix') != -1:
        chiffre_char = 9
        return chiffre_char

def salutation():
    if date.hour >= 19:
        engine.say("Bonsoir Monsieur, que puis-je faire pour vous ?")
        engine.runAndWait() 
        print(colored('Bonsoir Monsieur, que puis-je faire pour vous ? ', 'red'))
    elif date.hour >= 1 and date.hour < 7:
        engine.say("Bonsoir Monsieur, attention vous devriez aller vous coucher. Mais, que puis je faire pour vous ?")
        engine.runAndWait() 
        print(colored('Bonsoir Monsieur, attention vous devriez aller vous coucher. Mais, que puis je faire pour vous ?', 'red'))
    else:     
        engine.say("Bonjour Monsieur, que puis-je faire pour vous ?")
        engine.runAndWait() 
        print(colored('Bonjour Monsieur, que puis-je faire pour vous ? ', 'red'))


#variable contenant l'heure et la date actuelle
date = datetime.datetime.now()
# create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()
# Initialiser le text to speech
engine = pyttsx3.init() 


REMOTE_SERVER = "www.google.com"
connected_or_not = Check_connexion(REMOTE_SERVER)


while 1:
    if __name__ == "__main__":
        guess = start()
        if guess["transcription"] != None:
            if guess["transcription"].find('assistant') != -1:
                salutation()
                ecriture_fichier(guess)
                #guess = proposition_mot(guess)
                
                while 1: 
                    guess = start()
                    
                    while guess["error"] == 'Unable to recognize speech':
                        guess = erreur()
                    # show the user the transcription
                    ecriture_fichier(guess)
                    print("You said: {}".format(guess["transcription"]))
                    
                    if guess["transcription"].find('ouvre') != -1:
                        open_app(guess)

                    if guess["transcription"].find('souviens-toi') != -1 or guess["transcription"].find('rappelle-toi') != -1 or guess["transcription"].find('rappelle-moi') != -1:
                        souvenir(guess["transcription"])

                    if guess["transcription"].find('souvenir') != -1 or guess["transcription"].find('rappeler') != -1:
                        rappelle()
                    
                    if guess["transcription"].find('supprimer') != -1 or guess["transcription"].find('rappels') != -1:
                        rappelle_supp()

                    if guess["transcription"].find('météo') != -1:
                        meteo(guess)
                    
                    if guess["transcription"].find('active') != -1 and guess["transcription"].find('wifi') != -1:
                        wifi_on()
                    
                    if guess["transcription"].find('désactive') != -1 and guess["transcription"].find('wifi') != -1:
                        wifi_off()

                    if guess["transcription"].find('merci') != -1:
                        ecriture_fichier(guess)
                        engine.say("Fermeture Assistant")
                        engine.runAndWait() 
                        print(colored('Fermeture Assistant', 'red'))
                        quit()
                    #condition avec if qui prend tout pour bypass mais relou a ecrire
                    else:
                        url_base = "http://www.google.fr/search?hl=en&q="
                        url_final = url_base + guess["transcription"]
                        webbrowser.open(url_final)

                    
                    
                    

                