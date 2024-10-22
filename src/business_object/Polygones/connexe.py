from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire

class Connexe(PolygonePrimaire):
    """ Connexe contient les polygones primaires
    paramètres:
    connexe : List<PolygonePrimaire>
    """
    def __init__(self, connexe):
        self.connexe = connexe

    def __str__(self):
        """ str sert à afficher les informations de Connexe """
        return "Connexe: " + str(self.connexe)

    def get_Connexe(self):
        """ Retourne connexe """
        return self.connexe
