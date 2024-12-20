import pytest
from src.business_object.subdivisions.canton import Canton


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'INSEE_CAN': 2}, TypeError, "Le code INSEE du canton doit être un"
         " str"),

        ({'INSEE_DEP': [35]}, TypeError, "Le code INSEE du département doit"
         " être"
         " un str"),

        ({'INSEE_REG': 53.0}, TypeError, "Le code INSEE de la région doit être"
         " un str"),
    ]
)
def test_canton_init(canton_kwargs, kwargs, type_erreur,
                     message_erreur):
    canton_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Canton(**canton_kwargs)
