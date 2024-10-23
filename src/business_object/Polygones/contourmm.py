from src.business_object.Polygones.Connexe import Connexe
from src.business_object.Polygones.Polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique
from typing import List


class ContourMM:
    def __init__(self, connexes: List[Connexe]):
        self.connexes = connexes

    def estDansPolygone(self, point: PointGeographique) -> bool:
        """
        Vérifie si le point est dans l'un des polygones de ce contour.
        """
        for connexe in self.connexes:
            for polygone in connexe.Connexe:  # `connexe` est une liste de Polygones
                if self.point_dans_polygone(point, polygone):
                    return True
        return False

    def point_dans_polygone(self, point: PointGeographique, polygone: PolygonePrimaire) -> bool:
        """
        Algorithme du Ray-Casting pour vérifier si un point est dans un polygone.
        """
        points = polygone.polygoneprimaire
        n = len(points)
        inside = False

        x, y = point.latitude, point.longitude
        p1x, p1y = points[0].latitude, points[0].longitude

        for i in range(n + 1):
            p2x, p2y = points[i % n].latitude, points[i % n].longitude
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

