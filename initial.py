# python 3.8
# Made by sum cunt
import psycopg2
from updateSDE import config


def dbConnectionOpen():
    """ Connect to the PostgreSQL database server """
    conn = None
    params = config()
        
        # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    return conn

def dbConnectionClose(conn):
    conn.close()
    print('Database connection closed.')

def dbprint(conn):
    # create a cursor
    cur = conn.cursor()
        
	# execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

# __name__
if __name__=="__main__":
    conn = dbConnectionOpen()

    # dbprint(conn)
    dbConnectionClose(conn)
