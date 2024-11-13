import fiona
from src.dao2.pointgeographiquedao import PointGeographiqueDAO
from src.dao2.polygonedao import PolygoneDAO
from src.dao2.connexedao import ConnexeDAO
from src.dao2.contourdao import ContourDAO
from src.dao2.subdivisiondao import SubdivisionDAO
import os


def traiter_shapefile(type_subdivision, chemin_shapefile):
    """Traite un shapefile pour créer des subdivisions et les enregistrer dans la base de données."""
    point_dao = PointGeographiqueDAO()
    polygone_dao = PolygoneDAO()
    contour_dao = ContourDAO()
    subdivision_dao = SubdivisionDAO()

    # Ouvrir le shapefile avec Fiona
    with fiona.open(chemin_shapefile, 'r') as shapefile:
        for feature in shapefile:
            geometry = feature['geometry']
            properties = feature['properties']
            geom_type = geometry['type']  # Peut être 'Polygon' ou 'MultiPolygon'

            if geom_type == 'Polygon':
                # Si c'est un Polygon, il ne devrait y avoir qu'un seul contour
                connexe = creer_connexe_avec_polygones(geometry['coordinates'], point_dao, polygone_dao)
                contour = contour_dao.creer_contour([connexe])  # Liste avec un seul Connexe

            elif geom_type == 'MultiPolygon':
                # Si c'est un MultiPolygon, on peut avoir plusieurs contours (connexes)
                liste_connexes = []
                for polygone_coords in geometry['coordinates']:
                    connexe = creer_connexe_avec_polygones(polygone_coords, point_dao, polygone_dao)
                    liste_connexes.append(connexe)
                contour = contour_dao.creer_contour(liste_connexes)  # Liste de plusieurs Connexes

            # Utiliser l'ID tel quel sans modification
            id_value = properties['ID']

            # Créer l'objet Subdivision avec les informations de la feature
            subdivision = subdivision_dao.creer_subdivision(
                type_subdivision=type_subdivision,
                id=id_value,  # Utiliser l'ID tel quel
                nom=properties.get('NOM', None),
                annee=2024,
                insee_com=properties.get('INSEE_COM', None),
                insee_can=properties.get('INSEE_CAN', None),
                insee_arr=properties.get('INSEE_ARR', None),
                insee_dep=properties.get('INSEE_DEP', None),
                insee_reg=properties.get('INSEE_REG', None),
                siren_epci=properties.get('SIREN_EPCI') or properties.get('CODE_SIREN') or None,
                polygones=contour
            )

            # Enregistrer la subdivision dans la base de données
            subdivision_dao.ajouter_subdivision(subdivision)


def creer_connexe_avec_polygones(polygone_coords, point_dao, polygone_dao):
    """
    Crée un objet Connexe contenant des PolygonePrimaire pour chaque anneau du polygone.
    Le premier anneau est l'extérieur et les suivants sont les anneaux intérieurs (trous).
    """
    liste_polygones = []
    connexe_dao = ConnexeDAO()
    for index, anneau_coords in enumerate(polygone_coords):
        points = []
        for coord in anneau_coords:
            # Création des objets PointGeographique pour chaque coordonnée
            point = point_dao.creer_point(coord[1], coord[0])  # Assume longitude, latitude format
            points.append(point)

        # Créer un objet PolygonePrimaire pour cet anneau
        polygone = polygone_dao.creer_polygone(points)
        liste_polygones.append(polygone)

    # Créer un objet Connexe qui regroupe tous les PolygonePrimaire de ce polygone
    return connexe_dao.creer_connexe(liste_polygones)

# Chemin complet vers le dossier où se trouve votre shapefile
dossier_donnees = os.path.join(
    "Z:", "Desktop", "Projet Info",
    "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-08-26",
    "ADMIN-EXPRESS", "1_DONNEES_LIVRAISON_2024-08-00122",
    "ADE_3-2_SHP_WGS84G_FRA-ED2024-08-26"
)

# Spécifiez le nom de votre fichier shapefile ici
nom_fichier_shapefile = "REGION.shp"  # Remplacez par le nom réel du fichier shapefile

chemin_shapefile = os.path.join(dossier_donnees, nom_fichier_shapefile)

# Appel de la fonction pour traiter le shapefile
traiter_shapefile("REGION",chemin_shapefile)
