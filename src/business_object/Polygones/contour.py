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
    def point_dans_polygone(point, polygone):
        """Vérifie si un point est à l'intérieur d'un polygone."""
        n = len(polygone.get_polygone())  # Assume que get_polygone() retourne la liste des points
        inside = False
        x, y = point.get_latitude(), point.get_longitude()  # ou les méthodes appropriées pour récupérer les coordonnées

        p1x, p1y = polygone.get_polygone()[0].get_latitude(), polygone.get_polygone()[0].get_longitude()
        for i in range(n + 1):
            p2x, p2y = polygone.get_polygone()[i % n].get_latitude(), polygone.get_polygone()[i % n].get_longitude()
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside


    def estDansPolygone(self, point: PointGeographique) -> bool:
        """
        Vérifie si le point est dans l'un des polygones de ce contour.
        """
        for connexe in self.contour:
            for polygone in connexe.get_polygones():  # Remplace par la méthode appropriée
                print("Polygone:", [f"({p.latitude}, {p.longitude})" for p in polygone.polygoneprimaire])  # Pour débogage
                if self.point_dans_polygone(point, polygone):
                    return True
        return False
