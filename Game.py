import random
import sys
import time
from copy import deepcopy
from functools import partial

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QGraphicsDropShadowEffect, QPushButton, QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsProxyWidget
from PyQt5.QtGui import QFont, QColor, QPainter, QPixmap, QIcon, QPolygonF, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QPointF

"""
Trap the mouse game

Jocul este format dintr-o tablă de dimensiune 11 x 11, fiecare bloc fiind un hexagon. În mijlocul acestei table se află un șoarece, iar inițial
tabla de joc generată are între 5-10 piloni puși. Scopul player-ului este de a amplasa piloni astfel încât să blocheze șoarecele într-un singur
bloc. În acest caz câștigă. Pentru fiecare pilon pus, șoarecele se va muta cu o poziție. Dacă reușește să iasă din tabla de joc, acesta câștigă.

Module folosite:
  -random
  -sys
  -copy
  -PyQt5.QtWidgets
  -PyQt5.QtGui
  -PyQt5.QtCore
  
Clase folosite:
  -HexButton
    În această clasă sunt modelate blocurile din tabla de joc.
  -TrapTheMouse
    Aceasta este clasa principală, cuprinzând logica jocului, dar și elemente de grafică.    
    
  Programul main.py este folosit pentru a genera jocul și de a putea aplica funcționalitatea acestuia.
"""
class HexButton(QGraphicsPolygonItem):

    """
    Clasa HexButton se ocupă cu generarea blocurilor tablei de joc, dar și de apariția șoarecelui, respectiv a pilonilor amplasați.

    Metode folosite:
      -__init__()
        Este inițializat hexagonul, forma și dimensiunea acestuia, dar și culoarea, posibilitatea de a cuprinde o imagine în interior și
        atașarea de un buton pentru amplasarea pilonilor.
    """

    def __init__(self):
        super().__init__(parent = None)
        self.setAcceptHoverEvents(True)

        self.polygon = QPolygonF([
            QPointF(-13.5, 300), QPointF(13.5, 300), QPointF(25, 321.75),
            QPointF(13.5, 350), QPointF(-13.5, 350), QPointF(-25, 321.75)
        ])
        self.setPolygon(self.polygon)
        self.setRotation(30);
        self.setBrush(QBrush(QColor(0,0,255)))
        self.mice_image = QGraphicsPixmapItem(QPixmap("Jerry.png").scaled(40,40))
        image_x = -self.mice_image.pixmap().width() / 2
        image_y = -self.mice_image.pixmap().height() / 2
        self.mice_image.setPos(self.polygon.boundingRect().center() + QPointF(image_x, image_y))
        self.btn = QPushButton()
        self.btn.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.button_proxy = QGraphicsProxyWidget(self)
        self.button_proxy.setWidget(self.btn)
        self.button_proxy.setPos(self.polygon.boundingRect().center() - QPointF(self.button_proxy.size().width() / 2, self.button_proxy.size().height() / 2))

