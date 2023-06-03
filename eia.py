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

def createResourceTextItemsAndConnections(scene, relationships, planetTextItems):
    resourceTextItems = []
    for relationship in relationships:
        planet_name = relationship['planet']
        resource_name = relationship['p0']

        # Find the corresponding PlanetTextItem in planet_text_items
        planetText = next(
            (item for item in planetTextItems if item.toPlainText() == planet_name),
            None,
        )

        # If the corresponding PlanetTextItem is not found, continue to the next relationship
        if planetText is None:
            continue

        # Find the corresponding ResourceTextItem in resource_text_items or create a new one
        resourceText = next(
            (item for item in resourceTextItems if item.toPlainText() == resource_name),
            None,
        )
        if resourceText is None:
            # Create a new ResourceTextItem for the resource_name
            resourceText = rawResourceTextItem(resource_name)

            # Set the position and add the ResourceTextItem to the scene
            resourceText.setPos(200, 150 + len(resourceTextItems) * 20)
            scene.addItem(resourceText)
            resourceTextItems.append(resourceText)

        connection = createConnection(planetText, resourceText)
        scene.addItem(connection)

def main():
        
    app = QApplication([])

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 800, 600)

    relationships = getP0Data()

    # Extract unique planet names and resource names
    planetTypes = list(set([relationship['planet'] for relationship in relationships]))
    rawResources = list(set([relationship['p0'] for relationship in relationships]))

    planetTextItems = createPlanetTextItems(scene, planetTypes)
    createResourceTextItemsAndConnections(scene, relationships, planetTextItems)


    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    view.show()

    app.exec()


if __name__ == "__main__":
    main()