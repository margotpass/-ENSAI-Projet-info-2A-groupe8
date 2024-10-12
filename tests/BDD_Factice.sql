-- Création de la table Commune

CREATE TABLE Commune(
    ID_co PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    INSEE_COM VARCHAR,
    STATUT VARCHAR,
    INSEE_CAN int,
    INSEE_ARR int,
    INSEE_DEP int,
    INSEE_REG int,
    SIREN_EPCI int,
    Polygons JSON
)

-- Création de la table Département

CREATE TABLE Departement(
    ID_d PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    INSEE_DEP VARCHAR,
    INSEE_REG int,
    Polygons JSON
)

-- Création de la table Arrondissement

CREATE TABLE Arrondissement(
    ID_a PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    INSEE_ARR int,
    INSEE_DEP int,
    INSEE_REG int,
    Polygons JSON
)

-- Creation de la table Canton

CREATE TABLE Canton(
    ID_ca PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    INSEE_CAN int,
    INSEE_DEP int,
    INSEE_REG int,
    Polygons JSON
)

-- Création de la table Région

CREATE TABLE Region(
    ID_r PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    INSEE_REG int,
    Polygons JSON
)


-- Création de la table EPCI

CREATE TABLE EPCI(
    ID_epci PRIMARY KEY AUTO_INCREMENT,
    NOM_M VARCHAR,
    NATURE VARCHAR,
    SIREN_EPCI int,
    Polygons JSON
)