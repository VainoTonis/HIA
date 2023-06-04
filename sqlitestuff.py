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

def writePISchemaComponents(piData,cursor,outputLevel):

    # Manually setting the groupIDs of the final output
    groupIDMapping = {
        # P0 Wont be used but just in case marked it if it is eventually required
        "P0" : [1032,1033,1035], # Solid, Liquid-gas, Organic 
        "P1" : 1042,
        "P2" : 1034,
        "P3" : 1040,
        "P4" : 1041
    }

    if outputLevel in groupIDMapping:
        groupID = groupIDMapping[outputLevel]
    else:
        print("FALSE INPUT was given", outputLevel)
        exit()

    findEveryResourceInGroupQuery = "SELECT typeID, typeName FROM invTypes WHERE groupID IN (:groupID)"    
    cursor.execute(findEveryResourceInGroupQuery, {"groupID": groupID})
    endProducts = cursor.fetchall()

    for endProduct in endProducts:
        productID = endProduct[0]
        productName = endProduct[1]

        allInputQuery = '''
        SELECT typeID FROM planetSchematicsTypeMap
        WHERE isInput = 1 
            AND schematicID = (
                SELECT schematicID FROM planetSchematicsTypeMap
                WHERE isInput = 0 
                    AND typeID = (:outputID))
        '''
        cursor.execute(allInputQuery, {"outputID": productID})
        allInputs = cursor.fetchall()
        if endProduct not in piData[outputLevel]:
            piData[outputLevel][productName] = {
                "typeID" : productID,
                "inputResource" : allInputs
            }
        else:
            print("wtf")
            exit()

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
    writePISchemaComponents(piData,cursor,"P1")
    writePISchemaComponents(piData,cursor,"P2")
    writePISchemaComponents(piData,cursor,"P3")
    writePISchemaComponents(piData,cursor,"P4")

    print(piData)
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