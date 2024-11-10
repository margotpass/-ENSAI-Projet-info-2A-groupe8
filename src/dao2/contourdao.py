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

        # Obtenez les ID des connexes associés
        connexes_ids = [connexe_dao.ajouter_connexe(connexe) for connexe in contour.contour]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Insérer le Contour dans la table Contours avec l'année
                cursor.execute(
                    "INSERT INTO geodata.Contours (annee) VALUES (%s) RETURNING id",
                    (annee,)
                )
                contour_id = cursor.fetchone()[0]  # L'ID du contour inséré

                # Insérer les relations dans la table d'association contour_connexe
                for ordre, connexe_id in enumerate(connexes_ids):
                    cursor.execute(
                        "INSERT INTO geodata.contour_connexe (id_contour, id_connexe, ordre) VALUES (%s, %s, %s)",
                        (contour_id, connexe_id, ordre)
                    )

                # Retourner l'ID du Contour ajouté
                return contour_id

    def update_contour(self, contour_id, nouvelle_liste_connexes, nouvelle_annee):
        """Met à jour un Contour existant en remplaçant ses connexes et en modifiant son année si nécessaire."""
        connexe_dao = ConnexeDAO()
        nouveaux_connexes_ids = [connexe_dao.ajouter_connexe(connexe) for connexe in nouvelle_liste_connexes]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Mettre à jour l'année du Contour dans la table Contours
                cursor.execute(
                    "UPDATE geodata.Contours SET annee = %s WHERE id = %s",
                    (nouvelle_annee, contour_id)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Le contour avec l'id {contour_id} n'existe pas.")

                # Supprimer les anciennes associations dans la table contour_connexe
                cursor.execute(
                    "DELETE FROM geodata.contour_connexe WHERE id_contour = %s",
                    (contour_id,)
                )

                # Ajouter les nouvelles associations avec la liste mise à jour de connexes
                for ordre, connexe_id in enumerate(nouveaux_connexes_ids, start=1):
                    cursor.execute(
                        "INSERT INTO geodata.contour_connexe (id_contour, id_connexe, ordre) VALUES (%s, %s, %s)",
                        (contour_id, connexe_id, ordre)
                    )

                # Commit des modifications
                connection.commit()

    def delete_contour(self, contour_id):
        """Supprime un Contour de la base de données, y compris ses connexes associés et ses relations."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Supprimer les associations dans la table contour_connexe
                cursor.execute(
                    "DELETE FROM geodata.contour_connexe WHERE id_contour = %s",
                    (contour_id,)
                )

                # Supprimer le contour lui-même dans la table Contours
                cursor.execute(
                    "DELETE FROM geodata.Contours WHERE id = %s",
                    (contour_id,)
                )

                if cursor.rowcount == 0:
                    raise ValueError(f"Le contour avec l'id {contour_id} n'existe pas.")

                # Commit des modifications
                connection.commit()
