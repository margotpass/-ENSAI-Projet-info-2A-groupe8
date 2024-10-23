from src.business_object.pointgeographique import PointGeographique
from src.dao.db_connection import DBConnection
from typing import List


class PointGeographiqueDAO:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_points_from_geom(self, geom_coordinates: list) -> List[PointGeographique]:
        """
        Convertit les coordonnées géométriques en une liste de points géographiques.
        """
        points = [PointGeographique(latitude=coord[1], longitude=coord[0]) for coord in geom_coordinates]
        return points
