import pytest
import numpy as np
import pandas as pd
from src.RechercheCorpus import RechercheCorpus
from src.DocumentClasses import Document

@pytest.fixture
def corpus_fixture():
    # Créer un corpus avec des documents factices
    corpus = RechercheCorpus("Corpus")
    doc1 = Document(titre="Document 1", auteur="Author 1", url="url1", texte="Bonjour le monde. Voici un texte.")
    doc2 = Document(titre="Document 2", auteur="Author 2", url="url2", texte="Le monde est grand et le texte est court.")
    doc3 = Document(titre="Document 3", auteur="Author 1", url="url3", texte="Bonjour à nouveau, monde.")
    corpus.add(doc1)
    corpus.add(doc2)
    corpus.add(doc3)
    return corpus

def test_create_docustring(corpus_fixture):
    corpus_fixture.create_docustring()
    docustring = corpus_fixture.get_docustring()
    assert isinstance(docustring, str)
    assert "Bonjour le monde" in docustring
    assert "Le monde est grand" in docustring

def test_search_nul(corpus_fixture):
    corpus_fixture.create_docustring()
    occurrences = corpus_fixture.search_nul("monde")
    assert isinstance(occurrences, list)
    assert len(occurrences) > 0
    assert all(word == "monde" for word in occurrences)

def test_search(corpus_fixture):
    corpus_fixture.create_vocabulaire()
    corpus_fixture.create_tf_matrix()
    corpus_fixture.create_tfidf_matrix()
    results = corpus_fixture.search("monde texte", top_k=2)
    assert isinstance(results, pd.DataFrame)
    assert results.shape[0] <= 2
    assert "monde" in results["texte"].iloc[0].lower()
