from src.business_object.Polygones.contour import Contour


class Subdivision:
    def __init__(self, id, nom=None, annee=None, polygones=None):
        """Initialise la casse Subdivision

        Args:
            id (str): identifiant de la subdivision
            nom (str): nom de la subdivision. Défaut à None.
            annee (int, optional): année de recherche dans la table. Défaut à None.
            polygones (list(PointGeographique), optional): Liste de points géographiques. Défaut à None

        Raises:
            TypeError: l'id est un string
            TypeError: le nom est un string
            TypeError: l'année est un nombre
            ValueError: l'année est positive
            TypeError: le polygone est une instance de contour
        """

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
