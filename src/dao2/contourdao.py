from src.business_object.Polygones.contour import Contour
from src.dao2.connexedao import ConnexeDAO
from src.dao.db_connection import DBConnection


class ContourDAO:
    def creer_contour(self, liste_connexes):
        """Crée un objet Contour à partir d'une liste de connexes."""
        connexe_dao = ConnexeDAO()
        connexes = [connexe_dao.creer_connexe(connexe) for connexe in liste_connexes]
        return Contour(connexes)

    def ajouter_contour(self, contour):
        """Ajoute un Contour dans la base de données."""
        connexe_dao = ConnexeDAO()
        connexes_ids = [connexe_dao.ajouter_connexe(connexe) for connexe in contour.connexes]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO geodata.Contours (connexes) VALUES (%s) RETURNING id",
                    (connexes_ids,)
                )
                contour.id = cursor.fetchone()[0]
                return contour.id
