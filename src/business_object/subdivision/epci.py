class EPCI:
    def __init__(self, ID_e, SIREN, NOM, NATURE, Polygons):

        """
        Initialisation de la classe EPCI

        Paramètres:
        -----------
        ID_e : str
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

        if not isinstance(ID_e, str):
            raise TypeError("L'identifiant doit être un str")

        if not isinstance(SIREN, str):
            raise TypeError("Le code SIREN doit être un str")

        if not isinstance(NOM, str):
            raise TypeError("Le nom de l'EPCI doit être un str")

        if not isinstance(NATURE, str):
            raise TypeError("La nature de l'EPCI doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dict")

        self.ID_e = ID_e
        self.SIREN = SIREN
        self.NOM = NOM
        self.NATURE = NATURE
        self.Polygons = Polygons
