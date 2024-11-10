from src.business_object.Polygones.connexe import Connexe
from src.dao2.polygonedao import PolygoneDAO
from src.dao.db_connection import DBConnection


class ConnexeDAO:
    def creer_connexe(self, liste_polygones):
        """Crée un objet Connexe à partir d'une liste de polygones."""
        polygone_dao = PolygoneDAO()
        polygones = [polygone_dao.creer_polygone(poly) for poly in liste_polygones]
        return Connexe(polygones)

    def ajouter_connexe(self, connexe):
        """Ajoute un Connexe dans la base de données."""
        polygone_dao = PolygoneDAO()
        polygones_ids = [polygone_dao.ajouter_polygone(poly) for poly in connexe.polygones]

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO geodata.Connexes (polygones) VALUES (%s) RETURNING id",
                    (polygones_ids,)
                )
                connexe.id = cursor.fetchone()[0]
                return connexe.id
