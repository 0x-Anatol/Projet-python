import customtkinter
import tkinter
from..constants import empty_data_frame, DEBUG

class Resultat(customtkinter.CTkFrame):
    """
    frame contenant
    le résultat de la recherche
    le bouton de téléchargement de ce même résultat
    """
    def __init__(self, master):
        super().__init__(master)

        # variables
        self.style = tkinter.ttk.Style()
        self.style.theme_use("default")

        # Title
        self.titre = customtkinter.CTkLabel(
            master=self,
            text="Résultat de la recherche",
            font=("Arial", 18, "bold")
        )
        self.titre.grid(row=0, column=0, columnspan=8, pady=(10, 20), sticky="n")

        # affichage du dataframe vide
        self.display_dataframe(empty_data_frame)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
    # fin init

    def display_dataframe(self, dataframe):
        """ ### """
        tree = tkinter.ttk.Treeview(self,
                                    columns=list(dataframe.columns),
                                    show="headings",
                                    height=10)
        tree.grid(row=1, column=0, columnspan=10, sticky="nsew", padx=10, pady=10)

        ###
        # Configuration des lignes du tableau
        self.style.configure("Treeview",
                        background="#2a2d2e", # Couleur de fond des cellules
                        foreground="white",   # Couleur du texte
                        rowheight=25,
                        fieldbackground="#2a2d2e",
                        bordercolor="gray",   # Couleur des bordures entre les cellules
                        borderwidth=1)        # Largeur des bordures

        # Configuration des en-têtes
        self.style.configure("Treeview.Heading",
                        background="#565b5e", # Couleur de fond des en-têtes
                        foreground="white",   # Couleur du texte des en-têtes
                        bordercolor="gray",   # Couleur des bordures entre les colonnes
                        borderwidth=2,        # Largeur des bordures
                        relief="ridge")       # Style des bordures (relief)

        # Enlever le survol moche du header
        self.style.map("Treeview.Heading", background=[])

        self.change_table_appearance("Light")

        # Configuration des colonnes
        for col in dataframe.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        # Ajout des données
        for index, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))

    def change_table_appearance(self, mode):
        """ ### """
        if mode == "Light":
            self.style.configure("Treeview",
                                background="#f5f5f5",  # Couleur claire
                                foreground="black",    # Texte sombre
                                fieldbackground="#f5f5f5")
            self.style.configure("Treeview.Heading",
                                background="#d9d9d9",  # En-têtes clairs
                                foreground="black")
        else:
            self.style.configure("Treeview",
                                background="#2a2d2e",  # Couleur sombre
                                foreground="white",    # Texte clair
                                fieldbackground="#2a2d2e")
            self.style.configure("Treeview.Heading",
                                background="#565b5e",  # En-têtes sombres
                                foreground="white")
    # fin resultat
