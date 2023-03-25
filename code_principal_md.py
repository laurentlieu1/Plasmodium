from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image as kivyim
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatIconButton,MDRaisedButton, MDFloatingActionButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.clock import Clock

from plyer import filechooser
from PIL import Image
import os.path
import os
from fpdf import FPDF
from time import strftime
from datetime import datetime
import json


from model import *


class HomePage(Screen):
    """
    Classe qui regroupe les éléments de la page d'accueil de l'interface 
    """
    pass


class MicroscopePage(Screen):
    """
    Classe qui regroupe les éléments de la page "Microscope" de l'interface 
    """
    
    def connect_microscope(self):
        # return False
        return True
    
    def run_microscope(self):
        connexion = self.connect_microscope()
        if connexion == True: 
            # Affichage de l'interface de réglage du microscope
            # Initialisation des touches du clavier pour les déplacements
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)
            self.btn_move_left.disabled = False
            self.btn_move_right.disabled = False
            self.btn_move_up.disabled = False
            self.btn_move_down.disabled = False
            self.add_widget(MDRaisedButton(text="Lancer la capture automatique", 
                                           font_name="louis_george_caf\Louis George Cafe.ttf",
                                           size_hint=(.25,.08),
                                           font_size=0.03*self.height,
                                           md_bg_color="#ad526d",
                                           pos_hint={"x": 0.05, "y": 0.04}, 
                                           on_press=self.cartographie_goutte))
        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def mouv_gauche(self, step_count):
        print("deplacement gauche ")

    def mouv_droite(self, step_count):
        print("deplacement droite ")

    def mouv_haut(self, step_count):
        print("deplacement haut")

    def mouv_bas(self, step_count):
        print("deplacement bas")

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 273: 
            self.mouv_haut(1)
        elif keycode[0] == 274:
            self.mouv_bas(1)    
        elif keycode[0] == 275:
            self.mouv_droite(1)
        elif keycode[0] == 276:
            self.mouv_gauche(1)
 
    def goto(self, cord_x, cord_y, speed):
        print(f"deplacement au coord {cord_x}, {cord_y}")

    def prise_photo(self):
        print("vous avez pris une photo")  

    # fonction a mettre en parametre de la fonction cartographie goute
    def creation_carte(self, nombre_photo_x, nombre_photo_y):
        carte_pos = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (1,1), (1,0), 
                     (2,0), (2,1), (2,2), (2,3), (3,3), (3,2), (3,1), (3,0)]
        return carte_pos


    
    def cartographie_goutte(self, instance): # Cartographier la goutte et prise de photos
        # carte_pos, photo_delay, speed, la  variable carte_pos doit etre créer via la fonction creation carte
        """for pos in carte_pos():
            self.goto(self,pos[0], pos[1])
            self.prise_photo(self)"""
        self.add_widget(MDRaisedButton(text="Voir le dossier avec les images", 
                                       font_name= "louis_george_caf\Louis George Cafe.ttf",
                                       size_hint=(.25,.08),
                                       font_size=0.03*self.height,
                                       md_bg_color="#65ab5e",
                                       pos_hint={"x": 0.32, "y": 0.04}))
        

    def abort(self):
        print("capture d'image arrêtée")    
    pass


