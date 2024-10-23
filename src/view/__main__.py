import dotenv
from vue_abstraite import VueAbstraite


if __name__ == "__main__":
    # On charge les variables d'envionnement
    dotenv.load_dotenv(override=True)

    vue_courante = VueAbstraite("Bienvenue")

    while vue_courante:

        # Affichage du menu
        vue_courante.afficher()

        # Affichage des choix possibles
        vue_courante = vue_courante.choisir_menu()

    # Lorsque l on quitte l application
    print("----------------------------------")
    print("Au revoir")
