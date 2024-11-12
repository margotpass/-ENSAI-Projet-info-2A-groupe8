import psycopg2

# Connexion à la base de données
conn = psycopg2.connect(
    host="sgbd-eleves.domensai.ecole",
    port="5432",
    database="id2534",
    user="id2534",
    password="id2534"
)
cursor = conn.cursor()

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

# Suppression des données dans chaque table
for table in tables:
    cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
    print(f"Données supprimées de la table {table}")

# Commit des modifications et fermeture de la connexion
conn.commit()
cursor.close()
conn.close()
print("Toutes les données ont été suspprimées.")