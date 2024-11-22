from src.utils.db_connection import DBConnection

# Liste des tables à vider, dans l'ordre des dépendances (les enfants avant
# les parents)
tables = [
    "geodata2.commune",
    "geodata2.arrondissement",
    "geodata2.departement",
    "geodata2.region",
    "geodata2.epci",
    "geodata2.canton"
]


def clear_tables():
    """
    Vide toutes les tables du schéma `geodata2`.
    """
    with DBConnection().connection as conn:
        with conn.cursor() as cursor:
            for table in tables:
                try:
                    # On utilise TRUNCATE pour éviter les erreurs de
                    # contraintes et nettoyer les tables efficacement
                    cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
                    print(f"Table {table} vidée avec succès.")
                except Exception as e:
                    print(f"Erreur lors du vidage de la table {table} : {e}")
            conn.commit()


if __name__ == "__main__":
    clear_tables()
