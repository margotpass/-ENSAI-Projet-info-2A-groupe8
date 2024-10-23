import tkinter as tk
from tkinter import Toplevel, PhotoImage, Canvas

# Fonction qui ouvre une la fenêtre recherche d'informations
def open_service_1():
    window_1 = Toplevel(root)  # Crée une nouvelle fenêtre à partir de la fenêtre principale
    window_1.title("Chercher une information")
    window_1.geometry("300x200")
    
    # Ajouter un label dans la nouvelle fenêtre
    label = tk.Label(window_1, text="Chercher une information")
    label.pack(pady=20)
    
    # Bouton pour fermer la nouvelle fenêtre
    close_button = tk.Button(window_1, text="Fermer", command=window_1.destroy)
    close_button.pack(pady=10)

# Fonction qui ouvre une la fenêtre localiser un point
def open_service_2():
    window_2 = Toplevel(root)  # Crée une nouvelle fenêtre à partir de la fenêtre principale
    window_2.title("Localiser un point")
    window_2.geometry("300x200")
    
    # Ajouter un label dans la nouvelle fenêtre
    label = tk.Label(window_2, text="Localiser une information")
    label.pack(pady=20)
    
    # Bouton pour fermer la nouvelle fenêtre
    close_button = tk.Button(window_2, text="Fermer", command=window_2.destroy)
    close_button.pack(pady=10)

# Fonction qui ouvre une la fenêtre localiser un fichier
def open_service_3():
    window_3 = Toplevel(root)  # Crée une nouvelle fenêtre à partir de la fenêtre principale
    window_3.title("Localiser un fichier")
    window_3.geometry("300x200")
    
    # Ajouter un label dans la nouvelle fenêtre
    label = tk.Label(window_3, text="Localiser un fichier")
    label.pack(pady=20)
    
    # Bouton pour fermer la nouvelle fenêtre
    close_button = tk.Button(window_3, text="Fermer", command=window_3.destroy)
    close_button.pack(pady=10)

# Créer la fenêtre principale
root = tk.Tk()
root.title("L'application qui vous dit où vous êtes...")
root.geometry("800x600")

# Charger l'image de fond
background_image = PhotoImage(file="fond_menu_0.png")

# Créer un widget Canvas
canvas = tk.Canvas(root, width=400, height=300)  # L'objet canvas est maintenant créé correctement
canvas.pack(fill="both", expand=True)

# Afficher l'image de fond dans le Canvas
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Créer les boutons
button1 = tk.Button(root, text="Chercher une information", command=open_service_1)
button2 = tk.Button(root, text="Localiser un point", command=open_service_2)
button3 = tk.Button(root, text="Localiser un fichier", command=open_service_3)
button4 = tk.Button(root, text="Quitter", command=root.quit)


# Placer les boutons dans le Canvas
canvas.create_window(400, 200, window=button1)
canvas.create_window(400, 300, window=button2)
canvas.create_window(400, 400, window=button3)
canvas.create_window(400, 550, window=button4)

# Lancer la boucle principale de Tkinter
root.mainloop()