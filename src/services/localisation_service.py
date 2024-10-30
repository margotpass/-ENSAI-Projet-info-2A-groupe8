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
        # Étape 1 : Récupérer la table du type de subdivision correspondante au code insee
        type_subdivision_liste = ["Arrondissement", "Canton", "Commune",  "Departement", "EPCI", "Region"]

        for type_subdivision in type_subdivision_liste:
            try:
                subdivisions = self.subdivision_dao.find_by_code_insee(type_subdivision, code_insee)
                break
            except:
                continue
 
        # Étape 2 : Parcourir les subdivisions du type de subdivision trouvé pour récupérer les contours
        for subdivision in subdivisions:
            contours = self.contour_dao.getAllContours(subdivision)

           # Etape 3 : vérifier si le point est dans un des contours
            for contour in contours :
                if contour.estDansPolygone(point):
                    return subdivision  # Retourner la subdivision si le point y appartient

        # Si aucun contour ne contient le point, retourner None
        return None

    def __str__(self):
        print(f"Le point de coordonnées {self.point} est dans la subdivision {subdivision}")

