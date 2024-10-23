from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.services.subdivision_service import SubdivisionService
from src.services.localisation_service import LocalisationService
from src.business_object.pointgeographique import PointGeographique
from src.services.fichier import Fichier


class MenuUtilisateur(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Choississez ce que vous souhaitez faire : ",
            choices=[
                "Obtenir une subdivision selon un code",
                #"Obtenir une subdivision selon un point géographique",
                #"Obtenir un fichier regroupant les différentes subdivisions selon un point géographique",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass # en gros là il va retourner à l'accueil

            case "Obtenir une subdivision selon un code":
                id = inquirer.text(message="Entrez le code de la subdivision dont vous souhaitez cnnaître le nom : ").execute()
                type = inquirer.text(message="Entrez le niveau de la subdivision (commune, département, etc.)").execute()
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) :").execute()
                result = SubdivisionService().chercherSubdivisionParID(type, id, annee if annee else None)
                return MenuUtilisateur(result)

"""
            case "Obtenir une subdivision selon un point géographique":
                latitude = inquirer.text("Entrez la première coordonnée de votre point (latitude) : ").execute()
                longitude = inquirer.text("Entrez la deuxième coordonnée de votre point (longitude) : ").execute()
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) : ").execute()
                coord = inquirer.text(message="Entrez le type de coordonnées que vous utilisez (si WGS84, vous pouvez laisser vide) : ").execute()
                point = PointGeographique(float(latitude), float(longitude), coord if coord else "WGS84")
                result = LocalisationService().localiserPointDansSubdivision(point, annee if annee else None)
                return MenuUtilisateur(result)
                
            case "Obtenir un fichier regroupant les différentes subdivisions selon un point géographique":
                fichier = inquirer.text("Entrez le chemin du fichier contenant les points géographiques (CSV) : ").execute()
                if fichier.endswith('.csv'):
                    format = "csv"
                else:
                    print("Format de fichier non supporté. Veuillez fournir un fichier au format csv.")
                    return
                fichier_genere = Fichier().obtenir_fichier(fichier, format) #méthode pas encore créée donc faire attention à son nom
                return fichier_genere
"""
