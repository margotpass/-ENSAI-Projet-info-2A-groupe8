class Fichier:
    def __init__(self, nom, format, cheminFichier):
        if not isinstance(nom, str):
            raise TypeError("Le nom du fichier doit être un str")
        
        if not isinstance(format,str):
            raise TypeError("Le format du fichier doit être un str")
        
        if (format!="csv"):
            raise ValueError("Le format du fichier doit être csv")
        
        if not isinstance(cheminFichier, str):
            raise TypeError("Le cheminFichier doit être une instance de str")
        
        self.nom = nom
        self.format = format
        self.cheminFichier = cheminFichier

    def importer(self):
        #retourne une liste de point géographique
        pass

    def exporter(self, map, subdivision):
        pass
