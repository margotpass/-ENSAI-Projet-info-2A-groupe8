import pytest
from src.business_object.pointgeographique import PointGeographique

# Données de la commune avec un point spécifique
data_commune = {
    "commune_id": "COMMUNE_0000000009738132",
    "commune_name": "Guerlesquin",
    "region": "GUERLESQUIN",
    "code_commune": 29067,
    "type": "Commune simple",
    "point": [-3.5993130297423552, 48.558479060419984],
    "type_coord": "WGS84"
}

@pytest.fixture

def point_commune():
    """Fixture pour créer un point géographique à partir des coordonnées de la commune"""
    latitude, longitude = data_commune["point"][1], data_commune["point"][0]  # On extrait latitude et longitude
    typecoordonnees = data_commune["type_coord"]
    return PointGeographique(latitude, longitude, typecoordonnees)

def test_point_geographique_commune(point_commune):
    """Test pour vérifier l'initialisation d'un point géographique"""
    assert isinstance(point_commune, PointGeographique)
    assert point_commune.latitude == 48.558479060419984
    assert point_commune.longitude == -3.5993130297423552
    assert point_commune.typecoordonnees == "WGS84"

def test_conversion_lamb93_to_wgs84():
    """Test pour vérifier la conversion des coordonnées Lambert 93 à WGS84"""
    point_lamb93 = PointGeographique(651000, 6863000, "Lamb93") # Longitude en premier, puis latitude
    print(f"Coordonnées avant conversion: Latitude = {point_lamb93.latitude}, Longitude = {point_lamb93.longitude}")

    # Appel de la conversion
    point_lamb93.convertir_type_coordonnees()

    # Vérifie que les coordonnées ont bien été transformées en WGS84
    expected_lat = 48.86516571317747
    expected_long = 2.3320684023104286
    print(f"Latitude obtenue: {point_lamb93.latitude}, Longitude obtenue: {point_lamb93.longitude}")
    assert abs(point_lamb93.latitude - expected_lat) < 1e-5, f"Erreur dans la latitude: {point_lamb93.latitude}"
    assert abs(point_lamb93.longitude - expected_long) < 1e-5, f"Erreur dans la longitude: {point_lamb93.longitude}"

