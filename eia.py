from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from sqlitestuff import getPIData
from uiElements import createInitialTextItems,createResourceTextItems

def main():
        
    app = QApplication([])

    # Create a QGraphicsScene and set the scene rect
    scene = QGraphicsScene(0, 0, 1100, 800)
    # Extract unique planet names and resource names
    piData = getPIData()

    createInitialTextItems(scene, piData)
    createResourceTextItems(scene, piData, "P1", 275)
    createResourceTextItems(scene, piData, "P2", 450)
    createResourceTextItems(scene, piData, "P3", 650)
    createResourceTextItems(scene, piData, "P4", 850)

    # Create a QGraphicsView and set the scene
    view = QGraphicsView(scene)
    view.show()

    app.exec()


if __name__ == "__main__":
    main()