class TrapTheMouse(QMainWindow):

    """
    Clasa TrapTheMouse conține logica jocului, clasificarea pe nivele de dificultate și generarea ferestrei pentru joc.

    Metode:
      -__init__()
        Se inițializează atributele principale pentru clasa respectivă.
      -initial_state()
        Se generează fereastra cu starea inițială a jocului dar și partea de background.
      -final_state(mice,table)
        Se verifică dacă o stare a jocului este stare finală.
      -put_piece(table,a,b)
        Se pune un pilon pe blocul care corespunde coordonatelor (a,b).
      -valid_piece(table,a,b)
        Se verifică dacă se poate amplasa pilonul pe poziția(a,b)
      -transition(table,mice,x,y)
        Se poziționează șoarecele pe poziția (x,y)
      -validation(table,mice,x,y)
        Se verifică dacă șoricelul poate fi amplasat pe poziția (x,y)
      -score_road(table,mice,directions)
        Se stabilește scorul pentru fiecare drum care poate fi parcurs de șoarece
      -heuristic(table,mice)
        Se calculează euristica pentru o stare a jocului.
      -minimax(depth,table,mice,player,alpha,beta)
        Se calculează toate posibilitățile de joc până la adâncimea depth și se alege cel mai bun punctaj.
      -mice_move(difficulty)
        Se stabilește mutarea șoarecelui în funcție de atributul difficulty. Acesta va fi citit din terminal.
      -graphic_wall(table,i,j)
        Se reprezintă grafic amplasarea pilonului pe poziția (i,j), dar și a șoricelului atunci când se joacă 2 adversari
      -game()
        Se desfășoară jocul principal.

    Atribute:
      -table: tabla de joc cu memorarea pilonilor și a șoarecelui
      -mice: coordonatele șoarecelui
      -ok: stabilirea următorului jucător
      -opponent: gradul de dificultate al jocului
    """

    def __init__(self, opponent):
        super().__init__()
        self.table = []
        self.mice = [5, 5]
        self.ok = 0
        self.opponent = opponent
        self.turn = 0

    def initial_state(self):
        self.resize(1030, 730)
        self.move(100, 100)
        self.setStyleSheet("background-color: rgb(100,200,150)")
        central = QWidget(self)
        self.setCentralWidget(central)
        scene = QGraphicsScene()
        view = QGraphicsView(scene)
        layout = QVBoxLayout(central)
        self.graphicTable = []
        x = 250
        y = 30
        lx = 48
        ly = 45
        for i in range(11):
            line = []
            graphicLine = []
            for j in range(11):
                if i == 0:
                    margin_button = HexButton()
                    margin_button.setBrush(QBrush(QColor(0,0,0,0)))
                    margin_button.setPen(QPen(Qt.NoPen))
                    scene.addItem(margin_button)
                    margin_button.setPos(x - 24, y - 45)
                    m = -1
                    n = deepcopy(j)
                    margin_button.btn.clicked.connect(lambda _, first=m, second=n: self.graphic_wall(self.table, self.mice, self.turn, m=first, n=second))
                if j == 0:
                    margin_button = HexButton()
                    margin_button.setBrush(QBrush(QColor(0, 0, 0, 1)))
                    margin_button.setPen(QPen(Qt.NoPen))
                    scene.addItem(margin_button)
                    margin_button.setPos(x - 48, y)
                    m = deepcopy(i)
                    n = -1
                    margin_button.btn.clicked.connect(lambda _, first=m, second=n: self.graphic_wall(self.table, self.mice, self.turn, m=first, n=second))
                if i == 10:
                    margin_button = HexButton()
                    margin_button.setBrush(QBrush(QColor(0, 0, 0, 1)))
                    margin_button.setPen(QPen(Qt.NoPen))
                    scene.addItem(margin_button)
                    margin_button.setPos(x - 24, y + 45)
                    m = 11
                    n = deepcopy(j)
                    margin_button.btn.clicked.connect(lambda _, first=m, second=n: self.graphic_wall(self.table, self.mice, self.turn, m=first, n=second))
                if j == 10:
                    margin_button = HexButton()
                    margin_button.setBrush(QBrush(QColor(0, 0, 0, 1)))
                    margin_button.setPen(QPen(Qt.NoPen))
                    scene.addItem(margin_button)
                    margin_button.setPos(x + 48, y)
                    m = deepcopy(i)
                    n = 11
                    margin_button.btn.clicked.connect(lambda _, first=m, second=n: self.graphic_wall(self.table, self.mice, self.turn, m=first, n=second))
                button = HexButton()
                scene.addItem(button)
                button.setPos(x, y)
                m = i
                n = j
                button.btn.clicked.connect(lambda _, first=m, second=n : self.graphic_wall(self.table, self.mice, self.turn, m=first, n=second))
                x += lx
                line.append(0)
                graphicLine.append(button)
            if i % 2 == 0:
                x = 277
            else:
                x = 250
            y += ly
            self.table.append(line)
            self.graphicTable.append(graphicLine)
        obstacles = random.randint(5, 10)
        self.table[5][5] = 2
        self.graphicTable[5][5].mice_image.setParentItem(self.graphicTable[5][5])
        while obstacles > 0:
            i = random.randint(0, 10)
            j = random.randint(0, 10)
            if self.table[i][j] == 0:
                self.table[i][j] = 1
                self.graphicTable[i][j].setBrush(QBrush(QColor(255,0,0)))
                obstacles -= 1
        layout.addWidget(view)
        self.show()

    def final_state(self, mice, table):
        if mice[0] == -1 or mice[0] == 11 or mice[1] == -1 or mice[1] == 11:
            return 1
        elif mice[0] - 1 >= 0 and mice[0] + 1 <= 10 and mice[1] - 1 >= 0 and mice[1] + 1 <= 10:
            if table[mice[0]][mice[1] - 1] == 1 and table[mice[0]][mice[1] + 1] == 1 and table[mice[0] - 1][mice[1]] == 1 and table[mice[0] + 1][mice[1]] == 1:
                if mice[0] % 2 == 0 and table[mice[0] - 1][mice[1] - 1] == 1 and table[mice[0] + 1][mice[1] - 1] == 1:
                    return 2
                elif mice[0] % 2 == 1 and table[mice[0] - 1][mice[1] + 1] == 1 and table[mice[0] + 1][mice[1] + 1] == 1:
                    return 2
        return 0

    def put_piece(self, table, a, b):
        table[a][b] = 1
        return table

    def valid_piece(self, table, a, b):
        if table[a][b] == 0 and a > -1 and a < 11 and b > -1 and b < 11:
            return 1
        else:
            return 0

    def transition(self, table, mice, x, y):
        table[mice[0]][mice[1]] = 0
        if x > -1 and x < 11 and y > -1 and y < 11:
            table[x][y] = 2
        mice = [x,y]
        return [table,mice]

    def validation(self, table, mice, x, y):
        if (x > -1 and x < 11 and y > -1 and y < 11 and table[x][y] == 0) or x == -1 or x == 11 or y == -1 or y == 11:
            if [x, y] == [mice[0], mice[1] - 1] or [x, y] == [mice[0], mice[1] + 1] or [x, y] == [mice[0] - 1, mice[1]] or [x, y] == [mice[0] + 1, mice[1]]:
                return 1
            elif x % 2 == 1 and ([x, y] == [mice[0] - 1, mice[1] - 1] or [x, y] == [mice[0] + 1, mice[1] - 1]):
                return 1
            elif x % 2 == 0 and ([x, y] == [mice[0] - 1, mice[1] + 1] or [x, y] == [mice[0] + 1, mice[1] + 1]):
                return 1
        return 0

    def score_road(self, table, mice, directions):
        score = 0
        distance = 0
        while mice[0] >= 0 and mice[0] <= 10 and mice[1] >= 0 and mice[1] <= 10:
            mice[0] += directions[0]
            mice[1] += directions[1]
            distance += 1
            if mice[0] >= 0 and mice[0] <= 10 and mice[1] >= 0 and mice[1] <= 10:
                if table[mice[0]][mice[1]] == 1:
                    score += 10 * distance
                else:
                    score += 1
            else:
                score += 1
        return score

    def heuristic(self, table, mice):
        minim = 10000
        directions = [[-1,0],[0,1],[-1,0],[1,0]]
        if mice[0] % 2 == 0:
            directions.append([-1,-1])
            directions.append([1,-1])
        else:
            directions.append([-1,1])
            directions.append([1,1])
        for direction in directions:
            copy_mice = deepcopy(mice)
            copy_table = deepcopy(table)
            value = self.score_road(copy_table, copy_mice, direction)
            minim = min(minim, value)
        return minim

    def minimax(self, depth, table, mice, player, alpha, beta):
        if self.final_state(mice, table) != 0 or depth == 0:
            if self.final_state(mice, table) == 1:
                return 0
            elif self.final_state(mice, table) == 2:
                return 1200
            else:
                return self.heuristic(table, mice)
        else:
            if player == 1:
                coordinates = [[mice[0],mice[1] - 1], [mice[0],mice[1] + 1], [mice[0] - 1,mice[1]], [mice[0] + 1,mice[1]]]
                if mice[0] % 2 == 1:
                    coordinates.append([mice[0] - 1, mice[1] + 1])
                    coordinates.append([mice[0] + 1, mice[1] + 1])
                else:
                    coordinates.append([mice[0] - 1, mice[1] - 1])
                    coordinates.append([mice[0] + 1, mice[1] - 1])
                minim = 100000
                for state in coordinates:
                    if self.validation(table, mice, state[0], state[1]) == 1:
                        mice_copy = deepcopy(mice)
                        table_copy = deepcopy(table)
                        result = self.transition(table_copy, mice_copy, state[0], state[1])
                        table_copy = result[0]
                        mice_copy = result[1]
                        copy_alpha = alpha
                        value = self.minimax(depth - 1, table_copy, mice_copy, 0, copy_alpha, beta)
                        minim = min(value, minim)
                        beta = min(value, beta)
                        if beta < copy_alpha:
                            break
                return minim
            else:
                maxim = -100000
                for i in range(11):
                    for j in range(11):
                        if self.valid_piece(table, i, j) == 1:
                            mice_copy = deepcopy(mice)
                            table_copy = deepcopy(table)
                            table_copy = self.put_piece(table_copy, i, j)
                            copy_beta = beta
                            value = self.minimax(depth - 1, table_copy, mice_copy, 1, alpha, beta)
                            maxim = max(value, maxim)
                            alpha = max(value, alpha)
                            if beta < alpha:
                                break
                return maxim

    def mice_move(self, difficulty):
        coordinates = [[self.mice[0], self.mice[1] - 1], [self.mice[0], self.mice[1] + 1], [self.mice[0] - 1, self.mice[1]], [self.mice[0] + 1, self.mice[1]]]
        if self.mice[0] % 2 == 1:
            coordinates.append([self.mice[0] - 1, self.mice[1] + 1])
            coordinates.append([self.mice[0] + 1, self.mice[1] + 1])
        else:
            coordinates.append([self.mice[0] - 1, self.mice[1] - 1])
            coordinates.append([self.mice[0] + 1, self.mice[1] - 1])
        state_points = dict()
        for state in coordinates:
            if self.validation(self.table, self.mice, state[0], state[1]) == 1:
                mice_copy = deepcopy(self.mice)
                table_copy = deepcopy(self.table)
                result = self.transition(table_copy, mice_copy, state[0], state[1])
                table_copy = deepcopy(result[0])
                mice_copy = deepcopy(result[1])
                points = self.minimax(2, table_copy, mice_copy, 0, -10000, 10000)
                if points not in state_points:
                    state_points[points] = [state]
                else:
                    state_points[points].append(state)
        state_points = dict(sorted(state_points.items()))
        if difficulty == 'hard':
            key_state = list(state_points)
            state = state_points[key_state[0]][0]
            self.graphicTable[self.mice[0]][self.mice[1]].scene().removeItem(self.graphicTable[self.mice[0]][self.mice[1]].mice_image)
            result = self.transition(self.table, self.mice, state[0], state[1])
            self.table = deepcopy(result[0])
            self.mice = deepcopy(result[1])
            if self.mice[0] > -1 and self.mice[0] < 11 and self.mice[1] > -1 and self.mice[1] < 11:
                self.graphicTable[state[0]][state[1]].mice_image.setParentItem(self.graphicTable[state[0]][state[1]])
        elif difficulty == 'medium':
            key_state = list(state_points)
            self.medium_contor += 1
            if len(key_state) > 1:
                index = random.randint(0, len(key_state) - 1)
            else:
                index = 0
            state = state_points[key_state[index]][0]
            self.graphicTable[self.mice[0]][self.mice[1]].scene().removeItem(self.graphicTable[self.mice[0]][self.mice[1]].mice_image)
            result = self.transition(self.table, self.mice, state[0], state[1])
            self.table = deepcopy(result[0])
            self.mice = deepcopy(result[1])
            if self.mice[0] > -1 and self.mice[0] < 11 and self.mice[1] > -1 and self.mice[1] < 11:
                self.graphicTable[state[0]][state[1]].mice_image.setParentItem(self.graphicTable[state[0]][state[1]])
        elif difficulty == 'easy':
            key_state = list(state_points)
            self.easy_contor += 1
            if len(key_state) > 1:
                index = random.randint(1, len(key_state) - 1)
            else:
                index = 0
            state = state_points[key_state[index]][0]
            self.graphicTable[self.mice[0]][self.mice[1]].scene().removeItem(self.graphicTable[self.mice[0]][self.mice[1]].mice_image)
            result = self.transition(self.table, self.mice, state[0], state[1])
            self.table = deepcopy(result[0])
            self.mice = deepcopy(result[1])
            if self.mice[0] > -1 and self.mice[0] < 11 and self.mice[1] > -1 and self.mice[1] < 11:
                self.graphicTable[state[0]][state[1]].mice_image.setParentItem(self.graphicTable[state[0]][state[1]])

    def graphic_wall(self, table, mice, turn, m, n):
        if turn == 0:
            if self.valid_piece(table, m, n) == 1:
                self.put_piece(table, m, n)
                self.graphicTable[m][n].setBrush(QBrush(QColor(255, 0, 0)))
                self.ok = 1
        else:
            print("Verify")
            if self.validation(table, mice, m, n):
                print("Yes")
                self.graphicTable[self.mice[0]][self.mice[1]].scene().removeItem(self.graphicTable[self.mice[0]][self.mice[1]].mice_image)
                result = self.transition(table, mice, m, n)
                self.table = deepcopy(result[0])
                self.mice = deepcopy(result[1])
                if self.mice[0] > -1 and self.mice[0] < 11 and self.mice[1] > -1 and self.mice[1] < 11:
                    self.graphicTable[self.mice[0]][self.mice[1]].mice_image.setParentItem(self.graphicTable[self.mice[0]][self.mice[1]])
                self.ok = 0

    def game(self):
        self.initial_state()
        player = 0
        while self.final_state(self.mice, self.table) == 0:
            if self.opponent == 'human':
                if player == 0:
                    print("Human1 turn")
                    while self.ok == 0:
                        QApplication.processEvents()
                    player = 1
                    self.turn = 1
                else:
                    print("Human2 turn")
                    while self.ok == 1:
                        QApplication.processEvents()
                    print("End of human2 loop")
                    player = 0
                    self.turn = 0
            else:
                if player == 0:
                    while self.ok == 0:
                        QApplication.processEvents()
                    player = 1
                    self.ok = 0
                    self.turn = 0
                else:
                    self.mice_move(self.opponent)
                    player = 0
        if self.final_state(self.mice, self.table) == 1:
            label = QLabel("The mice won!", self)
        else:
            label = QLabel("The player won!", self)
        label.setGeometry(450,650,130,40)
        label.show()




