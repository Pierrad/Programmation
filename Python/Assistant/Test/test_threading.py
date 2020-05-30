from threading import Thread 
from tkinter import *

class Affiche(Thread):


    def __init__(self):
        Thread.__init__(self)
        

    def run(self):
        fenetre = Tk()
        fenetre.mainloop()


class Affiche1(Thread):


    def __init__(self):
        Thread.__init__(self)
        

    def run(self):
        print("ok")


thread_1 = Affiche()
thread_2 = Affiche1()

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

