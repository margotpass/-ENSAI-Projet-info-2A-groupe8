from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.Polygoneprimaire import PolygonePrimaire
from src.business_object.Polygones.Connexe import Connexe
from src.business_object.Polygones.contourmm import ContourMM
from src.dao.db_connection import DBConnection


class LocaliserServiceMM:
    def __init__(self, db_connection):
        self.db = db_connection
        self.hierarchy = ['region', 'departement', 'arrondissement', 'canton', 'commune']

    def localiser_point(self, point: PointGeographique) -> dict:
        """
        Localise un point géographique dans la subdivision la plus fine possible et renvoie un dictionnaire avec
        la région, le département, la commune, etc.
        """
        localisation = {}
        current_subdivision_id = None

        # Parcourir la hiérarchie (de la région à la commune)
        for niveau in self.hierarchy:
            subdivision = self.rechercher_dans_niveau(point, niveau, current_subdivision_id)

            if subdivision is not None:
                # Stocker la subdivision trouvée dans le dictionnaire
                localisation[niveau] = subdivision['nom']
                # Mettre à jour l'ID de la subdivision trouvée pour filtrer le niveau suivant
                current_subdivision_id = subdivision['id']
            else:
                # Si on ne trouve pas à ce niveau, on arrête la recherche
                break

        return localisation

    def rechercher_dans_niveau(self, point: PointGeographique, niveau: str, parent_id: str = None) -> dict:
        """
        Recherche si le point donné se trouve dans une subdivision géographique pour un niveau donné
        (par exemple, région, département, commune).
        """
        # Déterminer la colonne INSEE et la table correspondantes
        table_name = niveau
        insee_column = self.get_insee_column(table_name)

        # Construire la requête SQL pour récupérer les contours du niveau donné
        query = f"SELECT geom_coordinates, geom_type, {insee_column} as id, nom FROM geodata2.{table_name}"
        params = []

        if parent_id:
            # Ajouter une clause WHERE pour filtrer par la subdivision parente (en utilisant l'INSEE)
            query += f" WHERE {insee_column} = %s"
            params.append(parent_id)

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()

                for result in results:
                    contour = self.transformer_geom_en_contour(result['geom_coordinates'], result['geom_type'])

                    # Vérifier si le point est dans ce contour
                    if contour.estDansPolygone(point):
                        return {'id': result['id'], 'nom': result['nom']}

        return None

    def get_insee_column(self, table_name: str) -> str:
        """
        Retourne le nom de la colonne INSEE en fonction du nom de la table.
        """
        if table_name == "region":
            return "insee_reg"
        elif table_name == "departement":
            return "insee_dep"
        elif table_name == "arrondissement":
            return "insee_arr"
        elif table_name == "canton":
            return "insee_can"
        elif table_name == "commune":
            return "insee_com"
        else:
            raise ValueError(f"Nom de table inconnu : {table_name}")

    def transformer_geom_en_contour(self, geom_coordinates: list, geom_type: str) -> ContourMM:
        """
        Convertit les données geom_coordinates en un objet ContourMM.
        """
        connexes = []

        if geom_type == 'Polygon':
            polygones = []
            for exterior_coords in geom_coordinates:
                points = [PointGeographique(latitude=coord[1], longitude=coord[0]) for coord in exterior_coords]
                polygones.append(PolygonePrimaire(points))
            connexes.append(Connexe(polygones))

        elif geom_type == 'MultiPolygon':
            for polygon_group in geom_coordinates:
                polygones = []
                for exterior_coords in polygon_group:
                    points = [PointGeographique(latitude=coord[1], longitude=coord[0]) for coord in exterior_coords]
                    polygones.append(PolygonePrimaire(points))
                connexes.append(Connexe(polygones))

        return ContourMM(connexes)