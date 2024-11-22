from src.business_object.pointgeographique import PointGeographique
from typing import List


class PointGeographiqueDAO:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_points_from_geom(
        self, geom_coordinates: list, typecoordonnees="WGS84"
    ) -> List[PointGeographique]:
        """
        Convertit les coordonnées géométriques en une liste de points
        géographiques avec un type de coordonnées donné.
        Par défaut, considère les coordonnées comme étant en WGS84.
        """
        points = [
            PointGeographique(
                latitude=coord[1], longitude=coord[0],
                typecoordonnees=typecoordonnees
            )
            for coord in geom_coordinates
        ]
        return points
