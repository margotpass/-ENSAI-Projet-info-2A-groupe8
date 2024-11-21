from src.business_object.Polygones.connexe import Connexe
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire


class Contour(Connexe):
    """ Contour contient les connexes
    paramètres:
    contour : List<Connexe>
    """
    def __init__(self, contour=None):
        """ Initialise la liste de connexes """
        if contour is None:
            self.contour = []
        else:
            # Vérifie que chaque élément de la liste est bien une instance de Connexe
            if not all(isinstance(connexe, Connexe) for connexe in contour):
                raise TypeError("Tous les éléments doivent être des instances de Connexe")
            self.contour = contour

    def __str__(self):
        """ Affiche les informations de Contour """
        return "Contour: [" + ", ".join(str(connexe) for connexe in self.contour) + "]"

    def get_contour(self):
        """ Retourne la liste des connexes """
        return self.contour

    def ajout_connexe(self, connexe):
        """Ajoute un Connexe au contour, ce qui représente ajouter une enclave par exemple

        Raises:
            TypeError: L'objet à ajouter doit être une instance de Connexe

        Returns:
            list : liste de connexe augmentée du nouveau
        """        

        if not isinstance(connexe, Connexe):
            raise TypeError("L'objet ajouté doit être une instance de Connexe")

        # Vérifie si la connexe est déjà présente
        if connexe in self.contour:
            print("Cette connexe est déjà présente dans le contour.")
            return  # Ne fait rien si la connexe est déjà présente

        self.contour.append(connexe)

    def retirer_connexe(self, connexe):
        """Retire un connexe du contour, ce qui représente retirer une enclave par exemple"""
        if connexe in self.contour:
            self.contour.remove(connexe)


    def point_dans_polygone(self, point: PointGeographique, polygone: PolygonePrimaire) -> bool:
        """Vérifie si le point est à l'intérieur du polygone ou sur ses bords

        Returns:
            bool : True si le point est dans le polygone
                   False si le point n'est pas dans le polygone
        """
        x, y = point.longitude, point.latitude
        inside = False
        n = len(polygone.polygoneprimaire)

        p1x, p1y = polygone.polygoneprimaire[0].longitude, polygone.polygoneprimaire[0].latitude
        for i in range(1, n + 1):
            p2x, p2y = polygone.polygoneprimaire[i % n].longitude, polygone.polygoneprimaire[i % n].latitude

            # Vérification si le point est sur le bord
            if self.point_sur_segment(point, (p1x, p1y), (p2x, p2y)):
                return True

            # Vérification de l'algorithme de ray-casting
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def point_sur_segment(self, point: PointGeographique, p1: tuple, p2: tuple) -> bool:
        """Vérifie si un point apartient à un semgent

        Args:
            point (PointGeographique): instance de PointGéographique
            p1 (tuple): extrémité 1 du segment
            p2 (tuple): extrémité 2 du segment

        Returns:
            bool: True si le PointGeographique est sur le segment
                  False sinon
        """

        x, y = point.longitude, point.latitude
        p1x, p1y = p1
        p2x, p2y = p2

        if (min(p1x, p2x) <= x <= max(p1x, p2x)) and (min(p1y, p2y) <= y <= max(p1y, p2y)):
            if (p2x - p1x) == 0:  # Segment vertical
                return abs(x - p1x) < 1e-9  # Tolérance pour les flottants
            else:
                slope = (p2y - p1y) / (p2x - p1x)
                expected_y = slope * (x - p1x) + p1y
                return abs(expected_y - y) < 1e-9  # Tolérance pour les flottants

        return False



    def estDansPolygone(self, point: PointGeographique) -> bool:
        """Vérifie si le point est dans l'un des polygones de ce contour.

        Args:
            point (PointGeographique): Instance de PointGeographique

        Returns:
            bool: True si le point entré est dans le polygone
                  False sinon
        """
        
        for connexe in self.contour:
            polygones = connexe.get_connexe()
            if isinstance(polygones, (list, tuple)):
                polygone_exterieur = polygones[0]
                if self.point_dans_polygone(point, polygone_exterieur):
                    return True
                return False

