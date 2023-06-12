""" 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""
from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QHBoxLayout, QWidget
from sqlitestuff import getPIData
from uiElements import initializeResourceTree, CollapsibleSidebar

eveSDE = "sqlite-latest.sqlite"
applicationCSS = "static/app.css"
title = "Eve Industry Assistant"
version = "0.0.1"


def main():
        
    app = QApplication([])
    with open(applicationCSS, "r") as styleSheet:
        app.setStyleSheet(styleSheet.read())

    main_window = QMainWindow()
    main_window.setWindowTitle(title + " " + version)
    sidebar = CollapsibleSidebar()

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 1100, 600)
    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_layout.addWidget(sidebar)
    main_layout.addWidget(view)

    central_widget = QWidget()
    central_widget.setLayout(main_layout)
    main_window.setCentralWidget(central_widget)

    main_window.show()

    # Extract unique planet names and resource names
    piData = getPIData(eveSDE)

    # Start planet - P4 tree viewer
    initializeResourceTree(scene, piData)

    view.show()
    app.exec()


if __name__ == "__main__":
    main()