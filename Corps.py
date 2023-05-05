# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:06:12 2023

@author: yoann
"""

import csv
import os
from fonction import *
import time

#setup database
#create the database 
db = sqlite3.connect('Babelio.db')

c = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Book'")
result = c.fetchone()
print(result)
if not(result):
    db.execute('''CREATE TABLE Book
               (id INTEGER PRIMARY KEY,
                Ean TEXT,
                Title TEXT,
                Author TEXT,
                Rating FLOAT,
                RatingNumber INT,
                ReviewNumber INT,
                Url TEXT,
                Babelio_id INT)''')
               
    #création de la table de tags
    db.execute('''CREATE TABLE Tags
               (id INTEGER PRIMARY KEY,
                idtag INT,
                tag TEXT)''')
               
    #Création de la table faisant la liaison entre les livres et les tags
    db.execute('''CREATE TABLE LiaisonTagBook
               (book_ean TEXT,
                book_title TEXT,
                tag_id INTEGER,
                PRIMARY KEY (book_ean, tag_id),
                FOREIGN KEY (book_ean) REFERENCES Book(Ean),
                FOREIGN KEY (book_title) REFERENCES Book(Title),
                FOREIGN KEY (tag_id) REFERENCES Tags(idtag))''')






# Définir le chemin du répertoire contenant les fichiers CSV
chemin = 'C:/Users/yoann/Documents/Projet librairie/csv_files'

# Parcourir tous les fichiers du répertoire
fichiernumber = 1
t0=time.time()
t=t0
for fichier in os.listdir(chemin):
    if fichier.endswith(".csv"):
        # Ouvrir le fichier CSV en mode lecture
        with open(os.path.join(chemin, fichier), "r") as f:
            # Lire toutes les lignes du fichier
            lignes = f.readlines()

        # Supprimer les lignes contenant "#critiques" ou "#citations"
        lignes = [ligne for ligne in lignes if "#critiques" not in ligne and "#citations" not in ligne]
        # Afficher chaque ligne restante
        lignenumber = 1
        for ligne in lignes:            
            babelio_id = re.findall(r'\d+',ligne)
            babelio_id = int(babelio_id[len(babelio_id)-1])
            c = db.cursor()
            c.execute("SELECT * FROM Book WHERE Babelio_id=?",(babelio_id,))
            result = c.fetchone()            
            if not result:
                ligne = ligne.strip()
                Add_to_DB(ligne[1:-1])
            print('fichier : ',fichiernumber,' ligne : ',lignenumber,' execution time : ',int((time.time()-t)*1000)/1000,'s time elapsed : ',int(time.time()-t0))
            t=time.time()
            lignenumber += 1
        fichiernumber += 1

            
            
