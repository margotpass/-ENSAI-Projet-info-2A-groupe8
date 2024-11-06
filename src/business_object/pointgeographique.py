import pyproj

class PointGeographique():
    """ Point géographique caractérisé par ses coordonnées géographiques.
    paramètres:
    latitude -- latitude du point (float)
    longitude -- longitude du point (float)
    typecoordonnees -- type de coordonnées (str) : soit Lamb93 soit WGS84
    """
    def __init__(self, latitude, longitude, typecoordonnees):
        """ Initialise les coordonnées géographiques du point """
        if not isinstance(latitude, (int, float)):
            raise TypeError("La latitude doit être un nombre")
        self.latitude = latitude
        if not isinstance(longitude, (int, float)):
            raise TypeError("La longitude doit être un nombre")
        self.longitude = longitude
        # les coordonnées sont soit en Lambert 93 soit en WGS84 soit vide
        if typecoordonnees not in ["Lamb93", "WGS84", "", None, "None", "lam93", "wgs84"]:
            raise ValueError("Type de coordonnées non reconnu")
        self.typecoordonnees = typecoordonnees            

    def __str__(self):
        """Affiche les informations du point géographique"""
        return "Latitude: " + str(self.latitude) + " Longitude: " + str(self.longitude) + " Type de coordonnées: " + str(self.typecoordonnees)

    def get_latitude(self):
        """Retourne la latitude du point"""
        return self.latitude

    def get_longitude(self):
        """Retourne la longitude du point"""
        return self.longitude

    def get_typecoordonnees(self):
        """Retourne le type de coordonnées du point"""
        return self.typecoordonnees

    def convertir_type_coordonnees(self):
        """Si les coordonnées sont en Lambert 93, les convertit en WGS84"""
        if self.typecoordonnees == "Lamb93":
            # Lambert 93 CRS (projection)
            lambert = pyproj.CRS.from_epsg(2154)  # EPSG code for Lambert 93
            # WGS84 CRS (référentiel géographique)
            wgs84 = pyproj.CRS.from_epsg(4326)    # EPSG code for WGS84
            # Initialisation du transformeur avec un ordre de coordonnées (latitude, longitude)
            transformer = pyproj.Transformer.from_crs(lambert, wgs84, always_xy=True)

            # Transformer attend (longitude, latitude) pour la projection Lambert 93
            self.longitude, self.latitude = transformer.transform(self.longitude, self.latitude)
            self.typecoordonnees = "WGS84"

            # Debugging : Affichage des valeurs après transformation
            print(f"Transformation réussie: Latitude = {self.latitude}, Longitude = {self.longitude}")

        elif self.typecoordonnees == "WGS84":
            print("Les coordonnées sont déjà en WGS84")
        else:
            print("Type de coordonnées non reconnu")

# Test de la classe
coord = PointGeographique(48.856578, 2.351828, "WGS84")
print(coord)
coord.convertir_type_coordonnees()
print(coord)

coord2 = PointGeographique(48.86516571317747, 2.3320684023104286, "Lamb93")
print(coord2)
coord2.convertir_type_coordonnees()
print(coord2)
