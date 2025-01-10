from Classes import *
from Classes_tp6 import *

class Document_factory:
    @staticmethod
    def create_doc(titre, auteur, date, url, texte, type, nb_coms=""):
        if type == "Reddit":
            return RedditDocument(titre, auteur, date, url, texte, type, nb_coms=nb_coms)
        elif type == "Arxiv":
            return ArxivDocument(titre, auteur, date, url, texte, type)
        else:
            raise ValueError(f"Type de document non reconnu :{type}")