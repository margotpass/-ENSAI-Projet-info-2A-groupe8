import pytest
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.connexe import Connexe


@pytest.fixture
def polygones_connexes():
    """Fixture pour créer un ensemble de polygones connexes avec des polygones 
    primaires pour les tests"""
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])

    point3 = PointGeographique(40.712776, -74.005974, "WGS84")
    point4 = PointGeographique(34.052235, -118.243683, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])

    return Connexe([polygone1, polygone2])


def test_initialisation_connexe_vide():
    """Test pour vérifier l'initialisation d'une liste connexe vide"""
    connexe_vide = Connexe()
    assert isinstance(connexe_vide, Connexe)
    assert len(connexe_vide.get_connexe()) == 0


def test_initialisation_connexe_avec_polygones():
    """Test pour vérifier l'initialisation d'une liste connexe avec des
    polygones primaires"""
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])

    point3 = PointGeographique(40.712776, -74.005974, "WGS84")
    point4 = PointGeographique(34.052235, -118.243683, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])

    connexe = Connexe([polygone1, polygone2])

    assert isinstance(connexe, Connexe)
    assert len(connexe.get_connexe()) == 2
    assert isinstance(connexe.get_connexe()[0], PolygonePrimaire)
    assert isinstance(connexe.get_connexe()[1], PolygonePrimaire)


def test_initialisation_connexe_avec_polygones_invalides():
    """Test pour vérifier que l'initialisation échoue si des éléments
     non valides sont fournis"""
    with pytest.raises(TypeError, match="Tous les éléments doivent être des instances de PolygonePrimaire"):
        Connexe([1, "non_polygone"])


def test_str_connexe_avec_polygones(polygones_connexes):
    """Test pour vérifier la méthode __str__ d'une liste connexe avec des polygones primaires"""
    point1 = PointGeographique(48.858844, 2.294351, "WGS84")
    point2 = PointGeographique(51.507351, -0.127758, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])

    point3 = PointGeographique(40.712776, -74.005974, "WGS84")
    point4 = PointGeographique(34.052235, -118.243683, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])

    connexe = Connexe([polygone1, polygone2])

    expected_str = (
        "Connexe: [Polygone Primaire: [Latitude: 48.858844 Longitude: 2.294351 Type de coordonnées: WGS84, "
        "Latitude: 51.507351 Longitude: -0.127758 Type de coordonnées: WGS84], "
        "Polygone Primaire: [Latitude: 40.712776 Longitude: -74.005974 Type de coordonnées: WGS84, "
        "Latitude: 34.052235 Longitude: -118.243683 Type de coordonnées: WGS84]]"
    )
    assert str(connexe) == expected_str, f"La représentation en chaîne de la liste connexe devrait être '{expected_str}'"


def test_ajout_polygone_dans_connexe(polygones_connexes):
    """Test pour vérifier l'ajout d'un polygone primaire dans une liste connexe"""
    point5 = PointGeographique(35.689487, 139.691711, "WGS84")
    point6 = PointGeographique(55.755825, 37.617298, "WGS84")
    nouveau_polygone = PolygonePrimaire([point5, point6])

    polygones_connexes.ajouter_polygone(nouveau_polygone)
    assert len(polygones_connexes.get_connexe()) == 3
    assert polygones_connexes.get_connexe()[-1] == nouveau_polygone

def test_ajout_polygone_invalide():
    """Test pour vérifier qu'un polygone non valide génère une erreur"""
    connexe = Connexe()
    with pytest.raises(TypeError, match="L'objet ajouté doit être une instance de PolygonePrimaire"):
        connexe.ajouter_polygone("non_polygone")


def test_ajout_polygone_vers_connexe_vide():
    """Test pour vérifier que l'ajout d'un polygone à une Connexe vide
     fonctionne correctement"""
    connexe_vide = Connexe()
    point = PointGeographique(48.858844, 2.294351, "WGS84")
    polygone = PolygonePrimaire([point])
    connexe_vide.ajouter_polygone(polygone)
    assert len(connexe_vide.get_connexe()) == 1
    assert connexe_vide.get_connexe()[0] == polygone


def test_get_connexe(polygones_connexes):
    """Test pour vérifier que get_connexe retourne la liste actuelle 
    des polygones"""
    assert polygones_connexes.get_connexe() == [polygones_connexes.get_connexe()[0], polygones_connexes.get_connexe()[1]]
