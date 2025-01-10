import customtkinter
from .RechercheAvancee import RechercheAvancee
from..constants import DEBUG

class RechercheClassique(customtkinter.CTkFrame):
    """frame des boutons de la recherche classique"""
    def __init__(self, master):
        super().__init__(master)

        # Mots clefs
        self.mots_clefs = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Entrez des mots clés séparés par des espaces"
            )
        self.mots_clefs.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky="nsew")

        # Label pour le slider
        self.slider_label = customtkinter.CTkLabel(master=self, text="Nombre de titres recherchées : 5")
        self.slider_label.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="w")

        # Slider
        self.slider = customtkinter.CTkSlider(master=self,
                                              from_=1,
                                              to=10,
                                              number_of_steps=10,
                                              command=self.event_slider)
        self.slider.grid(row=1, column=1, columnspan=3, padx=20, pady=(10, 10), sticky="ew")

        # Ajout du frame de recherche avancée
        self.recherche_avancee = RechercheAvancee(master=self)
        self.recherche_avancee.grid(row=3, column=0,
                                    columnspan=4, padx=20,
                                    pady=(20, 10), sticky="nsew")

        # Bouton valider
        self.bouton_valider = customtkinter.CTkButton(master=self,
                                                    command=self.event_bouton_valider,
                                                    text="Valider")
        self.bouton_valider.grid(row=6, column=0,
                                 columnspan=4, padx=20,
                                 pady=(20, 10), sticky="nsew")
    # fin de l'initialisation

    # =============== #
    # Event listeners #
    # =============== #

    def event_bouton_valider(self):
        """
        Quand le bouton 'valider' est pressé
        """
        if DEBUG:
            print("event_bouton_valider pressed")
        self.master.verify_entries()

    def event_slider(self, value):
        """
        Quand la valeur du 'slider' est actualisée :
        Changement de la valeur dans le label
        """
        if DEBUG:
            print(f"event_slider, value = {value}")
        # Changement de la valeur dans le label
        new_text = "Nombre de titres recherchées : " + str(int(value))
        self.slider_label.configure(text=new_text)

    # ====================== #
    # fin de Event listeners #
    # ====================== #
