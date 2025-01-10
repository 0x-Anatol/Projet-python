class Document:
    """
    Une classe représentant un document générique.

    Attributes
    ----------
    titre : str
        Le titre du document.
    auteur : str
        L'auteur du document.
    url : str
        L'URL associée au document.
    texte : str
        Le texte ou le contenu du document.
    type : str
        Le type du document (par défaut "générique").

    Methods
    -------
    __repr__()
        Retourne une représentation textuelle détaillée du document.
    __str__()
        Retourne une représentation textuelle simple du document (titre et auteur).
    get_text()
        Retourne le texte du document.
    """
    def __init__(self, titre="", auteur="", url="", texte="", type=""):
        """
        Initialise une instance de la classe Document.

        Parameters
        ----------
        titre : str, optional
            Le titre du document (par défaut est une chaîne vide).
        auteur : str, optional
            L'auteur du document (par défaut est une chaîne vide).
        url : str, optional
            L'URL associée au document (par défaut est une chaîne vide).
        texte : str, optional
            Le contenu textuel du document (par défaut est une chaîne vide).
        type : str, optional
            Le type de document (par défaut "générique").
        """
        self.titre = titre
        self.auteur = auteur
        self.url = url
        self.texte = texte
        self.type = type

    def __repr__(self):
        """
        Retourne une représentation détaillée du document.

        Returns
        -------
        str
            Une chaîne de caractères représentant le document avec titre, auteur, URL et texte.
        """
        aff = (f"Titre : {self.titre}\tAuteur : {self.auteur}"
               f"\tURL : {self.url}\tTexte : {self.texte}")
        return aff

    def __str__(self):
        """
        Retourne une représentation simple du document.

        Returns
        -------
        str
            Une chaîne de caractères contenant le titre et l'auteur du document.
        """
        return f"{self.titre}, par {self.auteur}"

    def get_text(self):
        """
        Retourne le texte contenu dans le document.

        Returns
        -------
        str
            Le texte du document.
        """
        return self.texte


class MusicDocument(Document):
    """
    Une classe représentant un document musical, héritant de la classe Document.

    Methods
    -------
    __init__(titre, auteur, url, texte)
        Initialise un document de type Musique.
    """
    def __init__(self, titre, auteur, url, texte):
        """
        Initialise une instance de la classe MusicDocument, en définissant le type comme 'Musique'.

        Parameters
        ----------
        titre : str
            Le titre de la musique.
        auteur : str
            L'auteur de la musique.
        url : str
            L'URL associée à la musique.
        texte : str
            Le contenu textuel de la musique.
        """
        super().__init__(titre, auteur, url, texte, "Musique")

# note: Ajouter les différentes sous-classes ici
