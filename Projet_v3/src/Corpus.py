import pickle
import re

from src.Author import Author
from src.SingletonMeta import SingletonMeta

class Corpus(metaclass=SingletonMeta):
    """
    Une classe représentant un corpus de documents.

    Attributes
    ----------
    nom : str
        Nom du corpus.
    authors : dict
        Dictionnaire associant un identifiant à chaque auteur.
    aut2id : dict
        Dictionnaire associant un nom d'auteur à son identifiant.
    id2doc : dict
        Dictionnaire associant un identifiant à chaque document.
    ndoc : int
        Nombre total de documents dans le corpus.
    naut : int
        Nombre total d'auteurs dans le corpus.

    Methods
    -------
    add(doc)
        Ajoute un document au corpus et met à jour les auteurs et les identifiants.
    show(n_docs=-1, tri="abc")
        Affiche une sélection des documents du corpus triés selon un critère.
    __repr__()
        Retourne une représentation textuelle triée des documents du corpus.
    nettoyer_texte(texte)
        Nettoie un texte en supprimant la ponctuation, les chiffres, et les espaces inutiles.
    sauvegarder_corpus(fichier)
        Sauvegarde les données du corpus dans un fichier pickle.
    charger_corpus(fichier)
        Charge les données d'un corpus depuis un fichier pickle.
    """
    def __init__(self, nom):
        """
        Initialise une instance de la classe Corpus.

        Parameters
        ----------
        nom : str
            Nom du corpus.
        """
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        """
        Ajoute un document au corpus. Si l'auteur du document n'existe pas encore,
        il est ajouté au dictionnaire des auteurs.

        Parameters
        ----------
        doc : Document
            Le document à ajouter au corpus.
        """
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        """
        Affiche une sélection des documents du corpus triés selon un critère.

        Parameters
        ----------
        n_docs : int, optional
            Nombre de documents à afficher (par défaut, tous les documents).
        tri : str, optional
            Critère de tri : "abc" pour alphabétique, "123" pour temporel (par défaut "abc").
        """
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        """
        Retourne une représentation textuelle triée des documents du corpus.

        Returns
        -------
        str
            Une chaîne contenant les documents triés par titre.
        """
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    def nettoyer_texte(self, texte):
        """
        Nettoie un texte en supprimant la ponctuation, les chiffres, les espaces inutiles
        et les métadonnées entre crochets.

        Parameters
        ----------
        texte : str
            Le texte à nettoyer.

        Returns
        -------
        str
            Le texte nettoyé.
        """
        texte = texte.lower()                 # Convertir le texte en minuscules
        texte = re.sub(r'\[.*?\]', '', texte) # Métadonnées entre crochets (comme [Refrain])
        texte = texte.replace('\n', ' ')      # Les sauts de ligne
        texte = re.sub(r'[^\w\s]', '', texte) # La ponctuation (garder seulement lettres et espaces)
        texte = re.sub(r'\d+', '', texte)     # Les chiffres
        texte = re.sub(r'\s+', ' ', texte)    # Réduire les espaces multiples
        texte = texte.strip()                 # Les espaces inutiles au début et à la fin
        return texte

    def sauvegarder_corpus(self, fichier):
        """
        Sauvegarde les données du corpus dans un fichier pickle.

        Parameters
        ----------
        fichier : str
            Chemin vers le fichier où sauvegarder les données.
        """
        temp_save = {
        "authors": self.authors,
        "aut2id": self.aut2id,
        "id2doc": self.id2doc,
        "ndoc": self.ndoc,
        "naut": self.naut
        }
        with open(fichier, 'wb') as file:
            pickle.dump(temp_save, file)
        print(f"Corpus sauvegardé dans {fichier}")

    def charger_corpus(self, fichier):
        """
        Charge les données d'un corpus depuis un fichier pickle.

        Parameters
        ----------
        fichier : str
            Chemin vers le fichier contenant les données du corpus.

        Returns
        -------
        None
        """
        try:
            with open(fichier, 'rb') as file:
                data_loaded = pickle.load(file)


            self.authors = data_loaded.get("authors", {})
            self.aut2id = data_loaded.get("aut2id", {})
            self.id2doc = data_loaded.get("id2doc", {})
            self.ndoc = data_loaded.get("ndoc", 0)
            self.naut = data_loaded.get("naut", 0)

            print(f"Corpus chargé depuis {fichier}")
        except FileNotFoundError:
            return None
