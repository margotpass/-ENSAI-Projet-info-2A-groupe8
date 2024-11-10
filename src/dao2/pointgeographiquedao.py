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

    def update_point(self, point_id, new_longitude, new_latitude):
        """Met à jour les coordonnées d'un PointGeographique dans la base de données."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE geodata.Points SET longitude = %s, latitude = %s WHERE id = %s",
                    (new_longitude, new_latitude, point_id)
                )
                # Vérifier si une ligne a été affectée
                if cursor.rowcount == 0:
                    raise ValueError(f"Le point avec l'id {point_id} n'existe pas.")
                connection.commit()

    def delete_point(self, point_id):
        """Supprime un PointGeographique de la base de données."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM geodata.Points WHERE id = %s",
                    (point_id,)
                )
                # Vérifier si une ligne a été affectée
                if cursor.rowcount == 0:
                    raise ValueError(f"Le point avec l'id {point_id} n'existe pas.")
                connection.commit()
