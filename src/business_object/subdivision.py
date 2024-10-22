from src.business_object.Polygones.Contour import Contour


class Subdivision:
    def __init__(self, id, nom=None, typeSubdivision=None, annee=None,
                 polygones=None):

        if not isinstance(id, str):
            raise TypeError("L'identifiant doit être un str")

        if not isinstance(nom, str):
            raise TypeError("Le nom doit être un str")

        if not isinstance(annee, int):
            raise TypeError("L'année doit être un int")
        if (annee <= 0):
            raise ValueError("L'année doit être positive")

        if not isinstance(polygones, Contour):
            raise TypeError("Le nom doit être une instance de Contour")

        self.id = id
        self.nom = nom
        self.typeSubdivision = typeSubdivision
        self.annee = annee
        self.polygones = polygones
