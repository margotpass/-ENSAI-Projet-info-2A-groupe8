from dao.db_connection import DBConnection


class PointGeographiqueDao:
    def get_point_by_coordinates(self, longitude, latitude):
        with DBConnection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("select lngitude, latitude from 
                ")