import pyproj


class PointGeographique():
    """ Point géographique caractérisé par ses coordonnées géographiques.
    paramètres:
    latitude -- latitude du point (float)
    longitude -- longitude du point (float)
    typeCoordonnees -- type de coordonnées (str) : soit Lamb93 soit WGS84
    """
    def __init__(self, latitude, longitude, typeCoordonnees):
        self.latitude = latitude
        self.longitude = longitude
        self.typeCoordonnees = typeCoordonnees

    def __str__(self):
        """ str sert à afficher les informations du point géographique """
        return "Latitude: " + str(self.latitude) + " Longitude: "
        + str(self.longitude) + " Type de coordonnées: "
        + str(self.typeCoordonnees)

    def convertir_type_coordonnees(self):
        """ Si les coordonnées sont en Lambert 93, les convertit en WGS84"""
        if self.typeCoordonnees == "Lamb93":
            lambert = pyproj.Proj(init='epsg:2154')
            wgs84 = pyproj.Proj(init='epsg:4326')
            self.longitude, self.latitude = pyproj.transform(lambert, wgs84,
                                                             self.latitude,
                                                             self.longitude)
            self.typeCoordonnees = "WGS84"
        elif self.typeCoordonnees == "WGS84":
            print("Les coordonnées sont déjà en WGS84")
        else:
            print("Type de coordonnées non reconnu")


# Test de convertir_type_coordonnees
coord = PointGeographique(48.856578, 2.351828, "WGS84")
print(coord)
coord.convertir_type_coordonnees()
print(coord)

coord2 = PointGeographique(651000, 6863000, "Lamb93")
print(coord2)
coord2.convertir_type_coordonnees()
print(coord2)
