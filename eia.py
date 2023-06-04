from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from sqlitestuff import getPIData
from uiElements import planetTextItem,rawResourceTextItem,createConnection


def createPlanetTextItems(scene, planetNames):
    planetTextItems = []
    for i, planetName in enumerate(planetNames):
        planetText = planetTextItem(planetName)
        planetText.setPos(25, 150 + i * 20)
        scene.addItem(planetText)
        planetTextItems.append(planetText)
    return planetTextItems

def createResourceTextItem(scene, resourceName, resourceTextItems):
    resourceText = next(
        (item for item in resourceTextItems if item.toPlainText() == resourceName),
        None,
    )
    if resourceText is None:
        resourceText = rawResourceTextItem(resourceName)
        resourceText.setPos(200, 150 + len(resourceTextItems) * 20)
        scene.addItem(resourceText)
        resourceTextItems.append(resourceText)
    return resourceText

def createResourceConnection(scene, planetText, resourceText):
    connection = createConnection(planetText, resourceText)
    scene.addItem(connection)
    return connection

def createTextItemsAndConnections(scene, piData, sourceAttribute, targetAttribute):
    targetTextItems = []
    processed_planets = set()  # Set to store processed planets
    # Iterate over the P0 data
    for p0, p0Data in piData[targetAttribute].items():
        planetTypes = p0Data[sourceAttribute]
        
        # Create planetTextItem for each planet type
        for planetType in planetTypes:
            if planetType in processed_planets:
                continue

            planetText = planetTextItem(planetType)
            planetText.setPos(25, 150 + len(targetTextItems) * 20)
            scene.addItem(planetText)
            targetTextItems.append(planetText)
            processed_planets.add(planetType)  # Add processed planet to set
                
    return targetTextItems


def main():
        
    app = QApplication([])

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 800, 600)
    # Extract unique planet names and resource names
    piData = getPIData()

    createTextItemsAndConnections(scene, piData, 'planetTypes', 'P0')

    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    view.show()

    app.exec()


if __name__ == "__main__":
    main()