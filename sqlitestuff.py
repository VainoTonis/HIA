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

def sortPIData(piData,level):
    piData[level] = dict(sorted(piData[level].items()))

def writePISchemaComponents(piData,cursor,inputLevel,outputLevel):
    getOutputResourceTypeID = '''
    SELECT typeID, typeName FROM invTypes 
    WHERE typeID IN (
        SELECT typeID FROM planetSchematicsTypeMap 
        WHERE isInput = 0 
            AND schematicID IN (
                SELECT schematicID FROM planetSchematicsTypeMap 
                WHERE isInput = 1 
                    AND typeID IN (:inputTypes)))
    '''
    for resource in piData[inputLevel]:
        inputTypeID = piData[inputLevel][resource]["typeID"]
        cursor.execute(getOutputResourceTypeID, {"inputTypes": inputTypeID})
        P1Name = cursor.fetchall()

        for inputResource in P1Name:
            if inputResource[1] not in piData[outputLevel]:
                piData[outputLevel][inputResource[1]] = {
                    "typeID" : inputResource[0],
                    "inputResource" : [resource]
                }
            else:
                piData[outputLevel][P1Name[0][1]]["inputResource"].append(resource)

    sortPIData(piData,outputLevel)
    return piData


def getPIData():
    conn, cursor = connectToSDE()

    # Get the node extractors for each planet
    # This is the only way I could get from the SDE the types of raw resources that exist in each planet
    planetRawResourcesQuery = "SELECT typeName FROM invTypes WHERE groupID IN (1026)"
    cursor.execute(planetRawResourcesQuery)
    results = cursor.fetchall()
    # Create a dictionary structure to hold the data for each tier of resource
    piData = {
        "P0": {},
        "P1": {},
        "P2": {},
        "P3": {},
        "P4": {},
    }

    # The liquid extractor extracts liquids, and thus I the typename is the same, i simply just replace the liquid with liquids
    nameMapping = {
        'Aqueous Liquid': 'Aqueous Liquids',
    }

    # Get the planet and the raw resources that are being able to be collected
    for row in results:
        planetType = row[0].split()[0]
        rawResource = ' '.join(row[0].split()[1:-1])
        # Check if the P0 name exists in the mapping dictionary
        if rawResource in nameMapping:
            rawResource = nameMapping[rawResource]

        # Get the typeID
        typeIDQuery = "SELECT typeID FROM invTypes WHERE typeName LIKE :resourceName"
        cursor.execute(typeIDQuery, {"resourceName": rawResource})
        rawResourceID = cursor.fetchone()
        # Save the resource to piData
        if rawResource not in piData["P0"]:
            piData["P0"][rawResource] = {
                "typeID" : [rawResourceID][0][0],
                "planetTypes": [planetType]
            }
        else:
            piData["P0"][rawResource]["planetTypes"].append(planetType)

    sortPIData(piData,"P0")
    writePISchemaComponents(piData,cursor,"P0","P1")
    writePISchemaComponents(piData,cursor,"P1","P2")
    writePISchemaComponents(piData,cursor,"P2","P3")

    completePIResourceMap = []

    # Close the connection
    conn.close()

    return completePIResourceMap



getPIData()
# White = Planet
# Yellow = Resource
# Green = Tier 1 Product (P1)
# Aqua = Tier 2 Product (P2)
# Blue = Tier 3 Product (P3)
# Pink = Tier 4 Product (P4)