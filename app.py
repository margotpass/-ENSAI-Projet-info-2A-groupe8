from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from src.business_object.pointgeographique import PointGeographique
from src.services.localisation_service import LocalisationService
from src.services.subdivision_service import SubdivisionService
import csv

app = FastAPI()
subdivision_service = SubdivisionService()


@app.get("/recherche/{type_subdivision}/{id}")
async def rechercher_information(type_subdivision: str, id: str, annee: int = 2024, insee_dep: str = None):
    try:
        subdision = subdivision_service.chercherSubdivisionParID(type_subdivision, id, annee, insee_dep)
        return subdision
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/localisation/{type_subdivision}")
async def localisation_point(type_subdivision: str, lat: float,
                             long: float, annee: int = 2024,
                             typecoordonnees: str = "WGS84"):
    """
    Localise un point géographique (latitude, longitude) dans un niveau
    spécifié pour une année donnée.
    """
    # Convertir les coordonnées si besoin
    if typecoordonnees != "WGS84":
        if typecoordonnees == "Lamb93":
            lat, long = PointGeographique(lat, long, typecoordonnees).convertir_type_coordonnees()
            typecoordonnees = "WGS84"  # Mise à jour du type après conversion
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Type de coordonnées inconnu : {typecoordonnees}"
            )
    # Créer un objet PointGeographique pour représenter les coordonnées
    point = PointGeographique(latitude=lat, longitude=long,
                              typecoordonnees=typecoordonnees)

    # Utiliser le service pour localiser la subdivision contenant ce point
    subdivision = LocalisationService().localiserPointDansSubdivision(
     point,
     type_subdivision,
     annee
    )
    if type_subdivision in ["Commune", "Departement", "Region", "EPCI"]:
        if subdivision:
            result = {
                "code_insee": subdivision[0],
                "niveau": type_subdivision,
                "nom": subdivision[1].get("nom"),
                "annee": annee,
                "coordonnees": {"latitude": lat, "longitude": long}
            }
            return result
    elif type_subdivision in ["Arrondissement", "Canton"]:
        if subdivision:
            result = {
                "code_insee": subdivision[0],
                "insee_dep": subdivision[2],
                "niveau": type_subdivision,
                "nom": subdivision[1].get("nom"),
                "annee": annee,
                "coordonnees": {"latitude": lat, "longitude": long}
            }
            return result

    else:
        raise HTTPException(status_code=404,
                            detail="Point non localisé dans une subdivision.")


@app.post("/localisation-liste/")
async def localisation_liste_points(file: UploadFile = File(...),
                                    type_subdivision: str = "Commune",
                                    annee: int = 2024):
    """
    Localise un ensemble de points fournis dans un fichier CSV pour un niveau
    géographique spécifié et une année donnée.
    """
    # Vérifier le format du fichier
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format .csv")

    file_path = "localisation_resultats.csv"

    # Lecture du fichier CSV en entrée
    contents = await file.read()
    with open("input.csv", "wb") as input_file:
        input_file.write(contents)

    # Traitement des points
    with open("input.csv", mode="r") as csvfile, open(file_path, mode="w", newline="") as csv_output:
        reader = csv.DictReader(csvfile)
        writer = csv.writer(csv_output)
        writer.writerow(["Latitude", "Longitude", "Code INSEE", "niveau","Nom", "Annee"])  # En-têtes du fichier

        for row in reader:
            lat = float(row["latitude"])
            long = float(row["longitude"])
            point = PointGeographique(latitude=lat, longitude=long)

            # Utiliser le service pour localiser chaque point dans la subdivision demandée
            subdivision = LocalisationService().localiserPointDansSubdivision(point, type_subdivision, annee)

            if subdivision:
                code_subdivision = subdivision[0]
                niveau = type_subdivision
                nom_subdivision = subdivision[1]["nom"]
                writer.writerow([lat, long, code_subdivision, niveau, nom_subdivision, annee])
            else:
                writer.writerow([lat, long, "Non localisé", "", annee])

    return FileResponse(path=file_path, filename="localisation_resultats.csv", media_type="text/csv")


@app.get("/zonage/{type_subdivision}/{id}")
async def obtenir_zonage(type_subdivision: str, id: str, annee: int = 2024, dep: str = None):
    """
    Retourne le zonage complet d'une subdivision, y compris ses subdivisions supérieures.
    """
    try:
        zonage = subdivision_service.zonage(type_subdivision, id, annee, dep)
        return zonage
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
