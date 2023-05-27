import sys
import logging
from os import environ
from time import sleep
from threading import Thread
from subprocess import run
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow

environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        url = 'http://localhost:8000'

        self.view = QWebEngineView()
        self.view.load(QUrl(url))
        self.setCentralWidget(self.view)

def startWebView(webBrowser):
    # Sleeps for a second for django to come up
    sleep(0.5)

    webBrowser.setApplicationName("EIA")

    window = mainWindow()
    window.show()

    # Pass the QTWEBENGINE_CHROMIUM_FLAGS directly to QApplication
    webBrowser.arguments = ["--no-sandbox"]

    # Start the application event loop
    sys.exit(webBrowser.exec())

def startDjangoServer():
    run(['python', 'manage.py', 'runserver', '8000'])

if __name__ == '__main__':
    # Start the Django development server in a separate thread
    django_thread = Thread(target=startDjangoServer)
    django_thread.start()

    # Create a QApplication instance
    webBrowser = QApplication(sys.argv)

    # Start the web view in a seperate thread
    webViewThread = Thread(target=startWebView(webBrowser))
    webViewThread.start()

