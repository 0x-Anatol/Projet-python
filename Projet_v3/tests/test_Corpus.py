import pytest
from src.Corpus import Corpus

class MockDocument:
    def __init__(self, titre, auteur, texte, date=None):
        self.titre = titre
        self.auteur = auteur
        self.texte = texte
        self.date = date

    def get_text(self):
        return self.texte

    def __repr__(self):
        return f"{self.titre} by {self.auteur}"

def test_corpus_initialization():
    corpus = Corpus("Corpus")
    assert corpus.nom == "Corpus"
    assert corpus.authors == {}
    assert corpus.aut2id == {}
    assert corpus.id2doc == {}
    assert corpus.ndoc == 0
    assert corpus.naut == 0

def test_corpus_add_document():
    corpus = Corpus("Test Corpus")
    doc = MockDocument("Titre1", "Auteur1", "Texte1")
    corpus.add(doc)

    assert corpus.ndoc == 1
    assert corpus.naut == 1
    assert corpus.id2doc[1] == doc
    assert "Auteur1" in corpus.aut2id
    assert corpus.authors[1].name == "Auteur1"

def test_corpus_text_cleaning():
    corpus = Corpus("Test Corpus")
    dirty_text = "Hello, World! [Chorus] \n This is a TEST 123."
    cleaned_text = corpus.nettoyer_texte(dirty_text)
    assert cleaned_text == "hello world this is a test"

def test_corpus_save_and_load(tmp_path):
    corpus = Corpus("Test Corpus")
    doc = MockDocument("Titre1", "Auteur1", "Texte1")
    corpus.add(doc)
    
    save_path = tmp_path / "corpus.pkl"
    corpus.sauvegarder_corpus(save_path)
    
    new_corpus = Corpus("New Corpus")
    new_corpus.charger_corpus(save_path)
    
    assert new_corpus.ndoc == corpus.ndoc
    assert new_corpus.naut == corpus.naut
    assert new_corpus.authors.keys() == corpus.authors.keys()
