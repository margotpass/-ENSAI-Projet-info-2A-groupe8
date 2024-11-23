import pytest
from unittest.mock import MagicMock
from src.services.fichier_service import FichierService
from src.business_object.pointgeographique import PointGeographique


@pytest.fixture
def fichier_service():
    """Fixture pour initialiser l'objet FichierService avec des mocks."""
    fichier_service = FichierService()
    fichier_service.localisation_service.localiserPointDansSubdivision = MagicMock()
    return fichier_service


def test_creer_points_a_partir_de_coordonnees(fichier_service):
    """Test de la méthode creer_points_a_partir_de_coordonnees."""
    liste_coordonnees = "[[48.856578, 2.351828, 'WGS84'], [45.764043, 4.835659, 'WGS84']]"
    points = fichier_service.creer_points_a_partir_de_coordonnees(
        liste_coordonnees
    )

    assert len(points) == 2
    assert isinstance(points[0], PointGeographique)
    assert points[0].latitude == 48.856578
    assert points[0].longitude == 2.351828
    assert points[0].typecoordonnees == "WGS84"


def test_reponse_niveau_demande(fichier_service):
    """Test de la méthode reponse_niveau_demande avec des données mockées."""
    liste_points = "[[48.856578, 2.351828, 'WGS84'], [45.764043, 4.835659, 'WGS84']]"
    fichier_service.localisation_service.localiserPointDansSubdivision.side_effect = [
        ("1", "Paris"),
        ("2", "Lyon"),
    ]

    result = fichier_service.reponse_niveau_demande(liste_points, "commune")

    assert result == ["Paris", "Lyon"]


def test_mettre_reponse_dans_csv(fichier_service, tmp_path):
    """Test de la méthode mettre_reponse_dans_csv avec un fichier CSV temporaire."""
    liste_points = "[[48.856578, 2.351828, 'WGS84'], [45.764043, 4.835659, 'WGS84']]"
    fichier_service.localisation_service.localiserPointDansSubdivision.side_effect = [
        ("1", "Paris"),
        ("2", "Lyon"),
    ]

    # Créer un chemin temporaire pour le fichier CSV
    csv_file = tmp_path / "reponse.csv"

    # Utilisation de monkeypatch pour rediriger open
    def mock_open(file, mode='r', **kwargs):
        if file == 'reponse.csv' and 'w' in mode:
            return csv_file.open(mode, **kwargs)
        return open(file, mode, **kwargs)

    with pytest.MonkeyPatch().context() as monkeypatch:
        monkeypatch.setattr("builtins.open", mock_open)

        # Appeler la méthode avec le mock
        fichier_service.mettre_reponse_dans_csv(liste_points, "commune", 2024)

    # Vérifier le contenu du fichier temporaire
    with csv_file.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    # Vérifications
    assert len(lines) == 3  # Une ligne d'en-tête + 2 données
    assert lines[0].strip() == "Latitude,Longitude,Système de coordonnées,Subdivision"
    assert "48.856578,2.351828,WGS84,Paris" in lines[1]
    assert "45.764043,4.835659,WGS84,Lyon" in lines[2]
