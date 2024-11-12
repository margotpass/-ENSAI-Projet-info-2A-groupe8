from src.business_object.Polygones.contour import Contour
from src.dao2.contourdao import ContourDAO
from src.dao.db_connection import DBConnection
from src.business_object.subdivisions.arrondissement import Arrondissement
from src.business_object.subdivisions.canton import Canton
from src.business_object.subdivisions.commune import Commune
from src.business_object.subdivisions.departement import Departement
from src.business_object.subdivisions.epci import Epci
from src.business_object.subdivisions.region import Region


class SubdivisionDAO:

    def __init__(self):
        """
        Initialisation de la classe SubdivisionDAO avec une instance de ContourDAO pour la gestion des contours.
        """
        self.contour_dao = ContourDAO()

    def creer_subdivision(self, type_subdivision, id, nom=None, annee=None,
                          insee_com=None, insee_can=None, insee_arr=None,
                          insee_dep=None, insee_reg=None, siren_epci=None,
                          polygones=Contour):
        """
        Crée une instance de subdivision en fonction de son type et de ses attributs.

        Paramètres:
        -----------
        type_subdivision : str
            Le type de subdivision ('Arrondissement', 'Canton', 'Commune', 'Departement', 'Epci', 'Region').
        id : str
            L'identifiant de la subdivision.
        nom : str, optionnel
            Le nom de la subdivision (si applicable).
        annee : str, optionnel
            L'année associée à la subdivision.
        insee_com, insee_can, insee_arr, insee_dep, insee_reg, siren_epci : str, optionnel
            Les identifiants spécifiques à chaque type de subdivision.
        polygones : Contour, optionnel
            Un objet Contour représentant le polygone de la subdivision.

        Retourne:
        --------
        Une instance de la subdivision correspondant au type donné, avec les attributs appropriés.
        """
        # Créer la subdivision en fonction de son type
        if type_subdivision.upper()== 'ARRONDISSEMENT':
            subdivision = Arrondissement(id=id, nom=nom, annee=annee, insee_arr=insee_arr,
                                         insee_dep=insee_dep, insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision.upper() == 'CANTON':
            subdivision = Canton(id=id, nom=nom, annee=annee, insee_can=insee_can,
                                 insee_dep=insee_dep, insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision.upper() == 'COMMUNE':
            subdivision = Commune(id=id, nom=nom, annee=annee, insee_com=insee_com,
                                   statut='', insee_can=insee_can, insee_arr=insee_arr,
                                   insee_dep=insee_dep, insee_reg=insee_reg,
                                   siren_epci=siren_epci, polygones=polygones)
        elif type_subdivision.upper() == 'DEPARTEMENT':
            subdivision = Departement(id=id, nom=nom, annee=annee, insee_dep=insee_dep,
                                      insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision.upper() == 'EPCI':
            subdivision = Epci(id=id, nom=nom, annee=annee, siren=siren_epci,
                               nature='', polygones=polygones)  # nature='' pour Epci
        elif type_subdivision == 'REGION':
            subdivision = Region(id=id, nom=nom, annee=annee, insee_reg=insee_reg,
                                 polygones=polygones)
        else:
            raise ValueError("Type de subdivision inconnu")

        return subdivision

    def ajouter_subdivision(self, subdivision):
        """
        Ajoute une subdivision et son polygone associé dans les tables 'subdivision', 'contours', et
        'subdivision_contour' en respectant les liens entre ces tables.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Insertion de la subdivision dans la table 'subdivision'
                query_subdivision = """
                INSERT INTO geodata.subdivision
                (id, type, nom, insee_com, insee_can, insee_arr, insee_dep, insee_reg, siren_epci)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_subdivision, (
                    subdivision.id,
                    subdivision.__class__.__name__,
                    getattr(subdivision, 'insee_com', None),
                    getattr(subdivision, 'insee_can', None),
                    getattr(subdivision, 'insee_arr', None),
                    getattr(subdivision, 'insee_dep', None),
                    getattr(subdivision, 'insee_reg', None),
                    getattr(subdivision, 'siren_epci', None)
                ))

                # Si un polygone est spécifié, l'ajouter dans la table 'contours' via ContourDAO
                if subdivision.polygones:
                    contour = subdivision.polygones  # polygones est un objet Contour
                    self.contour_dao.ajouter_contour(contour, subdivision.annee)  # Utilise ContourDAO pour ajouter le contour

                    # Ajout de l'association entre subdivision et contour dans la table 'subdivision_contour'
                    query_assoc = """
                    INSERT INTO geodata.subdivision_contour (id_subdivision, id_contour)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query_assoc, (subdivision.id, contour.id))

                # Commit des modifications dans la base de données
                connection.commit()

    def update_subdivision(self, subdivision):
        """
        Met à jour les informations d'une subdivision dans la base de données, y compris son contour associé.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Mise à jour de la subdivision dans la table 'subdivision'
                query_update_subdivision = """
                UPDATE geodata.subdivision
                SET nom = %s, insee_com = %s, insee_can = %s, insee_arr = %s,
                    insee_dep = %s, insee_reg = %s, siren_epci = %s
                WHERE id = %s AND type = %s
                """
                cursor.execute(query_update_subdivision, (
                    subdivision.nom,
                    getattr(subdivision, 'insee_com', None),
                    getattr(subdivision, 'insee_can', None),
                    getattr(subdivision, 'insee_arr', None),
                    getattr(subdivision, 'insee_dep', None),
                    getattr(subdivision, 'insee_reg', None),
                    getattr(subdivision, 'siren_epci', None),
                    subdivision.id,
                    subdivision.__class__.__name__
                ))
                # Mise à jour du contour si spécifié
                if subdivision.polygones:
                    contour = subdivision.polygones
                    self.contour_dao.update_contour(contour)  # Utilise ContourDAO pour mettre à jour le contour
                    query_assoc = """
                    UPDATE geodata.subdivision_contour
                    SET id_contour = %s
                    WHERE id_subdivision = %s
                    """
                    cursor.execute(query_assoc, (contour.id, subdivision.id))

                # Commit des modifications
                connection.commit()

    def delete_subdivision(self, subdivision_id, type_subdivision):
        """
        Supprime une subdivision et son contour associé de la base de données.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # Récupérer l'ID du contour associé pour le supprimer ensuite
                query_get_contour_id = """
                SELECT id_contour FROM geodata.subdivision_contour
                WHERE id_subdivision = %s
                """
                cursor.execute(query_get_contour_id, (subdivision_id,))
                contour_id = cursor.fetchone()

                # Supprimer l'association entre la subdivision et le contour
                query_delete_assoc = """
                DELETE FROM geodata.subdivision_contour
                WHERE id_subdivision = %s
                """
                cursor.execute(query_delete_assoc, (subdivision_id,))

                # Supprimer la subdivision
                query_delete_subdivision = """
                DELETE FROM geodata.subdivision
                WHERE id = %s AND type = %s
                """
                cursor.execute(query_delete_subdivision, (subdivision_id, type_subdivision))

                # Supprimer le contour en utilisant ContourDAO si un contour est associé
                if contour_id:
                    self.contour_dao.delete_contour(contour_id[0])

                # Commit des modifications
                connection.commit()

    def find_by_code_insee(self, type_subdivision, code_insee):
        """
        Récupère le nom d'une subdivision en fonction de son type et de son code INSEE.

        Paramètres:
        -----------
        type_subdivision : str
            Le type de subdivision (par exemple, 'COMMUNE', 'DEPARTEMENT', 'REGION', etc.)
        code_insee : str
            Le code INSEE de la subdivision à rechercher.

        Retourne:
        --------
        str
            Le nom de la subdivision, ou None si aucune subdivision n'est trouvée.
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

        # Requête pour récupérer le nom de la subdivision en fonction du type et du code INSEE
        query = f"""
        SELECT s.nom
        FROM geodata.subdivision s
        WHERE UPPER(s.type) = UPPER(%s) AND s.{insee_field} = %s
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (type_subdivision, code_insee))
                result = cursor.fetchone()

                # Retourner le nom de la subdivision ou None si non trouvé
                if result:
                    return result[0]
                else:
                    return None
