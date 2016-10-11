class Item:
    """
    Класс, используемый для описания клетки игрового поля в модели игры
    """
    def __init__(self, game_table_item):
        """
        Инициализация объекта
        :param game_table_item: Образ клетки на GUI (GameTableItem)
        :return: None
        """
        self.game_table_item = game_table_item
        self.is_filled = False

    def set_item(self, color):
        """
        Назначение клетки
        :param color: Цвет клетки (QColor)
        :return: None
        """
        if self.game_table_item is not None:
            self.game_table_item.fill(color)
        self.is_filled = True

    def del_item(self):
        """
        Очистка клетки
        :return: None
        """
        if self.game_table_item is not None:
            self.game_table_item.unfill()
        self.is_filled = False

    def change_game_table_item(self, game_table_item):
        """
        Изменение game_table_item у объекта
        :param game_table_item: Образ клетки на GUI (GameTableItem)
        :return: None
        """
        self.game_table_item = game_table_item

    def copy(self, item):
        """
        Копирование клетки
        :param item: Новый объект (Item)
        :return: None
        """
        self.game_table_item.copy(item.game_table_item)
        self.is_filled = item.is_filled
