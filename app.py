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

from collections import defaultdict

from PySide2.QtCore import Slot
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import foo

import vtk
from paraview.simple import *

class PyWindow(QWidget):

    class InteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
        def __init__(self, parent, *args, **kwargs):
            self.parent = parent
            self.callbacks = defaultdict(list)

            self.events = [
                'LeftButtonPressEvent',
            ]
            for event in self.events:
                self.AddObserver(event, self._makeCallbackHook(event))

        def _makeCallbackHook(self, hook):
            def callback(obj, event):
                for cb in self.callbacks['LeftButtonPressEvent']:
                    cb(obj, event)
            return callback

    def __init__(self):
        QWidget.__init__(self)

        self.sphere = None

        self.setupUi()
        self.connectSlots()

        self.setupPVHandlers()

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

    def setupPVHandlers(self):
        view = GetActiveView()
        # Hm, probably should use GetViewOrCreate
        if not view:
            raise Exception('No available paraview view!')

        interactor = view.GetInteractor()
        interactor.SetPicker(vtk.vtkCellPicker())
        self.interactorStyle = self.InteractorStyle(self)
        interactor.SetInteractorStyle(self.interactorStyle)

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