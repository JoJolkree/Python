import os
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QInputDialog

from Model.Figure import Figure
from Model.Item import Item
from Model.Prototype import Prototype
from Model.Records import Records


class Board:
    """
    Модель игрового поля
    """
    def __init__(self, view_table, next_table):
        """
        Инициализация обхекта
        :param view_table: Таблица основного поля (GameTable)
        :param next_table: Таблица следующей фигуры (GameTable)
        :return: None
        """
        self.view_table = view_table
        self.rows, self.columns = self.view_table.get_dimensions()
        # self.rows += 1
        self.table = [[Item(self.view_table.get_element(y, x))
                       for x in range(self.columns)] for y in range(self.rows)]
        self.next_table = next_table
        self.prototypes = []
        for file in os.listdir('Figures'):
            self.prototypes.append(Prototype(os.path.join('Figures', file)))

        self.colors = []
        with open('colors.txt') as f:
            for line in f:
                colors = line.split(' ')
                red, green, blue = map(int, colors)
                self.colors.append(QColor(red, green, blue))

        self.cur_fig = None
        self.next_fig = Figure(
            self.prototypes[random.randint(0, len(self.prototypes) - 1)],
            self.colors[random.randint(0, len(self.colors) - 1)], self)
        self.score = 0
        self.game_over = False
        self.is_falling = False
        self.records = Records()

    def step(self):
        """
        Выполнение шага текущей фигуры
        :return: None
        """
        if self.cur_fig is None:
            self.cur_fig = self.next_fig
            self.next_fig = Figure(
                self.prototypes[random.randint(0, len(self.prototypes) - 1)],
                self.colors[random.randint(0, len(self.colors) - 1)], self)
            self.next_fig.show_next(self.next_table)
        else:
            if self.cur_fig.step():
                self.check()
                self.cur_fig = None
            if self.game_over and self.records.check_score(self.score):
                name, ok = QInputDialog().getText(self.view_table, 'Game over', 'Enter your name: ')
                if ok:
                    self.records.add_record(name, self.score)

    def check(self):
        """
        Проверка на заполненную строку на игровом поле
        :return: None
        """
        self.game_over = self.cur_fig.check_game_over()
        for y in range(len(self.table) - 1, 0, -1):
            if self.check_line(y):
                self.delete_line(y)
                self.score += 1

    def check_line(self, y):
        """
        Проверка строки y на заполнение
        :param y: Номер строки
        :return: True, если строка заполнена, иначе - False
        """
        result = True
        for x in range(len(self.table[y])):
            result = result and self.table[y][x].is_filled
        return result

    def delete_line(self, y):
        """
        Удаление строки y с игрового поля
        :param y: Номер строки
        :return: None
        """
        for x in range(len(self.table[y])):
            self.table[y][x].del_item()
        self.fall_lines(y)
        self.score += 1

    def fall_lines(self, line):
        """
        Падение строк после удаления
        :param line: Номер удаленной строки
        :return: None
        """
        for y in range(line, 1, -1):
            for x in range(len(self.table[y])):
                self.table[y][x].copy(self.table[y - 1][x])
        for x in range(len(self.table[0])):
            self.table[0][x].del_item()

    def left(self):
        """
        Шаг влево
        :return: None
        """
        if self.cur_fig is not None:
            self.cur_fig.left()

    def right(self):
        """
        Шаг вправо
        :return: None
        """
        if self.cur_fig is not None:
            self.cur_fig.right()

    def rotate(self):
        """
        Поворот текущей фигуры
        :return: None
        """
        if self.cur_fig is not None:
            self.cur_fig.rotate()
