import re
import pandas as pd
import scipy as sp
import numpy as np
from collections import defaultdict

from src.Corpus import Corpus
from src.constants import CORPUS

class RechercheCorpus(Corpus):
    """
    Une classe permettant de réaliser des recherches dans un corpus de documents.

    Hérite de la classe Corpus et ajoute des fonctionnalités spécifiques à la recherche et à l'analyse de texte.

    Attributes
    ----------
    authors : dict
        Dictionnaire des auteurs dans le corpus.
    aut2id : dict
        Dictionnaire des auteurs associant leur nom à un identifiant.
    id2doc : dict
        Dictionnaire associant l'identifiant d'un document à ce document.
    ndoc : int
        Nombre total de documents dans le corpus.
    naut : int
        Nombre total d'auteurs dans le corpus.
    docustring : str, optional
        Chaîne de texte concaténée représentant tous les documents du corpus.
    vocabulaire : dict, optional
        Dictionnaire contenant les mots du corpus et leurs caractéristiques.
    tf_matrix : scipy.sparse.csr_matrix, optional
        Matrice de fréquence des termes (TF) pour chaque document.
    tfidf_matrix : scipy.sparse.csr_matrix, optional
        Matrice TF-IDF pour chaque document.
    """
    def __init__(self, nom):
        """
        Initialise une instance de la classe RechercheCorpus.

        Parameters
        ----------
        nom : str
            Le nom du corpus.
        """
        super().__init__(nom)
        self.authors = CORPUS.authors.copy()
        self.aut2id = CORPUS.aut2id.copy()
        self.id2doc = CORPUS.id2doc.copy()
        self.ndoc = CORPUS.ndoc
        self.naut = CORPUS.naut
        self.docustring = None
        self.vocabulaire = None
        self.tf_matrix = None
        self.tfidf_matrix = None

# =============== 6 : TRAITEMENT DE TEXTE ===============

    def create_docustring(self, force=False):
        """
        Crée la chaîne de texte représentant tous les documents du corpus.

        Si la chaîne existe déjà, elle est recréée uniquement si le paramètre `force` est True.

        Parameters
        ----------
        force : bool, optional
            Si True, recrée la chaîne même si elle existe déjà (par défaut False).
        """
        if self.docustring is None or force is True:
            # création de la chaine de caractère
            self.docustring = " ".join([doc.get_text() for doc in [*self.id2doc.values()]])

    def get_docustring(self):
        """
        Retourne la chaîne de texte représentant tous les documents du corpus.

        Returns
        -------
        str
            La chaîne de texte concaténée.
        """
        return self.docustring

    def concorde(self, word_to_find, max_occurences=42):
        """
        Recherche les occurrences d'un mot dans le texte du corpus et extrait un contexte autour de chaque occurrence.

        Parameters
        ----------
        word_to_find : str
            Le mot à rechercher dans la chaîne de texte du corpus.
        max_occurences : int, optional
            Le nombre maximum d'occurrences à afficher (par défaut 42).

        Returns
        -------
        pd.DataFrame
            Un DataFrame contenant les contextes trouvés avec les colonnes "avant", "mot", et "après".
        """
        table = []
        if not self.docustring is None:
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

    def search_nul(self, word_to_find):
        """
        Recherche toutes les occurrences exactes d'un mot dans la chaîne de texte du corpus.

        Parameters
        ----------
        word_to_find : str
            Le mot à rechercher.

        Returns
        -------
        list
            Une liste des occurrences trouvées.
        """
        temp = re.findall(word_to_find, self.docustring)
        return temp

    def create_vocabulaire(self):
        """
        Crée le vocabulaire du corpus, c'est-à-dire un dictionnaire des mots uniques et leur fréquence d'apparition.

        Met à jour l'attribut `vocabulaire` avec les mots du corpus et leurs statistiques.
        """
        vocab = {}
        word_id = 0
        for doc in self.id2doc.values():
            words = set(doc.texte.lower().split())
            # Liste des mots dans chaque document
            for word in words:
                if word not in vocab:
                    vocab[word] = {
                        'id': word_id,
                        'occurrences_totales': 0,
                        'documents_contenant': 0
                    }
                    word_id += 1
                vocab[word]['occurrences_totales'] += doc.texte.lower().split().count(word)
                vocab[word]['documents_contenant'] += 1
        self.vocabulaire = vocab

    def get_vocabulaire(self):
        """
        Retourne le vocabulaire du corpus.

        Returns
        -------
        dict
            Le vocabulaire du corpus avec les statistiques des mots.
        """
        return self.vocabulaire

