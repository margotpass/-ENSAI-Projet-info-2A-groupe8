from typing import Optional
from src.business_object.subdivision import Subdivision
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.contour import Contour
from src.dao.contourdao import ContourDAO
from src.dao.subdivisiondao import SubdivisionDAO
from src.dao.db_connection import DBConnection
from src.services.subdivision_service import SubdivisionService


class LocalisationService:

    def __init__(self):
            self.subdivision_dao = SubdivisionDAO()
            self.contour_dao = ContourDAO(DBConnection)

    def localiserPointDansSubdivision(self, point: PointGeographique, type_subdivision, annee: int = 2024):
        """Localise un point dans une subdivision

        Args:
            point (PointGeographique): instance de PointGeographique
            type_subdivision (_type_): str parmi Arrondissement, Canton, Commune, Departement, EPCI et Region
            annee (int, optional): année souhaitée de la recherche. Défaut à 2024.

        Returns:
            contour[1]: numéro de la subdivision
            nom_subdivision: nom de la subdivision
        """

        # Étape 1 : Récupérer la table (contours, nom de la subdivision) associés au type de subdivision entré
        table_contours = self.contour_dao.get_all_contours(type_subdivision.lower())
            
        # Etape 2 : Parcourir la table (contours, nom de la subdivision)
        for contour in table_contours :
            # Regarder si le point est dans le contour de la table
            if contour[0].estDansPolygone(point):
                nom_subdivision = SubdivisionService().chercherSubdivisionParID(type_subdivision, contour[1], annee)
                return contour[1], nom_subdivision  # Retourner n° et le nom de la subdivision dans la table si le point est dans le contour

        # Si aucun contour ne contient le point, retourner None
        return None
