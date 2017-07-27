import sys
import os

# paraview paths
HOME = os.environ.get('HOME', '.')
for path in [
    # relative to HOME
    'tomviz/build/paraview-qt_5_6_2/lib/site-packages/',
    # needed for vtkCommonCorePython module
    'tomviz/build/paraview-qt_5_6_2/lib/',
    # for foo module
    'py2env/hello/build/foo',
]:
    sys.path.append(os.path.join(HOME, path))

from PySide2.QtCore import Slot
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import foo

from paraview.simple import *

class PyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.sphere = None

        self.setupUi()
        self.connectSlots()

    def setupUi(self):
        self.setWindowTitle("PyWindow")

        self.layout = QVBoxLayout()

        self.clickme = QPushButton("Click me!", self)
        self.layout.addWidget(self.clickme)

        # this takes ~2 sec to load...
        self.fooWindow = foo.Goba.MyWindow()
        # 0 == Qt::Widget
        self.fooWindow.setWindowFlags(0)
        self.layout.addWidget(self.fooWindow)

        self.setLayout(self.layout)

    def connectSlots(self):
        self.clickme.clicked.connect(self.onClickMe)

    @Slot()
    def onClickMe(self):
        if self.sphere is None:
            self.sphere = Sphere()
            self.sphere.Radius = 22

            Show(self.sphere)
            Render()

app = QApplication(sys.argv)

pyWindow = PyWindow()
pyWindow.show()

app.exec_()
