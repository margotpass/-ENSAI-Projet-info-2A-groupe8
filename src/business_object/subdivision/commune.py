class Commune:
    def __init__(self, ID_co, NOM_M, INSEE_COM, STATUT, INSEE_CAN, INSEE_ARR,
                 INSEE_DEP, INSEE_REG, SIREN_EPCI, Polygons):

        """
        Initialise la classe Commune.

        Paramètres:
        -----------
        ID_co : str
            identifiant de la commune
        NOM_M : str
            nom de la commune
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

        if not isinstance(ID_co, str):
            raise TypeError("L'ID doit être un str")

        if not isinstance(NOM_M, str):
            raise TypeError("Le nom doit être un str")

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

        if not isinstance(Polygons, dict):
            raise TypeError("L'attribut Polygons doit être un dictionnaire")

        self.ID_co = ID_co
        self.NOM_M = NOM_M
        self.INSEE_COM = INSEE_COM
        self.STATUT = STATUT
        self.INSEE_CAN = INSEE_CAN
        self.INSEE_ARR = INSEE_ARR
        self.INSEE_DEP = INSEE_DEP
        self.INSEE_REG = INSEE_REG
        self.SIREN_EPCI = SIREN_EPCI
        self.Polygons = Polygons
