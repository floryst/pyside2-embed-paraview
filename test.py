import sys
import os
sys.path.append('.')

# paraview paths
HOME = os.environ.get('HOME', '.')
for path in [
    # relative to HOME
    'tomviz/build/paraview-qt_5_6_2/lib/site-packages/',
    # needed for vtkCommonCorePython module
    'tomviz/build/paraview-qt_5_6_2/lib/',
]:
    sys.path.append(os.path.join(HOME, path))

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
