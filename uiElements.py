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


def createConnection(planetText, resourceText):
    connection = QGraphicsLineItem(
        planetText.pos().x() + planetText.boundingRect().width(),
        planetText.pos().y() + planetText.boundingRect().height() / 2,
        resourceText.pos().x(),
        resourceText.pos().y() + resourceText.boundingRect().height() / 2,
    )

    gradient = QLinearGradient(
        planetText.pos().x() + planetText.boundingRect().width(),
        planetText.pos().y() + planetText.boundingRect().height() / 2,
        resourceText.pos().x(),
        resourceText.pos().y() + resourceText.boundingRect().height() / 2,
    )
    
    gradient.setColorAt(0.0, QColor('white'))  # Color at the planet end
    gradient.setColorAt(1.0, QColor('yellow'))  # Color at the resource end

# White = Planet
# Yellow = Resource
# Green = Tier 1 Product (P1)
# Aqua = Tier 2 Product (P2)
# Blue = Tier 3 Product (P3)
# Pink = Tier 4 Product (P4)

    pen = QPen(QBrush(gradient), 1)  # Create a pen with the gradient brush
    connection.setPen(pen)

    connection.setVisible(False)  # Set the initial visibility to Fals
    connection.src_item = planetText  # Store the source item in the connection object
    connection.dest_item = resourceText  # Store the destination item in the connection object

    planetText.connections.append(connection)
    resourceText.connections.append(connection)

    return connection



