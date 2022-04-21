#!/usr/bin/python
from os import environ
from psycopg2 import connect
from decouple import config

def setDatabaseConnectionVariables():
    try:
        environ['PGHOST'] = config('host')
        environ['PGPORT'] = config('port')
        environ['PGDATABASE'] = config('database')
        environ['PGUSER'] = config('user')
        environ['PGPASSWORD'] = config('password')


    except (Exception) as error:
        print(error)
        exit()

def dbConnectionOpen():
    print(environ.get("PGHOST"))
    """ Connect to the PostgreSQL database server """
    setDatabaseConnectionVariables()
    conn = None
    # params = configOriginal(connectionFile)
        
        # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = connect('')

    return conn

def dbConnectionClose(conn):
    conn.close()
    print('Database connection closed.')
