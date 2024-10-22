from typing import Optional
from utils.singleton import Singleton
from business_object.subdivision.subdivision import Subdivision
from dao.subdivision_dao import SubdivisionDAO


class SubdivisionService(metaclass=Singleton):
    def __init__(self):
        self.subdivision_dao = SubdivisionDAO()

    def chercherSubdivisionParID(self, typeSubdivision: str, id: int, annee: int) -> Optional[Subdivision]:
        # Générer le code INSEE selon le type de subdivision et l'ID
        codeINSEE = self._genererCodeINSEE(typeSubdivision, id)

        # Rechercher la subdivision par le code INSEE via le DAO
        subdivision = self.subdivision_dao.getSubdivisionByCode(codeINSEE)

        # Vérifier si l'année correspond
        if subdivision and subdivision.annee == annee:
            return subdivision
        return None

    def _genererCodeINSEE(self, typeSubdivision: str, id: int) -> str:
        # Génère le code INSEE en fonction du type de subdivision
        if typeSubdivision == "COMMUNE":
            return f"{id:05d}"  # Code INSEE pour les communes, sur 5 chiffres
        elif typeSubdivision == "DEPARTEMENT":
            return f"{id:03d}"  # Code INSEE pour les départements, sur 3 chiffres
        elif typeSubdivision == "REGION":
            return f"{id:02d}"  # Code INSEE pour les régions, sur 2 chiffres
        elif typeSubdivision == "ARRONDISSEMENT":
            return f"{id:01d}"  # Code INSEE pour les arrondissements, sur 1 chiffre
        elif typeSubdivision == "CANTON":
            return f"{id:05d}"  # Code INSEE pour les cantons, sur 5 chiffres
        elif typeSubdivision == "EPCI":
            return f"{id:09d}"  # Code SIREN pour les EPCI, sur 9 chiffres
        else:
            raise ValueError(f"Type de subdivision inconnu pour génération de code INSEE : {typeSubdivision}")
