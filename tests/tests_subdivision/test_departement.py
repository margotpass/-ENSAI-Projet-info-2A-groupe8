import pytest
from src.business_object.subdivision.departement import Departement


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'ID_D': 35}, TypeError, "L'ID doit être un str"),

        ({'NOM_M': ["Ille-et-Vilaine"]}, TypeError, "Le nom doit être un str"),

        ({'INSEE_DEP': [35]}, TypeError, "Le code INSEE du département doit"
         " être un str"),

        ({'INSEE_REG': 53}, TypeError, "Le code INSEE de la région doit être"
         " un str"),

        ({'Polygons': [5, 'Polygons']}, TypeError, "L'attribut Polygons"
         " doit être un dictionnaire")
    ]
)
def test_canton_init(departement_kwargs, kwargs, type_erreur,
                     message_erreur):
    departement_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Departement(**departement_kwargs)
