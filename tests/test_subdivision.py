import pytest
from src.business_object.subdivision import Subdivision
from src.business_object.Polygones.contour import Contour
from src.business_object.Polygones.connexe import Connexe
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire
from src.business_object.pointgeographique import PointGeographique


@pytest.fixture
def subdivision_kwargs():
    point1 = PointGeographique(44.0, 5.0, "WGS84")
    point2 = PointGeographique(44.0, 6.0, "WGS84")
    point3 = PointGeographique(43.5, 6.0, "WGS84")
    point4 = PointGeographique(43.5, 5.0, "WGS84")
    polygone1 = PolygonePrimaire([point1, point2, point3, point4])
    connexe1 = Connexe([polygone1])

    contour = Contour([connexe1])
    return dict(
        id="351470",
        nom="Bruz",
        annee=2024,
        polygones=contour
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
