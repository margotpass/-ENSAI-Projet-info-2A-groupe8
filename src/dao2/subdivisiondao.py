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
        if type_subdivision == 'Arrondissement':
            subdivision = Arrondissement(id=id, nom=nom, annee=annee, insee_arr=insee_arr,
                                         insee_dep=insee_dep, insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision == 'Canton':
            subdivision = Canton(id=id, nom=nom, annee=annee, insee_can=insee_can,
                                 insee_dep=insee_dep, insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision == 'Commune':
            subdivision = Commune(id=id, nom=nom, annee=annee, insee_com=insee_com,
                                   statut='', insee_can=insee_can, insee_arr=insee_arr,
                                   insee_dep=insee_dep, insee_reg=insee_reg,
                                   siren_epci=siren_epci, polygones=polygones)
        elif type_subdivision == 'Departement':
            subdivision = Departement(id=id, nom=nom, annee=annee, insee_dep=insee_dep,
                                      insee_reg=insee_reg, polygones=polygones)
        elif type_subdivision == 'Epci':
            subdivision = Epci(id=id, nom=nom, annee=annee, siren=siren_epci,
                               nature='', polygones=polygones)  # nature='' pour Epci
        elif type_subdivision == 'Region':
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
                    subdivision.nom,
                    subdivision.insee_com,
                    subdivision.insee_can,
                    subdivision.insee_arr,
                    subdivision.insee_dep,
                    subdivision.insee_reg,
                    subdivision.siren_epci
                ))

                # Si un polygone est spécifié, l'ajouter dans la table 'contours' via ContourDAO
                if subdivision.polygones:
                    contour = subdivision.polygones  # polygones est un objet Contour
                    self.contour_dao.ajouter(contour)  # Utilise ContourDAO pour ajouter le contour

                    # Ajout de l'association entre subdivision et contour dans la table 'subdivision_contour'
                    query_assoc = """
                    INSERT INTO geodata.subdivision_contour (id_subdivision, id_contour)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query_assoc, (subdivision.id, contour.id))

                # Commit des modifications dans la base de données
                connection.commit()
