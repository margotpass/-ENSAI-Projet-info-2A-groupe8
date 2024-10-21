class Epci:
    def __init__(self, ID_E, SIREN, NOM, NATURE, Polygons):

        """
        Initialisation de la classe EPCI

        Paramètres:
        -----------
        ID_E : str
            identifiant de l'EPCI
        NOM : str
            nom de l'EPCI
        SIREN : str
            code SIREN de l'EPCI
        NATURE : str
            nature de l'EPCI
        Polygons : dict
            contient les coordonnées des points du polygone entourant l'
            EPCI
        """

        if not isinstance(ID_E, str):
            raise TypeError("L'identifiant doit être un str")

        if not isinstance(SIREN, str):
            raise TypeError("Le code SIREN doit être un str")

        if not isinstance(NOM, str):
            raise TypeError("Le nom de l'EPCI doit être un str")

        if not isinstance(NATURE, str):
            raise TypeError("La nature de l'EPCI doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dict")

        self.id_e = ID_E
        self.siren = SIREN
        self.nom = NOM
        self.nature = NATURE
        self.polygons = Polygons
