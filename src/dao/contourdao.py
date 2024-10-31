from src.business_object.Polygones.contourmm import ContourMM
from src.dao.connexedao import ConnexeDAO
from typing import List, Tuple
from src.dao.db_connection import DBConnection


class ContourDAO:
    def __init__(self, db_connection):
        self.connexe_dao = ConnexeDAO(db_connection)

    def get_all_contours(self, table_name: str, parent_id: str = None) -> List[Tuple[ContourMM, str]]:
        """
        Récupère tous les contours pour une subdivision donnée (par ex. région, département).
        Si parent_id est fourni, filtre les subdivisions par leur parent (par exemple, les départements dans une région).
        Renvoie une liste de tuples (ContourMM, subdivision_id)
        """
        insee_column = self.get_insee_column(table_name)

        query = f"SELECT geom_coordinates, geom_type, {insee_column} FROM geodata2.{table_name}"

        if parent_id:
            query += f" WHERE {insee_column} = %s"
            params = (parent_id,)
        else:
            params = ()

        contours = []
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()

                for result in results:
                    geom_coordinates = result['geom_coordinates']  # Données déjà au format JSON (liste)
                    geom_type = result['geom_type']
                    subdivision_id = result[insee_column]

                    # Transformation des coordonnées géométriques en ContourMM en passant par ConnexeDAO
                    contour = self.transformer_geom_en_contour(geom_coordinates, geom_type)
                    contours.append((contour, subdivision_id))

        return contours

    def get_insee_column(self, table_name: str) -> str:
        """
        Retourne le nom de la colonne INSEE en fonction du nom de la table.
        """
        columns = {
            "region": "insee_reg",
            "departement": "insee_dep",
            "arrondissement": "insee_arr",
            "canton": "insee_can",
            "commune": "insee_com",
            "epci": "code_siren"
        }
        return columns.get(table_name, f"Nom de table inconnu : {table_name}")

    def transformer_geom_en_contour(self, geom_coordinates: list, geom_type: str) -> ContourMM:
        """
        Convertit les données geom_coordinates (déjà au format JSON, sous forme de listes) en un objet ContourMM.
        Appelle ConnexeDAO pour récupérer les connexes, puis construit un ContourMM.
        """
        # Appel à ConnexeDAO pour récupérer la structure des connexes à partir des geom_coordinates
        connexes = self.connexe_dao.get_connexes_from_geom(geom_coordinates, geom_type)

        # Création de l'objet ContourMM avec les connexes récupérés
        return ContourMM(connexes)
