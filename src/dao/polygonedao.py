from src.dao.db_connection import DBConnection
from src.business_object.Polygones.Polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique
from typing import List


class PolygoneDAO:
    """ DAO qui permet d'obtenir des informations sur les polygones """

    def create_table_polygones(self):
        """Méthode pour créer la table où nous allons stocker nos polygones dans PostgreSQL et insérer les polygones existants des autres tables"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Créer la table polygones
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS geodata.polygones (
                        id SERIAL PRIMARY KEY,
                        subdivision_id TEXT NOT NULL,
                        geom_coordinates JSON NOT NULL,
                        geom_type TEXT NOT NULL
                    )
                    """
                    cursor.execute(create_table_query)

                    # Insérer les polygones des autres tables
                    insert_polygons_query = """
                    INSERT INTO geodata.polygones (subdivision_id, geom_coordinates, geom_type)
                    SELECT id, geom_coordinates, geom_type FROM geodata.arrondissement
                    UNION ALL
                    SELECT id, geom_coordinates, geom_type FROM geodata.commune
                    UNION ALL
                    SELECT id, geom_coordinates, geom_type FROM geodata.epci
                    UNION ALL
                    SELECT id, geom_coordinates, geom_type FROM geodata.region
                    UNION ALL
                    SELECT id, geom_coordinates, geom_type FROM geodata.canton
                    UNION ALL
                    SELECT id, geom_coordinates, geom_type FROM geodata.departement
                    ;
                    """
                    cursor.execute(insert_polygons_query)

                      # Valider la transaction
                    connection.commit()
                    print("Table 'polygones' créée et polygones existants insérés avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création de la table 'polygones' : {e}")

    def create_polygone(self, subdivision_id: int, type_subdivision: str, geom_coordinates: str, geom_type: str):
        """Méthode pour ajouter un polygone à la table"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO polygones (subdivision_id, type_subdivision, geom_coordinates, geom_type)
                VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s);
                """, (subdivision_id, type_subdivision, geom_coordinates, geom_type))
                connection.commit()
                print("Polygone créé avec succès.")

    def read_polygone(self, id: int) -> PolygonePrimaire:
        """Récupère un polygone à partir de son ID"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM polygones WHERE id = %s;
                """, (id,))
                res = cursor.fetchone()

        if res:
            return PolygonePrimaire(id=res[0], subdivision_id=res[1], type_subdivision=res[2], geom_coordinates=res[3], geom_type=res[4])
        else:
            print("Aucun polygone trouvé")
            return None

    def update_polygone(self, id: int, subdivision_id: int = None, type_subdivision: str = None, geom_coordinates: str = None, geom_type: str = None):
        """Met à jour un polygone existant"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                update_fields = []
                params = []

                if subdivision_id is not None:
                    update_fields.append("subdivision_id = %s")
                    params.append(subdivision_id)
                if type_subdivision is not None:
                    update_fields.append("type_subdivision = %s")
                    params.append(type_subdivision)
                if geom_coordinates is not None:
                    update_fields.append("geom_coordinates = ST_GeomFromText(%s, 4326)")
                    params.append(geom_coordinates)
                if geom_type is not None:
                    update_fields.append("geom_type = %s")
                    params.append(geom_type)

                if update_fields:
                    update_query = f"""
                    UPDATE polygones
                    SET {', '.join(update_fields)}
                    WHERE id = %s;
                    """
                    params.append(id)
                    cursor.execute(update_query, tuple(params))
                    connection.commit()
                    print("Polygone mis à jour avec succès.")
                else:
                    print("Aucune mise à jour à effectuer.")

    def delete_polygone(self, id: int):
        """Supprime un polygone de la base de données par son ID"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM polygones
                    WHERE id = %s;
                """, (id,))
                connection.commit()
                print(f"Polygone avec ID {id} supprimé avec succès.")

    def findPointsByPolygone(self, id: int) -> List[PointGeographique]:
        """Récupère une liste de points associés à un polygone donné par son ID"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.longitude, p.latitude, p.type_coordonnees
                    FROM points AS p
                    JOIN polygone_points AS pp ON pp.point_id = p.id
                    WHERE pp.polygone_id = %s;
                """, (id,))
                results = cursor.fetchall()

        points = []
        for res in results:
            point = PointGeographique(longitude=res[0], latitude=res[1], type_coordonnees=res[2])
            points.append(point)

        return points
