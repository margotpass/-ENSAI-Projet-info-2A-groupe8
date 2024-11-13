import pytest
from unittest.mock import MagicMock, patch
from src.business_object.pointgeographique import PointGeographique
from src.services.localisation_service import LocalisationService


@pytest.fixture
def localisation_service():
    # Crée une instance de LocalisationService avec des DAO simulés
    service = LocalisationService()
    service.subdivision_dao = MagicMock()
    service.contour_dao = MagicMock()
    return service

@pytest.fixture
def point_dans_contour():
    return PointGeographique(5, 5, None)

@pytest.fixture
def point_hors_contour():
    return PointGeographique(50, 50, None)

@pytest.fixture
def contour_qui_contient_point():
    # Crée un contour simulé qui contient le point
    contour = (MagicMock(), "SubdivisionExistante")
    contour[0].estDansPolygone.return_value = True
    return contour

@pytest.fixture
def contour_qui_ne_contient_pas_point():
    # Crée un contour simulé qui ne contient pas le point
    contour = (MagicMock(), "SubdivisionInexistante")
    contour[0].estDansPolygone.return_value = False
    return contour

@patch('src.services.subdivision_service.SubdivisionService.chercherSubdivisionParID', return_value="NomSubdivision")
def test_point_dans_subdivision(mock_chercherSubdivisionParID, localisation_service, point_dans_contour, contour_qui_contient_point, contour_qui_ne_contient_pas_point):
    # Simule le retour de get_all_contours avec un contour contenant le point
    localisation_service.contour_dao.get_all_contours.return_value = [
        contour_qui_contient_point, 
        contour_qui_ne_contient_pas_point
    ]

    # Exécute la méthode à tester
    result = localisation_service.localiserPointDansSubdivision(point_dans_contour, "commune")

    # Vérifie que le résultat est le tuple avec le numéro et le nom de la subdivision correcte
    assert result == ("SubdivisionExistante", "NomSubdivision")
    mock_chercherSubdivisionParID.assert_called_once_with("commune", "SubdivisionExistante", 2024)

def test_point_hors_subdivision(localisation_service, point_hors_contour, contour_qui_ne_contient_pas_point):
    # Simule le retour de get_all_contours pour des contours ne contenant pas le point
    localisation_service.contour_dao.get_all_contours.return_value = [
        contour_qui_ne_contient_pas_point
    ]

    # Exécute la méthode avec un point hors des contours
    result = localisation_service.localiserPointDansSubdivision(point_hors_contour, "commune")

    # Vérifie que le résultat est None
    assert result is None

def test_type_subdivision_invalide(localisation_service, point_dans_contour):
    # Simule le retour d'une liste vide pour un type de subdivision invalide
    localisation_service.contour_dao.get_all_contours.return_value = []

    # Exécute la méthode avec un type de subdivision invalide
    result = localisation_service.localiserPointDansSubdivision(point_dans_contour, "type_invalide")

    # Vérifie que le résultat est None
    assert result is None
