from src.business_object.subdivision import Subdivision


class Region(Subdivision):
    def __init__(self, ID_R, NOM_M, ANNEE, INSEE_REG, Polygons):

        """
        Initialisation de la classe Region

        Paramètres:
        -----------
        ID_R : str
            identifiant de la région
        NOM_M : str
            nom de la région
        ANNEE : int
            année que veut utiliser l'utilisateur pour sa recherche
        INSEE_REG : str
            code INSEE de la région
        Polygons : dict
            contient les coordonnées des points du polygone entourant la
            région
        """

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        super.__init__(ID_R, NOM_M, ANNEE, Polygons)
        self.insee_reg = INSEE_REG
