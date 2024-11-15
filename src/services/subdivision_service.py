from typing import Optional
from src.utils.singleton import Singleton
from src.business_object.subdivision import Subdivision
from src.dao.subdivisiondao import SubdivisionDAO


class SubdivisionService(metaclass=Singleton):
    def __init__(self):
        self.subdivision_dao = SubdivisionDAO()

    def chercherSubdivisionParID(self, typeSubdivision: str, id: str, annee: int) -> Optional[Subdivision]:
        # Générer le code INSEE selon le type de subdivision et l'ID
        codeINSEE = self._genererCodeINSEE(typeSubdivision, id)
        #codeINSEE = id
        # Rechercher la subdivision par le code INSEE via le DAO
        subdivision = self.subdivision_dao.find_by_code_insee(typeSubdivision, codeINSEE)
        return subdivision


    def _genererCodeINSEE(self, typeSubdivision: str, id: str) -> str:
        # Génère le code INSEE en fonction du type de subdivision

        if typeSubdivision == "Commune":
            return id.zfill(5) # code INSEE commune formater pour compléter avec 0 à gauche
        
        elif typeSubdivision == "Departement":
            return id.zfill(2) #ATTENTION NE PRENDS PAS EN COMPTE LES DEPARTEMENTS OUTRE MER
        
        elif typeSubdivision == "Region":
            return id.zfill(2)
        
        elif typeSubdivision == "Arrondissement":
            return id.zfill(3)
        
        elif typeSubdivision == "Canton":
            return id.zfill(4) #ATTENTION NE PRENDS PAS EN COMPTE un infime nmbre de canton à 5 chiffres
        
        elif typeSubdivision == "EPCI":
            return id.zfill(9)
        
        else:
            raise ValueError(f"Type de subdivision inconnu pour génération de code INSEE : {typeSubdivision}")
