import psycopg2
from psycopg2 import Error
def get_idmm_data(idmm):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="example")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        cursor.execute(f'SELECT * FROM idmm WHERE idmm={idmm};')
        # Fetch result
        record = cursor.fetchall()
        print(record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

get_idmm_data(1958)