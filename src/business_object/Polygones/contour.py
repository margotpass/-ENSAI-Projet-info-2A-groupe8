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
        """Ajoute un Connexe au contour, ce qui représente ajouter une enclave par exemple"""
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

    # Les deux méthodes suivantes sont liées pour vérifier si un point est dans un polygone
    def point_dans_polygone(self, point: PointGeographique, polygone: PolygonePrimaire) -> bool:
        """Vérifie si le point est à l'intérieur du polygone ou sur ses bords."""
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
        """Vérifie si le point est sur le segment défini par p1 et p2."""
        x, y = point.longitude, point.latitude
        p1x, p1y = p1
        p2x, p2y = p2

        # Vérifie si le point est aligné avec le segment et à l'intérieur des bornes
        if (min(p1x, p2x) <= x <= max(p1x, p2x)) and (min(p1y, p2y) <= y <= max(p1y, p2y)):
            # Calcule la pente pour vérifier l'alignement
            if (p2x - p1x) == 0:  # Segment vertical
                return x == p1x
            else:
                slope = (p2y - p1y) / (p2x - p1x)
                expected_y = slope * (x - p1x) + p1y
                return expected_y == y

        return False


    def estDansPolygone(self, point: PointGeographique) -> bool:
        """
        Vérifie si le point est dans l'un des polygones de ce contour.
        """
        for connexe in self.contour:
            for polygone in connexe.get_connexe():  # Remplace par la méthode appropriée
                print("Polygone:", [f"({p.latitude}, {p.longitude})" for p in polygone.polygoneprimaire])  # Pour débogage
                if self.point_dans_polygone(point, polygone):
                    return True
        return False
