import pytest
from src.business_object.Polygones.connexe import Connexe
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.business_object.Polygones.contour import Contour

@pytest.fixture
def polygone_contour():
    """Fixture pour créer un ensemble de connexes (= contour) avec des polygones primaires pour les tests"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2, point3, point4])

    point5 = PointGeographique(44.1, 5.1, "WGS84")
    point6 = PointGeographique(44.1, 5.2, "WGS84")
    point7 = PointGeographique(44.05, 5.2, "WGS84")
    point8 = PointGeographique(44.05, 5.1, "WGS84")
    polygone2 = PolygonePrimaire([point5, point6, point7, point8])

    connexe1 = Connexe([polygone1])
    connexe2 = Connexe([polygone2])

    return Contour([connexe1, connexe2])

# Tests pour la méthode __init__ de la classe Contour
def test_initialisation_contour_avec_connexes():
    """Test pour vérifier l'initialisation d'un contour avec des connexes valides"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2, point3, point4])
    connexe1 = Connexe([polygone1])

    contour = Contour([connexe1])
    assert len(contour.get_contour()) == 1
    assert contour.get_contour()[0] == connexe1

def test_initialisation_contour_avec_connexes_incorrects():
    """Test pour vérifier que l'initialisation échoue avec des connexes non valides"""
    with pytest.raises(TypeError):
        Contour([123])  # Un entier au lieu d'une instance de Connexe

def test_initialisation_contour_multiples_connexes():
    """Test pour vérifier l'initialisation d'un contour avec plusieurs connexes"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])
    connexe2 = Connexe([polygone2])

    contour = Contour([connexe1, connexe2])
    assert len(contour.get_contour()) == 2
    assert contour.get_contour() == [connexe1, connexe2]

def test_initialisation_contour_avec_connexes_vide():
    """Test pour vérifier l'initialisation d'un contour avec une liste de connexes vide"""
    contour = Contour([])
    assert len(contour.get_contour()) == 0

def test_initialisation_contour_mauvais_type():
    """Test pour vérifier que l'initialisation échoue avec un type incorrect"""
    with pytest.raises(TypeError):
        Contour("Not a list")  # Chaîne de caractères au lieu d'une liste

def test_initialisation_contour_vide():
    """Test pour vérifier l'initialisation d'un contour vide"""
    contour_vide = Contour()
    assert isinstance(contour_vide, Contour)
    assert len(contour_vide.get_contour()) == 0

# Tests pour la méthode __str__ de la classe Contour
def test_str_contour_avec_connexes_vide():
    """Test de la méthode __str__ pour un contour sans connexes"""
    contour = Contour([])
    assert str(contour) == "Contour: []"

def test_str_contour_avec_connexes():
    """Test de la méthode __str__ pour un contour avec des connexes"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")

    polygone1 = PolygonePrimaire([point1, point2])
    polygone2 = PolygonePrimaire([point3, point4])

    connexe1 = Connexe([polygone1])
    connexe2 = Connexe([polygone2])

    contour = Contour([connexe1, connexe2])

    expected_str = "Contour: [" + str(connexe1) + ", " + str(connexe2) + "]"

    assert str(contour) == expected_str

def test_str_contour_avec_connexes_une_seule_connexe():
    """Test de la méthode __str__ pour un contour avec une seule connexe"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    contour = Contour([connexe1])
    expected_str = "Contour: [" + str(connexe1) + "]"
    assert str(contour) == expected_str

# Tests pour la méthode get_contour de la classe Contour
def test_get_contour_connexes_vide():
    """Test de la méthode get_contour pour un contour sans connexes"""
    contour = Contour([])
    # Vérifie que get_contour renvoie une liste vide
    assert contour.get_contour() == []

def test_get_contour_une_seule_connexe():
    """Test de la méthode get_contour pour un contour avec une seule connexe"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    contour = Contour([connexe1])
    # Vérifie que get_contour renvoie la liste avec la seule connexe
    assert contour.get_contour() == [connexe1]

def test_get_contour_connexes():
    """Test de la méthode get_contour pour un contour avec des connexes"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])
    connexe2 = Connexe([polygone2])

    point5 = PointGeographique(44.5, 6.5, "WGS84")
    point6 = PointGeographique(44.5, 5.5, "WGS84")
    polygone3 = PolygonePrimaire([point5, point6])
    connexe3 = Connexe([polygone3])

    contour = Contour([connexe1, connexe2, connexe3])

    # Vérifie que get_contour renvoie bien la liste complète des connexes
    assert contour.get_contour() == [connexe1, connexe2, connexe3]

