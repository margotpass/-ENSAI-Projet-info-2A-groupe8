import csv
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from src.business_object.pointgeographique import PointGeographique
from src.services.localisation_service import LocalisationService
from src.services.subdivision_service import SubdivisionService

app = FastAPI(
    title="API de Géolocalisation - Vous Êtes Ici",
    description=(
        "Cette API permet de :\n"
        "- Localiser un point géographique et identifier la subdivision "
        "administrative correspondante.\n"
        "- Charger et traiter des fichiers géographiques (CSV, SHP).\n"
        "- Extraire des informations sur des subdivisions administratives "
        "(commune, canton, arrondissement, etc.)."
    ),
    version="1.0.O"
)
subdivision_service = SubdivisionService()


@app.get("/recherche/{type_subdivision}/{id}")
async def rechercher_information(type_subdivision: str, id: str,
                                 annee: int = 2024,
                                 insee_dep: str = None):
    """
    Recherche une subdivision géographique par ID et retourne ses informations.

    Args:
        type_subdivision (str): Le type de subdivision
         (Region, Departement, Commune, etc.).
        id (str): L'ID de la subdivision.
        annee (int): Année de référence (par défaut 2024).
        insee_dep (str, optionnel): Code INSEE du département.

    Returns:
        dict: Informations sur la subdivision trouvée.
    """
    try:
        subdision = subdivision_service.chercherSubdivisionParID(
            type_subdivision, id, annee, insee_dep)
        return subdision
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/localisation")
async def localisation_point(
    type_subdivision: str,
    lat: float,
    long: float,
    annee: int = 2024,
    typecoordonnees: str = "WGS84"
):
    """
    Localise un point géographique (latitude, longitude)
    dans un niveau spécifié
    (Région, Département, Arrondissement, ou Commune) pour une année donnée.

    Args:
        type_subdivision (str): Type de subdivision
         (Region, Departement, Arrondissement, Commune).
        lat (float): Latitude du point.
        long (float): Longitude du point.
        annee (int): Année pour la localisation (défaut : 2024).
        typecoordonnees (str): Type de coordonnées
        (WGS84 ou Lamb93, par défaut WGS84).

    Returns:
        dict: Informations de localisation pour la subdivision spécifiée.
    """
    # Conversion des coordonnées si nécessaire
    if typecoordonnees != "WGS84":
        if typecoordonnees == "Lamb93":
            lat, long = (
                PointGeographique(lat, long, typecoordonnees)
                .convertir_type_coordonnees()
            )
            typecoordonnees = "WGS84"  # Mise à jour après conversion
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Type de coordonnées inconnu : {typecoordonnees}"
            )

    # Création du point géographique
    point = PointGeographique(latitude=lat, longitude=long,
                              typecoordonnees=typecoordonnees)

    # Choisir la méthode de localisation en fonction du type de subdivision
    try:
        service = LocalisationService()

        if type_subdivision in ["Region", "Departement", "Arrondissement"]:
            # Localisation spécifique à une subdivision
            subdivision = service.localiserPointDansSubdivision(
                point,
                type_subdivision,
                annee)
            if not subdivision:
                raise HTTPException(
                    status_code=404,
                    detail="Subdivision introuvable pour le point spécifié.")

            # Construction de la réponse pour les subdivisions
            result = {
                "code_insee": subdivision[0],
                "niveau": type_subdivision,
                "nom": subdivision[1].get("nom") if subdivision[1] else None,
                "annee": annee,
                "coordonnees": {"latitude": lat, "longitude": long}
            }

            # Ajout du code département pour les arrondissements
            if type_subdivision == "Arrondissement":
                result["insee_dep"] = subdivision[2]

            return result

        elif type_subdivision == "Commune":
            # Localisation hiérarchique complète pour les communes
            localisation = service.localiser_point(point, annee)
            return localisation

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Type de subdivision inconnu : {type_subdivision}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/localisation-liste/")
async def localisation_liste_points(
    file: UploadFile = File(...),
    type_subdivision: str = "Commune",
    annee: int = 2024
):
    """
    Localise un ensemble de points fournis dans un fichier CSV pour un niveau
    géographique spécifié et une année donnée.

    Args:
        file (UploadFile): Fichier CSV contenant les points.
        type_subdivision (str): Type de subdivision
         ("Region", "Departement", "Arrondissement", "Commune").
        annee (int): Année pour la localisation (par défaut 2024).

    Returns:
        FileResponse: Fichier CSV avec les résultats de la localisation.
    """
    # Vérifier le format du fichier
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400,
                            detail="Le fichier doit être au format .csv")

    file_path = "localisation_resultats.csv"

    # Lecture du fichier CSV en entrée
    contents = await file.read()
    with open("input.csv", "wb") as input_file:
        input_file.write(contents)

    # Traitement des points
    with open("input.csv", mode="r") as csvfile, \
         open(file_path, mode="w", newline="") as csv_output:
        reader = csv.DictReader(csvfile)
        writer = csv.writer(csv_output)
        writer.writerow(
            ["Latitude", "Longitude", "Code INSEE", "Niveau", "Nom", "Annee"]
            )  # En-têtes du fichier

        service = LocalisationService()

        for row in reader:
            lat = float(row["latitude"])
            long = float(row["longitude"])
            point = PointGeographique(latitude=lat, longitude=long)

            if type_subdivision in ["Region", "Departement", "Arrondissement"]:
                # Utiliser la méthode `localiserPointDansSubdivision`
                subdivision = service.localiserPointDansSubdivision(
                    point,
                    type_subdivision,
                    annee
                )

                if subdivision:
                    code_subdivision = subdivision[0]
                    niveau = type_subdivision
                    nom_subdivision = (
                     subdivision[1]["nom"]
                     if subdivision[1]
                     else "Nom indisponible"
                    )
                    writer.writerow([lat, long, code_subdivision, niveau,
                                    nom_subdivision, annee])
                else:
                    writer.writerow([lat, long, "Non localisé",
                                    type_subdivision, "", annee])

            elif type_subdivision == "Commune":
                # Utiliser la méthode `localiser_point` pour gérer la
                # hiérarchie complète et extraire la commune
                localisation = service.localiser_point(point, annee)

                if "Commune" in localisation and localisation["Commune"]:
                    commune_data = localisation["Commune"]
                    writer.writerow(
                        [
                            lat,
                            long,
                            commune_data["code"],
                            "Commune",
                            commune_data["nom"],
                            annee
                        ]
                    )
                else:
                    writer.writerow(
                        [lat, long, "Non localisé", "Commune", "", annee]
                    )

            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Type de subdivision inconnu : {type_subdivision}"
                )

    # Retourner le fichier CSV avec les résultats
    return FileResponse(path=file_path, filename="localisation_resultats.csv",
                        media_type="text/csv")


@app.get("/zonage/{type_subdivision}/{id}")
async def obtenir_zonage(type_subdivision: str, id: str, annee: int = 2024,
                         dep: str = None):
    """
    Retourne le zonage complet d'une subdivision, y compris ses subdivisions
    supérieures.
    """
    try:
        zonage = subdivision_service.zonage(type_subdivision, id, annee, dep)
        return zonage
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
