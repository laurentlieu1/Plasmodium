
#IMPORTS
import torch
import detectron2
from detectron2.data import DatasetCatalog, MetadataCatalog, build_detection_test_loader, build_detection_train_loader
from detectron2.data import detection_utils as utils
import detectron2.data.transforms as T
from detectron2.engine import DefaultTrainer
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.modeling import build_model
from detectron2.checkpoint import DetectionCheckpointer
import skimage.io as io
import os
import cv2
import json 
import numpy as np
from datetime import datetime

#LOAD_MODEL
#Prends un fichier ".pth" en entrée pour charger les poids
def load_model(filename) : 
    cfg = get_cfg() #Crée un fichier de configuration
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml")) #Récupère l'architecture du modèle
    #cfg.MODEL.DEVICE = "cpu" #Décommentez ceci si vous n'avez pas de GPU Cuda
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 8 #Nombre de classes + 1 pour le background
    cfg.MODEL.WEIGHTS = filename #Chargement des poids
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 #Seuil de décision
    predictor = DefaultPredictor(cfg) #Création du prédicteur
    return predictor

#Inference
#Prends un chemin vers une image + le modèle à utiliser
def inference(img_name, model) :
    img = io.imread(img_name)
    return model(img)

#Inference_on_folder
#Prends un dossier contenant x images en entrée ainsi que le modèle à utiliser
def inference_on_folder(folder, model) :

    label_colormap = { "0" : (0,0,255)} #Colormap pour les labels
    label_name = {"0" : "P. Falciparum"} #Nom des labels => Si pas Falciparum, directement Distractor
    folder_name = os.path.split(folder)[1]
    dict = {"folder" : folder_name, 'files' : []} #Dictionnaire pour le report

    if not os.path.exists("output") : 
        os.mkdir("output")

    date_time = datetime.now()
    try:
        with open("patients.json", 'r') as fp : 
            patients_json_dict = json.load(fp)
            output_id = date_time.strftime("%Y-%m-") + str((len(patients_json_dict)) + 1) # numéro id
                    
    except FileNotFoundError:
        print('Sorry the file we\'re looking for doesn\' exist')
        output_id = date_time.strftime("%Y-%m-") + "1" # numéro id

    folder_path = os.path.join('output', output_id)

    if not os.path.exists(folder_path) : 
        os.mkdir(folder_path)

    for file in os.listdir(folder) : #Parcourt le dossier
        if ".jpg" in file :
            try :
                print(folder_name)
                filename = folder + '/' + file  #Construction de la ligne de chemin vers le fichier
                #print(filename)

                dict["files"].append({"filename" : file, "predictions" : []})   #Rajout d'un bloc pour chaque fichier

                output = inference(filename, model) #Inference

                #Récupération des informations de la prédictions (bouding_box, classe prédites, scores)
                bounding_boxes = output['instances'].pred_boxes.tensor.cpu().numpy()
                pred_classes = output['instances'].pred_classes.cpu().numpy()
                scores = output['instances'].scores.cpu().numpy()

                #Lecture de l'image
                img = cv2.imread(filename)

                #On parcourt toutes les classes prédites
                for i in range(len(pred_classes)) :

                    new_pred = summary_report(bounding_boxes, pred_classes, scores, i)
                    dict["files"][-1]["predictions"].append(new_pred)

                    if str(pred_classes[i]) in label_colormap : #Si Falciparum est la classe prédite d'une zone d'intérêt
                        #Positionnement du rectangle de la couleur correspondante + Nom de la classe
                        img = cv2.rectangle(img, (int(bounding_boxes[i][0]), int(bounding_boxes[i][1])),(int(bounding_boxes[i][2]),int(bounding_boxes[i][3])), color=label_colormap[str(pred_classes[i])], thickness=2)
                        img = cv2.putText(img, label_name[str(pred_classes[i])], (int(bounding_boxes[i][0]), int(bounding_boxes[i][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))
                    else : #Si la classe prédite n'est pas Falciparum donc Distractor
                        #Positionnement du rectangle de la couleur correspondante + Nom de la classe
                        img = cv2.rectangle(img, (int(bounding_boxes[i][0]), int(bounding_boxes[i][1])),(int(bounding_boxes[i][2]),int(bounding_boxes[i][3])), color=(255,0,0), thickness=2)
                        img = cv2.putText(img, 'Distractor', (int(bounding_boxes[i][0]), int(bounding_boxes[i][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0))


                #Sauvegarde de l'image
                
                file_path = os.path.join(folder_path, file)
                print("file path :", file_path)
                if not cv2.imwrite(file_path, img) : #Si l'image n'a pas pu être sauvegardé => Exception
                    raise Exception
                
            except Exception as error:
                print(error)

    json_path = os.path.join(folder_path, "result.json")
    print(json_path)
    with open(json_path, "w") as f : #Ecriture dans le fichier JSON
        json.dump(dict, f, indent=2)
    #print(dict)
    return folder_path, output_id

def summary_report(bounding_boxes, pred_classes, scores, i) :
    #Nouvelle ligne de pour predictions
    new_pred = {"id" : str(i), "predicted_class" : str(pred_classes[i]), "bounding_boxes" : str(bounding_boxes[i]), "score" : str(scores[i])}
    return new_pred


#TEST
#model = load_model('model.pth')
#output = inference_on_folder(r"2_img", model)  #Chemin à remplacer ici
#print(output)


