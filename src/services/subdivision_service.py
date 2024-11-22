# from typing import Optional
from src.utils.singleton import Singleton
# from src.business_object.subdivision import Subdivision
from src.dao.subdivisiondao import SubdivisionDAO


class SubdivisionService(metaclass=Singleton):
    def __init__(self):
        self.subdivision_dao = SubdivisionDAO()

    def chercherSubdivisionParID(self, type_subdivision: str, id: str,
                                 annee: int, insee_dep: str = None) -> dict:
        """
        Recherche une subdivision par son type et son identifiant via le DAO.

        Args:
            type_subdivision (str): Le type de subdivision (Commune, Canton,
                                     Arrondissement, etc.).
            id (str): L'identifiant unique de la subdivision.
            insee_dep (str, optional): Le code département INSEE requis pour
                                       certains types de subdivision.

        Returns:
            dict: Les données de la subdivision trouvée.

        Raises:
            ValueError: Si les paramètres sont invalides ou si la subdivision
                        n'est pas trouvée.
        """
        # Validation des entrées
        if not type_subdivision or not isinstance(type_subdivision, str):
            raise ValueError("Le type de subdivision doit être une chaîne "
                             "non vide.")
        if type_subdivision in ["Canton", "Arrondissement"] and not insee_dep:
            raise ValueError(f"Le type '{type_subdivision}' nécessite un code "
                             "INSEE départemental (insee_dep).")

        # Génération du code INSEE
        if type_subdivision in ["Canton", "Arrondissement"]:
            # Utilise uniquement l'ID directement pour les cantons et
            # arrondissements
            code_insee = id
        else:
            # Utilise la méthode de génération pour les autres types
            code_insee = self._genererCodeINSEE(type_subdivision, id)

        # Recherche dans le DAO
        if type_subdivision in ["Canton", "Arrondissement"]:
            # Passe également le code département pour ces types
            subdivision = self.subdivision_dao.find_by_code_insee(
                type_subdivision, code_insee, insee_dep)
        else:
            subdivision = self.subdivision_dao.find_by_code_insee(
                type_subdivision, code_insee)

        # Gestion des cas où la subdivision n'est pas trouvée
        if not subdivision:
            raise ValueError(f"Aucune subdivision trouvée pour le type {type_subdivision}, ID {id}, et code INSEE '{code_insee}'.")

        return subdivision

    def zonage(self, type_subdivision: str, id: str, annee: int, dep=None):
        """
        Retourne le zonage d'une subdivision, avec ses subdivisions
        supérieures complètes.
        """
        subdivision = self.chercherSubdivisionParID(type_subdivision, id,
                                                    annee)
        hierarchy = self._get_hierarchy(type_subdivision)
        superiors = {}
        for superior_type, superior_column in hierarchy:
            superior_id = subdivision.get(superior_column)
            if superior_id:
                # Si le type supérieur est un Arrondissement ou un Canton,
                # inclure insee_dep
                if superior_type in ["Arrondissement", "Canton"]:
                    superior_data = self.subdivision_dao.find_by_code_insee(
                        superior_type, superior_id,
                        subdivision.get("insee_dep"))
                else:
                    superior_data = self.subdivision_dao.find_by_code_insee(
                        superior_type, superior_id)

                if superior_data:
                    superiors[superior_column] = {
                        "id": superior_id,
                        "type": superior_type,
                        "nom": superior_data["nom"]
                    }
        return {
            "subdivision": {
                "id": id,
                "type": type_subdivision,
                "nom": subdivision["nom"],
            },
            "superieurs": superiors,
        }

    def ajouterSubdivision(self, typeSubdivision: str, data: dict):
        """
        Ajoute une nouvelle subdivision dans la base de données.
        """
        self.subdivision_dao.insert_subdivision(typeSubdivision, data)

    def supprimerSubdivision(self, typeSubdivision: str, id: str):
        """
        Supprime une subdivision par son type et son identifiant.
        """
        self.subdivision_dao.delete_subdivision(typeSubdivision, id)

    def mettreAJourSubdivision(self, typeSubdivision: str, id: str,
                               data: dict):
        """
        Met à jour une subdivision existante.
        """
        self.subdivision_dao.update_subdivision(typeSubdivision, data, id)

    def _get_hierarchy(self, typeSubdivision: str):
        """
        Définit la hiérarchie des subdivisions supérieures en fonction du type.
        """
        if typeSubdivision == "Commune":
            return [
                ("Arrondissement", "insee_arr"),
                ("Departement", "insee_dep"),
                ("Region", "insee_reg"),
            ]
        elif typeSubdivision == "Canton":
            return [
                ("Departement", "insee_dep"),
                ("Region", "insee_reg"),
            ]
        elif typeSubdivision == "Arrondissement":
            return [
                ("Departement", "insee_dep"),
                ("Region", "insee_reg"),
            ]
        elif typeSubdivision == "Departement":
            return [
                ("Region", "insee_reg"),
            ]
        elif typeSubdivision in ["Region", "EPCI"]:
            return []
        else:
            raise ValueError("Type de subdivision inconnu.")

    def _genererCodeINSEE(self, typeSubdivision: str, id: str) -> str:
        """
        Génère le code INSEE formaté en fonction du type de subdivision.

        Args:
            typeSubdivision (str): Le type de subdivision (Commune,
            Département, Région, Canton, etc.).
            id (str): L'identifiant unique de la subdivision.

        Returns:
            str: Le code INSEE correctement formaté.

        Raises:
            ValueError: Si le type de subdivision est inconnu ou si l'ID
            est invalide.
        """

        # Génération du code INSEE en fonction du type de subdivision
        if typeSubdivision == "Commune":
            return id.zfill(5)  # Le code INSEE des communes est toujours sur 5
            # chiffres

        elif typeSubdivision == "Departement":
            # Format département : 2 chiffres sauf pour l'Outre-Mer
            #  (3 chiffres)
            return id.zfill(3) if id.startswith("97") else id.zfill(2)

        elif typeSubdivision == "Region":
            return id.zfill(2)  # Le code INSEE des régions est sur 2 chiffres

        elif typeSubdivision in ["Canton", "Arrondissement"]:
            # Retourne directement l'ID pour les cantons et arrondissements
            return id

        elif typeSubdivision == "EPCI":
            return id.zfill(9)  # Les EPCI ont des codes INSEE sur 9 chiffres

        else:
            raise ValueError(f"Type de subdivision inconnu pour la génération "
                             f"de code INSEE : {typeSubdivision}")
