from src.business_object.subdivision import Subdivision
from src.dao.subdivisiondao import SubdivisionDAO
from src.services.subdivision_service import SubdivisionService
from unittest.mock import MagicMock


def test_trouver_code_succes():
    """ trouver le bon code """

    # GIVEN
    typeSubdivision, id, annee = "Departement", "53", 2024
    nom = "MAYENNE"
    SubdivisionDAO().find_by_code_insee = MagicMock(return_value=True)

    # WHEN
    subd = SubdivisionService().chercherSubdivisionParID(typeSubdivision, id, annee)

    # THEN
    assert subd == nom

