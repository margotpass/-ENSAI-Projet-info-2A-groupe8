from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.services.subdivision_service import SubdivisionService
from src.services.localisation_service import LocalisationService
from src.business_object.pointgeographique import PointGeographique
from src.services.fichier_service import FichierService


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

        print("\n" + "-" * 50 + "\nMenu Utilisateur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Choississez ce que vous souhaitez faire : ",
            choices=[
                "Obtenir une subdivision selon un code",
                "Obtenir une subdivision selon un point géographique",
                "Obtenir un fichier regroupant les différentes subdivisions selon un point géographique",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass # en gros là il va retourner à l'accueil

            case "Obtenir une subdivision selon un code":
                id = inquirer.text(message="Entrez le code de la subdivision dont vous souhaitez connaître le nom : ").execute()
                type = inquirer.text(message="Entrez le niveau de la subdivision (commune, département, etc.)").execute()
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) :").execute()
                result = SubdivisionService().chercherSubdivisionParID(type, id, annee if annee else None)
                return MenuUtilisateur(result)


            case "Obtenir une subdivision selon un point géographique":
                latitude = inquirer.text(message="Entrez la première coordonnée de votre point (latitude) : ").execute()
                longitude = inquirer.text(message="Entrez la deuxième coordonnée de votre point (longitude) : ").execute()
                type_subdivision = inquirer.text(message="Choisissez le type de subdivision parmi : Arrondissement,"
                                                 " Canton, Commune, Departement, EPCI et Region : ").execute()
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) : ").execute()
                coord = inquirer.text(message="Entrez le type de coordonnées que vous utilisez (si WGS84, vous pouvez laisser vide) : ").execute()
                point = PointGeographique(float(latitude), float(longitude), coord if coord else "WGS84")
                result = LocalisationService().localiserPointDansSubdivision(point, type_subdivision, annee if annee else None)
                return MenuUtilisateur(result)
            
            case "Obtenir un fichier regroupant les différentes subdivisions selon un point géographique":
                liste_coordonnees = inquirer.text(message = "Entrez la liste des points géographiques de type []: ").execute()
                type_subdivision = inquirer.text(message ="Choisissez le type de subdivision parmi : Arrondissement,"
                                                 " Canton, Commune, Departement, EPCI et Region : ").execute()  
                annee = inquirer.text(message="Entrez l'année si vous le souhaitez (laissez vide sinon) : ").execute()            
                result = FichierService().mettre_reponse_dans_csv(liste_coordonnees, type_subdivision, annee if annee else None) 
                return MenuUtilisateur(result)
