import sys
sys.path.append('.')
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import foo

class PyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("PyWindow")

        self.layout = QVBoxLayout()

        label = QLabel("hello")
        self.layout.addWidget(label)

        self.fooWindow = foo.Goba.MyWindow()
        # 0 == Qt::Widget
        self.fooWindow.setWindowFlags(0)
        self.layout.addWidget(self.fooWindow)

        self.setLayout(self.layout)

app = QApplication(sys.argv)

pyWindow = PyWindow()
pyWindow.show()

app.exec_()
