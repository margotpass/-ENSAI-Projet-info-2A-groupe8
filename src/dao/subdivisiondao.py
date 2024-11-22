from src.dao.db_connection import DBConnection
from src.business_object.subdivisions.arrondissement import Arrondissement
from src.business_object.subdivisions.region import Region
from src.business_object.subdivisions.epci import Epci
from src.business_object.subdivisions.commune import Commune
from src.business_object.subdivisions.canton import Canton
from src.business_object.subdivisions.departement import Departement
from src.business_object.Polygones.contour import Contour


class SubdivisionDAO:
    def insert_arrondissement(self, arrondissement: Arrondissement):
        geom_type = self.get_geom_type(arrondissement.polygones)
        geom_coordinates = self.get_geom_coordinates(arrondissement.polygones)

        query = """
        INSERT INTO arrondissement (nom_m, nom, insee_arr, insee_dep,
        insee_reg, geom_type, geom_coordinates)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    arrondissement.nom_m, arrondissement.nom,
                    arrondissement.insee_arr,
                    arrondissement.insee_dep, arrondissement.insee_reg,
                    geom_type,
                    geom_coordinates))

    def insert_canton(self, canton: Canton):
        geom_type = self.get_geom_type(canton.polygones)
        geom_coordinates = self.get_geom_coordinates(canton.polygones)

        query = """
        INSERT INTO canton (insee_can, insee_dep, insee_reg, geom_type,
        geom_coordinates)
        VALUES (%s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    canton.insee_can, canton.insee_dep, canton.insee_reg,
                    geom_type,
                    geom_coordinates))

    def insert_commune(self, commune: Commune):
        geom_type = self.get_geom_type(commune.polygones)
        geom_coordinates = self.get_geom_coordinates(commune.polygones)

        query = """
        INSERT INTO commune (nom, nom_m, insee_com, statut, population,
        insee_can, insee_arr, insee_dep, insee_reg, siren_epci, geom_type,
        geom_coordinates)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    commune.nom, commune.nom_m, commune.insee_com,
                    commune.statut, commune.population, commune.insee_can,
                    commune.insee_arr, commune.insee_dep, commune.insee_reg,
                    commune.siren_epci, geom_type, geom_coordinates))

    def insert_departement(self, departement: Departement):
        geom_type = self.get_geom_type(departement.polygones)
        geom_coordinates = self.get_geom_coordinates(departement.polygones)

        query = """
        INSERT INTO departement (nom_m, nom, insee_dep, insee_reg, geom_type,
        geom_coordinates)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    departement.nom_m, departement.nom, departement.insee_dep,
                    departement.insee_reg, geom_type, geom_coordinates))

    def insert_epci(self, epci: Epci):
        geom_type = self.get_geom_type(epci.polygones)
        geom_coordinates = self.get_geom_coordinates(epci.polygones)

        query = """
        INSERT INTO epci (nom_m, nom, code_siren, insee_dep, insee_reg,
        geom_type, geom_coordinates)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    epci.nom_m, epci.nom, epci.siren, epci.insee_dep,
                    epci.insee_reg,
                    geom_type, geom_coordinates))

    def insert_region(self, region: Region):
        geom_type = self.get_geom_type(region.polygones)
        geom_coordinates = self.get_geom_coordinates(region.polygones)

        query = """
        INSERT INTO region (nom_m, nom, insee_reg, geom_type, geom_coordinates)
        VALUES (%s, %s, %s, %s, %s)
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    region.nom_m, region.nom, region.insee_reg, geom_type,
                    geom_coordinates))

    # Méthodes de mise à jour
    def update_arrondissement(self, arrondissement):
        geom_type = self.get_geom_type(arrondissement.polygones)
        geom_coordinates = self.get_geom_coordinates(arrondissement.polygones)

        query = """
        UPDATE arrondissement
        SET nom_m = %s, nom = %s, insee_dep = %s, insee_reg = %s, geom_type = %s,
        geom_coordinates = %s WHERE insee_arr = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    arrondissement.nom_m, arrondissement.nom,
                    arrondissement.insee_dep,
                    arrondissement.insee_reg, geom_type, geom_coordinates,
                    arrondissement.insee_arr))

    def update_canton(self, canton):
        geom_type = self.get_geom_type(canton.polygones)
        geom_coordinates = self.get_geom_coordinates(canton.polygones)

        query = """
        UPDATE canton
        SET insee_dep = %s, insee_reg = %s, geom_type = %s, geom_coordinates = %s
        WHERE insee_can = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    canton.insee_dep, canton.insee_reg, geom_type,
                    geom_coordinates,
                    canton.insee_can))

    def update_commune(self, commune):
        geom_type = self.get_geom_type(commune.polygones)
        geom_coordinates = self.get_geom_coordinates(commune.polygones)

        query = """
        UPDATE commune
        SET nom = %s, nom_m = %s, statut = %s, population = %s, insee_can = %s,
        insee_arr = %s, insee_dep = %s, insee_reg = %s, siren_epci = %s,
        geom_type = %s,
        geom_coordinates = %s WHERE insee_com = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    commune.nom, commune.nom_m, commune.statut,
                    commune.population,
                    commune.insee_can, commune.insee_arr, commune.insee_dep,
                    commune.insee_reg,
                    commune.siren_epci, geom_type, geom_coordinates,
                    commune.insee_com))

    def update_departement(self, departement):
        geom_type = self.get_geom_type(departement.polygones)
        geom_coordinates = self.get_geom_coordinates(departement.polygones)

        query = """
        UPDATE departement
        SET nom_m = %s, nom = %s, insee_reg = %s, geom_type = %s,
        geom_coordinates = %s
        WHERE insee_dep = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    departement.nom_m, departement.nom, departement.insee_reg,
                    geom_type, geom_coordinates, departement.insee_dep))

    def update_epci(self, epci):
        geom_type = self.get_geom_type(epci.polygones)
        geom_coordinates = self.get_geom_coordinates(epci.polygones)

        query = """
        UPDATE epci
        SET nom_m = %s, nom = %s, insee_dep = %s, insee_reg = %s,
        geom_type = %s,
        geom_coordinates = %s WHERE siren = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    epci.nom_m, epci.nom, epci.insee_dep, epci.insee_reg,
                    geom_type,
                    geom_coordinates, epci.siren))

    def update_region(self, region):
        geom_type = self.get_geom_type(region.polygones)
        geom_coordinates = self.get_geom_coordinates(region.polygones)

        query = """
        UPDATE region
        SET nom_m = %s, nom = %s, geom_type = %s, geom_coordinates = %s
        WHERE insee_reg = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    region.nom_m, region.nom, geom_type, geom_coordinates,
                    region.insee_reg))

    # Méthodes pour déterminer le type et les coordonnées
    def get_geom_type(self, polygones):
        if len(polygones.contour) == 1:
            return 'Polygon'
        else:
            return 'MultiPolygon'
        return 'Unknown'

    def get_geom_coordinates(polygones: Contour) -> list[list[list[float]]]:
        """
        Retourne une liste imbriquée représentant les coordonnées géométriques d'un polygone.

        Args:
            polygone (Contour): Un objet de type Contour contenant les structures imbriquées.

        Returns:
            list[list[list[float]]]: Une liste de listes représentant les coordonnées des points.
        """
        # Parcourt les connexes dans le contour
        return [
            [
                [point.longitude, point.latitude]  # Récupère les coordonnées d'un PointGeographique
                for point in connexe.connexe       # Parcourt les points d'un Connexe
            ]
            for connexe in polygones.contour        # Parcourt les connexes dans le Contour
        ]

    def delete_arrondissement(self, insee_arr):
        query = """
        DELETE FROM arrondissement
        WHERE insee_arr = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_arr,))

    def delete_canton(self, insee_can):
        query = """
        DELETE FROM canton
        WHERE insee_can = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_can,))

    def delete_commune(self, insee_com):
        query = """
        DELETE FROM commune
        WHERE insee_com = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_com,))

    def delete_departement(self, insee_dep):
        query = """
        DELETE FROM departement
        WHERE insee_dep = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_dep,))

    def delete_epci(self, siren):
        query = """
        DELETE FROM epci
        WHERE siren = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (siren,))

    def delete_region(self, insee_reg):
        query = """
        DELETE FROM region
        WHERE insee_reg = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_reg,))
    # Méthodes de recherche

    def find_region_by_insee(self, insee_reg: str):
        """
        Trouve une région par son code INSEE.
        """
        query = """
        SELECT insee_reg, nom
        FROM geodata2.region
        WHERE insee_reg = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_reg,))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {"insee_reg": result["insee_reg"], "nom": result["nom"]}
                return None  # Aucun résultat trouvé

    def find_departement_by_insee(self, insee_dep: str, ):
        """
        Trouve un département par son code INSEE.
        """
        query = """
        SELECT insee_dep, nom, insee_reg
        FROM geodata2.departement
        WHERE insee_dep = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_dep,))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {
                        "insee_dep": result["insee_dep"],
                        "nom": result["nom"],
                        "insee_reg": result["insee_reg"],
                    }
                return None  # Aucun résultat trouvé

    def find_arrondissement_by_insee(self, insee_arr: str, insee_dep:str):
        """
        Trouve un arrondissement par son code INSEE.
        """
        query = """
        SELECT insee_arr, nom, insee_dep, insee_reg
        FROM geodata2.arrondissement
        WHERE insee_arr = %s AND insee_dep = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_arr,insee_dep))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {
                        "insee_arr": result["insee_arr"],
                        "nom": result["nom"],
                        "insee_dep": result["insee_dep"],
                        "insee_reg": result["insee_reg"],
                    }
                return None  # Aucun résultat trouvé

    def find_canton_by_insee(self, insee_can: str, insee_dep: str =None):
        """
        Trouve un canton par son code INSEE.
        """
        query = """
        SELECT insee_can, insee_dep, insee_reg
        FROM geodata2.canton
        WHERE insee_can = %s AND insee_dep = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_can,insee_dep))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {
                        "insee_can": result["insee_can"],
                        "insee_dep": result["insee_dep"],
                        "insee_reg": result["insee_reg"],
                    }
                return None  # Aucun résultat trouvé

    def find_commune_by_insee(self, insee_com: str):
        """
        Trouve une commune par son code INSEE.
        """
        query = """
        SELECT insee_com, nom, insee_can, insee_arr, insee_dep, insee_reg
        FROM geodata2.commune
        WHERE insee_com = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (insee_com,))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {
                        "insee_com": result["insee_com"],
                        "nom": result["nom"],
                        "insee_can": result["insee_can"],
                        "insee_arr": result["insee_arr"],
                        "insee_dep": result["insee_dep"],
                        "insee_reg": result["insee_reg"],
                    }
                return None  # Aucun résultat trouvé

    def find_epci_by_siren(self, code_siren: str):
        """
        Trouve un EPCI par son code SIREN.
        """
        query = """
        SELECT code_siren, nom, nature
        FROM geodata2.epci
        WHERE code_siren = %s
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (code_siren,))
                result = cursor.fetchone()
                if result:  # Vérifie si un résultat est trouvé
                    return {
                        "code_siren": result["code_siren"],
                        "nom": result["nom"],
                        "nature_epci": result["nature"],
                    }
                return None  # Aucun résultat trouvé

    def find_by_code_insee(self, type_subdivision: str, code_insee: str,
                           code_dep=None):
        """
        Trouve une subdivision par son type et son code INSEE.
        Utilise les méthodes dédiées pour chaque type de subdivision.
        """
        if type_subdivision == "Region":
            return self.find_region_by_insee(code_insee)
        elif type_subdivision == "Departement":
            return self.find_departement_by_insee(code_insee)
        elif type_subdivision == "Arrondissement":
            return self.find_arrondissement_by_insee(code_insee, code_dep)
        elif type_subdivision == "Canton":
            return self.find_canton_by_insee(code_insee, code_dep)
        elif type_subdivision == "Commune":
            return self.find_commune_by_insee(code_insee)
        elif type_subdivision == "EPCI":
            return self.find_epci_by_siren(code_insee)
        else:
            raise ValueError("Type de subdivision inconnu.")
