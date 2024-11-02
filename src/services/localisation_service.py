from typing import Optional
from src.business_object.subdivision import Subdivision
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.contour import Contour
from src.dao.contourdao import ContourDAO
from src.dao.subdivisiondao import SubdivisionDAO


class LocalisationService:

    def __init__(self, subdivision_dao, contour_dao):
            self.subdivision_dao = subdivision_dao
            self.contour_dao = contour_dao

    def localiserPointDansSubdivision(self, code_insee, point: PointGeographique, annee: int = 2024) -> Optional[Subdivision]:
        # Étape 1 : Récupérer la table du type de subdivision correspondante au code insee
        type_subdivision_liste = ["Arrondissement", "Canton", "Commune",  "Departement", "EPCI", "Region"]
        subdivisions = None

        for type_subdivision in type_subdivision_liste:
            try:
                subdivisions = self.subdivision_dao.find_by_code_insee(type_subdivision, code_insee)
                if subdivisions:  # Vérifier si des subdivisions ont été trouvées
                    break
            except:
                continue

        # Vérifiez si aucune subdivision n'a été trouvée
        if not subdivisions:
            return None

        # Étape 2 : Parcourir les subdivisions du type de subdivision trouvé pour récupérer les contours
        for subdivision in subdivisions:
            contours = self.contour_dao.get_all_contours(subdivision)

           # Etape 3 : vérifier si le point est dans un des contours
            for contour in contours :
                if contour.estDansPolygone(point):
                    return subdivision  # Retourner la subdivision si le point y appartient

        # Si aucun contour ne contient le point, retourner None
        return None



