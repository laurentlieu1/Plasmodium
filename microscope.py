import time
import math

# fonction pour la croix directionnel
def mouv_gauche(step_count):
    print("deplacement gauche ")
# fonction pour la croix directionnel
def mouv_droite(step_count):
    print("deplacement droite ")
# fonction pour la croix directionnel
def mouv_haut(step_count):
    print("deplacement haut")
# fonction pour la croix directionnel
def mouv_bas(step_count):
    print("deplacement bas")

def connect_microscope():
    # return False
    return True

def goto(cord_x, cord_y, speed):
    print(f"deplacement au coord {cord_x}, {cord_y}")

# sousfonction utiliser dans la librairie peut etre utiliser uniquement pour la previsualisation des photos
def prise_photo():
    print("vous avez pris une photo")  

# fonction a mettre en parametre de la fonction cartographie goute
def creation_carte(nombre_photo_x, nombre_photo_y):
    carte_pos = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,2), (1,1), (1,0), (2,0), (2,1), (2,2), (2,3), (3,3), (3,2), (3,1), (3,0),]
    return carte_pos


# uliser cette fonction pour cartographier la goute et prendre toute les photos
def cartographie_goutte(carte_pos, photo_delay, speed): # la  variable carte_pos doit etre créer via la fonction creation carte
    for pos in carte_pos():
        goto(pos[0], pos[1])
        prise_photo()

def abort():
    print("capture d'image a ete arreter")
