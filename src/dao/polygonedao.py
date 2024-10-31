from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.dao.pointgeographiquedao import PointGeographiqueDAO
from typing import List


class PolygoneDAO:
    def __init__(self, db_connection):
        self.point_geographique_dao = PointGeographiqueDAO(db_connection)

    def get_polygones_from_geom(self, geom_coordinates: list) -> List[PolygonePrimaire]:
        """
        Récupère des polygones primaires à partir des coordonnées géométriques.
        geom_coordinates est une liste où :
        - Le premier élément est le contour extérieur
        - Les éléments suivants (le cas échéant) sont des trous (anneaux intérieurs)
        """
        polygones = []

        # Le premier ensemble de coordonnées correspond au contour extérieur
        exterior_coords = geom_coordinates[0]
        exterior_points = self.point_geographique_dao.get_points_from_geom(exterior_coords)
        polygones.append(PolygonePrimaire(exterior_points))

        # Les ensembles suivants (s'il y en a) sont les trous
        for interior_coords in geom_coordinates[1:]:
            interior_points = self.point_geographique_dao.get_points_from_geom(interior_coords)
            polygones.append(PolygonePrimaire(interior_points))

        return polygones
