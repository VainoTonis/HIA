# python 3.10.4
# Made by sum cunt
from Legacy import dbConnectionClose, dbConnectionOpen
from dataIngress import SDEupdate, databaseQuery


databasename = "eveIndy"
dbappuser = "eveAPIapp"
newestSDE = "tmp/postgres-latest.dmp"

updateSDEBool = False

# __name__
if __name__=="__main__":
    conn = dbConnectionOpen()

    if updateSDEBool == True:
        SDEupdate(newestSDE)

    databaseQuery(conn)
    dbConnectionClose(conn)