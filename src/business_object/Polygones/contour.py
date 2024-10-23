from src.business_object.Polygones.connexe import Connexe
from src.business_object.pointgeographique import PointGeographique
from src.business_object.Polygones.polygoneprimaire import PolygonePrimaire


class Contour(Connexe):
    """ Contour contient les connexes
    paramètres:
    contour : List<Connexe>
    """
    def __init__(self, contour=None):
        """ Initialise la liste de connexes """
        if contour is None:
            self.contour = []
        else:
            # Vérifie que chaque élément de la liste est bien une instance de Connexe
            if not all(isinstance(connexe, Connexe) for connexe in contour):
                raise TypeError("Tous les éléments doivent être des instances de Connexe")
            self.contour = contour

    def __str__(self):
        """ Affiche les informations de Contour """
        return "Contour: [" + ", ".join(str(connexe) for connexe in self.contour) + "]"

    def get_contour(self):
        """ Retourne la liste des connexes """
        return self.contour

    def ajout_connexe(self, connexe):
        """Ajoute un Connexe au contour, ce qui représente ajouter une enclave par exemple"""
        if not isinstance(connexe, Connexe):
            raise TypeError("L'objet ajouté doit être une instance de Connexe")

        # Vérifie si la connexe est déjà présente
        if connexe in self.contour:
            print("Cette connexe est déjà présente dans le contour.")
            return  # Ne fait rien si la connexe est déjà présente

        self.contour.append(connexe)

    def retirer_connexe(self, connexe):
        """Retire un connexe du contour, ce qui représente retirer une enclave par exemple"""
        if connexe in self.contour:
            self.contour.remove(connexe)

# A absolument tester pour vérifier que la fonction estDansContour fonctionne correctement (copilote l'a fait)
    def estDansContour(PointGeographique, Contour):
        """ Renvoie True si le point est dans le contour, False sinon
        Algorithm of  Ray Casting :
        First step:
        Trace a ray: Draw a horizontal ray from the point being tested.
        Second step:
        Count the intersections: Count how many times this ray intersects the edges of the polygon.
        Third step:
        Determine the position: If the number of intersections is odd, the point is inside the polygon; if it is even, the point is outside.
        """
        # Get the coordinates of the point
        x = PointGeographique.latitude
        y = PointGeographique.longitude
        # Get the coordinates of the contour
        poly = Contour.get_contour()
        n = len(poly)
        # Initialize the number of intersections
        count = 0
        # For each edge of the polygon
        for i in range(n):
            # Get the coordinates of the two vertices of the edge
            x1 = poly[i].latitude
            y1 = poly[i].longitude
            x2 = poly[(i+1)%n].latitude
            y2 = poly[(i+1)%n].longitude
            # If the edge is horizontal
            if y1 == y2:
                continue
            # If the point is on the edge
            if y == y1 and x == x1:
                return True
            # If the point is above or below the edge
            if y < min(y1, y2) or y > max(y1, y2):
                continue
            # Calculate the x-coordinate of the intersection
            x0 = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            # If the intersection is to the right of the point
            if x0 > x:
                count += 1
        # If the number of intersections is odd
        if count % 2 == 1:
            return True
        # If the number of intersections is even
        return False
