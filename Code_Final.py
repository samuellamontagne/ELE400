from collections import deque
from threading import Thread
import time
import random
import RPi.GPIO as GPIO
import sys
from hx711 import HX711
from tkinter import *
from tkinter import font
import PIL
from PIL import Image
import os.path



GPIO.setwarnings(False)

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def get_data():
    
    global age
    global gender
    global groupe
    #On défini les variables age, gender et groupe a 'UNDEF' au cas ou l'utilisateur décide de ne pas répondre au questions
    age = 'UNDEF'
    gender = 'UNDEF'
    groupe = 'UNDEF'
    
    global duree
    duree = 0
    
    global z #On s'assure que le code ne se repete pas à l'infini
    global y #On fais rouler le code 1 fois pour afficher le GUI
    global util
    util = 0
    y=0
    z=0
    global x
    global flag
    global charge
    global flag_charge
    global flag_banc
    flag_banc = 0
    flag = 0
    flag_charge = 0
    charge = 0
    x = 0
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    #hx.set_reference_unit(92)
    hx.reset()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
    GPIO.setup(23,GPIO.IN)


    while True:
        try:
            #val = hx.read_long()
            #if val > 3000000:
            #   val = 1250000
            val = hx.read_average()
            print(val)
            #if val < 0:
            keep = flag
            keep_charge = flag_charge
            #    val = 1
            if val > 1370000:
                GPIO.output(18,GPIO.HIGH)#GPIO 18 pas pin 18 m8
                GPIO.output(15,GPIO.LOW)
                x = 1
                flag = 1
                if keep == 0:
                    get_timex()
                
            else:
                GPIO.output(18,GPIO.LOW)#GPIO 18 pas pin 18 m8
                GPIO.output(15,GPIO.HIGH)
                x = 0
                flag = 0
                if keep == 1:
                    get_timex()
                    
            if GPIO.input(23):
                
                charge = 0
                flag_charge = 0
                if keep_charge == 1:
                    get_timex2()
            else:
                
                charge = 1
                flag_charge = 1
                if keep_charge == 0:
                    get_timex2()
            #print(val)
            hx.power_down()
            hx.power_up()
            
            
            if (x == 1 and z == 0 and y == 1): # si quelqu'un est assis et nous avons parcouru le code au complet une fois
                salutation_visible()
                z=1

            elif(x == 0 and y == 1):# si personne n'est assis et que le code est parcouru une fois au complet
                ecran_acceuil()
                time.sleep(1)
            
            if (x == 1):
                if (keep == 0):# si queiqu'un est en train de se lever
                    z=0
                    util = util+1 # nombre d'utilisateur + 1
                    fichiertxt() # on update3 le fichier texte
                    #on redéfini les variables a 'UNDEF' au cas ou la personne ne répond pas à tout les questions
                    age = 'UNDEF'
                    gender = 'UNDEF'
                    groupe = 'UNDEF'
                    
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

def get_timex():
    
    global timex
    global duree
    
    if flag == 1:
        timex = time.time()
    else:
        now = time.time()
        duree = int(now - timex)
        print('Temps assis en secondes: ', duree)
        #print(duree)
'''        
def get_timex2():
    
    global timex2
    global duree2
    
    if flag_charge == 1:
        timex2 = time.time()
    else:
        now = time.time()
        duree2 = int(now - timex2)
        print('Temps de recharge en secondes: ', duree2)
        #print(duree)
    '''


t = Thread(target=get_data)
t.daemon = True # quit the thread when the program (main thread) quits
t.start() # start the background thread

