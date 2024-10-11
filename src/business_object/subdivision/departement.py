class Departement:
    def __init__(self, ID_d, NOM_M, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Departement

        Paramètres:
        -----------
        ID_d : str
            identifiant du département
        NOM_M : str
            nom du département
        INSEE_DEP : str
            code INSEE du département
        INSEE_REG : str
            code INSEE de la région
        Polygons : dict
            contient les coordonnées des points du polygone entourant le
            département
        """

        if not isinstance(ID_d, str):
            raise TypeError("L'ID doit être un str")

        if not isinstance(NOM_M, str):
            raise TypeError("Le nom doit être un str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.ID_d = ID_d
        self.NOM_M = NOM_M
        self.INSEE_DEP = INSEE_DEP
        self.INSEE_REG = INSEE_REG
        self.Polygons = Polygons
