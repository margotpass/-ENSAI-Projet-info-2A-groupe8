from src.dao.db_connection import DBConnection

with DBConnection().connection as connection:
    with connection.cursor() as cursor:
        res = cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
        for i in res.fetch():
            print(i)