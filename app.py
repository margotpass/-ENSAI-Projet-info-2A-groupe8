from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List, Optional
from fastapi.responses import FileResponse
from src.services.subdivision_service import SubdivisionService
from src.services.localisation_service import LocalisationService
from src.business_object.pointgeographique import PointGeographique
import csv

# Initialisation de l'application FastAPI
app = FastAPI()

# Initialisation des services
subdivision_service = SubdivisionService()
localisation_service = LocalisationService()

# Fonctionnalité 1 : Recherche d'informations
@app.get("/recherche/{type_subdivision}/{annee}/{id}")
async def recherche_information(type_subdivision: str, annee: int = 2024, id: str = None):
    """
    Recherche les informations pour un type de subdivision (Commune, Canton, Arrondissement, Departement, Region, EPCI)
    et un code INSEE spécifié pour une année donnée, ainsi que les subdivisions de niveau supérieur.
    """
    # Utiliser le service pour obtenir la subdivision demandée
    subdivision = subdivision_service.chercherSubdivisionParID(type_subdivision, id, annee)
    
    # Vérifier que la subdivision est trouvée et contient les informations nécessaires
    if subdivision:
        # Déterminer les types de subdivisions supérieurs
        types_superieurs = determine_types_superieurs(type_subdivision)
        
        # Récupérer les subdivisions de niveau supérieur
        superieurs = []
        for type_sup in types_superieurs:
            code_insee_sup = getattr(subdivision, f"insee_{type_sup.lower()}", None)
            if code_insee_sup:
                sup_subdivision = subdivision_service.chercherSubdivisionParID(type_sup, code_insee_sup, annee)
                if sup_subdivision:
                    superieurs.append({
                        "type": type_sup,
                        "nom": sup_subdivision,
                        "code_insee": code_insee_sup
                    })

        # Construire le résultat avec la subdivision demandée et les subdivisions supérieures
        result = {
            "id": id,
            "nom": subdivision,
            "type": type_subdivision,
            "annee": annee,
            "superieurs": superieurs
        }
        return result
    else:
        raise HTTPException(status_code=404, detail="Subdivision non trouvée")


def determine_types_superieurs(type_subdivision: str) -> List[str]:
    """
    Détermine les types de subdivisions supérieurs pour le type spécifié.
    """
    hierarchy = {
        "Commune": ["Canton", "Arrondissement", "Departement", "Region"],
        "Canton": ["Arrondissement", "Departement", "Region"],
        "Arrondissement": ["Departement", "Region"],
        "Departement": ["Region"],
        "EPCI": [],
        "Region": []
    }
    return hierarchy.get(type_subdivision, [])


# Fonctionnalité 2 : Localisation d'un point géographique
@app.get("/localisation/{type_subdivision}")
async def localisation_point(type_subdivision: str, lat: float, long: float, annee: int = 2024):
    """
    Localise un point géographique (latitude, longitude) dans un niveau spécifié
    pour une année donnée.
    """
    # Créer un objet PointGeographique pour représenter les coordonnées
    point = PointGeographique(latitude=lat, longitude=long)
    
    # Utiliser le service pour localiser la subdivision contenant ce point
    subdivision = localisation_service.localiserPointDansSubdivision(point, type_subdivision, annee)
    
    if subdivision:
        result = {
            "nom": subdivision,
            "annee": annee,
            "coordonnees": {"latitude": lat, "longitude": long}
        }
        return result
    else:
        raise HTTPException(status_code=404, detail="Point non localisé dans une subdivision.")

# Fonctionnalité 3 : Localisation d'un ensemble de points
@app.post("/localisation-liste/")
async def localisation_liste_points(file: UploadFile = File(...), type_subdivision: str = "Commune", annee: int = 2024):
    """
    Localise un ensemble de points fournis dans un fichier CSV pour un niveau géographique
    spécifié et une année donnée.
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
        writer.writerow(["Latitude", "Longitude", "Subdivision", "Code INSEE", "Annee"])  # En-têtes du fichier

        for row in reader:
            lat = float(row["latitude"])
            long = float(row["longitude"])
            point = PointGeographique(latitude=lat, longitude=long)
            
            # Utiliser le service pour localiser chaque point dans la subdivision demandée
            subdivision = localisation_service.localiserPointDansSubdivision(point, type_subdivision, annee)
            
            if subdivision:
                writer.writerow([lat, long, subdivision, annee])
            else:
                writer.writerow([lat, long, "Non localisé", "", annee])

    return FileResponse(path=file_path, filename="localisation_resultats.csv", media_type="text/csv")

# Lancer l'API avec uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
