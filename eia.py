import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QDockWidget, QStyle
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the side navigation bar
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        # Create the navigation buttons
        button_page1 = QPushButton("Page 1")
        button_page2 = QPushButton("Page 2")

        # Connect the buttons to their respective page in the stacked widget
        button_page1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        button_page2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Add the buttons to the navigation layout
        nav_layout.addWidget(button_page1)
        nav_layout.addWidget(button_page2)

        # Create the stacked widget for pages
        self.stacked_widget = QStackedWidget()

        # Create page widgets
        page1 = QWidget()
        page1.setStyleSheet("background-color: #E6E6FA")  # Example background color
        page2 = QWidget()
        page2.setStyleSheet("background-color: #FFDAB9")  # Example background color

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)

        # Set the initial page to display
        self.stacked_widget.setCurrentIndex(0)

        # Set the central widget of the main window to the stacked widget
        self.setCentralWidget(self.stacked_widget)

        # Set the side navigation bar as the left widget of the main window
        self.setCentralWidget(self.stacked_widget)

        # Create a dock widget for the navigation bar
        dock_widget = QDockWidget()
        dock_widget.setWidget(nav_widget)

        # Set the dock widget properties
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock_widget.setTitleBarWidget(QWidget())  # Remove the title bar

        # Add the dock widget to the left side of the main window
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())