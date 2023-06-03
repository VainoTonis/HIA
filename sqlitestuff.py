from sqlite3 import connect

def connectToSDE():
    conn = connect('sqlite/evesde.sqlite')
    cursor = conn.cursor()
    return conn, cursor

def closeDBConnection(conn):
    conn.close()

def getP0Data():
    conn, cursor = connectToSDE()

    planetRawResourcesQuery = "SELECT typeName FROM invTypes WHERE groupID IN (1026)"
    cursor.execute(planetRawResourcesQuery)
    results = cursor.fetchall()

    planetP1List = []

    nameMapping = {
        'Aqueous Liquid': 'Aqueous Liquids',
    }

    for row in results:
        planetType = row[0].split()[0]
        p0 = ' '.join(row[0].split()[1:-1])
        # Check if the P0 name exists in the mapping dictionary
        if p0 in nameMapping:
            p0 = nameMapping[p0]

        rawResources = {
            'planet': planetType,
            'p0': p0
        }

        planetP1List.append(rawResources)

    # Close the connection
    closeDBConnection(conn)
    return planetP1List


def getPIData(rawResources):
    conn, cursor = connectToSDE()
    query = "SELECT typeID, typeName FROM invTypes WHERE typeName LIKE (?)"

    for resource in rawResources:
        cursor.execute(query,(resource,))
        results = cursor.fetchall()
        print(results)


    # Close the connection
    conn.close()


testData = ['Planktic Colonies', 'Aqueous Liquids', 'Suspended Plasma', 'Ionic Solutions', 'Non-CS Crystals', 'Complex Organisms', 'Carbon Compounds', 'Felsic Magma', 'Autotrophs', 'Microorganisms', 'Base Metals', 'Noble Gas', 'Noble Metals', 'Reactive Gas', 'Heavy Metals']

# getPIData(testData)
# White = Planet
# Yellow = Resource
# Green = Tier 1 Product (P1)
# Aqua = Tier 2 Product (P2)
# Blue = Tier 3 Product (P3)
# Pink = Tier 4 Product (P4)