while True: # yep, another infinite loop!! Each thread can have it's own!
    try:        


        #-----------------------------------------INTERFACE_GRAPHIQUE----------------------------------------------------------------------------------
        
        window = Tk()
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        canvas_color = 'ghost white'#7993a5
        background_color = 'cadet blue'#1e2366

        my_font = font.Font(window, ("Garamond", 20, "bold"))

        window.attributes('-fullscreen', True)
        window['bg'] = background_color

        canvas_haut = Canvas(window, width=screen_width, height=screen_height/6, background=canvas_color)
        canvas_haut.pack()

        canvas_gauche = Canvas(window, width=screen_width/3, height=2*screen_height/3, background=canvas_color)
        canvas_gauche.pack(side=LEFT, padx=screen_width/9)

        canvas_droit = Canvas(window, width=screen_width/3, height=2*screen_height/3, background=canvas_color)
        canvas_droit.pack(side=LEFT)

        #-----------------------------------------GESTION_IMAGE---------------------------------------------------------------------------------------

        metro = Image.open('Metro.png')
        centreville = Image.open('Centreville.png')
        QRcode = Image.open('QRcode.png')

        metro = metro.resize((int(screen_width/3), int(2*screen_height/3)), PIL.Image.ANTIALIAS)
        centreville = centreville.resize((int(screen_width/3), int(2*screen_height/3)), PIL.Image.ANTIALIAS)
        QRcode = QRcode.resize((int(screen_height/4), int(screen_height/4)), PIL.Image.ANTIALIAS)

        metro.save('resized_metro.png')
        centreville.save('resized_centreville.png')
        QRcode.save('resized_QRcode.png')

        metro2 = PhotoImage(file="resized_metro.png")
        centreville2 = PhotoImage(file="resized_centreville.png")
        QRcode2 = PhotoImage(file="resized_QRcode.png")

        #------------------------------------------FONCTIONS--------------------------------------------------------------------------------------------


        def destroy(event):
            window.destroy()

        def ecran_acceuil():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_haut.delete("all")
            canvas_haut.create_text(screen_width/2, screen_height/12, text='Veuillez vous asseoir', fill='black', font=my_font)


        def bind_vide(event):
            pi=1

        def salutation_visible():
            canvas_haut.delete("all")
            message_salutation = canvas_haut.create_text(screen_width/2, screen_height/12, text='Bonjour, utilisateur', fill='black', font=my_font)
            canvas_haut.pack()
            window.after(500, salutation_invisible)


        def salutation_invisible():
            canvas_haut.delete("all")    
            window.after(500, action_visible)


        def action_visible():
            message_action = canvas_haut.create_text(screen_width/2, screen_height/12, text='Veuillez choisir une option', fill='black', font=my_font)
            canvas_haut.pack()
            window.after(500,option_visible)


        def option_visible():
            window.bind("<KP_1>", option1)
            window.bind("<KP_2>", option2)
            window.bind("<KP_3>", option3)
            action1 = canvas_gauche.create_text(screen_width/6, 1*screen_height/6, text='1. Promotions', fill='black', font=my_font)
            action2 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='2. Carte du metro', fill='black', font=my_font)
            action3 = canvas_gauche.create_text(screen_width/6, 3*screen_height/6, text='3. Carte du centre-ville', fill='black', font=my_font)
            canvas_gauche.pack()


        def option1(event):
            action1 = canvas_gauche.create_text(screen_width/6, 1*screen_height/6, text='1. Promotions', fill='red', font=my_font)
            action2 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='2. Carte du metro', fill='black', font=my_font)
            action3 = canvas_gauche.create_text(screen_width/6, 3*screen_height/6, text='3. Carte du centre-ville', fill='black', font=my_font)
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_haut.delete("all")
            intro_questions()

            
        def option2(event):
            action1 = canvas_gauche.create_text(screen_width/6, 1*screen_height/6, text='1. Promotions', fill='black', font=my_font)
            action2 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='2. Carte du metro', fill='red', font=my_font)
            action3 = canvas_gauche.create_text(screen_width/6, 3*screen_height/6, text='3. Carte du centre-ville', fill='black', font=my_font)
            canvas_droit.create_image(0,0, anchor=NW, image=metro2)
            canvas_droit.pack()


        def option3(event):
            action1 = canvas_gauche.create_text(screen_width/6, 1*screen_height/6, text='1. Promotions', fill='black', font=my_font)
            action2 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='2. Carte du metro', fill='black', font=my_font)
            action3 = canvas_gauche.create_text(screen_width/6, 3*screen_height/6, text='3. Carte du centre-ville', fill='red', font=my_font)
            canvas_droit.create_image(0,0, anchor=NW, image=centreville2)
            canvas_droit.pack()


        def intro_questions():
            entete_question = canvas_haut.create_text(screen_width/2, screen_height/12, text='Questions', fill='black', font=my_font)
            explication_question = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text=' Afin d\'obtenir un rabais\n chez un de nos\n collaborateurs,\n vous pouvez repondre au \n court sondage suivant.\n Voulez vous continuer?', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. Oui\n\n2. Non', fill='black', font=my_font)
            window.bind("<KP_1>", question1)
            window.bind("<KP_2>", opt_vis)
            window.bind("<KP_3>", bind_vide) 
            canvas_gauche.pack()
            canvas_droit.pack()

            
        def question1(event):
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            question1 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Dans quelle tranche \nd\'âge vous situez-vous?', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. 18 ans et moins\n2. 19 à 27 ans\n3. 28 à 36 ans\n4. 37 à 45 ans\n5. 46 à 63 ans\n6. 63 ans et plus', fill='black', font=my_font)
            
            window.unbind("<KP_1>")
            window.unbind("<KP_2>")
            window.unbind("<KP_3>")
            window.bind("<Key>", get_input_1)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_1(event):
            global age
            age = repr(event.char)

            if age=="'1'" or age=="'2'" or age=="'3'" or age=="'4'" or age=="'5'" or age=="'6'":
                age = switch_age(age)
                question2()

        def question2():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            question1 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Etes vous :', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. Un homme\n2. Une femme\n3. Autre\n4. Préfère ne pas répondre', fill='black', font=my_font)

            window.bind("<Key>", get_input_2)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_2(event):
            global gender
            gender = repr(event.char)

            if gender=="'1'" or gender=="'2'" or gender=="'3'" or gender=="'4'":
                gender = switch_gender(gender)
                question3()


        def question3():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            question1 = canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Etes-vous en groupe?', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. Non, je suis seul\n2. Groupe de 2\n3. Groupe de 3\n4. Groupe de plus de 3', fill='black', font=my_font)

            window.bind("<Key>", get_input_3)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_3(event):
            global groupe
            groupe = repr(event.char)
            if groupe=="'1'" or groupe=="'2'" or groupe=="'3'" or groupe=="'4'":
                groupe = switch_groupe(groupe)
                reward()

                
        def reward():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_haut.delete("all")
            
            print('you made it')
            print(age)
            print(gender)
            print(groupe)
            
            canvas_haut.create_text(screen_width/2, screen_height/12, text='Promotion', fill='black', font=my_font)    
            canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Réclamez votre rabais \nà l\'aide de ce code QR', fill='black', font=my_font)
            canvas_droit.create_image(screen_width/6, 2*screen_height/6, anchor=CENTER, image=QRcode2)
            canvas_droit.pack()
            window.after(10000,ecran_acceuil)
            
            
        def opt_vis(event):
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_haut.delete("all")   
            option_visible()


        def switch_age(argument):

            switcher = {
                "'1'" : "Moins de 18 ans",
                "'2'" : "19 à 27 ans",
                "'3'" : "28 à 36 ans",
                "'4'" : "37 à 45 ans",
                "'5'" : "46 à 63 ans",
                "'6'" : "63 ans et plus"
            }
            return switcher.get(argument,"nothing")


        def switch_gender(argument):

            switcher = {
                "'1'" : "Homme",
                "'2'" : "Femme",
                "'3'" : "Autres",
                "'4'" : "Ne préfère pas répondre",
            }
            return switcher.get(argument,"nothing")


        def switch_groupe(argument):

            switcher = {
                "'1'" : "Seul",
                "'2'" : "2 personnes",
                "'3'" : "3 personnes",
                "'4'" : "Plus de 3 personnes",
            }
            return switcher.get(argument,"nothing")
        
        def fichiertxt():
            global duree
            
            
            f = open("stats_utilisateurs.txt", "a+")
            f.write("\nUtilisateur---------------------------------------------------------------\r\n")
            f.write("age : %s\n"  % age)
            f.write("sexe : %s\n" % gender)
            f.write("Nombre de personnes : %s\n" % groupe)
            f.write("Temps assis en secondes %d\n" % duree)
            f.close()
  


        y = 1

        window.mainloop()

    
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
