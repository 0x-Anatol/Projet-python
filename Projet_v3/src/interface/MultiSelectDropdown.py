import tkinter as tk
from tkinter import ttk
import customtkinter


class MultiSelectDropdown(customtkinter.CTkFrame):
    def __init__(self, master, options, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.options = options
        self.command = command
        self.selected_options = []

        self.bg_color = "white"
        self.fg_color = "black"
        self.select_bg_color = "lightblue"

        # Stockage du mode d'apparence (sombre/lumineux)
        self.appearance_mode = customtkinter.get_appearance_mode()

        # Bouton principal pour afficher/masquer la liste déroulante
        self.main_button = customtkinter.CTkButton(
            self,
            text="Sélectionner des options",
            command=self.toggle_dropdown,
            state="disabled"
        )
        self.main_button.pack(padx=5, pady=5, fill="x")

        # Variables pour le Toplevel
        self.dropdown_window = None
        self.is_dropdown_open = False

    def toggle_dropdown(self):
        """Affiche ou masque la liste déroulante."""
        if self.is_dropdown_open:
            self.close_dropdown()
        else:
            self.open_dropdown()

    def open_dropdown(self):
        """Affiche la liste déroulante dans un Toplevel."""
        if self.is_dropdown_open:
            return

        # Créer une nouvelle fenêtre Toplevel
        self.dropdown_window = customtkinter.CTkToplevel(self)
        self.dropdown_window.overrideredirect(True)  # Supprime la barre de titre
        self.dropdown_window.geometry(self.get_dropdown_position())
        self.dropdown_window.lift()

        # Liste déroulante (Listbox avec sélection multiple)
        self.listbox = tk.Listbox(
            self.dropdown_window,
            selectmode="multiple",
            height=len(self.options),
            bg=self.bg_color,  # Couleur de fond (en fonction du thème)
            fg=self.fg_color,  # Couleur du texte
            selectbackground=self.select_bg_color,  # Couleur de sélection
            relief="flat"
        )
        self.listbox.pack(fill="both", expand=True)

        # Ajouter les options à la Listbox
        for option in self.options:
            self.listbox.insert(tk.END, option)

        # Bouton pour valider la sélection
        self.validate_button = customtkinter.CTkButton(
            self.dropdown_window,
            text="Valider",
            command=self.validate_selection
        )
        self.validate_button.pack(padx=5, pady=5)

        self.is_dropdown_open = True

    def close_dropdown(self):
        """Ferme la liste déroulante."""
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None
        self.is_dropdown_open = False

    def validate_selection(self):
        """Valide la sélection et met à jour le bouton principal."""
        selected_indices = self.listbox.curselection()
        self.selected_options = [self.options[i] for i in selected_indices]

        # Mettre à jour le texte du bouton principal
        if self.selected_options:
            self.main_button.configure(
                text=", ".join(self.selected_options)
            )
        else:
            self.main_button.configure(text="Sélectionner des options")

        # Appeler la commande si définie
        if self.command:
            self.command(self.selected_options)

        # Fermer le menu déroulant
        self.close_dropdown()

    def get_dropdown_position(self):
        """Calcule la position où le Toplevel doit apparaître."""
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width = self.winfo_width()
        return f"{width}x200+{x}+{y}"  # Taille et position : largeur x hauteur + x + y

    def change_dropdown_appearance(self, mode):
        """ ### """
        if mode == "Light":
            self.bg_color = "white"
            self.fg_color = "black"
            self.select_bg_color = "lightblue"
        else:
            self.bg_color = "#2a2d2e"
            self.fg_color = "white"
            self.select_bg_color = "#565b5e"
        if self.is_dropdown_open:
            self.listbox.config(bg=self.bg_color,
                                fg=self.fg_color,
                                selectbackground=self.select_bg_color)
