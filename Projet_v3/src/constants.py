import pandas as pd
from src.Corpus import Corpus
# permet d'afficher dans la console des logs
# 0 = silencieux, 1 = affichage
DEBUG = 0

# liste des artistes de base:
artistes = ["Angèle", "Clara Luciani", "Louane", "Vianney", "Aya Nakamura", "Stromae", "Julien Doré", "Gims", "Soprano", "Zaz"]

# le nombre de musiques récupérées pour chaque artiste
MAX_SONGS = 10

# clé "super secrète" pour l'API GENIUS
GENIUS_TOKEN = 'tPV6pc7DhJzBC9FWaC2jYw1Gc0FOsOgOkzgulrO23mXdYCeWNeKDRgZ2yL0NWDJ-'

# Path de l'emplacement du corpus
CORPUS_PATH = "data/corpus.pkl"

# dataframe vide
data = {
    "Titre": [],
    "Artiste":[],
    "Paroles": [],
    "Score": []
}
empty_data_frame = pd.DataFrame(data)

# Même si le corpus est un singleton,
# au lieu de redemander la création du corpus dans chaque fichier où il est demandé,
# on l'importe une fois depuis ce fichier
CORPUS = Corpus("Corpus")
