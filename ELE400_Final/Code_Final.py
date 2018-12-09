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
    global personnes
    age = 'UNDEF'
    gender = 'UNDEF'
    personnes = 'UNDEF'
    
    global z #On s'assure que le code ne se repete pas à l'infini
    global y #On fais rouler le code 1 fois pour afficher le GUI
    global util
    global util_stats
    util_stats = 0
    util = 0
    y=0
    z=0
    global x
    global flag
    global charge
    global flag_charge
    global flag_banc
    global duree
    global recharge
    
    global age_1
    global age_2
    global age_3
    global age_4
    global age_5
    global age_6
    age_1 = 0
    age_2 = 0
    age_3 = 0
    age_4 = 0
    age_5 = 0
    age_6 = 0

    global gender_homme
    global gender_femme
    global gender_autre_refus
    gender = 0
    gender_homme = 0
    gender_femme = 0
    gender_autre_refus = 0

    global nombre_seule
    global nombre_2
    global nombre_3
    global nombre_4
    nombre_seule = 0
    nombre_2 = 0
    nombre_3 = 0
    nombre_4 = 0

    global duree_totale
    duree_totale = 0

    global recharge_totale
    recharge_totale = 0
    
    recharge = 0
    duree = 0
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
            if val > 1300000:
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

            else:
                
                charge = 1
                flag_charge = 1
                if keep_charge == 0:
                    recharge = 1
            #print(val)
            hx.power_down()
            hx.power_up()
            
            
            if (x == 1 and z == 0 and y == 1):
                salutation_visible()
                z=1

            elif(x == 0 and y == 1):
                ecran_acceuil()
                time.sleep(1)
            
            if (x == 0 and keep == 1):
                z=0
                util = util+1
                fichiertxt()
                if util_stats > 0:
                    fichierstats()
                recharge = 0
                age = 'UNDEF'
                gender = 'UNDEF'
                personnes = 'UNDEF'
                    
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

t = Thread(target=get_data)
t.daemon = True # quit the thread when the program (main thread) quits
t.start() # start the background thread

