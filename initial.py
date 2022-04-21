# python 3.8
# Made by sum cunt
from dbConnection import dbConnectionClose, dbConnectionOpen
from dataIngress import SDEupdate


databasename = "eveIndy"
dbappuser = "eveAPIapp"
newestSDE = "tmp/postgres-latest.dmp"

updateSDEBool = False

# __name__
if __name__=="__main__":
    conn = dbConnectionOpen()

    if updateSDEBool == True:
        SDEupdate(newestSDE)

    dbConnectionClose(conn)
