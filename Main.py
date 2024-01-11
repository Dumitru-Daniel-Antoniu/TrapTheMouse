import sys
from PyQt5.QtWidgets import QApplication
from Game import TrapTheMouse
from GUI import Screen

app = QApplication(sys.argv)
window = TrapTheMouse()
sys.exit(app.exec_())