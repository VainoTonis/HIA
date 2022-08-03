#!/usr/bin/python
from os import environ
from psycopg2 import connect
from decouple import config

def setDatabaseConnectionVariables():
    try:
        environ['PGHOST'] = config('DB_HOST')
        environ['PGPORT'] = config('DB_PORT')
        environ['PGDATABASE'] = config('DB_NAME')
        environ['PGUSER'] = config('DB_USER')
        environ['PGPASSWORD'] = config('DB_PASSWORD')


    except (Exception) as error:
        print(error)
        exit()

def dbConnectionOpen():
    # connection info
    setDatabaseConnectionVariables()
    
    # connect to the PostgreSQL server
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = connect('')

    except (Exception) as error:
        print("Connection error: " + error)
        exit()
    
    return conn

def dbConnectionClose(conn):
    conn.close()
    print('Database connection closed.')
