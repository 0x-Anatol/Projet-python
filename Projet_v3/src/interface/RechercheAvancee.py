import customtkinter
import tkinter

from.MultiSelectDropdown import MultiSelectDropdown
from..constants import DEBUG, CORPUS

class RechercheAvancee(customtkinter.CTkFrame):
    """Classe pour gérer le frame de la recherche avancée"""
    def __init__(self, master):
        super().__init__(master)
        # Titre de la recherche avancée
        self.titre = customtkinter.CTkLabel(master=self,
                                            text="Recherche Avancée",
                                            font=("Arial", 18, "bold"))
        self.titre.grid(row=0, column=0, columnspan=4, pady=(10, 20), sticky="n")

        # Checkbox pour l'auteur
        self.checkbox_auteur_var = tkinter.BooleanVar(value=False)
        self.checkbox_auteur = customtkinter.CTkCheckBox(master=self, text="un auteur",
                                                        variable=self.checkbox_auteur_var,
                                                        command=self.event_checkbox_auteur)
        self.checkbox_auteur.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="w")

        # Combobox pour l'auteur
        self.choix_des_auteurs = MultiSelectDropdown(self,
                                                     options=[author.name for author in CORPUS.authors.values()])
        self.choix_des_auteurs.grid(row=1, column=1, padx=20, pady=(10, 10))
    # fin init

    # event listenners
    def event_checkbox_auteur(self):
        is_checked = self.checkbox_auteur_var.get()
        new_state = "normal" if is_checked else "disabled"
        self.choix_des_auteurs.main_button.configure(state=new_state)
        self.choix_des_auteurs.close_dropdown()
        self.choix_des_auteurs.main_button.configure(text="Sélectionner des options")
        if DEBUG:
            print(f"event_checkbox_auteur: Dropdown set to {new_state}")

    # fin de la classe recherche avancee
