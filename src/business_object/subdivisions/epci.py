from src.business_object.subdivision import Subdivision


class Epci(Subdivision):
    def __init__(self, ID_E, ANNEE, SIREN, NOM, NATURE, Polygons):

        """
        Initialisation de la classe EPCI

        Paramètres:
        -----------
        ID_E : str
            identifiant de l'EPCI
        ANNEE : int
            année que veut utiliser l'utilisateur pour sa recherche
        NOM : str
            nom de l'EPCI
        SIREN : str
            code SIREN de l'EPCI
        NATURE : str
            nature de l'EPCI
        Polygons : dict
            contient les coordonnées des points du polygone entourant l'
            EPCI
        """

        if not isinstance(SIREN, str):
            raise TypeError("Le code SIREN doit être un str")

        if not isinstance(NATURE, str):
            raise TypeError("La nature de l'EPCI doit être un str")

        super.__init__(ID_E, NOM, ANNEE, Polygons)
        self.siren = SIREN
        self.nature = NATURE
