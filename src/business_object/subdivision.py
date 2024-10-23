from src.business_object.Polygones.contour import Contour


class Subdivision:
    def __init__(self, id, nom=None, annee=None, polygones=None):

        if not isinstance(id, str):
            raise TypeError("L'identifiant doit être un str")

        if not isinstance(nom, str):
            raise TypeError("Le nom doit être un str")

        if not isinstance(annee, int):
            raise TypeError("L'année doit être un int")
        if (annee <= 0):
            raise ValueError("L'année doit être positive")

        if not isinstance(polygones, Contour):
            raise TypeError("Le polygone doit être une instance de Contour")

        self.id = id
        self.nom = nom
        self.annee = annee
        self.polygones = polygones
