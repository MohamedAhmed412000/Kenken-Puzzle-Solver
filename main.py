import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from configurations import *

# Main
app = QApplication(sys.argv)    # Defining the application and command is parameter to be able to run it
widget = QStackedWidget()       # Making Stack of widgets
configure = configuration(widget)
widget.addWidget(configure)     # Add mainWindow to the stack (index = 0)
widget.setWindowTitle("Kenken Game Solver")       # Setting Title of GUI App
widget.setFixedSize(400, 250)                   # Setting Fixed Size for the App
widget.show()                                   # Show first Widget (mainWindow)

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
