from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QWidget

from View.GameTableItem import GameTableItem


class GameTable(QWidget):
    """
    Класс таблицы, отображаемой в окне программы. Унаследован от QWidget
    """
    def __init__(self, height, width, size):
        """
        Инициализация объекта
        :param height: Количество строк
        :param width: Количество столбцов
        :param size: Размер клетки в пикселях
        :return: None
        """
        super(GameTable, self).__init__()
        self.rows, self.columns = height, width
        self.square_size = size
        self.table = [[GameTableItem() for x in range(self.columns)]
                      for y in range(self.rows)]
        self.setMinimumSize(self.square_size * self.columns + 1,
                            self.square_size * self.rows + 1)

    def paintEvent(self, e):
        """
        Перерисовка таблицы
        :param e: QPaintEvent
        :return: None
        """
        qp = QPainter()
        qp.begin(self)
        for y in range(self.rows + 1):
            qp.drawLine(0, self.square_size * y,
                        self.square_size * self.columns, self.square_size * y)

        for x in range(self.columns + 1):
            qp.drawLine(self.square_size * x, 0, self.square_size * x,
                        self.square_size * self.rows)

        for y in range(self.rows):
            for x in range(self.columns):
                if self.table[y][x].is_filled:
                    brush = QBrush(self.table[y][x].color)
                    qp.fillRect(self.square_size * x + 1,
                                self.square_size * y + 1,
                                self.square_size - 1, self.square_size - 1,
                                brush)
        qp.end()

    def resizeEvent(self, e):
        """
        Изменение размеров виджета. Пересчет размера клетки
        :param e: QResizeEvent
        :return: None
        """
        width = self.width() / self.columns - 1
        height = self.height() / self.rows - 1
        self.square_size = min(width, height)

    # def set_filled(self, row, column, color):
    #     self.table[row][column].fill(color)

    def get_dimensions(self):
        """
        :return: Количество строк, количество столбцов
        """
        return self.rows, self.columns

    def get_element(self, y, x):
        """
        :param y: Координата y клетки
        :param x: Координата x клетки
        :return: Элемент таблицы (GameTableItem), None - в случае ошибки
        """
        try:
            return self.table[y][x]
        except IndexError:
            return None
