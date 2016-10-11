class FigureForm:
    """
    Общий класс фигуры
    """
    def __init__(self):
        """
        Инициализация объекта
        :return: None
        """
        self.view = [[False for x in range(5)] for y in range(5)]
        self.dimension = 5
