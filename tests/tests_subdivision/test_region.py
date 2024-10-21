import pytest
from src.business_object.subdivision.region import Region


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'ID_R': 53}, TypeError, "L'identifiant doit être un str"),

        ({'NOM_M': ["Bretagne"]}, TypeError, "Le nom de la région doit être"
         " un str"),

        ({'INSEE_REG': 53}, TypeError, "Le code INSEE de la région doit être"
         " un str"),

        ({'Polygons': [5.0, 'Polygons']}, TypeError, "L'attribut Polygons"
         " doit être un dictionnaire")
    ]
)
def test_canton_init(region_kwargs, kwargs, type_erreur,
                     message_erreur):
    region_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Region(**region_kwargs)
