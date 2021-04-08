#!/usr/bin/python
import psycopg2
from psycopg2 import Error
import psycopg2.extras
import os
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config["DEBUG"] = True

def get_idmm_data(idmm):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(
        host = os.getenv('DB_HOST', 'db'),
        database = os.getenv('DB_NAME', 'postgres'),
        user = os.getenv('DB_USER', 'postgres'),
        password = os.getenv('DB_USER_PASS', 'example'))

        # Create a cursor to perform database operations
        cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        # Executing a SQL query
        cursor.execute(f'SELECT idmm, st_postaje, ime_postaje, ge_sirina FROM idmm WHERE idmm={idmm};')
        # Fetch result
        record = cursor.fetchall()
        # print(record)
        return record

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/api/v1/idmms', methods=['GET'])
def api_idmm():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'idmm' in request.args:
        idmm = int(request.args['idmm'])
    else:
        return "Error: No idmm field provided. Please specify an idmm."

    results = get_idmm_data(idmm)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)