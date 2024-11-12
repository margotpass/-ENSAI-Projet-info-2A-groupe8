import csv
from typing import List
from src.dao.pointgeographiquedao import PointGeographiqueDAO
from src.business_objects.pointgeographique import PointGeographique
from src.dao.subdivisiondao import SubdivisionDao

class FichierService:
    """ Ce service doit récupérer une liste de points (plusieurs ou un seul point) et le niveau souhaité
    Puis du niveau demandé, on renvoit un fichier csv qui contient la réponse du niveau demandé en utilisant le servide localisation_service

    """
    def __init__(self):
        self.point_dao = PointGeographiqueDAO()
        self.subdivision_dao = SubdivisionDao()
        self.contour_dao = ContourDAO(DBConnection)
    
    def reponse_niveau_demande(self, liste_point: List[PointGeographique], niveau: str) -> List[PointGeographique]:
        # renvoie la réponse du niveau demandé pour chaque point de la liste donnée par l'utilisateur en utilisant la méthode localiserPointDansSubdivision du servide localisation_service
        liste_reponse = []
        for point in liste_points:
            subdivision = self.localisation_service.localiserPointDansSubdivision(point)
            liste_reponse.append(subdivision)
        return liste_reponse
    
    def verifier_nom_subdivision_de_la_liste(self, liste_reponse: List[PointGeographique]) -> str:
        # vérifier que la liste_reponse n'est composé que d'un même nom de subdivision et renvoyer le nom de subdivision
        nom_subdivision = liste_reponse[0].nom
        for point in liste_reponse:
            if point.nom != nom_subdivision:
                raise ValueError("La liste de points est composée de plusieurs subdivisions")
        return nom_subdivision

    # mettre dans un fichier sous format csv la réponse du niveau demandé donnée par verifier_nom_subdivision_de_la_liste
    def mettre_reponse_dans_csv(self, liste_reponse: List[PointGeographique], nom_subdivision: str) -> None:
        # mettre dans un fichier sous format csv la réponse du niveau demandé donnée par verifier_nom_subdivision_de_la_liste
        with open('reponse.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([FichierService.verifier_nom_subdivision_de_la_liste(liste_reponse)])
    
    # envoyer le fichier csv créé à l'utilisateur





    

            
            
        

