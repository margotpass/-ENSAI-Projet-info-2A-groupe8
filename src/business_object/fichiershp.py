import fiona
import json
import gzip
import base64
from db_connection import DBConnection


class FichierShp:
    def __init__(self, chemin: str):
        """
        Initialise une instance de FichierShp.
        """
        self.chemin = chemin
        self.geometry = None
        self.attributs = {}

    def charger(self):
        """
        Charge les données du fichier shapefile dans les attributs de la
        classe.
        """
        try:
            with fiona.open(self.chemin) as src:
                self.geometry = [feature['geometry'] for feature in src]
                self.attributs = [feature['properties'] for feature in src]
        except Exception as e:
            print(f"Erreur lors du chargement du shapefile : {e}")

    def get_geometry(self):
        """
        Retourne les géométries chargées.
        """
        return self.geometry

    def get_attributs(self):
        """
        Retourne les attributs chargés.
        """
        return self.attributs

    def filtrer(self, condition: str):
        """
        Filtre les données en fonction d'une condition.
        La condition doit être une expression Python valide.
        Exemple : "attributs['population'] > 1000"
        """
        try:
            return [
                {"geometry": geom, "attributs": attr}
                for geom, attr in zip(self.geometry, self.attributs)
                if eval(condition, {"geometry": geom, "attributs": attr})
            ]
        except Exception as e:
            print(f"Erreur lors du filtrage : {e}")
            return []

    def sauvegarder(self, chemin: str) -> bool:
        """
        Sauvegarde les données filtrées dans un fichier shapefile.
        """
        try:
            with fiona.open(self.chemin) as src:
                schema = src.schema
                crs = src.crs

                with fiona.open(chemin, mode='w', driver=src.driver,
                                schema=schema, crs=crs) as dst:
                    for geom, attr in zip(self.geometry, self.attributs):
                        dst.write({
                            "geometry": geom,
                            "properties": attr
                        })
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

    @staticmethod
    def compress_to_base64(data: str) -> str:
        """
        Compresse les données en gzip puis les encode en base64.
        """
        compressed_data = gzip.compress(data.encode('utf-8'))
        return base64.b64encode(compressed_data).decode('utf-8')

    def importer_dans_bd(self, table_name: str):
        """
        Importe les données du shapefile dans une base de données.
        """
        db = DBConnection().connection
        cursor = db.cursor()

        try:
            with fiona.open(self.chemin) as src:
                field_names = list(src.schema['properties'].keys())

                # Créer la table
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    serial_id SERIAL PRIMARY KEY,
                    {" ,".join([f"{field.lower()} TEXT" for field in
                                field_names])},
                    geom_type TEXT,
                    geom_coordinates JSON
                );
                """
                cursor.execute(create_table_query)
                db.commit()

                # Insérer les données
                for feature in src:
                    properties = feature['properties']
                    geometry = feature['geometry']

                    geom_json = json.dumps(geometry['coordinates'])
                    geom_compressed_base64 = self.compress_to_base64(geom_json)

                    insert_query = f"""
                    INSERT INTO {table_name} ({", ".join([field.lower() for
                                                          field in field_names]
                                                        )}, geom_type,
                                                        geom_coordinates)
                    VALUES ({", ".join(['%s' for _ in field_names])}, %s, %s);
                    """
                    cursor.execute(insert_query, (*properties.values(),
                                                  geometry['type'], json.dumps(
                                                    geom_compressed_base64)))

                db.commit()
        except Exception as e:
            print(f"Erreur lors de l'importation dans la base de données : {e}")
        finally:
            cursor.close()
            db.close()
