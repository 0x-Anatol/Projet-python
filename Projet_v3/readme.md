# Application de Gestion de Corpus

## Description
Cette application permet de gérer et d'explorer un corpus de documents textuels. Elle inclut des fonctionnalités pour ajouter des documents, rechercher dans le corpus, sauvegarder et charger des données, et calculer des matrices TF-IDF pour l'analyse textuelle.

## Fonctionnalités principales
- **Gestion du corpus** : Ajouter des documents, enregistrer et charger le corpus avec Pickle.
- **Recherche avancée** : Rechercher des documents par mots-clés, auteurs, et effectuer un tri alphabétique ou temporel.
- **Analyse textuelle** : Nettoyer les textes et calculer des matrices pour des analyses statistiques (TF, TF-IDF).
- **Interface utilisateur** : Visualisation des résultats sous forme de tableaux.

## Structure du Projet
```
project/
├── src/
│   ├── Corpus.py
│   ├── RechercheCorpus.py
│   └── etc.
├── tests/
│   ├── test_corpus.py
│   └── etc.
└── main.py
```

### Fichiers principaux
- **`src/Corpus.py`** : Contient la classe `Corpus` pour gérer les documents et les auteurs.
- **`src/RechercheCorpus.py`** : Contient la classe `RechercheCorpus` qui hérite de `Corpus` et ajoute des fonctionnalités de recherche et d'analyse.
- **`tests/`** : Contient les tests unitaires pour l'application.
- **`main.py`** : Point d'entrée de l'application.

## Installation

### Prérequis
- Python 3.8+
- Bibliothèques requises (listées dans `requirements.txt`) :
  ```
  pip install -r requirements.txt
  ```

### Installation locale
1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-repo.git
   ```
2. Naviguez dans le dossier du projet :
   ```
   cd project
   ```
3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

### Lancer l'application
Exécutez le fichier `main.py` pour lancer l'application :
```bash
python main.py
```

## Lancer les tests
Pour exécuter les tests unitaires, utilisez la commande suivante :
```bash
python -m pytest tests/
```


## Auteurs
- **Olivier BOROT et Anatole GONET**

## Licence
Ce projet est sous licence [MIT](LICENSE). Il est libre d'utilisation par quiconque sauf si c'est pour faire de l'argent dessus

