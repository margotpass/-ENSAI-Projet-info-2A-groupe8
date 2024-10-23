import pytest
from unittest.mock import patch, MagicMock
from src.dao.pointgeographiquedao import PointGeographiqueDao


# Fixture pour l'instance DAO
@pytest.fixture
def point_dao():
    return PointGeographiqueDao()

# Fixture pour la requête SQL de création de table
@pytest.fixture
def requete_creation_table():
    return """
    CREATE TABLE IF NOT EXISTS points (
        id SERIAL PRIMARY KEY,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL
    )
    """

# Test pour vérifier que la table est correctement créée
@patch('point_geographique_dao.ConnexionBD')  # Mock ConnexionBD pour les tests
def test_create_table_points(mock_connexion_bd, point_dao, requete_creation_table):
    #GIVEN
    mock_connexion = MagicMock()
    mock_curseur = MagicMock()

    mock_connexion_bd.return_value.connection = mock_connexion
    mock_connexion.cursor.return_value.__enter__.return_value = mock_curseur

    #WHEN
    point_dao.creer_table_points()

    #THEN
    mock_curseur.execute.assert_called_once_with(requete_creation_table)
    mock_connexion.commit.assert_called_once()


if __name__ == "__main__":
    #Effectue le test
    pytest.main([__file__])