# Tests pour la méthode ajout_connexe de la classe Contour
def test_ajout_connexe_valide():
    """Test de la méthode ajout_connexe pour ajouter une connexe valide"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    contour = Contour()
    contour.ajout_connexe(connexe1)

    # Vérifie que la connexe a été ajoutée
    assert contour.get_contour() == [connexe1]

def test_ajout_connexe_multiple():
    """Test de la méthode ajout_connexe pour ajouter plusieurs connexes"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone2 = PolygonePrimaire([point3, point4])
    connexe2 = Connexe([polygone2])

    contour = Contour()
    contour.ajout_connexe(connexe1)
    contour.ajout_connexe(connexe2)

    # Vérifie que les deux connexes ont été ajoutées
    assert contour.get_contour() == [connexe1, connexe2]

def test_ajout_connexe_type_invalide():
    """Test de la méthode ajout_connexe pour vérifier que l'ajout d'un type invalide génère une erreur"""
    contour = Contour()

    # Vérifie que l'ajout d'un type non valide (str) génère une exception TypeError
    try:
        contour.ajout_connexe("invalid_connexe")
        assert False, "L'objet ajouté doit être une instance de Connexe"
    except TypeError:
        pass  # Test réussi si l'exception est levée

def test_ajout_connexe_connexe_deja_presente():
    """Test de la méthode ajout_connexe pour ajouter une connexe déjà présente dans le contour"""
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2])
    connexe1 = Connexe([polygone1])

    contour = Contour([connexe1])
    contour.ajout_connexe(connexe1)  # Essaye d'ajouter la même connexe

    # Vérifie que la connexe est toujours présente une seule fois
    assert contour.get_contour().count(connexe1) == 1

# Tests pour la méthode retirer_connexe de la classe Contour
def test_retirer_connexe_present_dans_contour(polygone_contour):
    """Test pour retirer une connexe qui est présente dans le contour"""
    connexe_a_retirer = polygone_contour.get_contour()[0]  # Prendre la première connexe
    contour = polygone_contour
    contour.retirer_connexe(connexe_a_retirer)

    # Vérifie que la connexe a été retirée
    assert connexe_a_retirer not in contour.get_contour()

def test_retirer_connexe_non_present(polygone_contour):
    """Test pour tenter de retirer une connexe qui n'est pas dans le contour"""
    connexe_inexistante = Connexe([])  # Connexe vide, donc pas présent
    contour = polygone_contour
    contour.retirer_connexe(connexe_inexistante)

    # Vérifie que le contour reste inchangé
    assert len(contour.get_contour()) == 2  # On devrait toujours avoir 2 connexes

def test_retirer_le_seul_connexe(polygone_contour):
    """Test pour retirer la seule connexe d'un contour avec un connexe unique"""
    contour = Contour([polygone_contour.get_contour()[0]])  # Créer un contour avec une seule connexe
    connexe_a_retirer = contour.get_contour()[0]
    contour.retirer_connexe(connexe_a_retirer)

    # Vérifie que le contour est maintenant vide
    assert len(contour.get_contour()) == 0

# Tests pour la méthode point_dans_polygone de la classe Contour
def test_point_dans_polygone_connexe_interieur(polygone_contour):
    """Test si un point à l'intérieur d'un polygone connexe retourne True."""
    point_interieur = PointGeographique(44.06, 5.15, "WGS84")  # À l'intérieur de polygone2
    polygone_test = polygone_contour.get_contour()[1].get_connexe()[0]  # Assurez-vous que c'est bien polygone2

    result = polygone_contour.point_dans_polygone(point_interieur, polygone_test)
    assert result is True, f"Expected True, but got {result}"

def test_point_sur_bord(polygone_contour):
    """Test si un point sur le bord d'un polygone connexe retourne True."""
    point_bord = PointGeographique(44.05, 5.1, "WGS84")  # Sur le bord de polygone2
    polygone_test = polygone_contour.get_contour()[1].get_connexe()[0]

    result = polygone_contour.point_dans_polygone(point_bord, polygone_test)
    assert result is True, f"Expected True, but got {result}"

