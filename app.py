import sys
import os
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

for path in [
    # needed for vtkCommonCorePython module
    os.environ.get('PARAVIEW_LIB'),
    # paraview python lib
    os.path.join(os.environ.get('PARAVIEW_LIB'), 'site-packages'),
    # foo module
    os.environ.get('FOO_LIB'),
]:
    sys.path.append(path)

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
                ('LeftButtonPressEvent', self.OnLeftButtonDown),
            ]
            for event, defaultCb in self.events:
                self.AddObserver(event,
                        self._makeCallbackHook(event, defaultCb))

        def _makeCallbackHook(self, hook, defaultCallback):
            def callback(obj, event):
                for cb in self.callbacks[hook]:
                    cb(obj, event)

                # forward events to default callback
                defaultCallback()
            return callback

    def __init__(self):
        QWidget.__init__(self)

        self.sphere = None

        self.setupUi()
        self.connectSlots()

        self.setupPVHandlers()

    def setupUi(self):
        self.setWindowTitle("PyWindow")
        self.resize(1024, 768)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    pyWindow = PyWindow()
    pyWindow.show()

    app.exec_()
