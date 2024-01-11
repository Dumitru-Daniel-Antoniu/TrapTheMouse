import random
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtGui import QFont, QColor, QPainter, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
class TrapTheMouse(QMainWindow):

    def __init__(self):
        super().__init__()
        self.table = []
        self.mice = [5, 5]
        self.initial_state()

    def initial_state(self):
        self.resize(1030, 730)
        self.move(100, 100)
        self.setStyleSheet("background-color: rgb(100,200,150)")
        font = QFont()
        font.setFamily("Silkscreen")
        font.setPointSize(20)
        self.points = "20000"
        self.title = QLabel(self)
        self.title.setText("Score:")
        self.title.setFont(font)
        self.title.setGeometry(45, 40, 130, 50)
        self.title.setStyleSheet("color: white")
        self.score = QLabel(self)
        self.score.setText(self.points)
        self.score.setFont(font)
        self.score.setGeometry(45, 85, 130, 50)
        self.score.setStyleSheet("color: white")
        self.graphicMice = QIcon("mice.jpg")
        # self.mice.setIconSize(QSize(65, 59))
        self.graphicTable = []
        x = 250
        y = 30
        lx = 66
        ly = 60
        for i in range(11):
            line = []
            graphicLine = []
            for j in range(11):
                button = QPushButton(self)
                button.setGeometry(x, y, 65, 59)
                button.setStyleSheet("background-image: url(white.jpg)")
                x += 66
                line.append(0)
                graphicLine.append(button)
            if i % 2 == 0:
                x = 284
            else:
                x = 250
            y += 60
            self.table.append(line)
            self.graphicTable.append(graphicLine)
        obstacles = random.randint(5, 10)
        self.table[5][5] = 2
        self.graphicTable[5][5].setIcon(self.graphicMice)
        while obstacles > 0:
            i = random.randint(0, 10)
            j = random.randint(0, 10)
            if self.table[i][j] == 0:
                self.table[i][j] = 1
                self.graphicTable[i][j].setStyleSheet("background-image: url(black.jpg)")
                obstacles -= 1
        for i in range(11):
            for j in range(11):
                self.graphicTable[i][j].clicked.connect(self.put_piece(i, j))
        self.show()

    def final_state(self):
        if self.mice[0] == -1 or self.mice[0] == 11 or self.mice[1] == -1 or self.mice[1] == 1:
            return 1
        elif self.mice[0] - 1 >= 0 and self.mice[0] + 1 <= 10 and self.mice[1] -1 >= 0 and self.mice[1] <= 10:
            if self.table[self.mice[0]][self.mice[1] - 1] == 1 and self.table[self.mice[0]][self.mice[1] + 1] == 1 and self.table[self.mice[0] - 1][self.mice[1]] == 1 and self.table[self.mice[0] + 1][self.mice[1]] == 1:
                if self.mice[0] % 2 == 0 and self.table[self.mice[0] - 1][self.mice[1] - 1] == 1 and self.table[self.mice[0] + 1][self.mice[1] - 1] == 1:
                    return 2
                elif self.mice[0] % 2 == 1 and self.table[self.mice[0] - 1][self.mice[1] + 1] == 1 and self.table[self.mice[0] + 1][self.mice[1] + 1] == 1:
                    return 2
        return 0

    def put_piece(self, a, b):
        if self.table[a][b] == 0:
            self.table[a][b] = 1
        #     return 1
        # else:
        #     return 0

    def transition(self, x, y):
        self.table[self.mice[0]][self.mice[1]] = 0
        self.table[x][y] = 2
        self.mice = [x,y]

    def validation(self, x, y):
        if (x >= 0 and x <= 10 and y >= 0 and y <= 10 and self.table[x][y] == 0) or x == -1 or x == 11 or y == -1 or y == 11:
            if [x, y] == [self.mice[0], self.mice[1] - 1] or [x, y] == [self.mice[0], self.mice[1] + 1] or [x, y] == [self.mice[0] - 1, self.mice[1]] or [x, y] == [self.mice[0] + 1, self.mice[1]]:
                if x % 2 == 0 and ([x, y] == [self.mice[0] - 1, self.mice[1] - 1] or [x, y] == [self.mice[0] + 1,self.mice[1] - 1]):
                    return 1
                elif x % 2 == 1 and ([x, y] == [self.mice[0] - 1, self.mice[1] + 1] or [x, y] == [self.mice[0] + 1,self.mice[1] + 1]):
                    return 1
        return 0

    def score(self):
        return min(self.mice[0],self.mice[1]) + 1

    #def minimax(self, ):