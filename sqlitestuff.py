from sqlite3 import connect

def connectToSDE():
    conn = connect('sqlite/evesde.sqlite')
    cursor = conn.cursor()
    return conn, cursor

def closeDBConnection(conn):
    conn.close()

def getP0Data():
    conn, cursor = connectToSDE()

    planetQuery = "SELECT typeName FROM invTypes WHERE groupID IN (1026)"

    cursor.execute(planetQuery)

    results = cursor.fetchall()

    planetP0List = []

    for row in results:
        rawResources = {
                'planet' : row[0].split()[0],
                'p0': ' '.join(row[0].split()[1:-1])
            }
        planetP0List.append(rawResources)

    # Close the connection
    closeDBConnection(conn)

    return planetP0List


def getPIData(rawResources):
    conn, cursor = connectToSDE()
    query = ""
    results = cursor.fetchall()

    for row in results:
        print(row)

    # Close the connection
    conn.close()


testData = ['Felsic Magma', 'Complex Organisms', 'Carbon Compounds', 'Noble Metals', 'Base Metals', 'Autotrophs', 'Reactive Gas', 'Planktic Colonies', 'Non-CS Crystals', 'Aqueous Liquid', 'Microorganisms', 'Suspended Plasma', 'Heavy Metals', 'Noble Gas', 'Ionic Solutions']

getPIData(testData)
# Gray = Planet
# Yellow = Resource
# Green = Tier 1 Product (P1)
# Aqua = Tier 2 Product (P2)
# Blue = Tier 3 Product (P3)
# Pink = Tier 4 Product (P4)