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


if __name__ == "__main__":
    point_dao = PointGeographiqueDao()

    # Créer la table points dans la base de données
    point_dao.create_table_points()
