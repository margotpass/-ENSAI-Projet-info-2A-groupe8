import pytest
from src.business_object.subdivision.commune import Commune


# Test méthode __init__()
@pytest.mark.parametrize(
    'kwargs, type_erreur, message_erreur',
    [
        ({'ID_CO': 35000}, TypeError, "L'ID doit être un str"),

        ({'NOM_M': 2}, TypeError, "Le nom doit être un str"),

        ({'INSEE_COM': [35000]}, TypeError, "Le code INSEE de la commune doit"
         " être un str"),

        ({'STATUT': 5.0}, TypeError, "Le statut doit être un str"),

        ({'INSEE_CAN': 3530.03}, TypeError, "Le code INSEE du canton doit "
         "être un str"),

        ({'INSEE_ARR': 353}, TypeError, "Le code INSEE de l'arrondissement"
         " doit être un str"),

        ({'INSEE_DEP': 35}, TypeError, "Le code INSEE du département doit être"
         " un str"),

        ({'INSEE_REG': 53.0}, TypeError, "Le code INSEE de la région doit être"
         " un str"),

        ({'SIREN_EPCI': [53.0]}, TypeError, "Le code SIREN doit être un str"),

        ({'Polygons': [[9.0], 'Polygons']}, TypeError, "L'attribut Polygons"
         " doit être un dictionnaire")
    ]
)
def test_arrondissement_init(commune_kwargs, kwargs, type_erreur,
                             message_erreur):
    commune_kwargs.update(**kwargs)
    with pytest.raises(type_erreur, match=message_erreur):
        Commune(**commune_kwargs)
