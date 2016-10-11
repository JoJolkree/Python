import copy

from Model.FigureForm import FigureForm


class Figure(FigureForm):
    """
    Класс фигуры, отображающейся на игровом поле
    """
    def __init__(self, prototype, color, board):
        """
        Инициализация фигуры
        :param prototype: Прототип фигуры (Prototype)
        :param color: Цвет фигуры (QColor)
        :param board: Игровое поле (Board)
        :return: None
        """
        super().__init__()
        self.board = board
        self.view = copy.deepcopy(prototype.view)
        self.old_coords = []
        self.cur_coords = []
        self.next_coords = []
        self.bottoms = []
        self.color = color
        self.x, self.y = 3, -4

    def step(self):
        """
        Падение фигуры на одну клетку вниз
        :return: True, если нет возможности ходить, иначе - False
        """
        if self.make_next(self.y + 1, self.x):
            self.make_bottoms()
            if self.check_bottoms():
                return True
            self.y += 1
            self.show()
            return False

    def left(self):
        """
        Перемещение фигуры на одну клетку влево
        :return: None
        """
        if self.make_next(self.y, self.x - 1):
            if not self.left_free():
                return
            self.x -= 1
            self.show()

    def right(self):
        """
        Перемещение фигуры на одну клетку вправо
        :return: None
        """
        if self.make_next(self.y, self.x + 1):
            if not self.right_free():
                return
            self.x += 1
            self.show()

    def rotate(self):
        """
        Поворот view по часовой стрелке
        :return: None
        """
        new_view = self.rotate_view()
        is_true_view = self.check_rotate(self.view, new_view)
        if self.check_view(new_view) and is_true_view:
            self.view = new_view
            self.make_next(self.y, self.x)
            self.show()

    def check_rotate(self, old_view, view):
        """
        Проверка на свободные клетки после поворота view
        :param old_view: view фигуры до поворота
        :param view: view фигуры после поворота
        :return: True, если поворот возможен, иначе - False
        """
        res = True
        for y in range(len(view)):
            for x in range(len(view[y])):
                if view[y][x] and not old_view[y][x]:
                    res = res and not self.board.table[y + self.y][x + self.x].is_filled
        return res

    def rotate_view(self):
        """
        Поворот модели фигуры (view) на 90 градусов по часовой стрелке
        :return: Новая модель фигуры (view)
        """
        new_view = []
        for x in range(len(self.view[0])):
            new_view.append([])
            for y in range(len(self.view) - 1, -1, -1):
                new_view[x].append(self.view[y][x])
        return new_view

    def check_view(self, view):
        """
        Проверка модели фигуры на нахождение в границах игрового поля
        :param view: Модель фигуры (view)
        :return: True, если поворот возможен, иначе - False
        """
        coords = []
        self.find_coords(coords, self.y, self.x, view)
        return self.check_left_right(coords)

    def show(self):
        """
        Отображение фигуры на игровом поле
        :return: None
        """
        self.old_coords = self.cur_coords
        self.cur_coords = self.next_coords
        self.clear()
        for coord in self.cur_coords:
            if coord[0] >= 0:
                self.board.table[coord[0]][coord[1]].set_item(self.color)

    def make_next(self, next_y, next_x):
        """
        Проверка фигуры после выполнения какого-либо действия на нахождения
        внутри игрового поля
        :param next_y: Координата y фигуры после какого-либо действия
        :param next_x: Координата x фигуры после какого-либо действия
        :return: True, если действие возможно, иначе - False
        """
        self.next_coords = []
        self.find_coords(self.next_coords, next_y, next_x, self.view)
        return self.check_left_right(self.next_coords)

    @staticmethod
    def find_coords(coords, next_y, next_x, view):
        """
        Нахождение координат фигуры после какого-либо действия
        :param coords: Пустой массив массивов ([[]])
        :param next_y: Координата y фигуры после какого-либо действия
        :param next_x: Координата x фигуры после какого-либо действия
        :param view: Модель фигуры (view)
        :return: coords
        """
        for y in range(len(view)):
            for x in range(len(view[y])):
                if view[y][x]:
                    coords.append((y + next_y, x + next_x))
        return coords

    def make_bottoms(self):
        """
        Нахождение координат всех нижних блоков фигуры
        :return: None
        """
        self.bottoms.clear()
        for coord in self.cur_coords:
            if (coord[0] + 1, coord[1]) not in self.cur_coords:
                self.bottoms.append(coord)

    @staticmethod
    def check_left_right(coords):
        """
        Проверка фигуры на нахождение в игровом поле после перемещения
        налево/направо
        :param coords: Координаты фигуры ([[]])
        :return: True, если фигура внутри поля, иначе - False
        """
        result = True
        for coord in coords:
            result = result and 0 <= coord[1] <= 9
        return result

    def left_free(self):
        """
        Проверка возможности движения фигуры влево
        :return: True, если перемещение возможно, иначе - False
        """
        arr = self.make_left_borders()
        for coords in arr:
            if coords[0] >= 0 and (
                            coords[1] == -1 or self.board.table[coords[0]][
                        coords[1]].is_filled):
                return False
        return True

    def make_left_borders(self):
        """
        Нахождение координат всех левых блоков фигуры
        :return: Координаты всех левых блоков фигуры ([()])
        """
        arr = []
        for coords in self.next_coords:
            if coords[1] == self.x - 1 \
                    or (coords[0], coords[1] - 1) not in self.next_coords:
                arr.append(coords)
        return arr

    def right_free(self):
        """
        Проверка возможности движения фигуры влево
        :return: True, если перемещение возможно, иначе - False
        """
        arr = self.make_right_borders()
        for coords in arr:
            if coords[0] >= 0 and (
                            coords[1] == 10 or self.board.table[coords[0]][
                        coords[1]].is_filled):
                return False
        return True

    def make_right_borders(self):
        """
        Нахождение координат всех правых блоков фигуры
        :return: Координаты всех правых блоков фигуры ([()])
        """
        arr = []
        for coords in self.next_coords:
            if coords[1] == self.x + 5 \
                    or (coords[0], coords[1] + 1) not in self.next_coords:
                arr.append(coords)
        return arr

    def check_bottoms(self):
        """
        Проверка фигуры на падение
        :return: True, если движение вниз невозможно, иначе - False
        """
        for coord in self.bottoms:
            if coord[0] + 1 >= 0 and (coord[0] + 1 == self.board.rows or
                                      self.board.table[coord[0] + 1][
                                              coord[1]].is_filled):
                return True
        return False

    def clear(self):
        """
        Очищает фигуру с игрового поля
        :return: None
        """
        for coord in self.old_coords:
            if coord[0] >= 0:
                self.board.table[coord[0]][coord[1]].del_item()

    def show_next(self, table):
        """
        Отображение следующей фигуры в специальном поле
        :param table: Таблица для отображения фигуры (GameTable)
        :return:
        """
        for y in range(len(self.view)):
            for x in range(len(self.view[y])):
                table.table[y][x].unfill()
                if self.view[y][x]:
                    table.table[y][x].fill(self.color)

    def check_game_over(self):
        """
        Проерка на конец игры
        :return: True, если новой фигуре негде появиться, иначе - False
        """
        for coords in self.cur_coords:
            if coords[0] < 0:
                return True
        return False
