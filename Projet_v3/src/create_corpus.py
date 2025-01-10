import re
from lyricsgenius import Genius
from src.Corpus import Corpus
from src.Document_factory import Document_factory
from src.Author import Author
from src.constants import CORPUS_PATH, DEBUG, MAX_SONGS, GENIUS_TOKEN

# Initialiser le client Genius avec votre token
genius = Genius(GENIUS_TOKEN)

# Initialiser le corpus
default_corpus_name = "Chansons Artistes Divers"
corpus = Corpus(default_corpus_name)

def create_corpus(artistes, max_songs=MAX_SONGS):
    """
    Crée un corpus contenant les chansons des artistes spécifiés en utilisant l'API Genius.

    Args:
        artistes (list): Liste des noms d'artistes dont les chansons doivent être récupérées.
        max_songs (int): Nombre maximum de chansons à récupérer par artiste (défini dans MAX_SONGS).

    Returns:
        None
    """
    # Dictionnaire pour stocker les instances des auteurs
    auteurs = {}

    # Récupérer les chansons pour chaque artiste et les ajouter au corpus
    for artiste in artistes:
        print(f"Recherche des chansons de {artiste}")

        # Utiliser l'API Genius pour rechercher l'artiste et ses chansons
        artist = genius.search_artist(artiste, max_songs=max_songs, sort="popularity")

        if artist is None:
            print(f"Aucune information trouvée pour l'artiste: {artiste}")
            continue

        # Créer une instance d'Author pour cet artiste s'il n'existe pas déjà
        if artiste not in auteurs:
            auteurs[artiste] = Author(artiste)

        # Ajouter chaque chanson de l'artiste au corpus et mettre à jour l'auteur
        for song in artist.songs:
            song_title = song.title
            song_artist = song.artist
            song_lyrics = corpus.nettoyer_texte(song.lyrics)  # Nettoyer les paroles
            song_url = song.url

            # Créer un document à partir des informations de la chanson
            doc = Document_factory.create_doc(
                titre=song_title,
                auteur=song_artist,
                url=song_url,
                texte=song_lyrics,
                type="Musique"
            )

            # Ajouter le document au corpus
            corpus.add(doc)

            # Ajouter la chanson au catalogue de l'auteur
            auteurs[artiste].add(song_title)

    # Sauvegarder le corpus dans un fichier
    corpus.sauvegarder_corpus(CORPUS_PATH)

    if DEBUG:
        print("create_corpus : Corpus créé et sauvegardé.")
