"""
This file is part of EIA.

EIA is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EIA is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EIA. If not, see <https://www.gnu.org/licenses/>. 
"""
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt6.QtGui import QPen, QColor, QLinearGradient,QBrush

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
            for connection in self.connections:
                connection.setVisible(True)
        else:
            # This should NEVER happen as resourceTextItem requires the resourceTier to be set
            # Also if the value is not one of 5 in the mapping it should never get here either
            SystemError("no resource colour found (AKA something very bad happened)")
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(QColor('gray'))
        for connection in self.connections:
            connection.setVisible(False)
        super().hoverLeaveEvent(event)

# Created a custom class to hold the resource name and its colour mapping
# Might add connections aswell, not sure
class resourceTextItem(hoverableTextItem):
    def __init__(self, text, resourceLevel):
        super().__init__(text)
        resourceColourMapping = {
            "Planets" : "White",
            "P0" : "Yellow",
            "P1" : "Green",
            "P2" : "Aqua",
            "P3" : "Blue",
            "P4" : "Pink"
        }
        if resourceLevel in resourceColourMapping:
            self.lines = {}  # Store lines in a dictionary
            self.resourceColour = resourceColourMapping[resourceLevel]
        else:
            raise SystemError("FALSE INPUT was given", resourceLevel)

def initializePlanetConnections(scene, piData ,  planetTextItems, p0TextItems):
    for rawResource, planetType in piData["P0"].items():
        planetTypes = planetType
        
        # Get the raw resource textItem to connect with
        for textItem in p0TextItems:
            if textItem.toPlainText() == rawResource:
                p0TextItem = textItem
        # Get the planetTextItem that the P0 resource exists 
        # and Create a connection based on that
        for planetTextItem in planetTextItems:
            if planetTextItem.toPlainText() in planetTypes:
                createConnection(scene, planetTextItem, planetTextItem.resourceColour, p0TextItem, p0TextItem.resourceColour)


def initializeConnections(scene, piData, planetTextItems , p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems):
    currentProductLevel = -1
    productLevels = {
            -1 : "Planets",
            0 : "P0",
            1 : "P1",
            2 : "P2",
            3 : "P3",
            4 : "P4"
        }
    
    # Create a dictionary to map product names to their text items
    textItemMapping = {}
    for productList in [planetTextItems, p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems]:
        for textItem in productList:
            textItemMapping[textItem.toPlainText()] = textItem
    
    for products in [p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems]:
        currentProductLevel += 1
        for product in products:
            productName = product.toPlainText()
            inputResources = piData[productLevels[currentProductLevel]][product.toPlainText()]
            potentialInputs = piData[productLevels[currentProductLevel - 1]]
            
            # Get the corresponding text items for each input
            inputTextItems = [textItemMapping[inputName] for inputName in inputResources if inputName in textItemMapping]
            
            # Now you can create connections between the product text item and the input text items
            for inputTextItem in inputTextItems:
                createConnection(scene, inputTextItem, inputTextItem.resourceColour, product, product.resourceColour)
                pass

    
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
def createResourceTextItems(scene, piData, endProductLevel, columnXPosition):
    targetTextItems = []
    processedResources = set()  # Set to store processed resources
    columnYPosition = (scene.height() - len(piData[endProductLevel]) * 20) / 2
    # Iterate over the product data
    for endProductName, endProductData in piData[endProductLevel].items():
        resourceText = resourceTextItem(endProductName, endProductLevel)
        resourceText.setPos(columnXPosition , columnYPosition + len(targetTextItems) * 20)
        scene.addItem(resourceText)
        targetTextItems.append(resourceText)
        processedResources.add(endProductName)  # Add processed resource to set

    return targetTextItems

# Creates text items for Planet and P0 resources since P0 structure is a bit different to P1-P4
def createPlanetTextItems(scene, piData, planetParent, columnXPosition):
    planetTextItems = []
    processedPlanets = set()

    planetTypes = piData[planetParent]
    
    # Create planetTextItem for each planet type
    for planetType in planetTypes:
        if planetType in processedPlanets:
            continue

        columnYPosition = (scene.height() - len(piData[planetParent]) * 20) / 2
        planetText = resourceTextItem(planetType, planetParent)
        planetText.setPos(columnXPosition , columnYPosition + len(processedPlanets) * 20)
        scene.addItem(planetText)
        planetTextItems.append(planetText)
        processedPlanets.add(planetType)

    return planetTextItems