# =============== 7 : MATRICE ===============

    def create_tf_matrix(self):
        """
        Crée la matrice de fréquence des termes (TF) pour chaque document du corpus.

        Cette matrice contient les fréquences des mots dans les documents sous forme de matrice creuse (sparse).
        """
        vocab_size = len(self.vocabulaire)
        tf_data = []
        tf_row_indices = []
        tf_col_indices = []

        for doc_id, doc in self.id2doc.items():
            doc_text = self.nettoyer_texte(doc.texte).split()
            word_counts = defaultdict(int)

            for word in doc_text:
                if word in self.vocabulaire:
                    word_counts[word] += 1

            # Ajouter les données pour chaque mot trouvé dans ce document
            for word, count in word_counts.items():
                word_idx = self.vocabulaire[word]['id']
                tf_data.append(count)
                tf_row_indices.append(doc_id - 1)
                tf_col_indices.append(word_idx)

        # Créer la matrice sparse
        self.tf_matrix = sp.sparse.csr_matrix((tf_data, (tf_row_indices, tf_col_indices)),
                                    shape=(self.ndoc, vocab_size))

    def get_tf_matrix(self):
        """
        Retourne la matrice de fréquence des termes (TF).

        Returns
        -------
        scipy.sparse.csr_matrix
            La matrice creuse (sparse) contenant les fréquences des termes pour chaque document.
        """
        return self.tf_matrix

    def create_tfidf_matrix(self):
        """
        Crée la matrice TF-IDF pour chaque document du corpus.

        Cette matrice est obtenue en multipliant la matrice TF par le facteur IDF (Inverse Document Frequency).
        """
        doc_frequencies = np.array(self.tf_matrix.sum(axis=0)).flatten()
        idf = np.log(self.ndoc / (doc_frequencies + 1))

        tfidf_data = self.tf_matrix.multiply(idf)

        self.tfidf_matrix = tfidf_data

    def get_tfidf_matrix(self):
        """
        Retourne la matrice TF-IDF.

        Returns
        -------
        scipy.sparse.csr_matrix
            La matrice creuse (sparse) contenant les valeurs TF-IDF pour chaque document.
        """
        return self.tfidf_matrix

# =============== 7 : MOTEUR DE RECHERCHE ===============

    def select_artists(self, artists):
        """
        Filtre le corpus pour ne contenir que les documents des artistes spécifiés.

        Parameters
        ----------
        artists : list
            Liste des artistes à filtrer dans le corpus.
        """
        # Vérifier si les artistes existent dans le corpus
        artist_ids = [CORPUS.aut2id[artist] for artist in artists if artist in CORPUS.aut2id]
        if not artist_ids:
            return None

        # Appliquer le filtrage
        authors = {aid: CORPUS.authors[aid] for aid in artist_ids}
        aut2id = {artist: CORPUS.aut2id[artist] for artist in artists if artist in CORPUS.aut2id}
        id2doc = {
            doc_id: doc for doc_id, doc in CORPUS.id2doc.items() if CORPUS.aut2id[doc.auteur] in artist_ids
        }

        # Réindexer les documents après filtrage
        new_id2doc = {}
        for new_index, (old_doc_id, doc) in enumerate(id2doc.items(), start=1):
            new_id2doc[new_index] = doc

        # Mettre à jour les attributs du corpus filtré
        self.authors = authors
        self.aut2id = aut2id
        self.id2doc = new_id2doc
        self.ndoc = len(new_id2doc)
        self.naut = len(authors)

        # Mise à jour des autres variables
        self.create_docustring(force=True)
        self.create_vocabulaire()
        self.create_tf_matrix()
        self.create_tfidf_matrix()

    def search(self, query, top_k=10, artists=None):
        """
        Effectue une recherche dans le corpus en fonction de la requête et retourne les documents les plus pertinents.

        Parameters
        ----------
        query : str
            La requête de recherche sous forme de chaîne de caractères.
        top_k : int, optional
            Le nombre de résultats à retourner (par défaut 10).
        artists : list, optional
            Liste des artistes à inclure dans la recherche (par défaut None).

        Returns
        -------
        pd.DataFrame
            Un DataFrame contenant les titres, auteurs, scores de pertinence et textes des documents les plus pertinents.
        """
        corpus_to_search = self
        if artists:
            self.select_artists(artists)

        if corpus_to_search.vocabulaire is None:
            corpus_to_search.create_vocabulaire()
        if corpus_to_search.tf_matrix is None:
            corpus_to_search.create_tf_matrix()
        if corpus_to_search.tfidf_matrix is None:
            corpus_to_search.create_tfidf_matrix()

        # Construction du vecteur requête
        query_vector = np.zeros(len(corpus_to_search.vocabulaire))
        for word in query.lower().split():
            if word in corpus_to_search.vocabulaire:
                query_vector[corpus_to_search.vocabulaire[word]['id']] += 1

        # Calcul de la similarité cosinus
        tfidf_query = query_vector * np.log(len(corpus_to_search.id2doc) / (1 + np.array([corpus_to_search.vocabulaire[word]['documents_contenant'] for word in corpus_to_search.vocabulaire])))

        scores = corpus_to_search.tfidf_matrix.dot(tfidf_query)  # Produit scalaire avec chaque document

        # Tri et sélection des meilleurs scores
        top_indices = np.argsort(scores)[::-1][:top_k]
        result = pd.DataFrame({
            "Titre": [corpus_to_search.id2doc[i+1].titre for i in top_indices],
            "Artiste": [corpus_to_search.id2doc[i + 1].auteur for i in top_indices],
            "Score": [round(scores[i], 3) for i in top_indices],
            "texte" : [corpus_to_search.id2doc[i+1].texte for i in top_indices]
        })

        return result
