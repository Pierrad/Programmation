import random
import time
import webbrowser
import speech_recognition as sr
import subprocess
import os 
from termcolor import colored
from os import system
from tkinter import *
from threading import Thread, RLock
import re


def recognize_speech_from_mic(recognizer, microphone):

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
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language= 'fr-FR')
    except sr.RequestError:
         # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response




class Assistant(Thread):


    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            if __name__ == "__main__":
            
                # create recognizer and mic instances
                recognizer = sr.Recognizer()
                microphone = sr.Microphone()
                guess = recognize_speech_from_mic(recognizer, microphone)
                
                if guess["transcription"] != None:
                    if guess["transcription"].find('bonjour') != -1:
                        system('say Vous pouvez parlez!')
                        print(colored('Vous pouvez parler ! ', 'red'))
                        guess = recognize_speech_from_mic(recognizer, microphone)
                        while guess["error"] == 'Unable to recognize speech':
                            guess = recognize_speech_from_mic(recognizer, microphone)
                            if guess["transcription"]:
                                break
                            print(colored('Pouvez-vous repéter ?', 'red'))
                            system('say Pouvez-vous repéter ?')
                        # show the user the transcription
                        print("You said: {}".format(guess["transcription"]))
                        #Je vérifie si ce que j'ai dit contient 'ouvre'
                        if guess["transcription"].find('ouvre') != -1:
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
                                system('say Voulez vous faire une recherche internet ?')
                                print(colored('Voulez vous faire une recherche internet ?', 'red'))
                                guess = recognize_speech_from_mic(recognizer, microphone)
                                if guess["transcription"].find('oui') != -1:
                                    system('say Que voulez vous rechercher ?')
                                    print(colored('Que voulez vous rechercher ?', 'red'))
                                    guess = recognize_speech_from_mic(recognizer, microphone)
                                    url_base = "http://www.google.fr/search?hl=en&q="
                                    url_final = url_base + guess["transcription"]
                                    webbrowser.open(url_final)

                        else:
                            url_base = "http://www.google.fr/search?hl=en&q="
                            url_final = url_base + guess["transcription"]
                            webbrowser.open(url_final)
    
class Fenetre(Thread):
        
    def __init__(self):
        Thread.__init__(self)
        
        
    def run(self):
        fenetre = Tk()
        fenetre.mainloop()


        


thread_1 = Fenetre()
thread_2 = Assistant()

thread_1.start()
thread_2.start()


thread_1.join()
thread_2.join()



