from src.business_object.Polygones.contour import Contour
from src.dao2.contourdao import ContourDAO
from src.dao.db_connection import DBConnection


class SubdivisionDAO:
    def creer_subdivision(self, nom, code, liste_contours):
        """Crée un objet Subdivision avec une liste de contours associés."""
        contour_dao = ContourDAO()
        contours = [contour_dao.creer_contour(contour) for contour in liste_contours]
        return Subdivision(nom, code, contours)

    def ajouter_subdivision(self, subdivision):
        """Ajoute une Subdivision dans la base de données avec ses contours."""
        contour_dao = ContourDAO()
        contours_ids = [contour_dao.ajouter_contour(contour) for contour in subdivision.contours]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO geodata.Subdivisions (nom, code, contours)
                    VALUES (%s, %s, %s) RETURNING id
                    """,
                    (subdivision.nom, subdivision.code, contours_ids)
                )
                subdivision.id = cursor.fetchone()[0]
                return subdivision.id
