import pyproj


class PointGeographique():
    """ Point géographique caractérisé par ses coordonnées géographiques.

    Paramètres:
    latitude -- latitude du point (float)
    longitude -- longitude du point (float)
    typecoordonnees -- type de coordonnées (str) : soit Lamb93 soit WGS84
    """

    def __init__(self, latitude, longitude,
                 typecoordonnees="WGS84"):
        """Initialisation des coordonnées géographiques du point

        Paramètres:
        latitude (float):
            latitude du point géographique
        longitude (float): longitude du point géographique
        typecoordonnees (str, optional):
            type de coordonnées renseignées parmi "Lamb93" ou "WGS84"
            Défaut à "WGS84".

        Raises:
            TypeError: latitude ou longitude n'est pas un float ou un int
            ValueError: type de coordonnées n'est pas "Lamb93", "WGS84", "",
            None, "None", "lamb93" ou "wgs84"

        Retourne:
            _type_: _description_
        """
        if not isinstance(latitude, (int, float)):
            raise TypeError("La latitude doit être un nombre")
        self.latitude = latitude
        if not isinstance(longitude, (int, float)):
            raise TypeError("La longitude doit être un nombre")
        self.longitude = longitude
        # les coordonnées sont soit en Lambert 93 soit en WGS84 soit vide
        if typecoordonnees not in (
            "Lamb93", "WGS84", "", None, "None", "lamb93", "wgs84"
        ):
            raise ValueError(
                "Type de coordonnées non reconnu"
            )
        self.typecoordonnees = typecoordonnees

    def __str__(self):
        """Affiche les informations du point géographique"""
        return (
            "Latitude: " + str(self.latitude) +
            " Longitude: " + str(self.longitude) +
            " Type de coordonnées: " + str(self.typecoordonnees)
        )

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
        if (
            self.typecoordonnees == "Lamb93" or
            self.typecoordonnees == "lamb93"
        ):
            # Lambert 93 projection
            lambert = pyproj.CRS.from_epsg(2154)
            # WGS84 est notre référentiel géographique
            wgs84 = pyproj.CRS.from_epsg(4326)
            # Initialisation du transformeur avec un ordre de coordonnées
            # (latitude, longitude)
            transformer = pyproj.Transformer.from_crs(
                lambert, wgs84, always_xy=True
            )

            # Transformer longitude, latitude en WGS84
            self.longitude, self.latitude = transformer.transform(
                self.longitude, self.latitude
            )
            self.typecoordonnees = "WGS84"
            # Vérificiation de la transformation
            print("Transformation réussie: Latitude =", self.latitude)
            print("Longitude =", self.longitude)

        elif self.typecoordonnees == "WGS84":
            print("Les coordonnées sont déjà en WGS84")
        else:
            print("Type de coordonnées non reconnu")
