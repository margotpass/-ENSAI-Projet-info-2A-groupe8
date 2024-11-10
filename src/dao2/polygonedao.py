from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.dao2.pointgeographiquedao import PointGeographiqueDAO
from src.dao.db_connection import DBConnection


class PolygoneDAO:
    def creer_polygone(self, liste_points):
        """Crée un objet PolygonePrimaire à partir d'une liste de points géographiques."""
        point_dao = PointGeographiqueDAO()
        points = [point_dao.creer_point(long, lat) for long, lat in liste_points]
        return PolygonePrimaire(points)

    def ajouter_polygone(self, polygone):
        """Ajoute un PolygonePrimaire dans la base de données."""
        point_dao = PointGeographiqueDAO()
        points_ids = [point_dao.ajouter_point(point) for point in polygone.points]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO geodata.Polygones (points) VALUES (%s) RETURNING id",
                    (points_ids,)
                )
                polygone.id = cursor.fetchone()[0]
                return polygone.id
