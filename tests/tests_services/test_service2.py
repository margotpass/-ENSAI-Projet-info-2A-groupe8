import pytest
from unittest.mock import MagicMock
from src.business_object.subdivision import Subdivision
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.contour import Contour
from src.dao.contourdao import ContourDAO
from src.dao.subdivisiondao import SubdivisionDAO
from src.services.localisation_service import LocalisationService


@pytest.fixture
def localisation_service():
    # Créer des mocks pour SubdivisionDAO et ContourDAO
    mock_subdivision_dao = MagicMock(spec=SubdivisionDAO)
    mock_contour_dao = MagicMock(spec=ContourDAO)
    # Initialiser le service avec les mocks
    return LocalisationService(mock_subdivision_dao, mock_contour_dao), mock_subdivision_dao, mock_contour_dao

def test_initialisation(localisation_service):
    service, mock_subdivision_dao, mock_contour_dao = localisation_service
    # Vérifie que les objets subdivision_dao et contour_dao sont des instances de MagicMock
    assert isinstance(service.subdivision_dao, MagicMock)
    assert isinstance(service.contour_dao, MagicMock)


from unittest.mock import MagicMock

def test_localiserPointDansSubdivision_point_in_contour(localisation_service):
    service, mock_subdivision_dao, mock_contour_dao = localisation_service

    # Configurer les mocks pour renvoyer une subdivision et un contour contenant le point
    mock_point = PointGeographique(48.8566, 2.3522, typecoordonnees="WGS84")  # Exemple de point avec type de coordonnées
    
    # Créer un mock pour le contour et l'utiliser comme polygones
    mock_polygone = MagicMock(spec=Contour)  # Utiliser un mock de Contour
    
    # Créer la subdivision avec un id, un nom, une année valide, et le mock pour polygones
    mock_subdivision = Subdivision(id="75056", nom="Paris", annee=2024, polygones=mock_polygone)

    # Configurer les mocks de DAO pour renvoyer cette subdivision et un contour
    mock_subdivision_dao.find_by_code_insee.return_value = [mock_subdivision]
    mock_contour_dao.get_all_contours.return_value = [mock_polygone]  # Utiliser mock_polygone ici

    # Configurer le contour pour qu'il contienne le point
    mock_polygone.estDansPolygone.return_value = True

    # Appeler la méthode et vérifier le résultat
    result = service.localiserPointDansSubdivision("75056", mock_point)
    assert result == mock_subdivision





def test_localiserPointDansSubdivision_point_not_in_any_contour(localisation_service):
    service, mock_subdivision_dao, mock_contour_dao = localisation_service

    # Configurer les mocks pour renvoyer une subdivision et un contour qui ne contient pas le point
    mock_point = PointGeographique(48.8566, 2.3522, typecoordonnees="WGS84")  # Exemple de point
    mock_contour = MagicMock(spec=Contour)  # Créer un mock pour Contour

    # Créer la subdivision avec le mock_contour pour polygones
    mock_subdivision = Subdivision(id="75056", nom="Paris", annee=2024, polygones=mock_contour)

    # Simuler le comportement des méthodes de DAO
    mock_subdivision_dao.find_by_code_insee.return_value = [mock_subdivision]
    mock_contour_dao.get_all_contours.return_value = [mock_contour]

    # Configurer le contour pour qu'il ne contienne pas le point
    mock_contour.estDansPolygone.return_value = False

    # Appeler la méthode et vérifier le résultat
    result = service.localiserPointDansSubdivision("75056", mock_point)
    assert result is None
