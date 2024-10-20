from src.dao.db_connection import DBConnection
from src.business_object.PointGeographique import PointGeographique


class PointGeographiqueDao:
    """ DAO qui permet d'obtenir des informations sur un point"""
    def create_table_points(self):
        """Métode pour créer la table où nous allons stocker nos points
           dans PostgreSQL
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête SQL pour créer la table points
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS points (
                        id SERIAL PRIMARY KEY,
                        latitude FLOAT NOT NULL,
                        longitude FLOAT NOT NULL
                    )
                    """
                    # Exécution de la requête
                    cursor.execute(create_table_query)
                    # Valider la transaction pour que la table soit créée
                    connection.commit()

                    print("Table 'points' créée avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création de la table 'points' : {e}")

    def alter_table_points_add_typecoordonnees(self):
        """
        Ajoute la colonne 'type_coordonnees' à la table 'points'.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                    ALTER TABLE points
                    ADD COLUMN type_coordonnees TEXT;"""
                    )
                    connection.commit()
                    print("Colonne 'type_coordonnees' ajoutée avec succès!")
        except Exception as e:
            print(
                f"Erreur lors de l'ajout de la colonne 'type_coordonnes: {e}")

    def create_point(self, longitude, latitude, type_coordonnees):
        """Méthode permettant l'ajout d'un point dont on connait les
        coordonnées et le système de coordonnées à la table points
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO points (longitude, latitude, type_coordonnees)
                VALUES (%s, %s, %s);
                """, (longitude, latitude, type_coordonnees))
                connection.commit()
                print("Point créé avec succès.")

    def get_point_by_coordinates(self, longitude, latitude, type_coordonnees):
        """Récupère un point de notre BDD à partir de ses coordonnées
        et d'un système de coordonnées spécifié """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """"SELECT * FROM points
                    WHERE longitude = %(longitude)s,
                    latitude = %(latitude)s AND
                    type_coordonnees = %(type_coordonnees)s
                    ; """,
                    {
                        "longitude": longitude,
                        "latitude": latitude,
                        "type_coordonnes": type_coordonnees
                    },
                )
            res = cursor.fetchone()

        if res:
            point = PointGeographique(
                longitude=res["longitude"],
                latitude=res["latitude"],
                typeCoordonnees=res["type_coordonnees"]
            )
            print(f"Point trouvé : {point}")
            return point
        else:
            print("Aucun point trouvé")
            return None

    def update_point(self):
