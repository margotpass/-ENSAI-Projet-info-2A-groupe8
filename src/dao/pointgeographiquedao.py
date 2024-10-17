from src.dao.db_connection import DBConnection


class PointGeographiqueDao:
    def create_table_points(self):
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

    def create_point(self, longitude, latitude):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO points (longitude, latitude)
                VALUES (%s, %s);
                """, (longitude, latitude))
                connection.commit()
                print("Point créé avec succès.")

    def get_point_by_coordinates(self, longitude, latitude):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM points                    "
                    "WHERE longitude = %(longitude)s AND     "
                    "latitude = %(latitude)s)                "
                    "RETURNIND id;",
                    {
                        "longitude": longitude,
                        "latitude": latitude
                    },
                )
            res = cursor.fetchone

        if res:
            longitude = res["longitude"],
            latitude = res["latitude"]

