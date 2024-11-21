import csv
from typing import List
from src.dao.pointgeographiquedao import PointGeographiqueDAO
from src.business_object.pointgeographique import PointGeographique
from src.dao.subdivisiondao import SubdivisionDAO
from src.services.localisation_service import LocalisationService
from src.dao.db_connection import DBConnection
from src.dao.contourdao import ContourDAO

class FichierService:
    """ Ce service doit récupérer une liste de points (plusieurs ou un seul point) et le niveau souhaité
    Puis du niveau demandé, on renvoit un fichier csv qui contient la réponse du niveau demandé en utilisant le servide localisation_service

    """
    def __init__(self):
        self.point_dao = PointGeographiqueDAO(DBConnection)
        self.subdivision_dao = SubdivisionDAO()
        self.contour_dao = ContourDAO(DBConnection)
        self.localisation_service = LocalisationService()
    
    def creer_points_a_partir_de_coordonnees(self, liste_coordonnees) -> List[PointGeographique]:
        """Transforme une liste de tuples (latitude, longitude, coordonnées)
        en une liste d'objets PointGeographique."""
        liste_coordonnees2 = eval(liste_coordonnees)
        points = []
        
        for item in liste_coordonnees2:
            lat, lon, systeme = item[0], item[1], item[2]
            # Crée un nouvel objet PointGeographique avec la latitude, la longitude et le système de coordonnées
            point = PointGeographique(latitude=lat, longitude=lon, typecoordonnees=systeme)
            points.append(point)
    
        return points
    
    def reponse_niveau_demande(self, liste_points, type_subdivision: str, annee: int = 2024) -> List[PointGeographique]:
        # renvoie la réponse du niveau demandé pour chaque point de la liste donnée par l'utilisateur en utilisant la méthode localiserPointDansSubdivision du servide localisation_service
        liste_reponse = []
        liste = self.creer_points_a_partir_de_coordonnees(liste_points)

        for point in liste:
            subdivision = self.localisation_service.localiserPointDansSubdivision(
                point, type_subdivision
            )
            if subdivision is not None:
                subdivision = subdivision[1]
            else:
                subdivision = ""
            liste_reponse.append(subdivision)
        return liste_reponse
    
    """def verifier_nom_subdivision_de_la_liste(self, liste_reponse: List[PointGeographique]) -> str:
        # vérifier que la liste_reponse n'est composé que d'un même nom de subdivision et renvoyer le nom de subdivision
        nom_subdivision = liste_reponse[0].nom
        for point in liste_reponse:
            if point.nom != nom_subdivision:
                raise ValueError("La liste de points est composée de plusieurs subdivisions")
        return nom_subdivision"""

    def mettre_reponse_dans_csv(self, liste_points, type_subdivision: str, annee: int = 2024) -> None:
        """Mettre la réponse du niveau demandé dans un fichier CSV."""
        liste_reponse = self.reponse_niveau_demande(liste_points, type_subdivision, annee)
        liste = self.creer_points_a_partir_de_coordonnees(liste_points)
        
        # Ouvre le fichier CSV avec l'encodage 'utf-8'
        with open('reponse.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # En-tête avec plus d'explications
            writer.writerow(["Latitude", "Longitude", "Système de coordonnées", "Subdivision"])
          
            assert len(liste) == len(liste_reponse), "Mismatch between points and subdivisions"
            # Ajouter les données point par point 
            for point, subdivision in zip(liste, liste_reponse):
                writer.writerow([point.latitude, point.longitude, point.typecoordonnees, subdivision])
        
        print(f"Les résultats ont été enregistrés dans 'reponse.csv' pour la subdivision '{type_subdivision}'.")




    
""" 
[[48.856578, 2.351828, "WGS84"], [45.764043, 4.835659, "WGS84"]]
"""