class InfectionRatePage(Screen):
    """
    Classe qui regroupe les éléments de la page "Taux d'infection" de l'interface 
    """

    def select_file(self, instance):

        try:
            # Fermeture de la popup d'erreur de sélection de répertoire si elle est déjà ouverte
            # Quand on a fait une première erreur de sélection et qu'on veut sélectionner un répertoire à nouveau
            self.main_pop.dismiss() 

        except AttributeError: 
            pass
        filechooser.choose_dir(on_selection=self.analyse_folder)   

    def analyse_folder(self, folder): 
        self.date_time = datetime.now()
        self.date = self.date_time.strftime("%Y-%m-%d") # on récupère la date et l'heure
        self.heure = self.date_time.strftime("%H:%M:%S")

        try: 
            global folder_path
            self.total_parasites_count = 0
            self.total_distractors_count = 0            

            # Détection automatique des parasites avec le modèle de Machine Learning
            # Retourne un répertoire des images annotées et d'un fichier d'annotations .json
            folder_path, self.numero = inference_on_folder(folder[0], model) 
            self.count_labels_in_total()

            if (len(os.listdir(folder_path))!=0):
                self.import_btn.background_color =(0, 1, 0, 1)
                self.resize_img()
                self.start = 0 # Variable pour connaître savoir quelle image est affichée en première dans le caroussel
                self.display_images(0.4)
                self.infection_rate()
                self.change_json("", "", self.rate, self.total_parasites_count, self.total_distractors_count)
                return "Unzip_selected successful"
            return "Unzip_selected failed"
        
        except IndexError : 
            # Affiche une popup d'erreur
            self.box=FloatLayout()
            self.label = Label(text="Vous n'avez pas sélectionné de dossier. \nSouhaitez-vous quitter ?", 
                               pos_hint={"x":0,"y":0.18})
            self.btn_continue =(MDFillRoundFlatButton(text="Choisir un dossier", 
                                                      font_size=self.height*0.02, 
                                                      size_hint=(.1, .05), 
                                                      pos_hint={"x":0.1,"y":0.1}))
            self.btn_quit =(MDFillRoundFlatButton(text="Quitter", 
                                                  font_size=self.height*0.02, 
                                                  size_hint=(.1, .05), 
                                                  pos_hint={"x":0.7,"y":0.1}))

            self.box.add_widget(self.label)
            self.box.add_widget(self.btn_continue)
            self.box.add_widget(self.btn_quit)
            
            self.error_pop = Popup(title= "Voulez-vous continuer ?", 
                                   content=self.box, 
                                   size_hint=(None,None),
                                   size=(400,200),
                                   auto_dismiss=False,
                                   title_size=15)
            
            self.btn_continue.bind(on_press=self.close_then_filechooser)
            self.btn_quit.bind(on_press=self.error_pop.dismiss)
            self.error_pop.open()

    def close_then_filechooser(self, instance):
        self.error_pop.dismiss()
        Clock.schedule_once(self.select_file, .5)

    def resize_img(self): # On resize pour afficher les images dans le caroussel d'images
        global resized_path
        self.list_images = os.listdir(folder_path)
        self.list_images.pop(-1) # On retire le fichier .json

        head, tail = os.path.split(folder_path) # On récupère le nom du répertoire (head)
        resized_path = os.path.join(head,"resized") 

        if os.path.exists(resized_path) == True: 
            delete_folder(resized_path)
        os.mkdir(resized_path) 
        
        for img in self.list_images: 
            img_path = os.path.join(folder_path, img)
            image = Image.open(img_path)
            new_width = int(160 / image.height*image.width)
            img_resize = image.resize((new_width, 160))
            resize_img_path = os.path.join(resized_path, img)
            img_resize.save(resize_img_path)

        
        self.add_widget(MDRaisedButton(text=f"Nombre total de parasite(s): {self.total_parasites_count}", 
                                       font_name="louis_george_caf\Louis George Cafe.ttf", 
                                       size_hint =(.27,.05), 
                                       font_size=0.03*self.height, 
                                       disabled=True, 
                                       disabled_color="white", 
                                       md_bg_color_disabled="b73123", 
                                       pos_hint={"center_x": 0.295, "y": 0.22}))
        self.add_widget(MDRaisedButton(text=f"Nombre total de distractor(s): {self.total_distractors_count}", 
                                       font_name="louis_george_caf\Louis George Cafe.ttf", 
                                       size_hint =(.27,.05), 
                                       font_size=0.03*self.height, 
                                       disabled=True, 
                                       disabled_color="white", 
                                       md_bg_color_disabled="315aa2", 
                                       pos_hint={"center_x": 0.295, "y": 0.15}))
        self.infection_btn = (MDRaisedButton(text=f"Taux d'infection: ", 
                                             font_name="louis_george_caf\Louis George Cafe.ttf", 
                                             size_hint =(.25,.125), 
                                             font_size=0.03*self.height, 
                                             disabled=True, 
                                             disabled_color="white", 
                                             md_bg_color_disabled="717171", 
                                             pos_hint={"x": 0.46, "y": 0.15}))
        self.add_widget(self.infection_btn)
        self.add_widget(MDFloatingActionButton(icon = "help",
                                               size_hint =(.017,.031),  
                                               pos_hint={"x": 0.68, "y": 0.234}, 
                                               on_press = self.help))
        self.btn_pdf = MDRaisedButton(text=f"Générer PDF", 
                                      font_name="louis_george_caf\Louis George Cafe.ttf", 
                                      size_hint =(.12,.125), 
                                      font_size=0.03*self.height, 
                                      md_bg_color ="#65ab5e", 
                                      pos_hint={"x": 0.74, "y": 0.15})
        self.add_widget(self.btn_pdf)
        

    def help(self, instance):
        self.box=FloatLayout()
        
        self.close_btn=(MDFillRoundFlatButton(text="Fermer", 
                                        font_size=self.height*0.03, 
                                        size_hint=(.09, .07), 
                                        pos_hint={"x":0.4,"y":0.03}))
        self.box.add_widget(self.close_btn)
        self.box.add_widget(Label(text = "+ = 1–10 parasites pour 100 champs de la goutte épaisse à l’objectif à immersion",
                                  font_size=self.height*0.025,
                                  size_hint=(.2, .07), 
                                  pos_hint={"x":0.4,"y":0.85}))
        self.box.add_widget(Label(text = "++ = 11–100 parasites pour 100 champs de la goutte épaisse à l’objectif à immersion", 
                                  font_size=self.height*0.025,
                                  size_hint=(.2, .07), 
                                  pos_hint={"x":0.4,"y":0.65}))
        self.box.add_widget(Label(text = "+++ = 1–10 parasites par champ de la goutte épaisse à l’objectif à immersion", 
                                  font_size=self.height*0.025,
                                  size_hint=(.2, .07), 
                                  pos_hint={"x":0.4,"y":0.45}))
        self.box.add_widget(Label(text = "++++ = plus de 10 parasites par champ de la goutte épaisse à l’objectif à immersion", 
                                  font_size=self.height*0.025,
                                  size_hint=(.2, .07), 
                                  pos_hint={"x":0.4,"y":0.25}))

        self.help_pop = Popup(title="Aide",
                              content=self.box, 
                              size_hint=(None,None),
                              size=(900,400),
                              auto_dismiss=False,
                              title_size=15)
    
        self.close_btn.bind(on_press=self.help_pop.dismiss)
        self.help_pop.open()
    
    def display_images(self, x_pos):   
        self.btn_next_viewer.disabled = False
        self.btn_previous_viewer.disabled = False
        self.patient_id.text = self.numero
        
        # Les images agissent comme des boutons pour ouvrir une popup en cliquant dessus
        self.list_btn = [self.btn_r1_c1, self.btn_r1_c2, self.btn_r1_c3, self.btn_r1_c4, self.btn_r1_c5, 
                         self.btn_r2_c1, self.btn_r2_c2, self.btn_r2_c3, self.btn_r2_c4, self.btn_r2_c5]

        # Si on passe aux 10 images suivantes et qu'on atteint pas le nombre d'images total
        if self.start + 10 <= len(self.list_images): 
            self.nb_img.text = f"Images: {self.start} à {self.start + 10}/{len(self.list_images)}"

            for i in range(self.start, self.start + 10):
                self.list_btn[i-self.start].background_normal = os.path.join(resized_path, self.list_images[i]) # Le bouton affiche l'image
                self.list_btn[i-self.start].disabled = False
        
        #  Si on passe aux 10 images suivantes et qu'on dépasse le nombre d'images total
        elif self.start + 10 > len(self.list_images):
            imgs_restantes = len(self.list_images) - self.start 
            # Si le nombre d'images n'est pas égal à 100, on gère la dernière série d'images qui affiche moins de 10 images
            if imgs_restantes <= 5:
                self.nb_img.text = f"Images: {self.start} à {imgs_restantes}/{len(self.list_images)}"

            else: 
                self.nb_img.text = f"Images: {self.start} à {imgs_restantes + 10}/{len(self.list_images)}"

            padding = len(self.list_btn) - imgs_restantes # Les boutons qui n'ont pas d'images associées ne sont pas activés

            for i in range(self.start, self.start + imgs_restantes): 
                self.list_btn[i-self.start].background_normal = os.path.join(resized_path,self.list_images[i])
                self.list_btn[i-self.start].disabled = False

            for i in range(imgs_restantes, imgs_restantes + padding): 
                self.list_btn[i].background_normal = ""
                self.list_btn[i].disabled = True
        
    
        self.btn_enabled = -1 # Car les indices d'une liste commence à 0
        for btn in self.list_btn: 
            if not btn.disabled:
                self.btn_enabled += 1    
   
    def next(self): 
        if self.start + 10 >= len(self.list_images):
            self.start = 0

        else: 
            self.start += 10
        self.display_images(0.4)

    def previous(self):
        if self.start <= 0:  
            self.start = len(self.list_images) - (len(self.list_images)-10)%10 # Cas où on a pas 100 images
            if self.start == 100: 
                self.start = 90

        else: 
            self.start -= 10
        self.display_images(0.4)

    def popup_image(self, instance):
        global btn_in_pop # Valeur du bouton avec l'image à afficher dans la popup
        btn_in_pop = instance

        self.box=FloatLayout()
        head, filename = os.path.split(instance.background_normal)
        img_path = os.path.join(folder_path, filename)
        
        self.close_btn=(MDFillRoundFlatButton(text="Fermer", 
                                        font_size=self.height*0.03, 
                                        size_hint=(.2, .07), 
                                        pos_hint={"x":0.4,"y":0.03}))
        self.prev_btn = MDFillRoundFlatButton(text="<", 
                                              font_size=self.height*0.02, 
                                              size_hint=(.015,.015), 
                                              pos_hint={"x":0.01,"y":0.49})
        self.next_btn=MDFillRoundFlatButton(text=">", 
                                            font_size=self.height*0.02, 
                                            size_hint=(.015,.015), 
                                            pos_hint={"x":0.92,"y":0.49})
        self.box.add_widget(self.prev_btn)
        self.box.add_widget(self.next_btn)
        self.box.add_widget(self.close_btn)
        self.box.add_widget(kivyim(source=img_path, 
                                   size_hint=(None,None), 
                                   size=(550,550),
                                   pos_hint={"x":0.1,"y":0.15}))
            
        self.count_falciparum, self.count_other = self.count_labels_in_img(filename)

        self.box.add_widget(MDRectangleFlatIconButton(text=f"P. Falciparum\n{self.count_falciparum}", 
                                                      font_name="louis_george_caf\Louis George Cafe.ttf", 
                                                      disabled_color="white", 
                                                      font_size=self.height*0.035,
                                                      md_bg_color_disabled= "red", 
                                                      size_hint=(.2,.1), 
                                                      text_color="white", 
                                                      line_color_disabled="red", 
                                                      disabled=True,  
                                                      pos_hint={"x":0.68,"y":0.57})) 
        self.box.add_widget(MDRectangleFlatIconButton(text=f"Distractor\n{self.count_other}", 
                                                      font_name="louis_george_caf\Louis George Cafe.ttf", 
                                                      font_size=self.height*0.035, 
                                                      disabled_color="white", 
                                                      md_bg_color_disabled= "blue", 
                                                      size_hint=(.2,.1), 
                                                      text_color="white", 
                                                      line_color_disabled="blue", 
                                                      disabled=True,  
                                                      pos_hint={"x":0.68,"y":0.40}))
    
        self.main_pop = Popup(title=filename,
                              content=self.box, 
                              size_hint=(None,None),
                              size=(1000,800),
                              auto_dismiss=False,
                              title_size=15)
    
        self.close_btn.bind(on_press=self.main_pop.dismiss)
        self.next_btn.bind(on_press=lambda x: self.pop_next(btn_in_pop))
        self.prev_btn.bind(on_press=lambda x: self.pop_previous(btn_in_pop))
        self.main_pop.open()

    def pop_next(self, instance):
        self.main_pop.dismiss()
        current_index = self.list_btn.index(instance)

        if current_index < self.btn_enabled:
            next_index = current_index + 1
            self.popup_image(self.list_btn[next_index])

        elif current_index == self.btn_enabled: 
            self.next()
            self.popup_image(self.list_btn[0])
        
    def pop_previous(self, instance):
        self.main_pop.dismiss()
        current_index = self.list_btn.index(instance)

        if current_index > 0:
            print(f"!=0")
            next_index = current_index - 1 
            self.popup_image(self.list_btn[next_index])

        elif current_index == 0: 
            print(f"==0")
            self.previous()
            self.popup_image(self.list_btn[self.btn_enabled]) # Le dernier bouton activé = avec une image          

    def count_labels_in_img(self, filename):
        json_file_path = os.path.join(folder_path, "result.json")

        with open(json_file_path, "r") as j:
            contents = json.loads(j.read())
        files = contents["files"]
        count_p_falciparum = 0
        count_other = 0

        for file in files: 
            if file["filename"] == filename: 
                predictions = file["predictions"]
                for prediction in predictions:
                    if prediction["predicted_class"] == "0": # 0 = Classe parasites
                        count_p_falciparum += 1

                    else:
                        count_other += 1
                break
        return count_p_falciparum, count_other
    
    def count_labels_in_total(self):
        json_file_path = os.path.join(folder_path, "result.json")

        with open(json_file_path, "r") as j:
            contents = json.loads(j.read())
        files = contents["files"]
        
        for file in files: 
            predictions = file["predictions"]
            for prediction in predictions:
                if prediction["predicted_class"] == "0": 
                    self.total_parasites_count += 1
                else:
                    self.total_distractors_count += 1

    def infection_rate(self):
        # Pour comprendre le calcul : Voir "Diagnostic Microscopique du Paludisme" de WHO
        total_normalized = self.total_parasites_count / len(self.list_images)*100
        print(f"Nombre de parasites par 100 champs: {total_normalized}")
        print(f"Nombre de parasites par 10 champs: {total_normalized/10}")
        print(f"Nombre de parasites par champ: {total_normalized/100}")            
        if total_normalized >= 1 and total_normalized < 11: 
            self.infection_btn.text = "Taux d'infection: +"
            self.rate = "+"
            self.btn_pdf.bind(state=self.create_pdf)
            return 1
        elif (total_normalized) >= 11 and (total_normalized) <= 100   : 
            self.infection_btn.text = "Taux d'infection: ++"
            self.rate = "++"
            self.btn_pdf.bind(state=self.create_pdf)
            return 2
        elif (total_normalized/100) >= 1 and (total_normalized/100) < 10: 
            self.infection_btn.text = "Taux d'infection: +++"
            self.rate = "+++"
            self.btn_pdf.bind(state=self.create_pdf)
            return 3
        elif (total_normalized/100) >= 10: 
            self.infection_btn.text = "Taux d'infection: ++++"
            self.rate = "++++"
            self.btn_pdf.bind(state=self.create_pdf)
            return 4     
        elif total_normalized ==0:
            self.infection_btn.text = "Négatif à la malaria"
            self.rate = "-"
            self.btn_pdf.bind(state=self.create_pdf)
            return 5

    def create_pdf(self, instance1, instance2) :
        if os.path.exists("resultats_pdf") == False: 
            os.mkdir("resultats_pdf") 

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=25)
        pdf.cell(200, 15, txt="RAPPORT DE TEST MALARIA", ln=1, align="C")
        
        pdf.set_font("Arial", size=40)
        pdf.cell(200, 30, txt=f'ID : {self.numero}', ln = 1, align ="C")
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt=f"Nom du patient : ", ln = 1, align ="L")
        pdf.cell(200, 10, txt=f"Date d'analyse : {self.date}", ln = 1, align ="L")
        pdf.cell(200, 10, txt=f"Heure d'analyse : {self.heure}", ln = 1, align ="L")
        pdf.cell(200, 10, txt=f"Nom de l'opérateur : ", ln = 1, align ="L")
        pdf.cell(200, 10, txt=f"Modèle d'appareil : Olympus", ln = 1, align ="L")

        pdf.cell(200, 15, txt=f"", ln = 1, align ="L")

        pdf.set_font("Arial", size=20)
        pdf.cell(200, 20, txt=f"\nRESULTATS D'ANALYSE", ln = 1, align = "C")
        pdf.set_font("Arial", size=30)
        if self.rate != "-" :
            pdf.cell(200, 20, txt=f"\nTaux d'infection : {self.rate}", ln = 1, align = "C")
        else :
            pdf.cell(200, 20, txt=f"\nTaux d'infection : NEGATIF", ln = 1, align = "C")
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 15, txt=f"\nNombre de parasites sur 100 champs de vue : {self.total_parasites_count}", ln = 1, align = "L")
        pdf.cell(200, 10, txt=f"\nNombre de distracteurs sur 100 champs de vue : {self.total_distractors_count}", ln = 1, align = "L")

        pdf.cell(200, 30, txt=f"", ln = 1, align ="L")

        pdf.set_font("Arial", size=14)
        pdf.cell(200, 15, txt=f"\nTableau de lecture du taux d'infection", ln = 1, align = "L")
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"\n+ = 1 à 10 parasites pour 100 champs de la goutte épaisse à l'objectif à immersion", ln = 1, align = "L")
        pdf.cell(200, 10, txt=f"\n++ = 11 à 100 parasites pour 100 champs de la goutte épaisse à l'objectif à immersion", ln = 1, align = "L")
        pdf.cell(200, 10, txt=f"\n+++ = 1 à 10 parasites par champ de la goutte épaisse à l'objectif à immersion", ln = 1, align = "L")
        pdf.cell(200, 10, txt=f"\n++++ = plus de 10 parasites par champ de la goutte épaisse à l'objectif à immersion", ln = 1, align = "L")
        
        pdf.output(f"resultats_pdf\{self.numero}.pdf")    
        self.btn_pdf.disabled = True 

        

    def change_json(self, nom_patient, nom_operateur, rate, total_parasites, total_distractors):

        new_patient = {
            "id": "",
            "nom_patient": nom_patient, 
            "date_analyse": self.date, 
            "heure_analyse": self.heure,
            "nom_operateur": nom_operateur,
            "rate": rate,
            "total_ parasites": total_parasites,
            "total_distractors": total_distractors            
            }
        
        try:
            with open("patients.json", 'r') as fp : 
                patients_json_dict = json.load(fp)
                new_patient.update({"id": self.numero})
                patients_json_dict.append(new_patient)
            with open("patients.json", 'w') as json_file:
                json.dump(patients_json_dict, json_file, 
                        indent=4,  
                        separators=(',',': '))
            
        except FileNotFoundError:
            print('Sorry the file we\'re looking for doesn\' exist')
            with open("patients.json", 'w') as json_file:
                new_patient.update({"id": self.numero})
                json.dump([new_patient], json_file, 
                        indent=4,  
                        separators=(',',': '))
        
    pass

    
class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomePage(name="home"))
        self.screen_manager.add_widget(MicroscopePage(name="microscope_page"))
        self.screen_manager.add_widget(InfectionRatePage(name="infection_page"))
        return self.screen_manager
        
kv = Builder.load_file("plasmodium.kv") # Fichier de style de l'interface

def delete_folder(folder_to_delete): 
    files_to_delete = os.listdir(folder_to_delete)
    for file in files_to_delete:
        os.remove(os.path.join(folder_to_delete, file))
    os.rmdir(folder_to_delete)

if __name__ == "__main__": 
    Window.maximize() 
    global model 
    model = load_model("model01032023.pth") # Chargement du modèle de Machine Learning
    MainApp().run()
    delete_folder(resized_path) # Libérer de l'espace en supprimant le fichier resize en fermant l'application