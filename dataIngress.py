# python 3.8
from subprocess import run
from os import environ

def SDEupdate(newestSDE):
    try:
        run(["pg_restore", "--dbname=" +  environ.get("PGDATABASE"), newestSDE])
       
    except (Exception) as error:
        print("SDE Update error: " + error)
        exit()

def databaseQuery(conn):
    curr = conn.cursor()
    curr.execute('select * from "invGroups" ig where "groupName" like ' + "'%Blueprint';")
    data = curr.fetchall()

    for result in data:
        print(result)

    # print(data)