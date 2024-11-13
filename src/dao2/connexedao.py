from src.business_object.Polygones.connexe import Connexe
from src.dao2.polygonedao import PolygoneDAO
from src.dao.db_connection import DBConnection


class ConnexeDAO:
    def creer_connexe(self, liste_polygones):
        """Crée un objet Connexe à partir d'une liste de polygones."""
        #polygone_dao = PolygoneDAO()
        #polygones = [polygone_dao.creer_polygone(poly) for poly in liste_polygones]
        return Connexe(liste_polygones)

    def ajouter_connexe(self, connexe, connection=DBConnection().connection):
        """Ajoute un Connexe dans la base de données avec ses polygones et la somme de contrôle totale."""
        polygone_dao = PolygoneDAO()

        # Calcul de la somme des sommes de contrôle des polygones
        somme_sommes_controle = 0
        polygones_ids = []
        for poly in connexe.connexe:
            # Ajout du polygone dans la base de données et récupération de son ID
            polygone_id = polygone_dao.ajouter_polygone(poly)
            polygones_ids.append(polygone_id)

            # Récupérer la somme de contrôle depuis la table Polygones pour le polygone ajouté

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT somme_coordonnees FROM geodata.Polygones WHERE id = %s",
                    (polygone_id,)
                )
                somme_coordonnees = list(cursor.fetchall())[0]['somme_coordonnees']
                #print(f"sommecoordonneesm: {somme_coordonnees}")
                somme_sommes_controle += somme_coordonnees

        with connection.cursor() as cursor:
            # Insérer le Connexe dans la table Connexes avec la somme totale des sommes de contrôle
            cursor.execute(
                "INSERT INTO geodata.Connexes (somme_sommes_controle) VALUES (%s) RETURNING id",
                (somme_sommes_controle,)
            )
            connexe_id = list(cursor.fetchall())[0]['id']

            # Insérer les relations dans la table d'association connexe_polygone avec l'ordre des polygones
            for ordre, polygone_id in enumerate(polygones_ids, start=1):
                cursor.execute(
                    "INSERT INTO geodata.connexe_polygone (id_connexe, id_polygone, ordre) VALUES (%s, %s, %s)",
                    (connexe_id, polygone_id, ordre)
                )
            connection.commit()
            # Retourner l'ID du Connexe ajouté
            return connexe_id

    def update_connexe(self, connexe_id, nouvelle_liste_polygones):
        """Met à jour un Connexe existant en remplaçant ses polygones par une nouvelle liste."""
        polygone_dao = PolygoneDAO()
        nouveaux_polygones_ids = []
        somme_sommes_controle = 0

        # Ajouter les nouveaux polygones et calculer la somme des sommes de contrôle
        for poly in nouvelle_liste_polygones:
            polygone_id = polygone_dao.ajouter_polygone(poly)
            nouveaux_polygones_ids.append(polygone_id)
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
                # Mettre à jour la somme des sommes de contrôle dans la table Connexes
                cursor.execute(
                    "UPDATE geodata.Connexes SET somme_sommes_controle = %s WHERE id = %s",
                    (somme_sommes_controle, connexe_id)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Le connexe avec l'id {connexe_id} n'existe pas.")

                # Supprimer les anciennes associations entre connexe et polygones
                cursor.execute(
                    "DELETE FROM geodata.connexe_polygone WHERE id_connexe = %s",
                    (connexe_id,)
                )

                # Ajouter les nouvelles associations dans la table connexe_polygone
                for ordre, polygone_id in enumerate(nouveaux_polygones_ids, start=1):
                    cursor.execute(
                        "INSERT INTO geodata.connexe_polygone (id_connexe, id_polygone, ordre) VALUES (%s, %s, %s)",
                        (connexe_id, polygone_id, ordre)
                    )

                # Commit des modifications
                connection.commit()

    def delete_connexe(self, connexe_id):
        """Supprime un Connexe de la base de données, y compris ses polygones associés et ses associations."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Supprimer les associations dans la table connexe_polygone
                cursor.execute(
                    "DELETE FROM geodata.connexe_polygone WHERE id_connexe = %s",
                    (connexe_id,)
                )

                # Supprimer le connexe lui-même dans la table Connexes
                cursor.execute(
                    "DELETE FROM geodata.Connexes WHERE id = %s",
                    (connexe_id,)
                )

                if cursor.rowcount == 0:
                    raise ValueError(f"Le connexe avec l'id {connexe_id} n'existe pas.")

                # Commit des modifications
                connection.commit()
