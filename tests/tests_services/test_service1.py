from unittest.mock import MagicMock
from src.dao.subdivisiondao import SubdivisionDAO
from src.services.subdivision_service import SubdivisionService


def test_trouver_code_succes():
    """ trouver le bon code """

    # GIVEN
    type_subdivision, id, annee = "Departement", "53", 2024
    nom = "MAYENNE"
    SubdivisionDAO().find_by_code_insee = MagicMock(return_value=True)

    # WHEN
    subd = (
        SubdivisionService().chercherSubdivisionParID(
            type_subdivision,
            id,
            annee)
    )

    # THEN
    assert subd == nom
