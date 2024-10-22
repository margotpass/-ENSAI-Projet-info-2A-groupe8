from src.business_object.pointgeographique import PointGeographique
import pyproj


class PolygonePrimaire:
    """ Polygone primaire caractérisé par ses points géographiques.
    paramètres:
    polygoneprimaire : List[PointGeographique]
    """
    def __init__(self, polygoneprimaire=None):
        # Initialise la liste des points, vide si non fournie
        if polygoneprimaire is None:
            self.polygoneprimaire = []
        else:
            # Vérifie que tous les points fournis sont des instances de PointGeographique
            if not all(isinstance(point, PointGeographique) for point in polygoneprimaire):
                raise ValueError("Tous les points doivent être des instances de PointGeographique")
            self.polygoneprimaire = polygoneprimaire

    def __str__(self):
        """ str sert à afficher les informations du polygone primaire """
        if not self.polygoneprimaire:
            raise ValueError("Le polygone est vide et ne peut pas être affiché")
        # Vérifie si tous les points sont valides
        for point in self.polygoneprimaire:
            if not isinstance(point, PointGeographique):
                raise ValueError("Tous les points du polygone doivent être des instances de PointGeographique")

        return f"Polygone Primaire: [{', '.join(str(point) for point in self.polygoneprimaire)}]"

    def get_polygoneprimaire(self):
        """ Retourne le polygone primaire """
        return self.polygoneprimaire

    def ajouter_point(self, point):
        """ Ajoute un point géographique au polygone """
        if isinstance(point, PointGeographique):
            self.polygoneprimaire.append(point)
        else:
            raise ValueError("L'objet ajouté doit être une instance de PointGeographique")
