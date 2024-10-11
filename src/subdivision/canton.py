class Canton:
    def __init__(self, ID_ca, INSEE_CAN, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Canton

        Paramètres:
        -----------
        ID_ca : str
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

        if not isinstance(ID_ca, str):
            raise TypeError("L'ID doit être un str")

        if not isinstance(INSEE_CAN, str):
            raise TypeError("Le code INSEE du canton doit être un str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.ID_ca = ID_ca
        self.INSEE_CAN = INSEE_CAN
        self.INSEE_DEP = INSEE_DEP
        self.INSEE_REG = INSEE_REG
        self.Polygons = Polygons
