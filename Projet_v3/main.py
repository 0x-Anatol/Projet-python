import sys
from src.create_corpus import create_corpus
from src.interface.App import App
from src.constants import DEBUG, artistes, CORPUS, CORPUS_PATH

def charger_corpus_ou_creer():
    """
    Fonction qui tente de charger le corpus. Si l'échec est détecté, 
    elle tente de le créer à partir des artistes définis.

    Returns
    -------
    bool
        True si le corpus a été chargé avec succès, False sinon.
    """
    CORPUS.charger_corpus(CORPUS_PATH)
    if CORPUS.ndoc == 0:
        if DEBUG:
            print(f"{__name__} - Corpus is None, attempting to create corpus...")
        # création du corpus si il n'existe pas
        create_corpus(artistes)
        CORPUS.charger_corpus(CORPUS_PATH)
    return CORPUS.ndoc > 0

def main():
    """
    Fonction principale qui gère le chargement du corpus et lance l'application.
    """
    if not charger_corpus_ou_creer():
        if DEBUG:
            print(f"{__name__} - Failed to load or create corpus. Terminating program.")
        sys.exit(1)  # Code d'erreur pour indiquer un échec

    # Lancer l'application
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
