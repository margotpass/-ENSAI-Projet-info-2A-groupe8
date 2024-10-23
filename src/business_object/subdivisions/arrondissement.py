from src.business_object.subdivision import Subdivision


class Arrondissement(Subdivision):
    def __init__(self, ID_A, NOM_M, ANNEE, INSEE_ARR, INSEE_DEP,
                 INSEE_REG, Polygons):

        """
        Initialisation de la classe Arrondissement

        Paramètres:
        -----------
        ID_A : str
            identifiant de l'arrondissement
        NOM_M : str
            nom de l'arrondissement
        ANNEE : int
            année que veut utiliser l'utilisateur pour sa recherche
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

        if not isinstance(INSEE_ARR, str):
            raise TypeError("Le code INSEE de l'arrondissement doit être un"
                            " str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        super().__init__(ID_A, NOM_M, ANNEE, Polygons)
        self.insee_arr = INSEE_ARR
        self.insee_dep = INSEE_DEP
        self.insee_reg = INSEE_REG