while True: # yep, another infinite loop!! Each thread can have it's own!
    #your normal code
    try:        
        #time.sleep(2)
        #print(x)


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
            canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Dans quelle tranche \nd\'âge vous situez-vous?', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. 18 ans et moins\n2. 19 à 27 ans\n3. 28 à 36 ans\n4. 37 à 45 ans\n5. 46 à 63 ans\n6. 63 ans et plus', fill='black', font=my_font)
            
            window.unbind("<KP_1>")
            window.unbind("<KP_2>")
            window.unbind("<KP_3>")
            window.bind("<Key>", get_input_1)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_1(event):
            global age
            global age_1
            global age_2
            global age_3
            global age_4
            global age_5
            global age_6
            
            age = repr(event.char)

            if age=="'1'" or age=="'2'" or age=="'3'" or age=="'4'" or age=="'5'" or age=="'6'":
                
                if age == "'1'":
                    age_1 = age_1+1
                if age == "'2'":
                    age_2 = age_2+1
                if age == "'3'":
                    age_3 = age_3+1
                if age == "'4'":
                    age_4 = age_4+1
                if age == "'5'":
                    age_5 = age_5+1
                if age == "'6'":
                    age_6 = age_6+1
                    
                age = switch_age(age)
                question2()

        def question2():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Etes vous :', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. Un homme\n2. Une femme\n3. Autre\n4. Préfère ne pas répondre', fill='black', font=my_font)

            window.bind("<Key>", get_input_2)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_2(event):
            global gender
            global gender_homme
            global gender_femme
            global gender_autre_refus
            gender = repr(event.char)

            if gender=="'1'" or gender=="'2'" or gender=="'3'" or gender=="'4'":
                
                if gender == "'1'":
                    gender_homme = gender_homme+1
                if gender == "'2'":
                    gender_femme = gender_femme+1
                if gender == "'3'":
                    gender_autre_refus = gender_autre_refus+1
                if gender == "'4'":
                    gender_autre_refus = gender_autre_refus+1
                    
                gender = switch_gender(gender)
                question3()


        def question3():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_gauche.create_text(screen_width/6, 2*screen_height/6, text='Etes-vous en groupe?', fill='black', font=my_font)
            reponse_question = canvas_droit.create_text(1*screen_width/6, 2*screen_height/6, text='1. Non, je suis seul\n2. Groupe de 2\n3. Groupe de 3\n4. Groupe de plus de 3', fill='black', font=my_font)

            window.bind("<Key>", get_input_3)
            
            canvas_gauche.pack()
            canvas_droit.pack()


        def get_input_3(event):
            global personnes
            global util_stats
            global nombre_seule
            global nombre_2
            global nombre_3
            global nombre_4
            
            personnes = repr(event.char)
            if personnes=="'1'" or personnes=="'2'" or personnes=="'3'" or personnes=="'4'":

                if personnes == "'1'":
                    nombre_seule = nombre_seule+1
                if personnes == "'2'":
                    nombre_2 = nombre_2+1
                if personnes == "'3'":
                    nombre_3 = nombre_3+1
                if personnes == "'4'":
                    nombre_4 = nombre_4+1
            
                personnes = switch_personnes(personnes)
                util_stats = util_stats+1
                reward()

                
        def reward():
            canvas_gauche.delete("all")
            canvas_droit.delete("all")
            canvas_haut.delete("all")
            
            print('you made it')
            print(age)
            print(gender)
            print(personnes)
            
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


        def switch_personnes(argument):

            switcher = {
                "'1'" : "Seul",
                "'2'" : "2 personnes",
                "'3'" : "3 personne",
                "'4'" : "Plus de 3 personnes",
            }
            return switcher.get(argument,"nothing")

        
        def fichiertxt():
            global duree
            global recharge

            if recharge == 1:
                recharge2 = "Oui"
            else:
                recharge2 = "Non"
            
            f = open("stats_utilisateurs.txt", "a+")
            f.write("\nUtilisateur---------------------------------------------------------------\r\n")
            f.write("age : %s\n"  % age)
            f.write("sexe : %s\n" % gender)
            f.write("Nombre de personnes : %s\n" % personnes)
            f.write("Temps assis en secondes: %d\n" % duree)
            f.write("Utilisation de la charge: %s\n" % recharge2)
            f.close()

            
        def fichierstats():
            global duree
            global recharge
            global duree_totale
            global recharge_totale

            pourcent_reponse = util_stats/util

            pourcent_age_1 = age_1/util_stats
            pourcent_age_2 = age_2/util_stats
            pourcent_age_3 = age_3/util_stats
            pourcent_age_4 = age_4/util_stats
            pourcent_age_5 = age_5/util_stats
            pourcent_age_6 = age_6/util_stats

            pourcent_homme = gender_homme/util_stats
            pourcent_femme = gender_femme/util_stats
            pourcent_autres = gender_autre_refus/util_stats

            pourcent_seule = nombre_seule/util_stats
            pourcent_2 = nombre_2/util_stats
            pourcent_3 = nombre_3/util_stats
            pourcent_4 = nombre_4/util_stats

            duree_totale = duree_totale+duree
            duree_moyenne = duree_totale/util
            
            recharge_totale = recharge_totale + recharge
            pourcent_recharge = recharge_totale/util

            f = open("stats_utilisation.txt", "w+")

            f.write("Nombre d'utilisateurs total: %s\n\n"  % util)
            f.write("Pourcentage d'utilisateurs ayant répondus aux 3 questions: %s\n\n"  % pourcent_reponse)
            
            f.write("Moins de 18 ans : %.2f \n"  % pourcent_age_1)
            f.write("19 à 27 ans : %.2f \n"  % pourcent_age_2)
            f.write("28 à 36 ans : %.2f \n"  % pourcent_age_3)
            f.write("37 à 45 ans : %.2f \n"  % pourcent_age_4)
            f.write("46 à 63 ans : %.2f \n"  % pourcent_age_5)
            f.write("63 ans et plus : %.2f \n\n"  % pourcent_age_6)
            
            f.write("Pourcentage d'hommes : %.2f \n" % pourcent_homme)
            f.write("Pourcentage de femmes : %.2f \n" % pourcent_femme)
            f.write("Pourcentage d'autres/refus : %.2f \n\n" % pourcent_autres)
            
            f.write("Personnes seules : %.2f\n" % pourcent_seule)
            f.write("Groupes de 2 : %.2f\n" % pourcent_2)
            f.write("Groupes de 3 : %.2f\n" % pourcent_3)
            f.write("Groupes de + de 3 : %.2f\n\n" % pourcent_4)

            
            f.write("Moyenne du temps d'utilisation: %.2f\n" % duree_moyenne)
            f.write("Pourcentage d'utilisation de la recharge: %.2f\n" % pourcent_recharge)
            f.close()

        y = 1

        window.mainloop()

    
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
