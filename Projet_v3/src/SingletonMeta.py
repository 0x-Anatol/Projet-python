class SingletonMeta(type):
    """
    Une classe métaclasse pour implémenter le patron de conception Singleton.

    Cette métaclasse garantit qu'une seule instance d'une classe utilisant `SingletonMeta` sera créée.
    Si une instance existe déjà, elle est réutilisée à chaque appel.

    Attributes
    ----------
    instances : dict
        Dictionnaire qui conserve les instances créées des classes utilisant cette métaclasse.
    """
    instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Permet de contrôler la création d'une instance pour une classe utilisant SingletonMeta.

        Si l'instance de la classe n'existe pas encore, une nouvelle instance est créée et stockée dans `instances`.
        Si l'instance existe déjà, la même instance est retournée.

        Parameters
        ----------
        *args : tuple
            Les arguments positionnels à passer au constructeur de la classe.
        **kwargs : dict
            Les arguments nommés à passer au constructeur de la classe.

        Returns
        -------
        object
            L'instance de la classe.
        """
        if cls not in cls.instances:
            # Créer une nouvelle instance si elle n'existe pas
            instance = super().__call__(*args, **kwargs)
            cls.instances[cls] = instance
        return cls.instances[cls]
