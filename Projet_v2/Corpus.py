# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
import re
import pandas as pd
import scipy  as sp
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

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
        self.tf_matrix = "Not created yet"
        self.tfidf_matrix = "Not created yet"

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

# =============== 6 : TRAITEMENT DE TEXTE ===============

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

    def search_crade(self, word_to_find):
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
        id = 1
        for e in list_text:
            if e not in vocabulaire:
                vocabulaire[e] = {"id":id, "nb":1}
                id += 1
            else:
                vocabulaire[e]["nb"] += 1
        self.vocabulaire = vocabulaire

    def get_vocabulaire(self):
        return self.vocabulaire

    # chatgpt
    def freq(self):
        vocabulaire = self.create_vocabulaire()
        freq = {}
        
        # Initialisation du dictionnaire de fréquences des mots
        for mot in vocabulaire:
            freq[mot] = {'tf': 0, 'df': 0}  # Initialisation avec 'tf' et 'df' à zéro

        # Compter les occurrences de chaque mot et la DF
        for document in self.documents:
            document_nettoye = self.nettoyer_texte(document)
            mots_dans_document = set(document_nettoye.split())  # Utiliser un set pour éviter les doublons dans un même document
            
            for mot in mots_dans_document:
                if mot in freq:
                    freq[mot]['tf'] += document_nettoye.split().count(mot)
                    freq[mot]['df'] += 1  # Si le mot apparaît dans ce document, augmenter la DF

        # Créer un DataFrame avec les résultats
        df_freq = pd.DataFrame.from_dict(freq, orient='index')
        return df_freq

# =============== 7 : matrice ===============

    def create_tf_matrix(self):
        """Construire la matrice de fréquence des termes (TF)."""
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
        return self.tf_matrix
    
    def create_tfidf_matrix(self):
        if self.tf_matrix is None:
            self.create_tf_matrix()

        doc_frequencies = np.array(self.tf_matrix.sum(axis=0)).flatten()
        idf = np.log(self.ndoc / (doc_frequencies + 1))

        tfidf_data = self.tf_matrix.multiply(idf)

        self.tfidf_matrix = tfidf_data

    def get_tfidf_matrix(self):
        return self.tfidf_matrix


# =============== 7 : moteur de recherche ===============

    def search(self, keywords):
        """Recherche dans le corpus en utilisant une requête de mots-clés."""
        # 1. Nettoyer et transformer les mots-clés en un vecteur basé sur le vocabulaire
        query_vector = self.create_query_vector(keywords)

        if query_vector is None:
            print("Aucun des mots-clés n'est présent dans le vocabulaire.")
            return []

        similarities = self.calculate_similarity(query_vector)

        ranked_docs = sorted(similarities, key=lambda x: x[1], reverse=True)

        self.display_results(ranked_docs)


    def create_query_vector(self, keywords):
        cleaned_keywords = self.nettoyer_texte(keywords).split()
        vector = np.zeros(len(self.vocabulaire))

        for word in cleaned_keywords:
            if word in self.vocabulaire:
                vector[self.vocabulaire[word]['id']] += 1

        if np.sum(vector) == 0:
            return None

        return vector

    def calculate_similarity(self, query_vector):
        if self.tfidf_matrix is None:
            self.create_tfidf_matrix()

        similarities = []

        for doc_id, doc in self.id2doc.items():
            doc_vector = self.tfidf_matrix[doc_id - 1].toarray().flatten()
            similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
            similarities.append((doc, similarity))

        return similarities

    def display_results(self, ranked_docs):
        print("\nRésultats de la recherche :")
        for doc, score in ranked_docs:
            print(f"Score: {score:.4f} - {doc.titre} (Auteur: {doc.auteur}, Date: {doc.date})")
