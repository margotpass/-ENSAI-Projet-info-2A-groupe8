class Canton:
    def __init__(self, ID_CA, INSEE_CAN, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Canton

        Paramètres:
        -----------
        ID_CA : str
            identifiant du canton
        INSEE_CAN : str
            code INSEE du canton
        INSEE_DEP : str
            code INSEE du département associé
        INSEE_REG : str
            code INSEE de la région associée
        Polygons : dict
            contient les coordonnées des points du polygone entourant le
            canton
        """

        if not isinstance(ID_CA, str):
            raise TypeError("L'ID doit être un str")

        if not isinstance(INSEE_CAN, str):
            raise TypeError("Le code INSEE du canton doit être un str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.id_ca = ID_CA
        self.insee_can = INSEE_CAN
        self.insee_dep = INSEE_DEP
        self.insee_reg = INSEE_REG
        self.polygons = Polygons
