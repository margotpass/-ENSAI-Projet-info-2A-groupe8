import fiona
import psycopg2
from psycopg2 import sql

# Connexion à la base de données
conn = psycopg2.connect(
    host="sgbd-eleves.domensai.ecole",
    port="5432",
    database="id2534",
    user="id2534",
    password="id2534"
)
cursor = conn.cursor()

# Fonction pour insérer un point avec vérification d'unicité
def insert_point(cursor, lat, long):
    cursor.execute("SELECT id FROM geodata.points WHERE lat = %s AND long = %s", (lat, long))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO geodata.points (lat, long) VALUES (%s, %s) RETURNING id", (lat, long))
    return cursor.fetchone()[0]

# Fonction pour insérer un polygone simple avec vérification des points
def insert_polygon(cursor, connexe_id, points, ordre):
    somme_coordonnees = sum(lat + long for lat, long in points)
    cursor.execute(
        "INSERT INTO geodata.polygones (somme_coordonnees) VALUES (%s) RETURNING id",
        (somme_coordonnees,)
    )
    polygone_id = cursor.fetchone()[0]
    
    # Insérer la relation entre le connexe et le polygone
    cursor.execute(
        "INSERT INTO geodata.connexe_polygone (id_connexe, id_polygone, ordre) VALUES (%s, %s, %s)",
        (connexe_id, polygone_id, ordre)
    )
    
    # Insérer les points dans le polygone
    for ordre_point, (lat, long) in enumerate(points, start=1):
        point_id = insert_point(cursor, lat, long)
        cursor.execute(
            "SELECT 1 FROM geodata.polygone_point WHERE id_polygone = %s AND id_point = %s",
            (polygone_id, point_id)
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO geodata.polygone_point (id_polygone, id_point, ordre) VALUES (%s, %s, %s)",
                (polygone_id, point_id, ordre_point)
            )

# Fonction pour insérer un connexe avec ses polygones
def insert_connexe(cursor, contour_id, coordinates):
    somme_sommes_controle = sum(
        lat + long
        for polygon in coordinates
        if isinstance(polygon[0], list)
        for lat, long in polygon[0]
        if isinstance(lat, (int, float)) and isinstance(long, (int, float))
    )
    cursor.execute(
        "INSERT INTO geodata.connexes (somme_sommes_controle) VALUES (%s) RETURNING id",
        (somme_sommes_controle,)
    )
    connexe_id = cursor.fetchone()[0]
    
    cursor.execute(
        "INSERT INTO geodata.contour_connexe (id_contour, id_connexe) VALUES (%s, %s)",
        (contour_id, connexe_id)
    )
    
    for ordre, polygon in enumerate(coordinates, start=1):
        if isinstance(polygon[0][0], (list, tuple)):
            exterior = polygon[0]
            holes = polygon[1:]
            insert_polygon(cursor, connexe_id, exterior, 1)
            for ordre_trou, hole in enumerate(holes, start=2):
                insert_polygon(cursor, connexe_id, hole, ordre_trou)
        else:
            insert_polygon(cursor, connexe_id, polygon, ordre)

# Fonction pour insérer les données d'une subdivision
def insert_subdivision_data(file_path, type_subdivision, insee_code_field):
    print(f"Traitement du fichier : {file_path}")
    
    with fiona.open(file_path, 'r') as shp:
        for feature in shp:
            properties = feature['properties']
            geom_type = feature['geometry']['type']
            coordinates = feature['geometry']['coordinates']
            
            nom = properties.get("NOM")
            code_insee = properties.get(insee_code_field)
            
            if not nom or not code_insee:
                continue

            cursor.execute(
                "SELECT id FROM geodata.subdivision WHERE nom = %s AND type = %s",
                (nom, type_subdivision)
            )
            subdivision_result = cursor.fetchone()
            if subdivision_result:
                subdivision_id = subdivision_result[0]
            else:
                cursor.execute(
                    "INSERT INTO geodata.subdivision (type, nom, insee_com, insee_can, insee_arr, insee_dep, insee_reg, siren_epci) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (type_subdivision, nom, properties.get('INSEE_COM'), properties.get('INSEE_CAN'), properties.get('INSEE_ARR'),
                     properties.get('INSEE_DEP'), properties.get('INSEE_REG'), properties.get('CODE_SIREN'))
                )
                subdivision_id = cursor.fetchone()[0]
            
            cursor.execute("INSERT INTO geodata.contours (annee) VALUES (2024) RETURNING id")
            contour_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO geodata.subdivision_contour (id_subdivision, id_contour) VALUES (%s, %s)",
                (subdivision_id, contour_id)
            )
            
            if geom_type == "Polygon":
                insert_connexe(cursor, contour_id, [coordinates])
            elif geom_type == "MultiPolygon":
                for connexe_coords in coordinates:
                    insert_connexe(cursor, contour_id, connexe_coords)

    conn.commit()
    print(f"Insertion terminée pour le fichier : {file_path}")

# Appels spécifiques pour les cantons et les communes
file_path_canton = "Z:/Downloads/ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2024-02-22/ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2024-02-22/ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2024-03-00168/ADECOG_3-2_SHP_WGS84G_FRA-ED2024-02-22/Canton.shp"


insert_subdivision_data(file_path_canton, "Canton", "INSEE_CAN")


# Fermeture de la connexion
cursor.close()
conn.close()
print("Insertion terminée pour les fichiers des cantons et des communes.")
