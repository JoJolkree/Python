from Model.FigureForm import FigureForm


class Prototype(FigureForm):
    """
    Прототип фигуры
    """
    def __init__(self, file):
        """
        Инициализация объекта
        :param file: Файл с моделью фигуры
        :return: None
        """
        super().__init__()
        self.parse(file)

    def parse(self, file):
        """
        Парсинг файла и создание view фигуры
        :param file: Файл с моделью фигуры
        :return: None
        """
        view = [[False for x in range(self.dimension)]
                for y in range(self.dimension)]
        with open(file) as f:
            text = f.readlines()
            for i in range(len(text)):
                for j in range(len(text[i])):
                    if text[i][j] == '#':
                        self.view[i][j] = True
