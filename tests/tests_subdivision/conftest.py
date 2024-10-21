import pytest


@pytest.fixture
def arrondissement_kwargs():
    return dict(
        ID_A="00 35 3",
        NOM_M="arrondissement de Rennes",
        INSEE_ARR="35 3",
        INSEE_DEP="35",
        INSEE_REG="53",
        Polygons={'coord': [1.2, 5.1], 'type': 'Polygons'}
        )


@pytest.fixture
def canton_kwargs():
    return dict(
        ID_CA="003518",
        INSEE_CAN="3518",
        INSEE_DEP="35",
        INSEE_REG="53",
        Polygons={'coord': [1.2, 9], 'type': 'Polygons'}
        )


@pytest.fixture
def commune_kwargs():
    return dict(
        ID_CO="003500",
        NOM_M="Rennes",
        INSEE_COM="35000",
        STATUT="ville",
        INSEE_CAN="3518",
        INSEE_ARR="35 3",
        INSEE_DEP="35",
        INSEE_REG="53",
        SIREN_EPCI="243500139",
        Polygons={'coord': [1.2, 5.3], 'type': 'Polygons'}
        )


@pytest.fixture
def departement_kwargs():
    return dict(
        ID_D="0035",
        NOM_M="Ille-et-Vilaine",
        INSEE_DEP="35",
        INSEE_REG="53",
        Polygons={'coord': [1.2, 19], 'type': 'Polygons'}
        )


@pytest.fixture
def epci_kwargs():
    return dict(
        ID_E="00243500",
        SIREN="243500139",
        NOM="Rennes Métropole",
        NATURE="Agglomération",
        Polygons={'coord': [1, 6], 'type': 'Polygons'}
        )


@pytest.fixture
def region_kwargs():
    return dict(
        ID_R="0053",
        NOM_M="Bretagne",
        INSEE_REG="53",
        Polygons={'coord': [1.2, 39], 'type': 'Polygons'}
        )
