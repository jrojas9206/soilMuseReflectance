import sys 
from PyQt5 import QtWidgets as qtw
from srmouse.ui.muse_ui import MuseApp

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MuseApp()
    sys.exit(app.exec())
