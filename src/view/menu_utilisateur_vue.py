from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.services.subdivision_service import SubdivisionService
from src.services.localisation_service import LocalisationService
from src.business_object.pointgeographique import PointGeographique
from src.services.fichier import Fichier


class MenuUtilisateur(VueAbstraite):
    """Vue du menu du utilisateur

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

        print("\n" + "-" * 50 + "\nMenu Utilisateur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Choississez ce que vous souhaitez faire : ",
            choices=[
                "Obtenir une subdivision selon un code",
                "Obtenir une subdivision selon un point géographique",
                #"Obtenir un fichier regroupant les différentes subdivisions selon un point géographique",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass # Retourner à l'accueil

            case "Obtenir une subdivision selon un code":
                dep = None
                id = inquirer.text(message="Entrez le code de la subdivision dont vous souhaitez connaître le nom (s'il s'agit d'un Arrondissement, "
                                   "merci de rentrer le numéro de l'arrondissement au sein du département et non le code INSEE (par exemple, si vous "
                                   "souhaitez connaître le nom du premier arrondissement de l'Ille-et-Vilaine, rentrez 1)): ").execute()
                type = inquirer.text(message="Entrez le niveau de la subdivision parmi : Arrondissement,"
                                                 " Canton, Commune, Departement, EPCI et Region : ").execute()
                if type == "Arrondissement":
                    dep = inquirer.text(message="Entrez le code insee du département : ").execute()
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) :").execute()
                result = SubdivisionService().chercherSubdivisionParID(type, id, annee if annee else None,  dep)
                return MenuUtilisateur(result)


            case "Obtenir une subdivision selon un point géographique":
                latitude = inquirer.text(message="Entrez la première coordonnée de votre point (latitude) : ").execute()
                longitude = inquirer.text(message="Entrez la deuxième coordonnée de votre point (longitude) : ").execute()
                type_subdivision = inquirer.text(message="Choisissez le type de subdivision parmi : Arrondissement,"
                                                 " Canton, Commune, Departement, EPCI et Region : ").execute()
                if type_subdivision == "Arrondissement" :
                    dep = inquirer.text(message="Entrez le code insee du département : ").execute()
                else :
                    dep=None
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) : ").execute()
                coord = inquirer.text(message="Entrez le type de coordonnées que vous utilisez (si WGS84, vous pouvez laisser vide) : ").execute()
                point = PointGeographique(float(latitude), float(longitude), coord if coord else "WGS84")
                result = LocalisationService().localiserPointDansSubdivision(point, type_subdivision, dep, annee if annee else None)
                return MenuUtilisateur(result)
"""                
            case "Obtenir un fichier regroupant les différentes subdivisions selon un point géographique":
                fichier = inquirer.text("Entrez la liste des points géographiques : ").execute()

                fichier_genere = Fichier().obtenir_fichier(fichier, format) #méthode pas encore créée donc faire attention à son nom
                return fichier_genere
"""


