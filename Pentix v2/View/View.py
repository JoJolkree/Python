from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from Model.Board import Board
from View.GameTable import GameTable
from View.RecordsView import RecordsView


class View(QWidget):
    """
    Основное окно программы
    """
    def __init__(self):
        """
        Инициализация объекта
        :return: None
        """
        super(View, self).__init__()
        self.grid = QGridLayout()
        self.table = GameTable(20, 10, 32)
        self.next = GameTable(5, 5, 24)
        self.board = Board(self.table, self.next)
        self.scores = QLabel()
        self.restart = QPushButton()
        self.pause = QPushButton()
        self.state = QLabel()
        self.records = RecordsView(self.board.records)
        self.make_gui()
        self.timer = QBasicTimer()
        self.timer.start(700, self)
        self.setFixedSize(self.height(), self.width())

    def make_gui(self):
        """
        Создание GUI
        :return: None
        """
        self.setWindowTitle('Pentix')
        self.restart.setText('Restart (R)')
        self.restart.clicked.connect(self.restart_game)
        self.pause.setText('Pause (P)')
        self.pause.clicked.connect(self.pause_game)
        self.pause.setFocusPolicy(Qt.NoFocus)
        self.scores.setText('Score: ')
        self.scores.setFocusPolicy(Qt.NoFocus)
        next_fig = QLabel()
        next_fig.setText('Next figure:')
        self.grid.addWidget(self.table, 0, 0, 13, 1)
        self.grid.addWidget(self.restart, 0, 1)
        self.grid.addWidget(self.pause, 1, 1)
        self.grid.addWidget(self.scores, 2, 1)
        self.grid.addWidget(next_fig, 3, 1)
        self.grid.addWidget(self.next, 4, 1)
        self.grid.addWidget(self.state, 5, 1)
        self.grid.addWidget(self.records, 6, 1)
        self.setLayout(self.grid)
        self.grid.setRowStretch(7 , 1)
        self.grid.setColumnStretch(0, 1)
        self.setFocus()
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)

    def pause_game(self):
        """
        Пауза игры
        :return: None
        """
        if self.timer.isActive():
            self.timer.stop()
            self.state.setText('Game paused')
            self.pause.setText('Resume (P)')
            self.restart.setDisabled(True)
        else:
            self.timer.start(700, self)
            self.state.setText('')
            self.pause.setText('Pause (P)')
            self.restart.setDisabled(False)
        self.setFocus()

    def stop_game(self):
        """
        Остановка игры после проигрыша
        :return: None
        """
        self.timer.stop()
        self.state.setText('Game over')

    def restart_game(self):
        """
        Перезапуск игры
        :return: None
        """
        for y in range(len(self.table.table)):
            for x in range(len(self.table.table[y])):
                self.table.table[y][x].unfill()
        self.board = Board(self.table, self.next)
        self.setFocus()
        self.timer.start(700, self)
        self.state.setText('')
        self.board.score = 0

    def timerEvent(self, e):
        """
        Реакция на срабатывание таймера
        :param e: QTimerEvent
        :return: None
        """
        self.board.step()
        self.update()
        if self.board.game_over:
            self.stop_game()
        if self.board.is_falling and self.board.cur_fig is None:
            self.timer.stop()
            self.timer.start(700, self)
            self.board.is_falling = False

    def changeEvent(self, e):
        """
        Реакция на изменение окна
        :param e: QChangeEvent
        :return: None
        """
        self.scores.setText('Score: ' + str(self.board.score))

    def keyPressEvent(self, e):
        """
        Реакция на нажатие клавиши
        :param e: QKeyEvent
        :return: None
        """
        key = e.key()
        if self.timer.isActive() and not self.board.is_falling:
            if key == Qt.Key_Down or key == Qt.Key_S:
                self.board.step()
            if key == Qt.Key_Left or key == Qt.Key_A:
                self.board.left()
            if key == Qt.Key_Right or key == Qt.Key_D:
                self.board.right()
            if key == Qt.Key_Up or key == Qt.Key_W:
                self.board.rotate()
        if key == Qt.Key_R:
            self.restart.click()
        if key == Qt.Key_P:
            self.pause.click()
        if self.timer.isActive():
            if key == Qt.Key_Space:
                self.board.is_falling = True
                self.fall()
        self.update()

    def fall(self):
        self.timer.stop()
        self.timer.start(20, self)
