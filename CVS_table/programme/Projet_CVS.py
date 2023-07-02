#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:01:13 2023

@author: gordibus
"""
import spacy
import json 
import glob
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

def stocker(chemin, contenu):
    w =open(chemin, "w")
    w.write(json.dumps(contenu , indent = 2))
    w.close()
    print(chemin)
    
    ### On initialise nos définition que l'on met en haut repris des corrections des projet prècèdant
def lire_corpus(chemin):    
        with open (chemin,"r", encoding='utf-8') as fichier:
            texte=fichier.read()
            return texte

def entite_nommee(text):
    entities = {}
    i = 0
    ### On initialise une boucle for dans laquelle on met une fonction qui prend le contexte avant et après l'entité nomée a l'aide de la fonction spacy .end et .start
    for entite in text.ents:
        debut = max(entite.start - 5, 0)
        fin = min(entite.end + 5, len(text))
        gauche = text[debut:entite.start].text
        droite = text[entite.end:fin].text
        enti="Entite"+str(i)
        entities[enti]={}
        entities[enti]['entite']=entite.text
        entities[enti]['label']=entite.label_
        entities[enti]['Contexte gauche']= gauche
        entities[enti]['Contexte droite']= droite
        i += 1
    return entities

def lire_json(chemin):
    with open(chemin) as mon_fichier:
        data = json.load(mon_fichier)
        return data

def convert_to_dataframe(entities):
    df = pd.DataFrame.from_dict(entities, orient='index')
            ### On identifi les label et leurs position pour qu'ils soient reconnaissable par la définition (dans l'ordre sinon ça ne fonction #j'ai du essayé pendant 1h pour comprendre que ce n'était pas dans l'odre mais ça fonctionne !!!)
    df['id'] = df.index
    df['entite']
    df['label']
    df['Contexte gauche']
    df['Contexte droite']
    return df

def conv_csv(df, file_path):
    df.to_csv(file_path, index=False)
    
### MAIN / Chemin 
path_corpora = "../DATA/*.txt"
nlp=spacy.load("fr_core_news_sm")
for chemin in glob.glob(path_corpora):
    print(chemin)
            ### Grande 3 du devoir 
    texte_fichier = lire_corpus(chemin)
    texte_nlp = nlp(texte_fichier)
    r_entite = entite_nommee(texte_nlp)
    stocker("%s_entite-nomees_.json" % chemin, r_entite)
        ### Fonctionne pas
# def lire_fichier_json (chemin):
#     with open (chemin) as json_data:
#         dist = json.load(json_data)
# path = '../DATA/def_totalitarisme.txt_entite-nomee_annotation.json'
# data = lire_fichier_json(path)
# liste_FP=[]
# liste_VP=[]
# for cle, valeur in data.items():
#     print(valeur)
#     for val3,val4 in valeur.items:
#         print (val3,val4)
#         if val3 == "FP":
#             liste_FP.append("FP")
#             liste_FP.append(valeur)
#         if val4 == "VP":
#             liste_VP.append("VP")
#             liste_VP.append(valeur)
# labels = liste_FP[0],liste_VP[0]
# sizes = len(liste_FP)-1, len(liste_VP)-1
# colors = ["lightcaral","gold"]

        ### Grand 4 du devoir
# Initialisation des listes qui serviront à construire le DataFrame de pandas
ids = []
textes = []
labels = []
contextes_gauches = []
contextes_droits = []
annotations = []
            #Chemin du dossier spécifique qui a été manuellement annoté
chemin_json = "../DATA/def_totalitarisme.txt_entite-nomee_annotation.json"
for ch in glob.glob(chemin_json):
    json_lu=lire_json(ch)
    df = convert_to_dataframe(json_lu)
    #Conversion de celui ci en tableau CSV
    conv_csv(df,"%s_entite-csv_.csv"%ch)
    for nom_entite, entite in json_lu.items():
        # Ajout de valeurs sur le tableau
        ids.append(nom_entite)
        textes.append(entite["entite"])
        labels.append(entite["label"])
        contextes_gauches.append(entite["Contexte gauche"])
        contextes_droits.append(entite["Contexte droite"])
        annotations.append(entite["annotation"])
        

            ### Création du dictionnaire DataFrame
data = {
    "id": ids,
    "texte_entite": textes,
    "label_entite": labels,
    "contexte_gauche": contextes_gauches,
    "contexte_droit": contextes_droits,
    "annotation": annotations
}
df = pd.DataFrame(data)

# On print le tout histoire de voir le résultat sur le terminal optionnel surtout sinon je trouve que le terminal rreste bien vide...
print(df)

        ### Creation d'un graphique avec légende "(s'il vous plait) avec Seaborn 
sns.countplot(x='label_entite', hue='annotation', data=df)
sns.set_style("whitegrid")
plt.show()
#plt.savefig('../DATA/graphique_VF_FP.png')