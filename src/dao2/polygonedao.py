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
        """Ajoute un PolygonePrimaire dans la base de données avec ses points et calcule la colonne de contrôle."""
        point_dao = PointGeographiqueDAO()

        # Calcul de la somme des coordonnées pour la colonne de contrôle
        somme_coordonnees = sum(point.longitude + point.latitude for point in polygone.polygoneprimaire)

        # Ajoute chaque point et récupère les IDs
        points_ids = [point_dao.ajouter_point(point) for point in polygone.polygoneprimaire]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Insérer le Polygone dans la table Polygones avec la somme des coordonnées
                cursor.execute(
                    "INSERT INTO geodata.Polygones (somme_coordonnees) VALUES (%s) RETURNING id",
                    (somme_coordonnees,)
                )
                polygone_id = cursor.fetchone()[0]

                # Insérer les relations dans la table d'association polygone_point avec l'ordre des points
                for ordre, point_id in enumerate(points_ids, start=1):
                    cursor.execute(
                        "INSERT INTO geodata.polygone_point (id_polygone, id_point, ordre) VALUES (%s, %s, %s)",
                        (polygone_id, point_id, ordre)
                    )
                connection.commit()
                # Retourner l'ID du Polygone ajouté
                return polygone_id

    def update_polygone(self, polygone_id, nouvelle_liste_points):
        """Met à jour un PolygonePrimaire existant en remplaçant ses points par une nouvelle liste de points."""
        point_dao = PointGeographiqueDAO()

        # Créer de nouveaux points géographiques pour le polygone
        nouveaux_points = [point_dao.creer_point(long, lat) for long, lat in nouvelle_liste_points]
        somme_coordonnees = sum(point.longitude + point.latitude for point in nouveaux_points)

        # Ajouter les nouveaux points et obtenir leurs IDs
        nouveaux_points_ids = [point_dao.ajouter_point(point) for point in nouveaux_points]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Mettre à jour la somme des coordonnées dans la table Polygones
                cursor.execute(
                    "UPDATE geodata.Polygones SET somme_coordonnees = %s WHERE id = %s",
                    (somme_coordonnees, polygone_id)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Le polygone avec l'id {polygone_id} n'existe pas.")

                # Supprimer les anciennes associations points-polygone
                cursor.execute(
                    "DELETE FROM geodata.polygone_point WHERE id_polygone = %s",
                    (polygone_id,)
                )

                # Insérer les nouvelles associations dans la table polygone_point
                for ordre, point_id in enumerate(nouveaux_points_ids, start=1):
                    cursor.execute(
                        "INSERT INTO geodata.polygone_point (id_polygone, id_point, ordre) VALUES (%s, %s, %s)",
                        (polygone_id, point_id, ordre)
                    )

                # Commit des modifications
                connection.commit()

    def delete_polygone(self, polygone_id):
        """Supprime un PolygonePrimaire de la base de données, y compris ses points associés et ses associations."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Supprimer les associations dans la table polygone_point
                cursor.execute(
                    "DELETE FROM geodata.polygone_point WHERE id_polygone = %s",
                    (polygone_id,)
                )

                # Supprimer le polygone lui-même dans la table Polygones
                cursor.execute(
                    "DELETE FROM geodata.Polygones WHERE id = %s",
                    (polygone_id,)
                )

                if cursor.rowcount == 0:
                    raise ValueError(f"Le polygone avec l'id {polygone_id} n'existe pas.")

                # Commit des modifications
                connection.commit()
