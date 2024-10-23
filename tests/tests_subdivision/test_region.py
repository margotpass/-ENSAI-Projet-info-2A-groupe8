import pytest
from src.business_object.subdivisions.region import Region


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'INSEE_REG': 53}, TypeError, "Le code INSEE de la région doit être"
         " un str"),
    ]
)
def test_canton_init(region_kwargs, kwargs, type_erreur,
                     message_erreur):
    region_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Region(**region_kwargs)
