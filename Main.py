import sys
from PyQt5.QtWidgets import QApplication
from Game import TrapTheMouse
from GUI import Screen

app = QApplication(sys.argv)
opponent = sys.argv[1]
window = TrapTheMouse(opponent)
window.game()
sys.exit(app.exec_())