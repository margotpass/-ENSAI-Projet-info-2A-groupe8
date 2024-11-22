import os
import fiona
from src.dao2.pointgeographiquedao import PointGeographiqueDAO
from src.dao2.polygonedao import PolygoneDAO
from src.dao2.connexedao import ConnexeDAO
from src.dao2.contourdao import ContourDAO
from src.dao2.subdivisiondao import SubdivisionDAO


class ShapefileProcessor:
    """
    Classe pour traiter un shapefile et enregistrer les données en base.
    """

    def __init__(self, type_subdivision: str, chemin_shapefile: str):
        """
        Initialise le processeur de shapefile.

        :param type_subdivision: Type de subdivision à traiter.
        :param chemin_shapefile: Chemin vers le fichier shapefile.
        """
        self.type_subdivision = type_subdivision
        self.chemin_shapefile = chemin_shapefile
        self.point_dao = PointGeographiqueDAO()
        self.polygone_dao = PolygoneDAO()
        self.contour_dao = ContourDAO()
        self.subdivision_dao = SubdivisionDAO()
        self.connexe_dao = ConnexeDAO()

    def traiter_shapefile(self):
        """
        Traite le shapefile pour créer des subdivisions et les enregistrer.
        """
        with fiona.open(self.chemin_shapefile, 'r') as shapefile:
            for feature in shapefile:
                geometry = feature['geometry']
                properties = feature['properties']
                geom_type = geometry['type']
                # geom_type Peut être 'Polygon' ou 'MultiPolygon'

                if geom_type == 'Polygon':
                    connexe = self._creer_connexe_avec_polygones(
                        geometry['coordinates']
                    )
                    contour = self.contour_dao.creer_contour([connexe])

                elif geom_type == 'MultiPolygon':
                    liste_connexes = [
                        self._creer_connexe_avec_polygones(polygone_coords)
                        for polygone_coords in geometry['coordinates']
                    ]
                    contour = self.contour_dao.creer_contour(liste_connexes)

                id_value = properties['ID']  # Utiliser l'ID tel quel

                subdivision = self.subdivision_dao.creer_subdivision(
                    type_subdivision=self.type_subdivision,
                    id=id_value,
                    nom=properties.get('NOM'),
                    annee=2024,
                    insee_com=properties.get('INSEE_COM'),
                    insee_can=properties.get('INSEE_CAN'),
                    insee_arr=properties.get('INSEE_ARR'),
                    insee_dep=properties.get('INSEE_DEP'),
                    insee_reg=properties.get('INSEE_REG'),
                    siren_epci=properties.get('SIREN_EPCI')
                    or properties.get('CODE_SIREN'),
                    polygones=contour
                )

                self.subdivision_dao.ajouter_subdivision(subdivision)

    def _creer_connexe_avec_polygones(self, polygone_coords):
        """
        Crée un objet Connexe contenant des PolygonePrimaire pour chaque anneau

        :param polygone_coords: Coordonnées des polygones.
        :return: Objet Connexe.
        """
        liste_polygones = []
        for anneau_coords in polygone_coords:
            points = [
                self.point_dao.creer_point(coord[1], coord[0])
                for coord in anneau_coords
            ]
            polygone = self.polygone_dao.creer_polygone(points)
            liste_polygones.append(polygone)
        return self.connexe_dao.creer_connexe(liste_polygones)


# Exemple d'utilisation
if __name__ == "__main__":
    DOSSIER_DONNEES = os.path.join(
        "Z:", "Desktop", "Projet Info",
        "ADMIN-EXPRESS_3-2__SHP_WGS84G_FRA_2024-08-26",
        "ADMIN-EXPRESS", "1_DONNEES_LIVRAISON_2024-08-00122",
        "ADE_3-2_SHP_WGS84G_FRA-ED2024-08-26"
    )

    NOM_FICHIER_SHAPEFILE = "REGION.shp"
    CHEMIN_SHAPEFILE = os.path.join(DOSSIER_DONNEES, NOM_FICHIER_SHAPEFILE)

    processeur = ShapefileProcessor("REGION", CHEMIN_SHAPEFILE)
    processeur.traiter_shapefile()
