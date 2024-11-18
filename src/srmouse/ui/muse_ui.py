import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MuseApp(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Muse Tool")
        self.show()