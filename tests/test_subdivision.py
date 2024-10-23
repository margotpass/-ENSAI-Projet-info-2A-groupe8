import pytest
from src.business_object.subdivision import Subdivision
from src.business_object.Polygones.contour import Contour


@pytest.fixture
def subdivision_kwargs():
    return dict(
        id="351470",
        nom="Bruz",
        annee=2024,
        polygones=Contour([[[2.0, 5.0, "WGS84"]]])
    )


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'id': 353}, TypeError, "L'identifiant doit être un str"),

        ({'nom': ["Bretagne"]}, TypeError, "Le nom doit être un str"),

        ({'annee': 2024.0}, TypeError, "L'année doit être un int"),

        ({'polygones': [5.0, "Polygons"]}, TypeError, "Le polygone doit être"
         " une instance de Contour"),

        ({'annee': -3}, ValueError, "L'année doit être positive")
    ]
)
def test_subdivision_init(subdivision_kwargs, kwargs, type_erreur,
                          message_erreur):
    subdivision_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Subdivision(**subdivision_kwargs)
