from src.business_object.subdivision import Subdivision


class Departement(Subdivision):
    def __init__(self, ID_D, NOM_M, ANNEE, INSEE_DEP, INSEE_REG, Polygons):

        """
        Initialisation de la classe Departement

        Paramètres:
        -----------
        ID_D : str
            identifiant du département
        NOM_M : str
            nom du département
        ANNEE : int
            année que veut utiliser l'utilisateur pour sa recherche
        INSEE_DEP : str
            code INSEE du département
        INSEE_REG : str
            code INSEE de la région
        Polygons : dict
            contient les coordonnées des points du polygone entourant le
            département
        """

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        super.__init__(ID_D, NOM_M, ANNEE, Polygons)
        self.insee_dep = INSEE_DEP
        self.insee_reg = INSEE_REG
