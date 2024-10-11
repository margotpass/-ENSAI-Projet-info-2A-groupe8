from Connexe import Connexe

class Contour(Connexe):
    """ Contour contient les connexes
    paramètres:
    Polygones : List<Connexe>
    """
    def __init__(self, Contour):
        self.Contour = Contour

    def __str__(self):
        """ str sert à afficher les informations de Contour """
        return "Contour: " + str(self.Contour)

    def get_Connexe(self):
        """ Retourne Contour """
        return self.Contour
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
        poly = Contour.get_Connexe()
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





