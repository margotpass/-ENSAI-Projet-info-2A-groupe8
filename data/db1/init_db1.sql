DROP SCHEMA IF EXISTS geodata2 CASCADE;
CREATE SCHEMA geodata2;

--------------------------------------------------------------
-- Canton
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.canton CASCADE;
CREATE TABLE geodata2.canton (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    insee_can TEXT,
    insee_dep TEXT,
    insee_reg TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);

--------------------------------------------------------------
-- EPCI
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.epci CASCADE;
CREATE TABLE geodata2.epci (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    code_siren TEXT,
    nom TEXT NOT NULL,
    nature TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);

--------------------------------------------------------------
-- Région
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.region CASCADE;
CREATE TABLE geodata2.region (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    nom TEXT NOT NULL,
    nom_m TEXT,
    insee_reg TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);

--------------------------------------------------------------
-- Département
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.departement CASCADE;
CREATE TABLE geodata2.departement (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    nom TEXT NOT NULL,
    nom_m TEXT,
    insee_dep TEXT,
    insee_reg TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);

--------------------------------------------------------------
-- Arrondissement
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.arrondissement CASCADE;
CREATE TABLE geodata2.arrondissement (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    nom TEXT NOT NULL,
    nom_m TEXT,
    insee_arr TEXT,
    insee_dep TEXT,
    insee_reg TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);

--------------------------------------------------------------
-- Commune
--------------------------------------------------------------

DROP TABLE IF EXISTS geodata2.commune CASCADE;
CREATE TABLE geodata2.commune (
    serial_id SERIAL PRIMARY KEY,
    id TEXT NOT NULL,
    nom TEXT NOT NULL,
    nom_m TEXT,
    insee_com TEXT,
    statut TEXT,
    population INTEGER,
    insee_can TEXT,
    insee_arr TEXT,
    insee_dep TEXT,
    insee_reg TEXT,
    siren_epci TEXT,
    geom_type TEXT,
    geom_coordinates JSON
);
