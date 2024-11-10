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

                # Retourner l'ID du Polygone ajouté
                return polygone_id
