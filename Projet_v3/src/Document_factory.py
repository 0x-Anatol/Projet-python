from src.DocumentClasses import MusicDocument

class Document_factory:
    """
    Une fabrique pour créer des documents spécifiques basés sur leur type.

    Methods
    -------
    create_doc(titre, auteur, url, texte, type)
        Crée une instance de document basée sur le type spécifié.
    """

    @staticmethod
    def create_doc(titre, auteur, url, texte, type):
        """
        Crée un document basé sur le type spécifié.

        Parameters
        ----------
        titre : str
            Le titre du document.
        auteur : str
            L'auteur ou créateur du document.
        url : str
            L'URL associée au document (par exemple, une source en ligne).
        texte : str
            Le contenu textuel du document.
        type : str
            Le type du document, par exemple "Musique".

        Returns
        -------
        MusicDocument
            Une instance de MusicDocument si le type est "Musique".

        Raises
        ------
        ValueError
            Si le type de document n'est pas reconnu.
        """
        if type == "Musique":
            return MusicDocument(titre, auteur, url, texte)
        else:
            raise ValueError(f"Type de document non reconnu : {type}")