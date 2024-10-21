from src.dao.db_connection import DBConnection
from src.business_object.subdivision.arrondissement import Arrondissement
from src.business_object.subdivision.canton import Canton
from src.business_object.subdivision.commune import Commune
from src.business_object.subdivision.departement import Departement
from src.business_object.subdivision.epci import EPCI
from src.business_object.subdivision.region import Region

class SubdivisionDao :
    "DAO qui permet la gestion des différentes subdivisions dans la base de données"

    def create_table(self):