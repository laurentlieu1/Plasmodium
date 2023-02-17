from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.image import Image as kivyim
from kivy.uix.button import Button
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatIconButton,MDRaisedButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.clock import Clock

from plyer import filechooser
from PIL import Image
from pathlib import Path
import os.path
import os
import cv2
import subprocess
import skimage.io as io
import time

from model import *
class HomePage(Screen):
    
 
    pass

class MicroscopePage(Screen):
    
    def run_microscope(self):
        connexion = self.connect_microscope()
        if connexion == True : 
            #self.connected_microscope.text = "Microscope connecté"
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            self._keyboard.bind(on_key_down = self._on_key_down)
            self.btn_move_left.disabled = False
            self.btn_move_right.disabled = False
            self.btn_move_up.disabled = False
            self.btn_move_down.disabled = False
            self.add_widget(MDRaisedButton(text = "Lancer la capture automatique", 
                                        font_name= 'louis_george_caf\Louis George Cafe.ttf',
                                        size_hint = (.35,.08),
                                        font_size = 0.03*self.height,
                                        md_bg_color = "#ad526d",
                                        pos_hint = {"x" : 0.05, "y" : 0.04}, 
                                        on_press = self.cartographie_goutte))




        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers) :
        if keycode[0] == 273 :
            self.mouv_haut(1)
        elif keycode[0] == 274 :
            self.mouv_bas(1)    
        elif keycode[0] == 275 :
            self.mouv_droite(1)
        elif keycode[0] == 276 :
            self.mouv_gauche(1)

    # fonction pour la croix directionnel   
    def mouv_gauche(self, step_count):
        print("deplacement gauche ")
    # fonction pour la croix directionnel
    def mouv_droite(self, step_count):
        print("deplacement droite ")
    # fonction pour la croix directionnel
    def mouv_haut(self, step_count):
        print("deplacement haut")
    # fonction pour la croix directionnel
    def mouv_bas(self, step_count):
        print("deplacement bas")

    def connect_microscope(self):
        # return False
        return True

    def goto(self, cord_x, cord_y, speed):
        print(f"deplacement au coord {cord_x}, {cord_y}")

    # sousfonction utiliser dans la librairie peut etre utiliser uniquement pour la previsualisation des photos
    def prise_photo(self):
        print("vous avez pris une photo")  

    # fonction a mettre en parametre de la fonction cartographie goute
    def creation_carte(self, nombre_photo_x, nombre_photo_y):
        carte_pos = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (1,1), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3), (3,2), (3,1), (3,0),]
        return carte_pos


    # uliser cette fonction pour cartographier la goute et prendre toute les photos
    def cartographie_goutte(self, instance): # , carte_pos, photo_delay, speed, la  variable carte_pos doit etre créer via la fonction creation carte
        """for pos in carte_pos():
            self.goto(self,pos[0], pos[1])
            self.prise_photo(self)"""
        self.add_widget(MDRaisedButton(text = "Voir le dossier avec les images", 
                                        font_name= 'louis_george_caf\Louis George Cafe.ttf',
                                        size_hint = (.25,.08),
                                        font_size = 0.03*self.height,
                                        md_bg_color = "#65ab5e",
                                        pos_hint = {"x" : 0.465, "y" : 0.04}))

    def abort(self):
        print("capture d'image a ete arreter")

    
    pass

