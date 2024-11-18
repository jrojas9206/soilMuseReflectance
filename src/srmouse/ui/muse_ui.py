import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MuseApp(qtw.QMainWindow):

    MAIN_WINDOW_HEIGHT = 480
    MAIN_WINDOW_WIDTH = 720

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Muse Tool")
        self.setFixedSize(self.MAIN_WINDOW_WIDTH,
                          self.MAIN_WINDOW_HEIGHT)
        central_widget = qtw.QWidget()
        self.setCentralWidget(central_widget)
        mw_layout = qtw.QGridLayout(central_widget)
        self.show()