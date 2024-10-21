import pytest
from src.business_object.subdivision.epci import Epci


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'ID_E': 2351}, TypeError, "L'identifiant doit être un str"),

        ({'NOM': ["Rennes Métropole"]}, TypeError, "Le nom de l'EPCI doit être"
         " un str"),

        ({'SIREN': [3522]}, TypeError, "Le code SIREN doit être un str"),

        ({'NATURE': ["Agglomération"]}, TypeError, "La nature de l'EPCI doit"
         " être un str"),

        ({'Polygons': [5, 'Polygons']}, TypeError, "L'attribut Polygons"
         " doit être un dict")
    ]
)
def test_canton_init(epci_kwargs, kwargs, type_erreur,
                     message_erreur):
    epci_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Epci(**epci_kwargs)
