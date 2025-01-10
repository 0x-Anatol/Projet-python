import pytest
from src.Author import Author

def test_author_initialization():
    author = Author("Jean dame")
    assert author.name == "Jean dame"
    assert author.ndoc == 0
    assert author.production == []

def test_author_add_production():
    author = Author("Marie jeanne")
    author.add("Production 1")
    assert author.ndoc == 1
    assert author.production == ["Production 1"]

def test_author_str_representation():
    author = Author("John Smith")
    author.add("First Document")
    assert str(author) == "Auteur : John Smith\t productions : 1"
