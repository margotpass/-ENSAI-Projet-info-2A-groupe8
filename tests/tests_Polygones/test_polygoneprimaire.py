import pytest
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire


@pytest.fixture
def polygone():
    """Fixture pour créer un polygone avec des points pour les tests"""
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")
    return PolygonePrimaire([point1, point2])

def test_initialisation_polygone_vide():
    """Test pour vérifier l'initialisation d'un polygone vide"""
    polygone_vide = PolygonePrimaire()
    assert isinstance(polygone_vide, PolygonePrimaire)
    assert len(polygone_vide.get_polygoneprimaire()) == 0


def test_initialisation_polygone_avec_points(polygone):
    """Test pour vérifier l'initialisation d'un polygone avec des points"""
    assert isinstance(polygone, PolygonePrimaire)
    assert len(polygone.get_polygoneprimaire()) == 2
    assert isinstance(polygone.get_polygoneprimaire()[0], PointGeographique)


def test_ajout_point_dans_polygone(polygone):
    """Test pour vérifier l'ajout d'un point géographique dans le polygone"""
    point = PointGeographique(45.7640, 4.8357, "WGS84")
    polygone.ajouter_point(point)
    assert len(polygone.get_polygoneprimaire()) == 3
    assert polygone.get_polygoneprimaire()[-1].latitude == 45.7640


def test_ajout_point_invalide():
    """Test pour vérifier qu'un point non valide génère une erreur"""
    polygone = PolygonePrimaire()
    with pytest.raises(ValueError, match="L'objet ajouté doit être une instance de PointGeographique"):
        polygone.ajouter_point("non_point")


def test_str_polygone_vide():
    """Test pour vérifier la méthode __str__ d'un polygone vide"""
    polygone_vide = PolygonePrimaire()  # Polygone vide
    with pytest.raises(ValueError, match="Le polygone est vide et ne peut pas être affiché"):
        str(polygone_vide)

def test_str_polygone_avec_points():
    """Test pour vérifier la méthode __str__ d'un polygone avec des points"""
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")

    polygone = PolygonePrimaire([point1, point2])

    expected_str = (
        "Polygone Primaire: ["
        "Latitude: 48.858844 Longitude: 2.294351 Type de coordonnées: WGS84, "
        "Latitude: 51.507351 Longitude: -0.127758 Type de coordonnées: WGS84]"
    )
    assert str(polygone) == expected_str, f"La représentation en chaîne du polygone devrait être '{expected_str}'"


def test_str_polygone_invalide():
    """Test pour vérifier que __str__ lève une erreur pour un polygone vide ou invalide"""

    # Test pour un polygone vide
    polygone_vide = PolygonePrimaire([])  # Polygone vide
    with pytest.raises(ValueError, match="Le polygone est vide et ne peut pas être affiché"):
        str(polygone_vide)

    # Test pour un polygone avec un point invalide
    class PointInvalide:
        """Classe pour simuler un point invalide"""
        pass  # Ne définit pas __str__, donc ce ne sera pas un PointGeographique

    polygone_avec_point_invalide = PolygonePrimaire([PointInvalide()])  # Ajout d'un point invalide
    with pytest.raises(ValueError, match="Tous les points du polygone doivent être des instances de PointGeographique"):
        str(polygone_avec_point_invalide)


def test_get_polygoneprimaire():
    """Test pour vérifier la méthode get_polygoneprimaire"""
    # Crée deux points géographiques
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")

    # Crée un polygone avec ces points
    polygone = PolygonePrimaire([point1, point2])

    # Récupère le polygone primaire via la méthode
    points = polygone.get_polygoneprimaire()

    # Vérifie que les points sont correctement renvoyés
    assert len(points) == 2, f"Le polygone devrait contenir 2 points, mais en contient {len(points)}"
    assert points[0] == point1, "Le premier point devrait être Paris"
    assert points[1] == point2, "Le second point devrait être Londres"
