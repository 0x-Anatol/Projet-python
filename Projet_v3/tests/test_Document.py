import pytest
from src.DocumentClasses import Document, MusicDocument

def test_document_initialization():
    doc = Document(
        titre="Titre générique",
        auteur="Auteur générique",
        url="http://example.com",
        texte="Contenu du document",
        type="Générique"
    )
    assert doc.titre == "Titre générique"
    assert doc.auteur == "Auteur générique"
    assert doc.url == "http://example.com"
    assert doc.texte == "Contenu du document"
    assert doc.type == "Générique"
    assert str(doc) == "Titre générique, par Auteur générique"
    assert repr(doc) == ("Titre : Titre générique\tAuteur : Auteur générique\tURL : http://example.com\t"
                         "Texte : Contenu du document")

def test_music_document_initialization():
    music_doc = MusicDocument(
        titre="Titre de la chanson",
        auteur="Artiste",
        url="http://example.com/song",
        texte="Paroles de la chanson"
    )
    assert music_doc.titre == "Titre de la chanson"
    assert music_doc.auteur == "Artiste"
    assert music_doc.url == "http://example.com/song"
    assert music_doc.texte == "Paroles de la chanson"
    assert music_doc.type == "Musique"
    assert str(music_doc) == "Titre de la chanson, par Artiste"
