from Classes import *

class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", type="Reddit", nb_coms=None):
        super().__init__(titre, auteur, date, url, texte)
        self.type = type
        self.nb_coms = nb_coms

    def __str__(self):
        return f"{self.titre}, par {self.auteur}, nb de commentaires {self.nb_coms}"
    
    def getType(self):
        return self.type

class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", type="Arxiv"):
        super().__init__(titre, auteur, date, url, texte)
        self.type = type
        
        if isinstance(auteur, list):
            self.coauteurs = auteur[1:]
            self.auteur = auteur[0]
        else:
            self.coauteurs = None
            self.auteur = auteur

    def __str__(self):
        return f"{self.titre}, par {self.auteur}, coauteurs {self.coauteurs}"
    
    def getType(self):
        return self.type