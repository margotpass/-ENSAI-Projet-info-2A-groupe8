from typing import Optional
from src.business_object.subdivision import Subdivision
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.contour import Contour
from src.dao.contourdao import ContourDAO
from src.dao.subdivisiondao import SubdivisionDAO
from src.dao.db_connection import DBConnection



class LocalisationService:

    def __init__(self):
            self.subdivision_dao = SubdivisionDAO()
            self.contour_dao = ContourDAO(DBConnection)

    def localiserPointDansSubdivision(self, point: PointGeographique, type_subdivision, annee: int = 2024):
        """# Étape 1 : Récupérer la table du type de subdivision entré
        table_subdivisions = None

        try:
            table_subdivisions = self.subdivision_dao.find_by_code_insee(type_subdivision, code_insee = "02")
        except:
            return None"""

        # Étape 1 : Récupérer la table (contours, nom de la subdivision) associés au type de subdivision entré
        table_contours = self.contour_dao.get_all_contours(type_subdivision.lower())
            
        # Etape 2 : Parcourir la table (contours, nom de la subdivision)
        for contour in table_contours :
            # Regarder si le point est dans le contour de la table
            if contour[0].estDansPolygone(point):
                return contour[1]  # Retourner nom de la subdivision dans la table si le point est dans le contour

        # Si aucun contour ne contient le point, retourner None
        return None
            
            
 
    """
    def localiserPointDansSubdivisionByCodeInsee(self, code_insee, point: PointGeographique, annee: int = 2024) -> Optional[Subdivision]:
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
"""


