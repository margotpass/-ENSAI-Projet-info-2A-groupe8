from src.dao.db_connection import DBConnection

# Ouverture de la connexion à la base de données
connection = DBConnection().connection

with connection.cursor() as cursor:
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS geodata;

        CREATE TABLE IF NOT EXISTS geodata.Points (
            id SERIAL PRIMARY KEY,
            lat FLOAT4 NOT NULL,
            long FLOAT4 NOT NULL,
            UNIQUE (lat, long)
        );

        CREATE TABLE IF NOT EXISTS geodata.Polygones (
            id SERIAL PRIMARY KEY,
            somme_coordonnees FLOAT4 NOT NULL
        );

        CREATE TABLE IF NOT EXISTS geodata.Connexes (
            id SERIAL PRIMARY KEY,
            somme_sommes_controle FLOAT4 NOT NULL
        );

        CREATE TABLE IF NOT EXISTS geodata.Contours (
            id SERIAL PRIMARY KEY,
            annee INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS geodata.Subdivision (
            id VARCHAR(100) NOT NULL,
            nom VARCHAR(50) NOT NULL,
            type VARCHAR(15) NOT NULL,
            insee_com CHAR(5),
            insee_can CHAR(5),
            insee_arr CHAR(4),
            insee_dep CHAR(3),
            insee_reg CHAR(2),
            siren_epci CHAR(9),
            UNIQUE (nom, type, insee_com, insee_can, insee_arr, insee_dep, insee_reg, siren_epci)
        );

        CREATE TABLE IF NOT EXISTS geodata.Polygone_Point (
            id_polygone INTEGER NOT NULL REFERENCES geodata.Polygones(id) ON DELETE CASCADE,
            id_point INTEGER NOT NULL REFERENCES geodata.Points(id) ON DELETE CASCADE,
            ordre INTEGER NOT NULL,
            PRIMARY KEY (id_polygone, id_point)
        );

        CREATE TABLE IF NOT EXISTS geodata.Connexe_Polygone (
            id_connexe INTEGER NOT NULL REFERENCES geodata.Connexes(id) ON DELETE CASCADE,
            id_polygone INTEGER NOT NULL REFERENCES geodata.Polygones(id) ON DELETE CASCADE,
            ordre INTEGER NOT NULL,
            PRIMARY KEY (id_connexe, id_polygone)
        );

        CREATE TABLE IF NOT EXISTS geodata.Contour_Connexe (
            id_contour INTEGER NOT NULL REFERENCES geodata.Contours(id) ON DELETE CASCADE,
            id_connexe INTEGER NOT NULL REFERENCES geodata.Connexes(id) ON DELETE CASCADE,
            ordre INTEGER NOT NULL,
            PRIMARY KEY (id_contour, id_connexe)
        );

        CREATE TABLE IF NOT EXISTS geodata.Subdivision_Contour (
            id_subdivision INTEGER NOT NULL REFERENCES geodata.Subdivision(id) ON DELETE CASCADE,
            id_contour INTEGER NOT NULL REFERENCES geodata.Contours(id) ON DELETE CASCADE,
            annee INTEGER NOT NULL,
            PRIMARY KEY (id_subdivision, annee)  -- Contrainte d'unicité par subdivision et année
        );
    """)

# Commit des modifications et fermeture de la connexion
connection.commit()
print("Base de données créée et connexion fermée.")
