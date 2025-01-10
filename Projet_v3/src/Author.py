class Author:
    """
    Une classe représentant un.e artiste

    Attributes
    ----------
    name : str
        nom de l'artiste
    ndoc : int
        nombre de documents (musiques)
    production : list
        liste de musiques

    Methods
    -------
    add(production)
        Ajoute une musique à l'auteur et incrémente le nombre de documents.
    __str__()
        Retourne une représentation textuelle de l'auteur et de sa production.
    """
    def __init__(self, name):
        """
        Initialise une instance de la classe Author.

        Parameters
        ----------
        name : str
            Le nom de l'artiste.
        """
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        """
        Ajoute une musique à la liste de productions et incrémente le compteur de documents.

        Parameters
        ----------
        production : str
            Le titre de la musique à ajouter.
        """
        self.ndoc += 1
        self.production.append(production)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'auteur.

        Returns
        -------
        str
            Une chaîne de caractères contenant le nom de l'auteur et le nombre de productions.
        """
        return f"Auteur : {self.name}\t productions : {self.ndoc}"
