from PointGeographique import PointGeographique

class PolygonePrimaire:
    """ Polygone primaire caractérisé par ses points géographiques.
    paramètres:
    polygoneprimaire : List[PointGeographique]
    """
    def __init__(self, polygoneprimaire=None):
        # Initialise la liste des points, vide si non fournie
        self.polygoneprimaire = polygoneprimaire if polygoneprimaire else []

    def __str__(self):
        """ str sert à afficher les informations du polygone primaire """
        return f"Polygone Primaire: {[str(point) for point in self.polygoneprimaire]}"

    def get_polygoneprimaire(self):
        """ Retourne le polygone primaire """
        return self.polygoneprimaire

    def ajouter_point(self, point):
        """ Ajoute un point géographique au polygone """
        if isinstance(point, PointGeographique):
            self.polygoneprimaire.append(point)
        else:
            raise ValueError("L'objet ajouté doit être une instance de PointGeographique")
