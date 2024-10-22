import pytest
from src.business_object.subdivisions.departement import Departement


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'INSEE_DEP': [35]}, TypeError, "Le code INSEE du département doit"
         " être un str"),

        ({'INSEE_REG': 53}, TypeError, "Le code INSEE de la région doit être"
         " un str"),
    ]
)
def test_canton_init(departement_kwargs, kwargs, type_erreur,
                     message_erreur):
    departement_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Departement(**departement_kwargs)
