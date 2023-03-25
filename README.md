# Plasmodium
Ce dossier est composé de :

 - un fichier "code_principal_md.py" qui implémente l'interface utilisateur et relie le module électronique et IA
 - un fichier "model.py" qui détecte les parasites et annotes les images sélectionnées par l'utilisateur
 - un fichier "model01032023.pth" qui regroupe les valeurs des poids et biais utilisés dans notre model de détection "model.py"
 - un répertoire "100_img+" où on a 1-9 parasite par 100 champs de vue (dataset ZENODO)
 - un répertoire "100_img++" où on a 1-9 parasite par 10 champs de vue (dataset ZENODO)
 - un répertoire "100_img+++" où on a 1-9 parasite par 1 champ de vue (dataset ZENODO)
 - un répertoire "100_img++++" où on a > 10 parasite par 1champ de vue (dataset ZENODO)
 - un répertoire "test" avec des images de test du dataset ZENODO
 - un répertoire "Images-Lubumbashi" avec des images de terrain
 - des répertoires "font_lemon" et "louis_george_caf" pour gérer le style de police

Librairies à installer : 

 - kivy 
 - kivymd
 - plyer 
 - pillow 
 - opencv-python
 - scikit-image 
 - torch 
 - detectron2
 - numpy
 - skimage.io
 - json
 - datetime
 - fpdf


Un patient est défini en fonction de la date d'analyse par son identifiant qui reprend le format suivant : année-mois-compteur
Le compteur est incrémenté de 1 à chaque fois qu'une analyse est réalisée. 
L'identifiant est le nom du répertoire des images annotés du patient et le nom du pdf dans lequel on retrouve les résultats de l'analyse.

Le lien vers les modèles qui sont au format .pth et qui sont dans le répertoire model_folder : https://drive.google.com/drive/u/1/folders/13nViVT-kJAV_AspLqJDfGzXYGUpvD-Zv

!! Ne pas renommer le fichier "patients.json", les répertoires "output" et "resultats_pdf"
