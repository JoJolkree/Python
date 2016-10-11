from PyQt5.QtGui import QColor


class GameTableItem:
    """
    Объект rлетки, назначаемый в таблицу GameTable
    """
    default_color = QColor(255, 255, 255)

    def __init__(self):
        """
        Инициализация объекта
        :return: None
        """
        self.color = GameTableItem.default_color
        self.is_filled = False

    def fill(self, color):
        """
        Заполнение клетки
        :param color: Цвет клетки (QColor)
        :return: None
        """
        self.color = color
        self.is_filled = True

    def unfill(self):
        """
        Освобождение клетки
        :return: None
        """
        self.color = GameTableItem.default_color
        self.is_filled = False

    def copy(self, item):
        """
        Копирование клетки
        :param item: Модель элемента (Item)
        :return: None
        """
        self.color = item.color
        self.is_filled = item.is_filled
