import pytest
from src.Document_factory import Document_factory
from src.DocumentClasses import Document, MusicDocument

def test_create_generic_document():
    # Test pour vérifier si un document générique peut être créé correctement
    doc = Document(
        titre="Titre générique",
        auteur="Auteur générique",
        url="http://example.com",
        texte="Texte générique",
        type="Générique"
    )
    assert doc.titre == "Titre générique"
    assert doc.auteur == "Auteur générique"
    assert doc.url == "http://example.com"
    assert doc.texte == "Texte générique"
    assert doc.type == "Générique"

def test_create_music_document_via_factory():
    # Test pour la méthode factory avec un type valide (Musique)
    doc = Document_factory.create_doc(
        titre="Ma Chanson",
        auteur="Mon Artiste",
        url="http://example.com/song",
        texte="Voici les paroles",
        type="Musique"
    )
    assert isinstance(doc, MusicDocument)
    assert doc.titre == "Ma Chanson"
    assert doc.auteur == "Mon Artiste"
    assert doc.url == "http://example.com/song"
    assert doc.texte == "Voici les paroles"
    assert doc.type == "Musique"

def test_invalid_document_type_in_factory():
    # Test pour s'assurer que des types invalides lèvent une exception
    with pytest.raises(ValueError) as excinfo:
        Document_factory.create_doc(
            titre="Titre Invalide",
            auteur="Auteur Invalide",
            url="http://example.com/invalid",
            texte="Contenu Invalide",
            type="Invalide"
        )
    assert "Type de document non reconnu" in str(excinfo.value)
