import tkinter
import customtkinter
import pandas as pd
import re

from .OptionsPopup import OptionsPopup
from .Recherche import RechercheClassique
from .Resultat import Resultat

from ..RechercheCorpus import RechercheCorpus
from..constants import DEBUG, CORPUS

# interface customTkinter pour le projet python
# Anatol GONET - Olivier BOROT

customtkinter.set_appearance_mode("System")
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")
# Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    """Classe principale pour l'interface"""
    def __init__(self):
        super().__init__()
        self.title("Moteur de recherche des titres")
        self.geometry(f"{1100}x{580}")
        self.current_scaling = "100%"

        self.recherche_classique = RechercheClassique(self)
        self.recherche_classique.grid(row=0, column=0,
                                 columnspan=4, padx=20,
                                 pady=(20, 10), sticky="w")

        # Bouton options (déplacé en bas)
        self.bouton_options = customtkinter.CTkButton(master=self,
                                                    command=self.event_bouton_options_pressed,
                                                    text="Ouvrir les options")
        self.bouton_options.grid(row=10, column=0,
                                 columnspan=1, padx=20,
                                 pady=(20, 10), sticky="w")

        # ajout du frame du résultat

        self.result_frame = Resultat(self)
        self.result_frame.grid(
            row=0, column=4,
            columnspan=8, padx=20,
            pady=(20, 10), sticky="nsew")

    # ======================= #
    # Fin de l'initialisation #
    # ======================= #

    # =============== #
    # Event listeners #
    # =============== #

    def event_bouton_options_pressed(self):
        """
        Quand le boutons "ouvrir les options" est pressé
        """
        if DEBUG:
            print("event_bouton_options_pressed pressed")
        OptionsPopup(self)

    # ======================== #
    # fin des events listeners #
    # ======================== #

    def update_with_result(self, result):
        """ ### """
        temp_corpus = RechercheCorpus("temp")
        temp_mots_cles = temp_corpus.nettoyer_texte(result["mots_cles"])
        new_table = temp_corpus.search(query=temp_mots_cles,
                                  top_k=result["nb_titres"],
                                  artists=result["nom_auteur"])
        self.result_frame.display_dataframe(new_table)
        del temp_corpus

    def verify_entries(self):
        """
        Vérifie les différentes entrées.
        Affiche un pop-up montrant les mauvaises entrées si elles existent.
        Renvoie un dictionnaire contenant les différentes entrées si tout va bien.
        """
        if DEBUG:
            print("verify entries accessed ...")
        # Liste des différentes erreurs
        errors = []

        # Entrée 1: le Nombre de publications
        nb_titres = int(self.recherche_classique.slider.get())

        # Entrée 2: les mots clés
        mots_cles = self.recherche_classique.mots_clefs.get()
        if not mots_cles or len(mots_cles) < 2:
            errors.append("Veuillez entrer au moins un mot clé.")

        # Vérification des autres entrées:

        # Entrée facultative 1: nom de l'auteur
        is_checked = self.recherche_classique.recherche_avancee.checkbox_auteur_var.get()
        if is_checked is True:
            if DEBUG:
                print("auteurs checkbox 1")
            # on récupère la liste des auteurs sélectionnées dans le dropdown
            noms_auteurs = self.recherche_classique.recherche_avancee.choix_des_auteurs.selected_options
            if noms_auteurs == "":
                noms_auteurs = None
        else:
            if DEBUG:
                print("auteurs checkbox 0")
            noms_auteurs = None

        if errors:
            error_message = "\n".join(errors)
            self.show_alert("Erreurs de saisie",
                            f"Veuillez corriger les erreurs suivantes :\n\n{error_message}")
            if DEBUG:
                print(f"verify entries finished.\nerrors: {errors}")
            return None

        result = {
            "nb_titres": nb_titres,
            "mots_cles": mots_cles,
            "nom_auteur": noms_auteurs
        }

        if DEBUG:
            print(f"verify entries finished.\nresult: {result}")
        self.update_with_result(result)

    def show_alert(self, title, message):
        """
        Affiche une fenêtre d'alerte personnalisée avec un titre et un message.
        """
        alert_window = customtkinter.CTkToplevel(self)
        alert_window.title(title)
        alert_window.resizable(False, False)
        alert_window.grab_set()

        # Label pour le message
        label = customtkinter.CTkLabel(master=alert_window,
                                       text=message,
                                       wraplength=350,
                                       justify="center")
        label.pack(pady=20, padx=20)

        # Bouton Fermer
        close_button = customtkinter.CTkButton(master=alert_window,
                                               text="Fermer",
                                               command=alert_window.destroy)
        close_button.pack(pady=20)

        # Centrer l'alerte sur la fenêtre principale
        alert_width = 400
        alert_height = 200

        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()

        center_x = main_window_x + (main_window_width // 2) - (alert_width // 2)
        center_y = main_window_y + (main_window_height // 2) - (alert_height // 2)

        alert_window.geometry(f"{alert_width}x{alert_height}+{center_x}+{center_y}")
        alert_window.wait_window()
