"""
This file is part of EIA.

EIA is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EIA is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EIA. If not, see <https://www.gnu.org/licenses/>. 
"""
from sqlite3 import connect

def connectToSDE():
    conn = connect('sqlite/evesde.sqlite')
    cursor = conn.cursor()
    return conn, cursor

def closeDBConnection(conn):
    conn.close()

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
    # Get the ingredients for all the end products and write them down under 
    for endProduct in endProducts:
        productID = endProduct[0]
        productName = endProduct[1]

        ingredientsQuery = '''
        SELECT typeName FROM invTypes 
        WHERE typeID IN (
            SELECT typeID FROM planetSchematicsTypeMap
            WHERE isInput = 1 
                AND schematicID = (
                    SELECT schematicID FROM planetSchematicsTypeMap
                    WHERE isInput = 0 
                        AND typeID = (:outputID)))
        '''
        cursor.execute(ingredientsQuery, {"outputID": productID})
        ingredients = cursor.fetchall()
        if endProduct not in piData[outputLevel]:
            piData[outputLevel][productName] = []
            # Ingridients come in a tuple, to avoid having a dictionary inside a dictionary that has a dictionary that has a list which has tuples and the tuples have Integers, i simply removed the tuple part which makes it mildly less interesting
            for ingredient in ingredients:
                piData[outputLevel][productName].append(ingredient[0])
        else:
            # This should NEVER happen
            print("wtf")
            exit()

    if outputLevel == "P1":
        def findTypeIDIndex(typeID, P0):
            for index, key in enumerate(P0):
                if key == typeID:
                    return index
            return -1
        piData[outputLevel] = dict(sorted(piData["P1"].items(), key=lambda item: findTypeIDIndex(item[1][0], piData["P0"])))
    else:
        piData[outputLevel] = dict(sorted(piData[outputLevel].items()))
        
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
    
        # Save the resource to piData
        if rawResource not in piData["P0"]:
            piData["P0"][rawResource] = [planetType]
        else:
            piData["P0"][rawResource].append(planetType)

    # Sorting and getting all the relational data regarding PI only things
    piData["P0"] = dict(sorted(piData["P0"].items()))
    writePISchemaComponents(piData,cursor,"P1")
    writePISchemaComponents(piData,cursor,"P2")
    writePISchemaComponents(piData,cursor,"P3")
    writePISchemaComponents(piData,cursor,"P4")

    # Close the connection
    conn.close()
    return piData

def main():
    print("Wrong file m8")

if __name__ == "__main__":
    main()