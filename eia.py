from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from sqlitestuff import getP0Data
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

def createTextItemsAndConnections(scene, relationships, sourceItems, sourceAttribute, targetAttribute):
    targetTextItems = []
    for relationship in relationships:
        sourceName = relationship[sourceAttribute]
        targetName = relationship[targetAttribute]

        sourceText = next(
            (item for item in sourceItems if item.toPlainText() == sourceName),
            None,
        )

        if sourceText is None:
            continue

        targetText = createResourceTextItem(scene, targetName, targetTextItems)
        createResourceConnection(scene, sourceText, targetText)

    return targetTextItems



def main():
        
    app = QApplication([])

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 800, 600)

    relationships = getP0Data()
    # Extract unique planet names and resource names
    planetTypes = list(set([relationship['planet'] for relationship in relationships]))
    rawResources = list(set([relationship['p0'] for relationship in relationships]))

    planetTextItems = createPlanetTextItems(scene, planetTypes)
    createTextItemsAndConnections(scene, relationships, planetTextItems, 'planet', 'p0')



    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    view.show()

    app.exec()


if __name__ == "__main__":
    main()