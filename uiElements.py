from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QColor, QLinearGradient,QBrush
from PyQt6.QtCore import QPointF

#This handles logic for hovering, both colour changes and connection creation init
class hoverableTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        defaultColour = "gray"
        self.setDefaultTextColor(QColor(defaultColour))  # Set the text color to gray
        self.setAcceptHoverEvents(True)
        self.connections = []  # Initialize the connections attribute as a list

    def hoverEnterEvent(self, event):
        if isinstance(self, resourceTextItem):
            self.setDefaultTextColor(QColor(self.resourceColour))
        else:
            # This should NEVER happen as resourceTextItem requires the resourceTier to be set
            # Also if the value is not one of 5 in the mapping it should never get here either
            SystemError("no resource colour found (AKA something very bad happened)")
        super().hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(QColor('gray'))
        super().hoverLeaveEvent(event)

# Created a custom class to hold the resource name and its colour mapping
# Might add connections aswell, not sure
class resourceTextItem(hoverableTextItem):
    def __init__(self, text, resourceLevel):
        super().__init__(text)
        resourceColourMapping = {
            "Planet" : "White",
            "P0" : "Yellow",
            "P1" : "Green",
            "P2" : "Aqua",
            "P3" : "Blue",
            "P4" : "Pink"
        }
        if resourceLevel in resourceColourMapping:
            self.lines = {}  # Store lines in a dictionary
            self.resourceColour = resourceColourMapping[resourceLevel]
            self.resourceLevel = resourceLevel
        else:
            SystemError("FALSE INPUT was given", resourceLevel)

# Creates the line between ingridient and product, with a nice gradient of colour changing into the next Tier
def createConnection(scene, ingredient, ingredientColour, product, productColour):
    connection = QGraphicsLineItem(
        ingredient.pos().x() + ingredient.boundingRect().width(),
        ingredient.pos().y() + ingredient.boundingRect().height() / 2,
        product.pos().x(),
        product.pos().y() + product.boundingRect().height() / 2,
    )

    gradient = QLinearGradient(
        ingredient.pos().x() + ingredient.boundingRect().width(),
        ingredient.pos().y() + ingredient.boundingRect().height() / 2,
        product.pos().x(),
        product.pos().y() + product.boundingRect().height() / 2,
    )
    
    gradient.setColorAt(0.0, QColor(ingredientColour))   # Colour at the ingredient end
    gradient.setColorAt(1.0, QColor(productColour))   # Colour at the product end

    pen = QPen(QBrush(gradient), 1)  # Create a pen with the gradient brush
    connection.setPen(pen)

    connection.setVisible(False)  # Set the initial visibility to False
    connection.src_item = ingredient  # Store the source item in the connection object
    connection.dest_item = product  # Store the destination item in the connection object

    ingredient.connections.append(connection)
    product.connections.append(connection)

    scene.addItem(connection)
    return connection

# This creates the text items for every type of resource
def createResourceTextItems(scene, piData, endProductLevel, staticGap):
    targetTextItems = []
    processedResources = set()  # Set to store processed resources
    # Iterate over the product data
    for i in piData[endProductLevel].items():
        resourceText = resourceTextItem(i[0], endProductLevel)
        resourceText.setPos(staticGap , 25 + len(targetTextItems) * 20)
        scene.addItem(resourceText)
        targetTextItems.append(resourceText)
        processedResources.add(i[0])  # Add processed resource to set
    
    return targetTextItems

# Creates text items for Planet and P0 resources since P0 structure is a bit different to P1-P4
def createInitialTextItems(scene, piData):
    targetTextItems = []
    rawResourceTextItems = []
    processed_planets = set()
    for rawResource, planetType in piData["P0"].items():
        planetTypes = planetType["planetTypes"]
        
        # Create planetTextItem for each planet type
        for planetType in planetTypes:
            if planetType in processed_planets:
                continue

            planetText = resourceTextItem(planetType, "Planet")
            planetText.setPos(25 , 25 + len(targetTextItems) * 20)
            scene.addItem(planetText)
            targetTextItems.append(planetText)
            processed_planets.add(planetType)  # Add processed planet to set
    
        rawResourceText = resourceTextItem(rawResource, "P0")
        rawResourceText.setPos(125, 25 + len(rawResourceTextItems) * 20)
        scene.addItem(rawResourceText)
        rawResourceTextItems.append(rawResourceText)