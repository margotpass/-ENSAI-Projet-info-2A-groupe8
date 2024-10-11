import pyproj

class PointGeographique():
    """ Point géographique caractérisé par ses coordonnées géographiques.
    paramètres:
    latitude -- latitude du point (float)
    longitude -- longitude du point (float)
    typeCoordonnees -- type de coordonnées (str) : soit Lamb97, soit WGS84
    """
    def __init__(self, latitude, longitude, typeCoordonnees):
        self.latitude = latitude
        self.longitude = longitude
        self.typeCoordonnees = typeCoordonnees

    def __str__(self):
        """ str sert à afficher les informations du point géographique """
        return "Latitude: " + str(self.latitude) + " Longitude: " + str(self.longitude) + " Type de coordonnées: " + str(self.typeCoordonnees)

    def convertir_type_coordonnees(self):
        """ Si les coordonnées sont en Lamb97, les convertit en WGS84"""
        if self.typeCoordonnees == "Lamb97":
            # Conversion des coordonnées en Lambert 93 en WGS84
            lambert = pyproj.Proj("+init=EPSG:2154")
            wgs84 = pyproj.Proj("+init=EPSG:4326")
            self.longitude, self.latitude = pyproj.Transformer(lambert, wgs84, self.longitude, self.latitude)
            self.typeCoordonnees = "WGS84"
        else:
            print("Les coordonnées sont déjà en WGS84")

coord = PointGeographique(341120, 6875760, "Lamb97")
coord.convertir_type_coordonnees()
print(f"Longitude: {coord.longitude}, Latitude: {coord.latitude}")


