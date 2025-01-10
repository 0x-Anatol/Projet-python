import customtkinter
from..constants import DEBUG

class OptionsPopup(customtkinter.CTkToplevel):
    """Popup pour changer les quelques options possibles"""
    def __init__(self, master):
        super().__init__(master)
        self.title("Options")
        # Centrer l'alerte sur la fenêtre principale
        alert_width = 400
        alert_height = 200

        main_window_x = self.master.winfo_x()
        main_window_y = self.master.winfo_y()
        main_window_width = self.master.winfo_width()
        main_window_height = self.master.winfo_height()

        center_x = main_window_x + (main_window_width // 2) - (alert_width // 2)
        center_y = main_window_y + (main_window_height // 2) - (alert_height // 2)

        self.geometry(f"{alert_width}x{alert_height}+{center_x}+{center_y}")
        self.grab_set()

        # Label for appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Thème:")
        self.appearance_mode_label.pack(pady=(10, 0))

        # OptionMenu for appearance mode (Light, Dark, System)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.set(value=customtkinter.get_appearance_mode())
        self.appearance_mode_optionemenu.pack(pady=10)

        # Label for scaling
        self.scaling_label = customtkinter.CTkLabel(self, text="Mise à l'échelle de l'interface:")
        self.scaling_label.pack(pady=(10, 0))

        # OptionMenu for scaling (80%, 90%, 100%, 110%, 120%)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionemenu.set(value=self.master.current_scaling)
        self.scaling_optionemenu.pack(pady=(10, 20))

    # Méthode pour changer le mode d'apparence (Light, Dark, System)
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        # appel à la fonction qui change la couleur du tableau.
        self.master.result_frame.change_table_appearance(new_appearance_mode)
        # appel à la fonction qui change la couleur du dropdownbutton
        self.master.recherche_classique.recherche_avancee.choix_des_auteurs.change_dropdown_appearance(new_appearance_mode)
        if DEBUG:
            print(f"change_appearance_mode_event set to : {new_appearance_mode}")

    # Méthode pour changer la mise à l'échelle de l'interface
    def change_scaling_event(self, new_scaling: str):
        self.master.current_scaling = new_scaling
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        if DEBUG:
            print(f"change_scaling_event set to : {new_scaling_float}")

