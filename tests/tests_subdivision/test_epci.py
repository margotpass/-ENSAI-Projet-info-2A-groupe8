import pytest
from src.business_object.subdivisions.epci import Epci


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'SIREN': [3522]}, TypeError, "Le code SIREN doit être un str"),

        ({'NATURE': ["Agglomération"]}, TypeError, "La nature de l'EPCI doit"
         " être un str"),
    ]
)
def test_canton_init(epci_kwargs, kwargs, type_erreur,
                     message_erreur):
    epci_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Epci(**epci_kwargs)
