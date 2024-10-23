from src.business_object.Polygones.Connexe import Connexe
from src.dao.polygone_dao import PolygoneDAO
from typing import List


class ConnexeDAO:
    def __init__(self, db_connection):
        self.polygone_dao = PolygoneDAO(db_connection)

    def get_connexes_from_geom(self, geom_coordinates: list, geom_type: str) -> List[Connexe]:
        """
        Récupère les connexes à partir des coordonnées géométriques.
        Si geom_type est 'Polygon', il peut contenir plusieurs polygones au sein d'un même connexe (comme dans le cas de la Drôme).
        Si geom_type est 'MultiPolygon', chaque groupe de coordonnées représente un connexe distinct.
        """
        connexes = []
       
        if geom_type == 'Polygon':
            # Un seul connexe avec potentiellement plusieurs polygones (trous inclus)
            polygones = self.polygone_dao.get_polygones_from_geom(geom_coordinates)
            connexes.append(Connexe(polygones))

        elif geom_type == 'MultiPolygon':
            # Plusieurs connexes, chacun avec ses polygones
            for polygon_group in geom_coordinates:  # Chaque élément est un groupe de polygones pour un connexe
                polygones = self.polygone_dao.get_polygones_from_geom(polygon_group)
                connexes.append(Connexe(polygones))

        return connexes