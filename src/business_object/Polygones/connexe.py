
from src.business_object.Polygones.Polygoneprimaire import PolygonePrimaire


class Connexe(PolygonePrimaire):
    """ Connexe contient les polygones primaires
    paramètres:
    Connexe : List<PolygonePrimaire>
    """
    def __init__(self, Connexe: list[PolygonePrimaire]):
        self.Connexe = Connexe

    def __str__(self):
        """ str sert à afficher les informations de Connexe """
        return "Connexe: " + str(self.Connexe)

    def get_Connexe(self):
        """ Retourne Connexe """
        return self.Connexe