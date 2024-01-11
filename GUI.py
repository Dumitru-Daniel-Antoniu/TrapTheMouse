from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtGui import QFont, QColor, QPainter, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

class Screen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        self.title.setGeometry(45,40,130,50)
        self.title.setStyleSheet("color: white")
        self.score = QLabel(self)
        self.score.setText(self.points)
        self.score.setFont(font)
        self.score.setGeometry(45,85,130,50)
        self.score.setStyleSheet("color: white")
        self.mice = QIcon("mice.jpg")
        #self.mice.setIconSize(QSize(65, 59))
        self.table = []
        x = 250
        y = 30
        lx = 66
        ly = 60
        for i in range(11):
            line = []
            for j in range(11):
                button = QPushButton(self)
                button.setGeometry(x, y, 65, 59)
                #button.clicked.connect()
                button.setStyleSheet("background-image: url(white.jpg)")
                if i == 5 and j == 5:
                    button.setIcon(self.mice)
                x += 66
                line.append(button)
            if i % 2 == 0:
                x = 284
            else:
                x = 250
            y += 60
            self.table.append(line)
        self.show()

    # def paintEvent(self,event):
    #
    #     score = QPainter()
    #     score.begin(self)
    #     score.setPen(QColor(Qt.black))
    #     score.setFont(font)
    #     score.drawText(47, 72, "Score:")
    #     score.setPen(QColor(Qt.white))
    #     score.setFont(font)
    #     score.drawText(45,70,"Score:")
    #     score.setPen(QColor(Qt.black))
    #     score.setFont(font)
    #     score.drawText(47, 112, "20000")
    #     score.setPen(QColor(Qt.white))
    #     score.setFont(font)
    #     score.drawText(45, 110, "20000")
    #     score.end()

        # self.shadowTitle = QLabel(self)
        # self.shadowTitle.setText("Score:")
        # self.shadowTitle.setFont(font)
        # self.shadowTitle.setGeometry(85, 42, 130, 50)
        # self.shadowTitle.setStyleSheet("color: black")