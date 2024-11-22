DROP SCHEMA IF EXISTS geodata CASCADE;
CREATE SCHEMA geodata;

--------------------------------------------------------------
-- Table Connexes
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.connexes CASCADE;
CREATE TABLE geodata.connexes (
    id SERIAL PRIMARY KEY,
    somme_sommes_controle NUMERIC UNIQUE
);

--------------------------------------------------------------
-- Table Polygones
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.polygones CASCADE;
CREATE TABLE geodata.polygones (
    id SERIAL PRIMARY KEY,
    somme_coordonnees NUMERIC UNIQUE
);

--------------------------------------------------------------
-- Table Contours
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.contours CASCADE;
CREATE TABLE geodata.contours (
    id SERIAL PRIMARY KEY,
    annee INTEGER NOT NULL
);

--------------------------------------------------------------
-- Table Points
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.points CASCADE;
CREATE TABLE geodata.points (
    id SERIAL PRIMARY KEY,
    lat NUMERIC NOT NULL,
    long NUMERIC NOT NULL
);

--------------------------------------------------------------
-- Table Subdivision
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.subdivision CASCADE;
CREATE TABLE geodata.subdivision (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    type TEXT NOT NULL,
    insee_com TEXT,
    insee_can TEXT,
    insee_arr TEXT,
    insee_dep TEXT,
    insee_reg TEXT,
    siren_epci TEXT
);

--------------------------------------------------------------
-- Table Connexe_Polygone
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.connexe_polygone CASCADE;
CREATE TABLE geodata.connexe_polygone (
    id_connexe INTEGER REFERENCES geodata.connexes(id) ON DELETE CASCADE,
    id_polygone INTEGER REFERENCES geodata.polygones(id) ON DELETE CASCADE,
    PRIMARY KEY (id_connexe, id_polygone)
);

--------------------------------------------------------------
-- Table Contour_Connexe
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.contour_connexe CASCADE;
CREATE TABLE geodata.contour_connexe (
    id_contour INTEGER REFERENCES geodata.contours(id) ON DELETE CASCADE,
    id_connexe INTEGER REFERENCES geodata.connexes(id) ON DELETE CASCADE,
    ordre INTEGER NOT NULL,
    PRIMARY KEY (id_contour, id_connexe)
);

--------------------------------------------------------------
-- Table Polygone_Point
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.polygone_point CASCADE;
CREATE TABLE geodata.polygone_point (
    id_polygone INTEGER REFERENCES geodata.polygones(id) ON DELETE CASCADE,
    id_point INTEGER REFERENCES geodata.points(id) ON DELETE CASCADE,
    ordre INTEGER NOT NULL,
    PRIMARY KEY (id_polygone, id_point)
);

--------------------------------------------------------------
-- Table Subdivision_Contour
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata.subdivision_contour CASCADE;
CREATE TABLE geodata.subdivision_contour (
    id_subdivision INTEGER REFERENCES geodata.subdivision(id) ON DELETE CASCADE,
    id_contour INTEGER REFERENCES geodata.contours(id) ON DELETE CASCADE,
    PRIMARY KEY (id_subdivision, id_contour)
);
