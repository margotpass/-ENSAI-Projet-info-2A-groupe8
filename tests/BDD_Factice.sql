CREATE TABLE Commune(
    id PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50),
    INSEE_ARR int,
    INSEE_DEP int,
    INSEE_REG int,
    polygon FLOAT[]
)