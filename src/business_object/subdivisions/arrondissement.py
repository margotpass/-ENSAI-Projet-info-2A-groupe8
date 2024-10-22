class Arrondissement:
    def __init__(self, ID_A, NOM_M, INSEE_ARR, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Arrondissement

        Paramètres:
        -----------
        ID_A : str
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

        if not isinstance(ID_A, str):
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

        self.id_a = ID_A
        self.nom_m = NOM_M
        self.insee_arr = INSEE_ARR
        self.insee_dep = INSEE_DEP
        self.insee_reg = INSEE_REG
        self.polygons = Polygons
