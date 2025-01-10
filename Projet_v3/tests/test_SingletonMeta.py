import pytest
from src.SingletonMeta import SingletonMeta

# Exemple d'une classe utilisant SingletonMeta
class SingletonTest(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

def test_singleton_instance():
    """Vérifie qu'une seule instance est créée pour la classe Singleton."""
    instance1 = SingletonTest("First")
    instance2 = SingletonTest("Second")

    # Vérifier que les deux instances sont identiques
    assert instance1 is instance2

    # Vérifier que la valeur est celle de la première instance créée
    assert instance1.value == "First"
    assert instance2.value == "First"

def test_singleton_different_classes():
    """Vérifie que des classes différentes utilisant SingletonMeta créent leurs propres instances."""
    class AnotherSingleton(metaclass=SingletonMeta):
        def __init__(self, value):
            self.value = value

    instance1 = SingletonTest("First")
    instance2 = AnotherSingleton("Second")

    # Vérifier que ce sont des instances distinctes pour des classes différentes
    assert instance1 is not instance2

    # Vérifier les valeurs respectives
    assert instance1.value == "First"
    assert instance2.value == "Second"

