import sys
sys.path.append('.')
from PySide2.QtWidgets import QApplication
import foo

app = QApplication(sys.argv)
window = foo.MyWindow()

window.show()
app.exec_()
