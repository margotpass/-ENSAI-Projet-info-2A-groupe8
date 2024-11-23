from src.business_object.pointgeographique import PointGeographique
from src.dao.db_connection import DBConnection


class PointGeographiqueDAO:
    def creer_point(self, lat, long):
        """Crée un objet PointGeographique."""
        return PointGeographique(lat, long)

    def ajouter_point(self, point, connection):
        """Ajoute un PointGeographique dans la base de données,
        sauf s'il existe déjà."""

        with connection.cursor() as cursor:
            # Vérifier si un point avec les mêmes coordonnées existe déjà
            cursor.execute(
                "SELECT id FROM geodata.Points WHERE lat = %s AND long = %s",
                (point.latitude, point.longitude)
            )
            result = cursor.fetchall()

            if len(list(result)) != 0:
                # Le point existe déjà, renvoyer l'ID existant
                return list(result)[0]['id']

            # Si le point n'existe pas, insérer le nouveau point
            cursor.execute(
                "INSERT INTO geodata.Points (lat, long) "
                "VALUES (%s, %s) RETURNING id",
                (point.latitude, point.longitude)
            )

            # Récupérer l'ID du nouveau point inséré
            point_id = list(cursor.fetchall())[0]['id']
            connection.commit()
            return point_id

    def update_point(self, point_id, new_latitude, new_longitude):
        """Met à jour les coordonnées d'un PointGeographique
        dans la base de données."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE geodata.Points SET lat = %s, long = %s "
                    "WHERE id = %s",
                    (new_latitude, new_longitude, point_id)
                )
                # Vérifier si une ligne a été affectée
                if cursor.rowcount == 0:
                    raise ValueError(f"Le point avec l'id {point_id}"
                                     f" n'existe pas.")
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
                    raise ValueError(f"Le point avec l'id {point_id}"
                                     f" n'existe pas.")
                connection.commit()
