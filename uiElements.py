from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QColor, QLinearGradient,QBrush
from PyQt6.QtCore import QPointF

class hoverableTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setDefaultTextColor(QColor('gray'))  # Set the text color to gray
        self.setAcceptHoverEvents(True)
        self.connections = []  # Initialize the connections attribute as a list

    def hoverEnterEvent(self, event):
        if isinstance(self, planetTextItem):
            self.setDefaultTextColor(QColor('white'))
            for connection in self.connections:
                if isinstance(connection, QGraphicsLineItem):
                    connection.setVisible(True)
                    if isinstance(connection.dest_item, rawResourceTextItem):
                        connection.dest_item.setDefaultTextColor(QColor('yellow'))
        elif isinstance(self, rawResourceTextItem):
            self.setDefaultTextColor(QColor('yellow'))
            for connection in self.connections:
                if isinstance(connection, QGraphicsLineItem):
                    connection.setVisible(True)
                    if isinstance(connection.src_item, planetTextItem):
                        connection.src_item.setDefaultTextColor(QColor('white'))
        super().hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        if isinstance(self, planetTextItem):
            self.setDefaultTextColor(QColor('gray'))
            for connection in self.connections:
                if isinstance(connection, QGraphicsLineItem):
                    connection.setVisible(False)
                    if isinstance(connection.dest_item, rawResourceTextItem):
                        connection.dest_item.setDefaultTextColor(QColor('gray'))
        elif isinstance(self, rawResourceTextItem):
            self.setDefaultTextColor(QColor('gray'))
            for connection in self.connections:
                if isinstance(connection, QGraphicsLineItem):
                    connection.setVisible(False)
                    if isinstance(connection.src_item, planetTextItem):
                        connection.src_item.setDefaultTextColor(QColor('gray'))
        super().hoverLeaveEvent(event)

class planetTextItem(hoverableTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.lines = {}  # Store lines in a dictionary

class rawResourceTextItem(hoverableTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.lines = {}  # Store lines in a dictionary

class resourceTextItem(hoverableTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.lines = {}  # Store lines in a dictionary
    # White = Planet
    # Yellow = Resource
    # Green = Tier 1 Product (P1)
    # Aqua = Tier 2 Product (P2)
    # Blue = Tier 3 Product (P3)
    # Pink = Tier 4 Product (P4)


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


def createResourceTextItems(scene, piData, endProductLevel, staticGap):
    targetTextItems = []
    processedResources = set()  # Set to store processed planets
    # Iterate over the P0 data
    for i in piData[endProductLevel].items():
        resourceText = rawResourceTextItem(i[0])
        resourceText.setPos(staticGap , 150 + len(targetTextItems) * 20)
        scene.addItem(resourceText)
        targetTextItems.append(resourceText)
        processedResources.add(i[0])  # Add processed planet to set
    
    return targetTextItems

# This is to display both Planet and P0 resources
def createInitialTextItems(scene, piData):
    targetTextItems = []
    rawResourceTextItems = []
    processed_planets = set()  # Set to store processed planets
    # Iterate over the P0 data
    for rawResource, planetType in piData["P0"].items():
        planetTypes = planetType["planetTypes"]
        
        # Create planetTextItem for each planet type
        for planetType in planetTypes:
            if planetType in processed_planets:
                continue

            planetText = planetTextItem(planetType)
            planetText.setPos(25 , 150 + len(targetTextItems) * 20)
            scene.addItem(planetText)
            targetTextItems.append(planetText)
            processed_planets.add(planetType)  # Add processed planet to set
    
        rawResourceText = rawResourceTextItem(rawResource)
        rawResourceText.setPos(125, 150 + len(rawResourceTextItems) * 20)
        scene.addItem(rawResourceText)
        rawResourceTextItems.append(rawResourceText)