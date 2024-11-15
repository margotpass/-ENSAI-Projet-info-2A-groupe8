from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique


class Connexe(PolygonePrimaire):
    """ Classe Convexe, qui représente une liste de polygones primaires
    paramètres:
    connexe : List[PolygonePrimaire]
    """

    def __init__(self, connexe=None):
        """Initialise la liste de polygones connexe

        Args:
            connexe (liste): liste de connexes. Défault à None.

        Raises:
            TypeError: Pas une instance de PolygonePrimaire
        """
        
        # Par défaut, une liste vide de polygones
        if connexe is None:
            self.connexe = []
        else:
            # Vérifie que chaque élément de la liste est bien une instance de PolygonePrimaire
            if not all(isinstance(polygone, PolygonePrimaire) for polygone in connexe):
                raise TypeError("Tous les éléments doivent être des instances de PolygonePrimaire")
            self.connexe = connexe

    def __str__(self):
        """ Affiche les informations des polygones connexes """
        return f"Connexe: [{', '.join(str(polygone) for polygone in self.connexe)}]"

    def get_connexe(self):
        """ Retourne la liste de polygones """
        return self.connexe

    def ajouter_polygone(self, polygone):
        """ Ajoute un polygone primaire à la liste des convexes """
        if isinstance(polygone, PolygonePrimaire):
            self.connexe.append(polygone)
        else:
            raise TypeError("L'objet ajouté doit être une instance de PolygonePrimaire")
