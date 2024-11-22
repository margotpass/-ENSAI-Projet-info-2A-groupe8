from src.utils.db_connection import DBConnection

# Liste des tables dans l'ordre des dépendances pour éviter les erreurs de contrainte
tables = [
    "geodata.Polygone_Point",
    "geodata.Connexe_Polygone",
    "geodata.Contour_Connexe",
    "geodata.Subdivision_Contour",
    "geodata.Points",
    "geodata.Polygones",
    "geodata.Connexes",
    "geodata.Contours",
    "geodata.Subdivision"
]

try:
    # Connexion à la base de données via DBConnection
    with DBConnection().connection as conn:
        with conn.cursor() as cursor:
            # Suppression des données dans chaque table
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
                print(f"Données supprimées de la table {table}")

        # Commit des modifications
        conn.commit()
        print("Toutes les données ont été supprimées avec succès.")

except Exception as e:
    print(f"Une erreur est survenue : {e}")
