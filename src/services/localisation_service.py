from typing import Optional
from business_object.subdivision.subdivision import Subdivision
from business_object.point_geographique import PointGeographique
from business_object.contour import Contour
from dao.contour_dao import ContourDAO
from dao.subdivision_dao import SubdivisionDAO


class LocalisationService:

    def __init__(self, subdivision_dao, contour_dao):
            self.subdivision_dao = SubdivisionDAO()
            self.contour_dao = ContourDAO()

    def localiserPointDansSubdivision(self, code_insee, point: PointGeographique, annee: int = 2024) -> Optional[Subdivision]:
        # Étape 1 : Récupérer toutes les subdivisions
        subdivisions = self.subdivision_dao.find_by_code_insee()
 
        # Étape 2 : Parcourir chaque subdivision pour vérifier si le point est dans ses polygones
        for subdivision in subdivisions:
            contour = subdivision.polygones  # Accéder directement à l'attribut polygones

            # Vérifier si le point est dans l'un des polygones de cette subdivision
            if contour.estDansPolygone(point):
                return subdivision  # Retourner la subdivision si le point y appartient

        # Si aucun polygone ne contient le point, retourner None
        return None

    def __str__(self):
        print(f"Le point de coordonnées {self.point} est dans la subdivision {subdivision}")