class InfectionRatePage(Screen):
    

    def select_file(self, instance):
        try :
            self.main_pop.dismiss()
        except AttributeError : 
            pass
        filechooser.choose_dir(on_selection = self.analyse_folder)   # faire un try except quand on ne choisit pas de fichier, quand on ne choisit pas un dossier avec des img
        #self.analyse_folder("output")

    def analyse_folder(self, folder): 
        try : 
            self.total_parasites = 0
            self.total_distractor = 0
            print(folder)
            
            global folder_path
            folder_path = inference_on_folder(folder[0], model)
            #folder_path = folder
            if (len(os.listdir(folder_path))!=0):
                self.import_btn.background_color =(0, 1, 0, 1)
                self.resize_img()
                self.start = 0  
                self.display_images(0.4)
                return "Unzip_selected successful"
            return "Unzip_selected failed"
        except IndexError : 
            print("Vous n'avez pas choisi de fichier. Veuillez réessayer")
            self.box=FloatLayout()
            
            self.label = Label(text = "Vous n'avez pas sélectionné de dossier. \nSouhaitez-vous quitter ?", pos_hint={'x':0,'y':0.18})
            self.btn_continue =(MDFillRoundFlatButton(text="Choisir un dossier", font_size = self.height * 0.02, size_hint=(.1, .05), pos_hint={'x':0.1,'y':0.1}))
            self.btn_quit =(MDFillRoundFlatButton(text="Quitter", font_size = self.height * 0.02, size_hint=(.1, .05), pos_hint={'x':0.7,'y':0.1}))

            self.box.add_widget(self.btn_continue)
            self.box.add_widget(self.btn_quit)
            self.box.add_widget(self.label)

            self.error_pop = Popup(title= "Voulez-vous continuer ?", content=self.box, size_hint=(None,None),size=(400,200),auto_dismiss=False,title_size=15)
            self.btn_continue.bind(on_press = self.close_then_filechooser)
            self.btn_quit.bind(on_press=self.error_pop.dismiss)
            self.error_pop.open()

    def close_then_filechooser(self, instance):
        self.error_pop.dismiss()
        Clock.schedule_once(self.select_file, .5)

    def resize_img(self):
        self.list_images = os.listdir(folder_path)
        self.list_images.pop(-1) # on enlève le fichier .json
        head, tail = os.path.split(folder_path)
        global resized_path
        resized_path = os.path.join(head,'resized')
        
        if os.path.exists(resized_path) == True : 
            delete_folder(resized_path)
        
        os.mkdir(resized_path)
        
        for img in self.list_images : 
            if (os.path.splitext(img)[1]) != ".json" : 
                img_path = os.path.join(folder_path, img)
                resize_img_path = os.path.join(head,'resized', img)
                image = Image.open(img_path)
                new_height = 160
                new_width = int(new_height / image.height * image.width)
                img_resize = image.resize((new_width,new_height))
                img_resize.save(resize_img_path)
        self.count_labels_in_total()
        self.add_widget(MDRaisedButton(text = f'Nombre total de parasite(s) : {self.total_parasites}', font_name = 'louis_george_caf\Louis George Cafe.ttf', size_hint =(.27,.05), font_size = 0.03*self.height, disabled = True, disabled_color = "white", md_bg_color_disabled = "b73123", pos_hint = {"center_x" : 0.295, "y" : 0.22}))
        self.add_widget(MDRaisedButton(text = f'Nombre total de distractor(s) : {self.total_distractor}', font_name = 'louis_george_caf\Louis George Cafe.ttf', size_hint =(.27,.05), font_size = 0.03*self.height, disabled = True, disabled_color = "white", md_bg_color_disabled = "315aa2", pos_hint = {"center_x" : 0.295, "y" : 0.15}))
        self.infection_btn = (MDRaisedButton(text = f"Taux d'infection : ", font_name = 'louis_george_caf\Louis George Cafe.ttf', size_hint =(.4,.125), font_size = 0.03*self.height, disabled = True, disabled_color = "white", md_bg_color_disabled = "717171", pos_hint = {"center_x" : 0.65, "y" : 0.15}))
        self.add_widget(self.infection_btn)
        
    
    def display_images(self, x_pos):   
        
        self.btn_next_viewer.disabled = False
        self.btn_previous_viewer.disabled = False
        
        print(f'\nImage folder : {folder_path}')
        self.list_btn = [self.btn_r1_c1, self.btn_r1_c2, self.btn_r1_c3, self.btn_r1_c4, self.btn_r1_c5, 
                    self.btn_r2_c1, self.btn_r2_c2, self.btn_r2_c3, self.btn_r2_c4, self.btn_r2_c5]

        # tant qu'on ajoute fait +10 et que ça ne dépasse pas le nb d'images total
        if self.start + 10 <= len(self.list_images) : # vérif < ou <=
            self.nb_img.text = f"Images : {self.start} à {self.start + 10}/{len(self.list_images)}"
            for i in range(self.start, self.start + 10):
                self.list_btn[i-self.start].background_normal = os.path.join(resized_path,self.list_images[i])
                self.list_btn[i-self.start].disabled = False
        
        # quand on fait +10 et que ça dépasse nb img totale
        elif self.start + 10 > len(self.list_images) :
            imgs_restants = len(self.list_images) - self.start
            if imgs_restants <= 5 :
                self.nb_img.text = f"Images : {self.start} à {imgs_restants}/{len(self.list_images)}"
            else : 
                self.nb_img.text = f"Images : {self.start} à {imgs_restants+10}/{len(self.list_images)}"
            padding = len(self.list_btn) - imgs_restants
            for i in range(self.start, self.start + imgs_restants) : 
                self.list_btn[i-self.start].background_normal = os.path.join(resized_path,self.list_images[i])
                self.list_btn[i-self.start].disabled = False
            for i in range(imgs_restants, imgs_restants + padding) : 
                self.list_btn[i].background_normal = ""
                self.list_btn[i].disabled = True
        
        self.infection_rate()

        self.btn_enabled = -1
        for btn in self.list_btn : 
            if not btn.disabled :
                self.btn_enabled += 1
        
    
   
    def next(self): 
        if self.start+10 >= len(self.list_images):
            self.start = 0
        else : 
            self.start += 10
        self.display_images(0.4)

    def previous(self):
        print(f'self_start : {self.start}')
        if self.start <= 0 :  
            self.start = len(self.list_images) - (len(self.list_images)-10)%10 
            if self.start == 100 : 
                self.start = 90
            print(f'self_start after : {self.start}')
        else : 
            self.start -= 10
        self.display_images(0.4)


    def show_it(self, instance): # un compteur d'élément pour les images et un par image
        global btn_in_pop
        btn_in_pop = instance
        self.box=FloatLayout()
        head, filename = os.path.split(instance.background_normal)
        img_path = os.path.join(folder_path, filename)

        self.btn_index = self.list_btn.index(instance)
        print(f"instance : {self.btn_index}")
        self.box.add_widget(kivyim(source=img_path, size_hint=(None,None), size = (550,550),pos_hint={'x':0.1,'y':0.15}))
            
        self.but=(MDFillRoundFlatButton(text="Fermer", font_size = self.height * 0.03, size_hint=(.2, .07), pos_hint={'x':0.4,'y':0.03}))
        self.box.add_widget(self.but)
            
        self.count_falciparum, self.count_other = self.count_labels_in_img(filename)

        self.box.add_widget(MDRectangleFlatIconButton(text = f'P. Falciparum\n{self.count_falciparum}', font_name = 'louis_george_caf\Louis George Cafe.ttf', disabled_color = "white", font_size = self.height * 0.035, md_bg_color_disabled= "red", size_hint = (.2,.1), text_color = "white", line_color_disabled = "red", disabled = True,  pos_hint={'x':0.68,'y':0.57}))      
        self.box.add_widget(MDRectangleFlatIconButton(text = f'Distractor\n{self.count_other}', font_name = 'louis_george_caf\Louis George Cafe.ttf', font_size = self.height * 0.035, disabled_color = "white", md_bg_color_disabled= "blue", size_hint = (.2,.1), text_color = "white", line_color_disabled = "blue", disabled = True,  pos_hint={'x':0.68,'y':0.40}))
        self.prev_btn = MDFillRoundFlatButton(text='<', font_size = self.height * 0.02, size_hint = (.015,.015), pos_hint={'x':0.01,'y':0.49})
        self.next_btn = MDFillRoundFlatButton(text='>', font_size = self.height * 0.02, size_hint = (.015,.015), pos_hint={'x':0.92,'y':0.49})

        self.box.add_widget(self.prev_btn)
        self.box.add_widget(self.next_btn)
        self.main_pop = Popup(title=filename,content=self.box, size_hint=(None,None),size=(1000,800),auto_dismiss=False,title_size=15)
    
        self.but.bind(on_press=self.main_pop.dismiss)
        self.next_btn.bind(on_press = lambda x : self.pop_next(btn_in_pop))
        self.prev_btn.bind(on_press = lambda x : self.pop_previous(btn_in_pop))

        self.main_pop.bind(on_dismiss = self._on_keyboard_closed)
        self.main_pop.open()

    def pop_next(self, instance):
        self.main_pop.dismiss()
        current_index = self.list_btn.index(instance)
        if current_index < self.btn_enabled :
            next_index = current_index + 1
            self.show_it(self.list_btn[next_index])
        elif current_index == self.btn_enabled : 
            self.next()
            self.show_it(self.list_btn[0]) #0-1
        

    def pop_previous(self, instance):
        self.main_pop.dismiss()
        current_index = self.list_btn.index(instance)
        if current_index > 0 :
            print(f'!=0')
            next_index = current_index - 1 
            self.show_it(self.list_btn[next_index])
        elif current_index == 0 : 
            print(f'==0')
            self.previous()
            self.show_it(self.list_btn[self.btn_enabled])
            

    def count_labels_in_img(self, filename):
        #print(filename)
        json_file_path = os.path.join(folder_path, "result.json")
        print(json_file_path)
        with open(json_file_path, 'r') as j:
            contents = json.loads(j.read())

        files = contents["files"]
        count_p_falciparum = 0
        count_other = 0

        for file in files : 
            if file['filename'] == filename : 
                predictions = file["predictions"]
                for prediction in predictions :
                    if prediction["predicted_class"] == '0' : 
                        count_p_falciparum += 1
                    else :
                        count_other += 1
                break
        return count_p_falciparum, count_other
    
    def count_labels_in_total(self):
        json_file_path = os.path.join(folder_path, "result.json")
        with open(json_file_path, 'r') as j:
            contents = json.loads(j.read())

        files = contents["files"]
        
        for file in files : 
            predictions = file["predictions"]
            for prediction in predictions :
                if prediction["predicted_class"] == '0' : 
                    self.total_parasites += 1
                else :
                    self.total_distractor += 1

    def infection_rate(self) :
        # dans le cas où on a pas 100 champs de  vue : normalisation 
        total_normalized = self.total_parasites / len(self.list_images) * 100
        print(f"Nombre de parasites par 100 champs : {total_normalized}")
        print(f"Nombre de parasites par 10 champs : {total_normalized/10}")
        print(f"Nombre de parasites par champ : {total_normalized/100}")            
        if total_normalized >= 1 and total_normalized <= 9 : 
            self.infection_btn.text = "Taux d'infection : +"
            return 1
        elif (total_normalized/10) >= 1 and (total_normalized/10) <= 9 : 
            self.infection_btn.text = "Taux d'infection : ++"
            return 2
        elif (total_normalized/100) >= 1 and (total_normalized/100) <= 9 : 
            self.infection_btn.text = "Taux d'infection : +++"
            return 3
        elif (total_normalized/100) >= 10 : 
            self.infection_btn.text = "Taux d'infection : ++++"
            return 4
             
    pass

    
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomePage(name="home"))
        self.screen_manager.add_widget(MicroscopePage(name="microscope_page"))
        self.screen_manager.add_widget(InfectionRatePage(name="infection_page"))
        return self.screen_manager
        
kv = Builder.load_file('plasmodium.kv')

def delete_folder(folder_to_delete) :
    files_to_delete = os.listdir(folder_to_delete)
    for file in files_to_delete :
        os.remove(os.path.join(folder_to_delete, file))
    os.rmdir(folder_to_delete)


if __name__ == "__main__": # à rechercher ce que ça veut dire...
    Window.maximize()
    global model 
    model = load_model('model.pth')
    MainApp().run()
    delete_folder(resized_path) # on garde pas le fichier resized à  = stockage inutile
