# python 3.8
from subprocess import run
from os import environ

def SDEupdate(newestSDE):
    try:
        run(["pg_restore", "--dbname=" +  environ.get("PGDATABASE"), newestSDE])
       
    except (Exception) as error:
        print(error)
        exit()