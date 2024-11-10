from src.business_object.Polygones.contour import Contour
from src.dao2.connexedao import ConnexeDAO
from src.dao.db_connection import DBConnection


class ContourDAO:
    def creer_contour(self, liste_connexes):
        """Crée un objet Contour à partir d'une liste de connexes."""
        connexe_dao = ConnexeDAO()
        connexes = [connexe_dao.creer_connexe(connexe) for connexe in liste_connexes]
        return Contour(connexes)

    def ajouter_contour(self, contour, annee):
        """Ajoute un Contour dans la base de données avec une année."""
        connexe_dao = ConnexeDAO()
        connexes_ids = [connexe_dao.ajouter_connexe(connexe) for connexe in contour.connexes]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Insérer le Contour dans la table Contours avec l'année
                cursor.execute(
                    "INSERT INTO geodata.Contours (annee) VALUES (%s) RETURNING id",
                    (annee,)
                )
                contour_id = cursor.fetchone()[0]  # L'ID du contour inséré

                # Insérer les relations dans la table d'association contour_connexe
                for connexe_id in connexes_ids:
                    cursor.execute(
                        "INSERT INTO geodata.contour_connexe (id_contour, id_connexe) VALUES (%s, %s)",
                        (contour_id, connexe_id)
                    )

                # Retourner l'ID du Contour ajouté
                return contour_id