def test_point_dans_polygone_exterieur(polygone_contour):
    """Test si un point à l'extérieur du polygone retourne False."""
    point_exterieur = PointGeographique(44.2, 5.2, "WGS84")
    assert polygone_contour.point_dans_polygone(point_exterieur, polygone_contour.get_contour()[0].get_connexe()[0]) is False

def test_point_sur_bordure(polygone_contour):
    """Test si un point sur la bordure du polygone retourne True."""
    point_bordure = PointGeographique(44.0, 5.0, "WGS84")  # Un des points du polygone
    assert polygone_contour.point_dans_polygone(point_bordure, polygone_contour.get_contour()[0].get_connexe()[0]) is True

def test_point_exterieur(polygone_contour):
    """Test si un point à l'extérieur d'un polygone connexe retourne False."""
    point_exterieur = PointGeographique(44.0, 6.0, "WGS84")  # À l'extérieur de polygone2
    assert polygone_contour.point_dans_polygone(point_exterieur, polygone_contour.get_contour()[1].get_connexe()[0]) is False

# Tests pour la méthode point_sur_segment de la classe Contour
def test_point_sur_segment_horizontal(polygone_contour):
    """Test si un point sur un segment horizontal retourne True."""
    point_horizontal = PointGeographique(5.1, 44.05, "WGS84")  # Sur un segment horizontal
    p1 = (44.05, 5.1)
    p2 = (44.1, 5.1)

    result = polygone_contour.point_sur_segment(point_horizontal, p1, p2)
    assert result is True, f"Expected True, but got {result}"

def test_point_sur_segment_vertical(polygone_contour):
    """Test si un point sur un segment vertical retourne True."""
    point_vertical = PointGeographique(5.1, 44.1, "WGS84")  # Sur un segment vertical
    p1 = (44.1, 5.1)  # Premier point du segment
    p2 = (44.1, 5.2)  # Deuxième point du segment

    result = polygone_contour.point_sur_segment(point_vertical, p1, p2)
    assert result is True, f"Expected True, but got {result}"

def test_point_non_sur_segment(polygone_contour):
    """Test si un point en dehors du segment retourne False."""
    point_exterieur = PointGeographique(44.05, 5.2, "WGS84")  # En dehors du segment
    p1 = (44.05, 5.1)  # Premier point du segment
    p2 = (44.1, 5.1)   # Deuxième point du segment

    result = polygone_contour.point_sur_segment(point_exterieur, p1, p2)
    assert result is False, f"Expected False, but got {result}"

def test_point_sur_segment_invalide(polygone_contour):
    """Test si un point sur un segment invalide retourne False."""
    point_invalide = PointGeographique(44.05, 5.1, "WGS84")  # Sur un segment invalide
    p1 = (44.05, 5.1)  # Premier point du segment
    p2 = (44.1, 5.1)   # Deuxième point du segment

    result = polygone_contour.point_sur_segment(point_invalide, p1, p2)
    assert result is False, f"Expected False, but got {result}"

# Tests pour la méthode estDansPolygone de la classe Contour
def test_est_dans_polygone_interieur(polygone_contour):
    """Test si un point à l'intérieur d'un polygone connexe retourne True."""
    point_interieur = PointGeographique(44.06, 5.15, "WGS84")  # À l'intérieur de polygone2
    assert polygone_contour.estDansPolygone(point_interieur) is True

def test_est_dans_polygone_bord(polygone_contour):
    """Test si un point sur le bord d'un polygone connexe retourne True."""
    point_bord = PointGeographique(44.05, 5.1, "WGS84")  # Sur le bord de polygone2
    assert polygone_contour.estDansPolygone(point_bord) is True

def test_est_dans_polygone_exterieur(polygone_contour):
    """Test si un point à l'extérieur du polygone retourne False."""
    point_exterieur = PointGeographique(44.2, 5.2, "WGS84")
    assert polygone_contour.estDansPolygone(point_exterieur) is False

def test_est_dans_polygone_bordure(polygone_contour):
    """Test si un point sur la bordure du polygone retourne True."""
    point_bordure = PointGeographique(44.0, 5.0, "WGS84")  # Un des points du polygone
    assert polygone_contour.estDansPolygone(point_bordure) is True

