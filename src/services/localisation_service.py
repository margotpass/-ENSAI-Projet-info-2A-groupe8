# from typing import Optional
# from src.business_object.subdivision import Subdivision
from src.business_object.pointgeographique import PointGeographique
# from src.business_object.Polygones.contour import Contour
from src.dao.contourdao import ContourDAO
from src.dao.subdivisiondao import SubdivisionDAO
from src.dao.db_connection import DBConnection
from src.services.subdivision_service import SubdivisionService


class LocalisationService:

    def __init__(self):
        self.subdivision_dao = SubdivisionDAO()
        self.contour_dao = ContourDAO(DBConnection)

    def localiserPointDansSubdivision(self, point: PointGeographique,
                                      type_subdivision, annee: int = 2024):
        """Localise un point dans une subdivision

        Args:
            point (PointGeographique): instance de PointGeographique
            type_subdivision (_type_): str parmi Arrondissement, Canton,
                                        Commune,
                                        Departement, EPCI et Region
            annee (int, optional): année souhaitée de la recherche.
             Défaut à 2024.

        Returns:
            contour[1]: numéro de la subdivision
            nom_subdivision: nom de la subdivision
        """

        # Étape 1 : Récupérer la table (contours, nom de la subdivision)
        # associés au type de subdivision entré
        table_contours = self.contour_dao.get_all_contours(
            type_subdivision.lower()
        )

        # Etape 2 : Parcourir la table (contours, nom de la subdivision)
        for contour in table_contours:
            # Regarder si le point est dans le contour de la table
            if contour[0].estDansPolygone(point):
                if type_subdivision in [
                    "Commune", "Departement", "Region", "EPCI"
                ]:
                    nom_subdivision = SubdivisionService(
                    ).chercherSubdivisionParID(
                        type_subdivision, contour[1], annee
                    )
                    return contour[1], nom_subdivision
                    # Retourner n° et le nom de
                    # la subdivision dans la table si le point
                    # est dans le contour
                elif type_subdivision in ["Arrondissement", "Canton"]:
                    departement = self.localiserPointDansSubdivision(
                        point=point, type_subdivision="Departement",
                        annee=annee
                    )
                    insee_depart = departement[0]
                    nom_subdivision = SubdivisionService(
                    ).chercherSubdivisionParID(
                        type_subdivision=type_subdivision, id=contour[1],
                        annee=annee, insee_dep=insee_depart
                    )
                    return contour[1], nom_subdivision, insee_depart

        # Si aucun contour ne contient le point, retourner None
        return None

    def localiser_point_dans_contours(self, point: PointGeographique, type_sup: str, type_inf: str, code_insee_sup: str) -> dict:
        """
        Localise un point dans une subdivision enfant en vérifiant les contours.

        Args:
            point (PointGeographique): Point à localiser.
            type_sup (str): Type de la subdivision parent (ex : "Region").
            type_inf (str): Type de la subdivision enfant (ex : "Departement").
            code_insee_sup (str): Code INSEE de la subdivision parent.

        Returns:
            dict: Un dictionnaire contenant le code et le nom de la subdivision enfant trouvée.
        """
        # Récupère tous les contours enfants dans le parent donné
        contours = self.subdivision_dao.get_all_contours_inf_in_sup(
            type_inf=type_inf, type_sup=type_sup, code_insee_sup=code_insee_sup
        )

        # Parcourt chaque contour et vérifie si le point y est inclus
        for contour, code_insee_inf in contours:
            if contour.estDansPolygone(point):  # Vérifie si le point est dans le contour
                if type_inf == "Arrondissement":
                    subdivision = self.subdivision_dao.find_by_code_insee(type_inf, code_insee_inf, code_insee_sup)
                else:
                    subdivision = self.subdivision_dao.find_by_code_insee(type_inf, code_insee_inf)
                
                if not subdivision:  # Si aucune subdivision n'est trouvée
                    print(f"Subdivision introuvable pour {type_inf} avec code INSEE {code_insee_inf}")
                    return None
                # Récupère le nom de la subdivision, ou un message par défaut
                nom_subdivision = subdivision.get("nom", "Nom indisponible")
                return {"code": code_insee_inf, "nom": nom_subdivision}

        # Si aucun contour ne contient le point
        print(f"Aucun contour trouvé contenant le point {point}")
        return None

  


    def localiser_point(self, point: PointGeographique, annee: int = 2024) -> dict:
        """
        Localise un point géographique à travers les subdivisions hiérarchiques :
        Région → Département → Arrondissement → Commune.

        Args:
            point (PointGeographique): Instance de PointGeographique.
            annee (int): Année de la localisation. Par défaut 2024.

        Returns:
            dict: Localisation complète avec Région, Département, Arrondissement et Commune.
        """
        # Initialisation de la localisation
        localisation = {"Region": None, "Departement": None, "Arrondissement": None, "Commune": None}

        # Étape 1 : Localiser la région
        localisation_region = self.localiserPointDansSubdivision(point, "Region", annee)
        if localisation_region:
            code_region, nom_region = localisation_region[0], localisation_region[1]
            localisation["Region"] = {"code": code_region, "nom": nom_region}

            # Étape 2 : Localiser le département
            localisation_dep = self.localiser_point_dans_contours(point, "Region", "Departement", code_region)
            if localisation_dep:
                code_dep, nom_dep = localisation_dep["code"], localisation_dep["nom"]
                localisation["Departement"] = {"code": code_dep, "nom": nom_dep}

                # Étape 3 : Localiser l'arrondissement
                localisation_arr = self.localiser_point_dans_contours(point, "Departement", "Arrondissement", code_dep)
                if localisation_arr:
                    code_arr, nom_arr = localisation_arr["code"], localisation_arr["nom"]
                    localisation["Arrondissement"] = {"code": code_arr, "nom": nom_arr}

                    # Étape 4 : Localiser la commune
                    localisation_com = self.localiser_point_dans_contours(point, "Arrondissement", "Commune", code_arr)
                    if localisation_com:
                        code_com, nom_com = localisation_com["code"], localisation_com["nom"]
                        localisation["Commune"] = {"code": code_com, "nom": nom_com}

        return localisation
