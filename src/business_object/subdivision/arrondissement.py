class Arrondissement:
    def __init__(self, ID_a, NOM_M, INSEE_ARR, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Arrondissement

        Paramètres:
        -----------
        ID_a : str
            identifiant de l'arrondissement
        NOM_M : str
            nom de l'arrondissement
        INSEE_ARR : str
            code INSEE de l'arrondissement
        INSEE_DEP : str
            code INSEE du département associé
        INSEE_REG : str
            code INSEE de la région associée
        Polygons : dict
            contient les coordonnées des points du polygone entourant l'
            arrondissement
        """

        if not isinstance(ID_a, str):
            raise TypeError("L'ID doit être un str")

        if not isinstance(NOM_M, str):
            raise TypeError("Le nom de l'arrondissement doit être un str")

        if not isinstance(INSEE_ARR, str):
            raise TypeError("Le code INSEE de l'arrondissement doit être un"
                            " str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.ID_a = ID_a
        self.NOM_M = NOM_M
        self.INSEE_ARR = INSEE_ARR
        self.INSEE_DEP = INSEE_DEP
        self.INSEE_REG = INSEE_REG
        self.Polygons = Polygons
