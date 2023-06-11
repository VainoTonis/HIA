""" 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from sqlitestuff import getPIData
from uiElements import initializeResourceTree

eveSDE = "sqlite-latest.sqlite"


def main():
        
    app = QApplication([])

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 1100, 600)
    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    view.show()

    # Extract unique planet names and resource names
    piData = getPIData(eveSDE)

    # Start planet - P4 tree viewer
    initializeResourceTree(scene,piData)
   
    app.exec()


if __name__ == "__main__":
    main()