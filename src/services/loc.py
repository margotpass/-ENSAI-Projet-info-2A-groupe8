from src.business_object.pointgeographique import PointGeographique
from src.services.localiser_servicemm import LocaliserServiceMM
from src.dao.db_connection import DBConnection  # Utiliser l'implémentation existante


def tester_localisation():
    # Créer un point de test (latitude, longitude)
    point_test = PointGeographique(latitude=48.8566, longitude=2.3522)  # Coordonnées de Paris

    # Utiliser la connexion à la base de données existante
    db_connection = DBConnection()  # Utiliser comme déjà implémenté

    # Initialiser le service de localisation avec la connexion à la base de données
    localisation_service = LocaliserServiceMM(db_connection)

    # Tester la localisation du point
    resultat = localisation_service.localiser_point(point_test)

    # Afficher le résultat
    print("Résultat de la localisation :", resultat)

# Exécuter le test
if __name__ == '__main__':
    tester_localisation()
