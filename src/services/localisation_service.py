from typing import Optional
from business_object.subdivision.subdivision import Subdivision
from business_object.point_geographique import PointGeographique
from dao.subdivision_dao import SubdivisionDAO

class LocalisationService:

    def __init__(self):
        self.subdivision_dao = SubdivisionDAO()

    def localiserPointDansSubdivision(self, point: PointGeographique, annee: int = 2024) -> Optional[Subdivision]:
        # Étape 1 : Récupérer toutes les subdivisions
        subdivisions = self.subdivision_dao.find_all()  # Assure-toi d'avoir une méthode pour récupérer toutes les subdivisions

        # Étape 2 : Parcourir chaque subdivision pour vérifier si le point est dans ses polygones
        for subdivision in subdivisions:
            contour = subdivision.polygones  # Accéder directement à l'attribut polygones

            # Vérifier si le point est dans l'un des polygones de cette subdivision
            if contour.est_dans_polygone(point):
                return subdivision  # Retourner la subdivision si le point y appartient

        # Si aucun polygone ne contient le point, retourner None
        return None
