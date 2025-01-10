# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
import re
import pandas as pd

class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            instance = super().__call__(*args, **kwargs)
            cls.instances[cls] = instance
        return cls.instances[cls]

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus(metaclass=SingletonMeta):
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.docustring = "Not created yet"
        self.vocabulaire = "Not created yet"

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))


    def create_docustring(self, force=False):
        if self.docustring == "Not created yet" or force is True:
            # creation de la chaine de caractère
            self.docustring = " ".join([doc.get_text() for doc in [*self.id2doc.values()]])
    
    def get_docustring(self):
        return self.docustring
    
    def concorde(self, word_to_find, max_occurences):
        table = []
        if not self.docustring == "Not created yet":
            temp = self.docustring.split(" ")
            temp = temp[5:]
            i = 0
            while i <= len(temp) and len(table) <= max_occurences:
                word = temp[i]
                if word == word_to_find:
                    result = [" ".join(temp[i-5:i]), word, " ".join(temp[i+1:i+5])]
                    table.append(result)
                i += 1
            table_to_return = pd.DataFrame(table)
            table_to_return.columns=["avant", "mot", "après"]
            return table_to_return

    def search(self, word_to_find):
        temp = re.findall(word_to_find, self.docustring)
        return temp
        
    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = texte.replace('\n', '')
        texte = re.sub(r'[^\w\s]', '', texte)  # Supprimer ponctuation (garder lettres et espaces)
        texte = re.sub(r'\d+', '', texte)     # Remplacer les chiffres par des espaces
        # texte = re.sub(r'\s+', ' ', texte) # supprimer les nombreux espaces
        texte = texte.strip()
        return texte

    def create_vocabulaire(self):
        vocabulaire = {}
        raw_text = self.nettoyer_texte(self.docustring)
        list_text = raw_text.split(" ")
        for e in list_text:
            if e not in vocabulaire:
                vocabulaire[e] = 1
            else:
                vocabulaire[e] += 1
        self.vocabulaire = vocabulaire

    def get_vocabulaire(self):
        return self.vocabulaire

    def stats(self, n_mots_les_plus_frequents=10):
        pass