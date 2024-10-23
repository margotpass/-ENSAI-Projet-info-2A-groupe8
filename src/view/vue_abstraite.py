from abc import ABC, abstractmethod


class VueAbstraite:
    """Classe abstraite pour les vues de l'application."""

    def __init__(self, message=''):
        self.message = message

    def afficher(self):
        """Méthode pour afficher la vue.
        """
        if self.message:
            print(self.message)

    @abstractmethod
    def choisir_menu(self):
        pass