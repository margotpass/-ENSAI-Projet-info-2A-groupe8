from src.business_object.subdivision import Subdivision


class Commune(Subdivision):
    def __init__(self, ID_CO, NOM_M, ANNEE, INSEE_COM, STATUT, INSEE_CAN,
                 INSEE_ARR, INSEE_DEP, INSEE_REG, SIREN_EPCI, Polygons):

        """
        Initialise la classe Commune.

        Paramètres:
        -----------
        ID_CO : str
            identifiant de la commune
        NOM_M : str
            nom de la commune
        ANNEE : int
            année que veut utiliser l'utilisateur pour sa recherche
        INSEE_COM : str
            numéro INSEE de la commune
        STATUT : str
            statut de la commune
        INSEE_CAN : str
            numéro INSEE du canton associé
        INSEE_ARR : str
            numéro INSEE de l'arrondissement associé
        INSEE_DEP : str
            numéro INSEE du département associé
        INSEE_REG : str
            numéro INSEE de la région associée
        SIREN_EPCI : str
            numéro SIREN de l'EPCI associée
        Polygons : dict
            contient les coordonnées des points du polygone entourant la
            commune
        """

        if not isinstance(INSEE_COM, str):
            raise TypeError("Le code INSEE de la commune doit être un str")

        if not isinstance(STATUT, str):
            raise TypeError("Le statut doit être un str")

        if not isinstance(INSEE_CAN, str):
            raise TypeError("Le code INSEE du canton doit être un str")

        if not isinstance(INSEE_ARR, str):
            raise TypeError("Le code INSEE de l'arrondissement doit être un"
                            " str")

        if not isinstance(INSEE_DEP, str):
            raise TypeError("Le code INSEE du département doit être un str")

        if not isinstance(INSEE_REG, str):
            raise TypeError("Le code INSEE de la région doit être un str")

        if not isinstance(SIREN_EPCI, str):
            raise TypeError("Le code SIREN doit être un str")

        super.__init__(ID_CO, NOM_M, ANNEE, Polygons)
        self.insee_com = INSEE_COM
        self.statut = STATUT
        self.insee_can = INSEE_CAN
        self.insee_arr = INSEE_ARR
        self.insee_dep = INSEE_DEP
        self.insee_reg = INSEE_REG
        self.siren_epci = SIREN_EPCI
