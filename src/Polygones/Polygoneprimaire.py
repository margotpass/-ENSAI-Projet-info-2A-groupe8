from PointGeographique import PointGeographique
import pyproj

class PolygonePrimaire():
    """ Polygone primaire caractérisé par ses points géographiques.
    paramètres:
    polygoneprimaire : List<PointGeographique>
    """
    def __init__(self, polygoneprimaire):
        self.polygoneprimaire = polygoneprimaire

    def __str__(self):
        """ str sert à afficher les informations du polygone primaire """
        return "Polygone primaire: " + str(self.polygoneprimaire)

    def get_polygoneprimaire(self):
        """ Retourne le polygone primaire """
        return self.polygoneprimaire

