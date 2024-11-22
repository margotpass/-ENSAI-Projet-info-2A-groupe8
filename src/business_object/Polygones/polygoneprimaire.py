from src.business_object.pointgeographique import PointGeographique


class PolygonePrimaire:
    """ Polygone primaire caractérisé par ses points géographiques.

    paramètres:
    polygoneprimaire : List[PointGeographique]

    retourne:
    PolygonePrimaire
    """
    def __init__(self, polygoneprimaire=None):
        # Initialise la liste des points, vide si non fournie
        if polygoneprimaire is None:
            self.polygoneprimaire = []
        else:
            # Vérifie que tous les points fournis sont des instances de
            # PointGeographique
            if not all(
                isinstance(point, PointGeographique)
                for point in polygoneprimaire
            ):
                raise TypeError(
                    "Tous les points doivent être des instances de "
                    "PointGeographique"
                )
            self.polygoneprimaire = polygoneprimaire

    def __str__(self):
        """ str sert à afficher les informations du polygone primaire """
        return (
            "Polygone Primaire: ["
            + ", ".join(str(point) for point in self.polygoneprimaire)
            + "]"
        )

    def get_polygoneprimaire(self):
        """ Retourne le polygone primaire """
        return self.polygoneprimaire

    def ajouter_point(
        self, point
    ):
        """ Ajoute un point géographique au polygone """
        if isinstance(point, PointGeographique):
            self.polygoneprimaire.append(point)
        else:
            raise TypeError(
                "L'objet ajouté doit être une instance de PointGeographique"
            )
