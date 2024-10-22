import pytest
from src.business_object.subdivisions.arrondissement import Arrondissement


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'INSEE_ARR': 353}, TypeError, "Le code INSEE de l'arrondissement"
         " doit être un str"),

        ({'INSEE_DEP': 35}, TypeError, "Le code INSEE du département doit être"
         " un str"),

        ({'INSEE_REG': 53.0}, TypeError, "Le code INSEE de la région doit être"
         " un str"),
    ]
)
def test_arrondissement_init(arrondissement_kwargs, kwargs, type_erreur,
                             message_erreur):
    arrondissement_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Arrondissement(**arrondissement_kwargs)
