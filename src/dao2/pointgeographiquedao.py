from src.business_object.pointgeographique import PointGeographique
from src.dao.db_connection import DBConnection


class PointGeographiqueDAO:
    def creer_point(self, long, lat):
        """Crée un objet PointGeographique."""
        return PointGeographique(long, lat)

    def ajouter_point(self, point):
        """Ajoute un PointGeographique dans la base de données."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO geodata.Points (longitude, latitude) VALUES (%s, %s) RETURNING id",
                    (point.longitude, point.latitude)
                )
                point.id = cursor.fetchone()[0]
                return point.id
