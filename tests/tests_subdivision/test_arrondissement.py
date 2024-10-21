import pytest
from src.business_object.subdivision.arrondissement import Arrondissement


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'ID_A': 353}, TypeError, "L'ID doit être un str"),

        ({'NOM_M': 2}, TypeError, "Le nom de l'arrondissement doit être un "
         "str"),

        ({'INSEE_ARR': 353}, TypeError, "Le code INSEE de l'arrondissement"
         " doit être un str"),

        ({'INSEE_DEP': 35}, TypeError, "Le code INSEE du département doit être"
         " un str"),

        ({'INSEE_REG': 53.0}, TypeError, "Le code INSEE de la région doit être"
         " un str"),

        ({'Polygons': [9.0, 'Polygons']}, TypeError, "L'attribut Polygons doit"
         " être un dictionnaire")
    ]
)
def test_arrondissement_init(arrondissement_kwargs, kwargs, type_erreur,
                             message_erreur):
    arrondissement_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Arrondissement(**arrondissement_kwargs)
