"""
This file is part of EIA.

EIA is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EIA is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EIA. If not, see <https://www.gnu.org/licenses/>. 
"""
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QPen, QColor, QLinearGradient, QBrush, QIcon, QPalette
from PyQt6.QtCore import Qt

defaultColour = "gray"
productLevels = {
        -1 : "Planets",
        0 : "P0",
        1 : "P1",
        2 : "P2",
        3 : "P3",
        4 : "P4"
    }
resourceColourMapping = {
    "Planets" : "White",
    "P0" : "Yellow",
    "P1" : "Green",
    "P2" : "Aqua",
    "P3" : "Blue",
    "P4" : "Pink"
}

#This handles logic for hovering, both colour changes and connection creation init
class hoverableTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setDefaultTextColor(QColor(defaultColour))  # Set the text color to gray
        self.setAcceptHoverEvents(True)
        self.connections = []  # Initialize the connections attribute as a list

    def hoverEnterEvent(self, event):
        if isinstance(self, resourceTextItem):
            self.setDefaultTextColor(QColor(self.resourceColour))
            self.connectionRelationships(True)
        else:
            # This should NEVER happen as resourceTextItem requires the resourceTier to be set
            # Also if the value is not one of 5 in the mapping it should never get here either
            raise SystemError("no resource colour found (AKA something very bad happened)")
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setDefaultTextColor(QColor(defaultColour))
        self.connectionRelationships(False)
        super().hoverLeaveEvent(event)

    def connectionRelationships(self, showRelationships):
        anchoredPlainText = self.toPlainText()
        for connection in self.connections:
            connectedItem = connection.destItem if connection.srcItem == self else connection.srcItem
            if connectedItem.resourceLevel == self.resourceLevel:
                break
            if self.resourceLevel == "Planets":
                singlePlanetVisualizationStart(self,showRelationships)
                return
            showRelevantConnections(anchoredPlainText, connectedItem, False, showRelationships)
            showRelevantConnections(anchoredPlainText, connectedItem, True, showRelationships)         

# Created a custom class to hold the resource name and its colour mapping
# Might add connections aswell, not sure
class resourceTextItem(hoverableTextItem):
    def __init__(self, text, resourceLevel):
        super().__init__(text)
        if resourceLevel in resourceColourMapping:
            self.lines = {}  # Store lines in a dictionary
            self.resourceColour = resourceColourMapping[resourceLevel]
            self.resourceLevel = resourceLevel
        else:
            raise SystemError("FALSE INPUT was given", resourceLevel)

class CollapsibleSidebar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        collapseIcon = "static/chevron-right.svg"
        planetRelationshipViewerIcon = "static/globe-europe-africa.svg"
        settingsIcon = "static/tools.svg"

        self.collapse = self.createButton(collapseIcon, True)
        self.planetRelationshipViewer = self.createButton(planetRelationshipViewerIcon)
        self.settings = self.createButton(settingsIcon)

        # Set up the layout for the buttons
        layout.addWidget(self.collapse)
        layout.addWidget(self.planetRelationshipViewer)
        layout.addWidget(self.settings)
        layout.addStretch(1)  # Add stretch to push widgets to the top

        self.setLayout(layout)
        self.collapsed = True

        # Set the minimum size of the sidebar

    def toggleSidebar(self):
        self.collapsed = not self.collapsed
        if self.collapsed:
            self.collapse.setIcon(QIcon("static/chevron-right.svg"))
        else:
            self.collapse.setIcon(QIcon("static/chevron-left.svg"))

    def createButton(self, icon, isCollapseButton=False):
        button = QPushButton()
        button.setIcon(QIcon(icon))
        button.setContentsMargins(0,0,0,0)
        button.setMinimumSize(60, 80)
        button.setMaximumSize(60, 80)
        if isCollapseButton:
            button.clicked.connect(self.toggleSidebar)
        return button

