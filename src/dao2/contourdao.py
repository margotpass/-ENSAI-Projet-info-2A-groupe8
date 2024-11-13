from src.business_object.Polygones.contour import Contour
from src.dao2.connexedao import ConnexeDAO
from src.dao.db_connection import DBConnection
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.connexe import Connexe


class ContourDAO:
    def creer_contour(self, liste_connexes):
        """Crée un objet Contour à partir d'une liste de connexes."""
        #connexe_dao = ConnexeDAO()
        #connexes = [connexe_dao.creer_connexe(connexe) for connexe in liste_connexes]
        return Contour(liste_connexes)

    def ajouter_contour(self, contour, annee=2024, connection=DBConnection().connection):
        """Ajoute un Contour dans la base de données avec une année."""
        connexe_dao = ConnexeDAO()

        # Obtenez les ID des connexes associés
        connexes_ids = [connexe_dao.ajouter_connexe(connexe) for connexe in contour.contour]

        try:
            with connection.cursor() as cursor:
                # Insérer le Contour dans la table Contours avec l'année
                cursor.execute(
                    "INSERT INTO geodata.Contours (annee) VALUES (%s) RETURNING id",
                    (annee,)
                )
                contour_id = list(cursor.fetchall())[0]['id']  # Récupérer l'ID du contour inséré

                # Insérer les relations dans la table d'association contour_connexe
                for ordre, connexe_id in enumerate(connexes_ids):
                    # Vérifier si la relation existe déjà dans contour_connexe
                    cursor.execute(
                        "SELECT 1 FROM geodata.contour_connexe WHERE id_contour = %s AND id_connexe = %s",
                        (contour_id, connexe_id)
                    )
                    if cursor.fetchone() is None:  # Si la relation n'existe pas déjà
                        cursor.execute(
                            "INSERT INTO geodata.contour_connexe (id_contour, id_connexe, ordre) VALUES (%s, %s, %s)",
                            (contour_id, connexe_id, ordre)
                        )

                # Commit final après toutes les insertions
                connection.commit()

                # Retourner l'ID du Contour ajouté
                return contour_id

        except Exception as e:
            connection.rollback()
            print(f"Erreur lors de l'insertion dans contour_connexe : {e}")


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

    def get_all_contours(self, type_subdivision, annee=2024):
        """
        Récupère tous les contours associés aux subdivisions du type spécifié, filtrés par année.
        Chaque contour est retourné avec les connexes, les polygones associés et leurs points.

        Paramètres:
        -----------
        type_subdivision : str
            Le type de subdivision (par exemple, 'COMMUNE', 'DEPARTEMENT', 'REGION', etc.)
        annee : int, optional
            L'année des contours à récupérer. Par défaut, c'est 2024.

        Retourne:
        --------
        List[Tuple[Contour, str]]
            Une liste de tuples contenant un objet Contour et le code INSEE associé à la subdivision.
        """
        # Dictionnaire des champs INSEE associés aux types de subdivisions
        insee_fields = {
            'ARRONDISSEMENT': 'insee_arr',
            'CANTON': 'insee_can',
            'COMMUNE': 'insee_com',
            'DEPARTEMENT': 'insee_dep',
            'EPCI': 'siren_epci',
            'REGION': 'insee_reg'
        }

        # Normalisation du type de subdivision
        type_subdivision = type_subdivision.upper()

        if type_subdivision not in insee_fields:
            raise ValueError(f"Type de subdivision {type_subdivision} non reconnu")

        insee_field = insee_fields[type_subdivision]

        # Requête pour récupérer les subdivisions du type donné avec leur code INSEE
        query = f"""
        SELECT s.id, s.{insee_field} AS code_insee
        FROM geodata.subdivision s
        WHERE UPPER(s.type) = UPPER(%s)
        """

        contours_with_codes = []

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (type_subdivision,))
                subdivisions = cursor.fetchall()

                # Pour chaque subdivision, récupérer ses contours associés
                for subdivision_id, code_insee in subdivisions:
                    # Requête pour récupérer les contours associés à cette subdivision pour l'année spécifiée
                    contours_query = """
                    SELECT contour.id
                    FROM geodata.subdivision_contour sc
                    JOIN geodata.contour contour ON sc.id_contour = contour.id
                    WHERE sc.id_subdivision = %s
                    AND contour.annee = %s
                    """
                    cursor.execute(contours_query, (subdivision_id, annee))
                    contours = cursor.fetchall()

                    # Pour chaque contour, récupérer les connexes associés
                    for contour_row in contours:
                        contour_id = contour_row[0]

                        # Requête pour récupérer les connexes associés à ce contour via contour_connexe
                        connexes_query = """
                        SELECT cc.id_connexe
                        FROM geodata.contour_connexe cc
                        WHERE cc.id_contour = %s
                        """
                        cursor.execute(connexes_query, (contour_id,))
                        connexes = cursor.fetchall()

                        # Pour chaque connexe, récupérer les polygones associés à ce connexe
                        connexes_list = []
                        for connexe_row in connexes:
                            connexe_id = connexe_row[0]

                            # Requête pour récupérer les polygones associés à ce connexe
                            polygones_query = """
                            SELECT cp.id_polygone
                            FROM geodata.connexe_polygone cp
                            WHERE cp.id_connexe = %s
                            """
                            cursor.execute(polygones_query, (connexe_id,))
                            polygones = cursor.fetchall()

                            # Pour chaque polygone, récupérer les points associés
                            polygons_with_points = []
                            for polygone_row in polygones:
                                polygone_id = polygone_row[0]

                                # Récupérer les points associés à ce polygone
                                points_query = """
                                SELECT p.lat, p.long
                                FROM geodata.polygone_point pp
                                JOIN geodata.points p ON pp.id_point = p.id
                                WHERE pp.id_polygone = %s
                                ORDER BY pp.ordre
                                """
                                cursor.execute(points_query, (polygone_id,))
                                points = cursor.fetchall()

                                # Convertir les points en une liste d'objets PointGeographique
                                points_list = [PointGeographique(lat, long) for lat, long in points]

                                # Ajouter un PolygonePrimaire contenant ces points
                                polygons_with_points.append(PolygonePrimaire(points_list))

                            # Ajouter ce connexe avec sa liste de PolygonePrimaire
                            connexes_list.append(Connexe(polygons_with_points))

                        # Créer l'objet Contour avec les connexes associés
                        contour = self.creer_contour(connexes_list)

                        # Ajouter le tuple (Contour, code_insee) à la liste des résultats
                        contours_with_codes.append((contour, code_insee))

        return contours_with_codes
