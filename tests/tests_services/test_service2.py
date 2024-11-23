from unittest.mock import MagicMock, patch
import pytest
from src.business_object.pointgeographique import PointGeographique
from src.services.localisation_service import LocalisationService


@pytest.fixture
def localisation_service():
    """Crée une instance de LocalisationService avec des DAO simulés"""
    service = LocalisationService()
    service.subdivision_dao = MagicMock()
    service.contour_dao = MagicMock()
    return service


@pytest.fixture
def point_dans_contour():
    return PointGeographique(2,2)


@pytest.fixture
def point_hors_contour():
    """ un point qui est hors contour"""
    return PointGeographique(50, 50, None)


@pytest.fixture
def contour_qui_contient_point():
    """Contour simulé qui contient le point"""
    contour = (MagicMock(), "SubdivisionExistante")
    contour[0].estDansPolygone.return_value = True
    return contour


@pytest.fixture
def contour_qui_ne_contient_pas_point():
    """ Teste un contour qui ne contient pas le point donné"""
    # Crée un contour simulé qui ne contient pas le point
    contour = (MagicMock(), "SubdivisionInexistante")
    contour[0].estDansPolygone.return_value = False
    return contour

@patch('src.services.subdivision_service.SubdivisionService.'
       'chercherSubdivisionParID')
def test_point_dans_subdivision(mock_chercherSubdivisionParID,
                                localisation_service,
                                point_dans_contour,
                                contour_qui_contient_point,
                                contour_qui_ne_contient_pas_point):
    """Teste la localisation d'un point dans une subdivision"""

    # Simule le retour de get_all_contours avec un contour contenant
    # le point
    localisation_service.contour_dao.get_all_contours.return_value = [
        contour_qui_contient_point,  # Le contour contenant le point
        contour_qui_ne_contient_pas_point  # Un autre contour qui
        # ne contient pas le point
    ]

    # Simule le retour de la recherche de subdivision
    mock_chercherSubdivisionParID.return_value = "NomSubdivision"

    # Définir la valeur que le mock renverra pour 'nom'
    contour_qui_contient_point[0].return_value = "SubdivisionExistante"

    # Exécute la méthode à tester
    result = localisation_service.localiserPointDansSubdivision(
        point=point_dans_contour,  # Point à l'intérieur du contour
        type_subdivision="Commune"  # Type de subdivision à tester
    )

    # Vérifie que le résultat est le tuple avec le nom de la
    # subdivision correcte
    assert result == ("SubdivisionExistante", "NomSubdivision")

    # Vérifie que la méthode chercherSubdivisionParID a été appelée
    # correctement
    mock_chercherSubdivisionParID.assert_called_once_with("Commune",
                                                          "SubdivisionExistante",
                                                          2024)


def test_type_subdivision_invalide(localisation_service, point_dans_contour):
    """Simule le retour d'une liste vide pour un type de subdivision
    invalide"""
    localisation_service.contour_dao.get_all_contours.return_value = []

    # Exécute la méthode avec un type de subdivision invalide
    result = localisation_service.localiserPointDansSubdivision(
        point_dans_contour,
        "type_invalide"
    )

    # Vérifie que le résultat est None
    assert result is None
