from src.dao.db_connection import DBConnection


class SubdivisionDAO:
    def insert_arrondissement(self, arrondissement):
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

    def insert_canton(self, canton):
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
                    canton.insee_can, canton.insee_dep, canton.insee_reg, geom_type,
                    geom_coordinates))

    def insert_commune(self, commune):
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

    def insert_departement(self, departement):
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

    def insert_epci(self, epci):
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

    def insert_region(self, region):
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
        if isinstance(polygones, Polygon):
            return 'Polygon'
        elif isinstance(polygones, MultiPolygon):
            return 'MultiPolygon'
        return 'Unknown'

    def get_geom_coordinates(self, polygones):
        if isinstance(polygones, Polygon):
            return list(polygones.exterior.coords)
        elif isinstance(polygones, MultiPolygon):
            return [list(p.exterior.coords) for p in polygones.geoms]
        return []

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
