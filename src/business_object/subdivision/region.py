class Region:
    def __init__(self, ID_r, NOM_M, INSEE_REG, Polygons):

        """
        Initialisation de la classe Region

        Paramètres:
        -----------
        ID_r : str
            identifiant de la région
        NOM_M : str
            nom de la région
        INSEE_REG : str
            code INSEE de la région
        Polygons : dict
            contient les coordonnées des points du polygone entourant la
            région
        """

        if not isinstance(ID_r, str):
            raise TypeError("L'identifiant doit être un str")

        if not isinstance(NOM_M, str):
            raise TypeError("Le nom de la région doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.ID_r = ID_r
        self.NOM_M = NOM_M
        self.INSEE_REG = INSEE_REG
        self.Polygons = Polygons
