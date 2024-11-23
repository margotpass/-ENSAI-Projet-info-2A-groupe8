from typing import List, Map
from src.business_object.pointgeographique import PointGeographique
from src.business_object.subdivision import Subdivision
import json
import csv


class Fichier:
    """Classe représentant un fichier de données géographiques

    Paramètres:
    -----------
    nom : str
    format : str
    chemin_fichier : str

    retourne:
    -----------
    Fichier
    """
    def __init__(self, nom: str, format: str, chemin_fichier: str):
        """ Initialisation de la classe Fichier """
        self.nom = nom
        self.format = format
        self.chemin_fichier = chemin_fichier

    def convertir(self, format_final: str) -> 'Fichier':
        """
        Convertit un fichier du format actuel à un nouveau format.

        Paramètres:
            format_final (str): Le format final souhaité

        Retourne:
            Fichier: Un nouvel objet Fichier avec le format converti.
        """
        if self.format == format_final:
            print(f"Le fichier est déjà au format {format_final}.")
            return self

        # Effectuer la conversion en fonction des formats
        # supportés (CSV et JSON)
        nouvelle_chemin = self.chemin_fichier.replace(self.format,
                                                      format_final)

        if format_final == 'json':
            self._convertir_csv_en_json(nouvelle_chemin)
        elif format_final == 'csv':
            self._convertir_json_en_csv(nouvelle_chemin)
        else:
            raise ValueError(f"Format {format_final} non supporté.")

        return Fichier(self.nom, format_final, nouvelle_chemin)

    def _convertir_csv_en_json(self, chemin_final: str):
        """Convertit un fichier CSV en format JSON."""
        with open(self.chemin_fichier, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader]

        with open(chemin_final, mode='w') as json_file:
            json.dump(rows, json_file)

    def _convertir_json_en_csv(self, chemin_final: str):
        """Convertit un fichier JSON en format CSV."""
        with open(self.chemin_fichier, mode='r') as json_file:
            data = json.load(json_file)

        with open(chemin_final, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def importer(self) -> List[PointGeographique]:
        """
        Importe des points géographiques depuis le fichier.

        Le format d'entrée attendu est soit CSV, soit JSON.
        Cette méthode retourne une liste d'objets PointGeographique.

        Retourne:
            List[PointGeographique]: Liste d'objets PointGeographique importés.
        """
        points = []

        if self.format == 'csv':
            with open(self.chemin_fichier, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    lat, long = float(row['lat']), float(row['long'])
                    points.append(PointGeographique(lat, long))

        elif self.format == 'json':
            with open(self.chemin_fichier, mode='r') as file:
                data = json.load(file)
                for item in data:
                    lat, long = float(item['lat']), float(item['long'])
                    points.append(PointGeographique(lat, long))

        else:
            raise ValueError(f"Format {self.format} non supporté "
                             f"pour l'importation.")

        return points

    def exporter(self,
                 map_points_subdivisions: Map[PointGeographique, Subdivision]):
        """
        Exporte des points géographiques associés à une subdivision
        dans le fichier.

        Paramètres:
            map_points_subdivisions (Map[PointGeographique, Subdivision]):
                Dictionnaire associant chaque point géographique
                à une subdivision.

        Retourne:
            None
        """
        if self.format == 'csv':
            with open(self.chemin_fichier, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['lat', 'long', 'subdivision'])

                for point, subdivision in map_points_subdivisions.items():
                    writer.writerow([point.latitude, point.longitude,
                                     subdivision.nom])

        elif self.format == 'json':
            data = []
            for point, subdivision in map_points_subdivisions.items():
                data.append({
                    'lat': point.latitude,
                    'long': point.longitude,
                    'subdivision': subdivision.nom
                })

            with open(self.chemin_fichier,
                      mode='w') as file:
                json.dump(data, file)

        else:
            raise ValueError(
                f"Format {self.format} non supporté pour l'exportation."
            )
