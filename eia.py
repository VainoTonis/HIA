""" 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""
from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QHBoxLayout, QWidget
from sqlitestuff import getPIData
from uiElements import initializeResourceTree, navigationSideBar

eveSDE = "sqlite-latest.sqlite"
applicationCSS = "static/app.css"
title = "Eve Industry Assistant"
version = "0.0.1"



def main():
        
    app = QApplication([])
    with open(applicationCSS, "r") as styleSheet:
        app.setStyleSheet(styleSheet.read())

    mainWindow = QMainWindow()
    mainWindow.setWindowTitle(title + " " + version)


    # Create a QGraphicsScene and set the scene rect
    planetRelationshipViewerScene = QGraphicsScene(0, 0, 1100, 600)
    scene2 = QGraphicsScene(0, 0, 1100, 600)

    sidebar = navigationSideBar(planetRelationshipViewerScene, settingsScene=scene2)

    # Create a QGraphicsView and set the scene
    view = QGraphicsView(planetRelationshipViewerScene)
    sidebar.setView(view)


    mainLayout = QHBoxLayout()
    mainLayout.setContentsMargins(0, 0, 0, 0)
    mainLayout.setSpacing(0)
    mainLayout.addWidget(sidebar)
    mainLayout.addWidget(view)

# Combine the final layout into a central widget that is used in the main window to make everything sticky
    centralWidget = QWidget()
    centralWidget.setLayout(mainLayout)
    mainWindow.setCentralWidget(centralWidget)

    mainWindow.show()

    # Extract unique planet names and resource names
    piData = getPIData(eveSDE)

    # Start planet - P4 tree viewer
    initializeResourceTree(planetRelationshipViewerScene, piData)

    view.show()
    app.exec()


if __name__ == "__main__":
    main()