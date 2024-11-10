from src.business_object.Polygones.connexe import Connexe
from src.dao2.polygonedao import PolygoneDAO
from src.dao.db_connection import DBConnection


class ConnexeDAO:
    def creer_connexe(self, liste_polygones):
        """Crée un objet Connexe à partir d'une liste de polygones."""
        polygone_dao = PolygoneDAO()
        polygones = [polygone_dao.creer_polygone(poly) for poly in liste_polygones]
        return Connexe(polygones)

    def ajouter_connexe(self, connexe):
        """Ajoute un Connexe dans la base de données avec ses polygones et la somme de contrôle totale."""
        polygone_dao = PolygoneDAO()

        # Calcul de la somme des sommes de contrôle des polygones
        somme_sommes_controle = 0
        polygones_ids = []
        for poly in connexe.polygones:
            # Ajout du polygone dans la base de données et récupération de son ID
            polygone_id = polygone_dao.ajouter_polygone(poly)
            polygones_ids.append(polygone_id)

            # Récupérer la somme de contrôle depuis la table Polygones pour le polygone ajouté
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT somme_coordonnees FROM geodata.Polygones WHERE id = %s",
                        (polygone_id,)
                    )
                    somme_coordonnees = cursor.fetchone()[0]
                    somme_sommes_controle += somme_coordonnees

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Insérer le Connexe dans la table Connexes avec la somme totale des sommes de contrôle
                cursor.execute(
                    "INSERT INTO geodata.Connexes (somme_sommes_controle) VALUES (%s) RETURNING id",
                    (somme_sommes_controle,)
                )
                connexe_id = cursor.fetchone()[0]

                # Insérer les relations dans la table d'association connexe_polygone avec l'ordre des polygones
                for ordre, polygone_id in enumerate(polygones_ids, start=1):
                    cursor.execute(
                        "INSERT INTO geodata.connexe_polygone (id_connexe, id_polygone, ordre) VALUES (%s, %s, %s)",
                        (connexe_id, polygone_id, ordre)
                    )

                # Retourner l'ID du Connexe ajouté
                return connexe_id
