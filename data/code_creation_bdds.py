import os
import json
from db_connection import DBConnection
import shapefile  # PyShp pour lire les fichiers .shp

def import_shapefile_to_db(shapefile_path, table_name, schema_name='geodata'):
    # Connexion à la base de données
    db = DBConnection().connection
    cursor = db.cursor()

    # Lire les attributs et géométries du shapefile
    with shapefile.Reader(shapefile_path) as shp:
        # Extraire les noms des champs dans le fichier shapefile
        fields = shp.fields[1:]  # On ignore le premier champ (supplémentaire généré par PyShp)
        field_names = [field[0].lower() for field in fields]  # Noms des champs en minuscules

        # Vérifier si 'id' est déjà présent dans le shapefile
        if 'id' in field_names:
            serial_id_col = ''  # Pas besoin de colonne 'serial_id'
        else:
            serial_id_col = 'serial_id SERIAL PRIMARY KEY,'

        # Création de la table dans le schéma spécifié avec les attributs et la géométrie
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
            {serial_id_col}
            {" ,".join([f"{name} TEXT" for name in field_names])},  -- Colonnes pour les attributs
            geom_type TEXT,  -- Colonne pour le type de géométrie
            geom_coordinates JSON  -- Colonne pour stocker les coordonnées en JSON
        );
        """
        cursor.execute(create_table_query)
        db.commit()

        # Parcourir toutes les formes géométriques et attributs dans le fichier
        for record, shape in zip(shp.records(), shp.shapes()):
            # Convertir la géométrie en format JSON
            json_geom = shape_to_json(shape)

            # Construire la requête d'insertion
            insert_query = f"""
            INSERT INTO {schema_name}.{table_name} ({", ".join(field_names)}, geom_type, geom_coordinates)
            VALUES ({", ".join(['%s' for _ in field_names])}, %s, %s);
            """

            # Insertion des données des attributs et de la géométrie dans la base
            cursor.execute(insert_query, (*record, json_geom['type'], json.dumps(json_geom['coordinates'])))
        db.commit()

    cursor.close()
    db.close()

def shape_to_json(shape):
    """
    Convertit une géométrie PyShp en format JSON.
    """
    if shape.shapeType == shapefile.POLYGON or shape.shapeType == shapefile.POLYGONZ:
        json_geom = {
            "type": "Polygon",
            "coordinates": shape.points
        }
        return json_geom
    else:
        raise ValueError("Type de géométrie non pris en charge")

if __name__ == "__main__":
    shapefile_path = r"Z:\Desktop\Projet Info\ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-08-26\ADMIN-EXPRESS\1_DONNEES_LIVRAISON_2024-08-00122\ADE_3-2_SHP_WGS84G_FRA-ED2024-08-26\ARRONDISSEMENT.shp"


    try:
        # Appel de la fonction pour importer les données du shapefile dans la table "region" dans le schéma "geodata"
        import_shapefile_to_db(shapefile_path, "arrondissement")
        print("Données insérées avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")