# Start the scene for the resource overview tree
def initializeResourceTree(scene, piData):
    # Text item creation for flowchart
    planetTextItems = createPlanetTextItems(scene, piData, "Planets", 25)
    p0TextItems = createResourceTextItems(scene, piData, "P0", 125)
    p1TextItems = createResourceTextItems(scene, piData, "P1", 275)
    p2TextItems = createResourceTextItems(scene, piData, "P2", 450)
    p3TextItems = createResourceTextItems(scene, piData, "P3", 650)
    p4TextItems = createResourceTextItems(scene, piData, "P4", 850)

    # Consider maybe creating a seperate sqlite file
    # that contains information about the planet relationships 
    # so this does not need to be calculated on each run 
    createAllConnectionRelationships(scene, piData, planetTextItems , p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems)

# This takes source and target information and makes the previously generated connection visible along with changing the colour of both source and target        
def makeConnectionVisible(connection, showRelationships):
    if showRelationships == True:
        connection.setVisible(True)
        connection.srcItem.setDefaultTextColor(QColor(connection.srcItem.resourceColour))
        connection.destItem.setDefaultTextColor(QColor(connection.destItem.resourceColour))
    else:
        connection.setVisible(False)
        connection.srcItem.setDefaultTextColor(QColor(defaultColour))
        connection.destItem.setDefaultTextColor(QColor(defaultColour))

# To avoid repetition when calculating the relationship tree for single planet origins
def singlePlanetVisibilityCalculation(inputResources, showRelationships):
    outputResources = set()
    for inputResource in inputResources:
        for inputResourceOutputConnections in inputResource.connections[1:]:
            outputResourceInputs = {stuff.srcItem for stuff in inputResourceOutputConnections.destItem.connections if stuff.destItem == inputResourceOutputConnections.destItem}
            if outputResourceInputs.issubset(inputResources):
                makeConnectionVisible(inputResourceOutputConnections, showRelationships)
                outputResources.add(inputResourceOutputConnections.destItem)

    return outputResources

# When you hover over a planet it calls this to only show what you can make with the resources from one planet
def singlePlanetVisualizationStart(planet, showRelationships):
    p0Items = set()
    for connection in planet.connections:
        if connection.srcItem.toPlainText() != planet.toPlainText():
            continue
        p0Items.add(connection.destItem)
        makeConnectionVisible(connection, showRelationships)

    p1Items = singlePlanetVisibilityCalculation(p0Items, showRelationships)
    p2Items = singlePlanetVisibilityCalculation(p1Items, showRelationships)
    singlePlanetVisibilityCalculation(p2Items, showRelationships)

# This is created to only show and highlight the connections that are either directly related or via children/parents
def showRelevantConnections(anchoredPlainText, connectedItem, flipSearch, showRelationships):
    for connection in connectedItem.connections:
        if flipSearch:
            itemSearchDirection = connection.srcItem
            itemSearchDirection2 = connection.destItem
        else:
            itemSearchDirection = connection.destItem
            itemSearchDirection2 = connection.srcItem

        if itemSearchDirection2.toPlainText() != anchoredPlainText:
            continue

        recurseivlyAnchoredPlainText = itemSearchDirection.toPlainText()
        recurseivlyConnectedItem = itemSearchDirection

        makeConnectionVisible(connection, showRelationships)
        showRelevantConnections(recurseivlyAnchoredPlainText, recurseivlyConnectedItem, flipSearch, showRelationships)

# Logic behind between what resources are connected and call out the actual connection creation for each valid connection
def createAllConnectionRelationships(scene, piData, planetTextItems , p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems):
    currentProductLevel = -1
    
    # Create a dictionary to map product names to their text items
    textItemMapping = {}
    for productList in [planetTextItems, p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems]:
        for textItem in productList:
            textItemMapping[textItem.toPlainText()] = textItem
    
    for products in [p0TextItems, p1TextItems, p2TextItems, p3TextItems, p4TextItems]:
        currentProductLevel += 1
        for product in products:
            inputResources = piData[productLevels[currentProductLevel]][product.toPlainText()]
            
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
    connection.srcItem = ingredient  # Store the source item in the connection object
    connection.destItem = product  # Store the destination item in the connection object

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