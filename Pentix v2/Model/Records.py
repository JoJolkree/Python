import os
import pickle


class Records:
    def __init__(self):
        """
        Инициализация таблицы рекордов
        """
        self.records = []
        if os.path.exists('records.txt'):
            with open('records.txt', 'rb') as f:
                self.records = pickle.load(f)

    def add_record(self, name, score):
        """
        Добавление рекорда в таблицу с учетом сортировки
        :param name: имя игрока
        :param score: счет игрока
        :return: None
        """
        if len(self.records) == 0:
            self.records.append((name, score))
        elif len(self.records) < 10 or self.records[9][1] < score:
            self.records.append((name, score))
            sorted(self.records, key=lambda x: x[1])
        elif self.records[9][1] < score:
            self.records[9] = (name, score)
            sorted(self.records, key=lambda x: x[1])

        with open('records.txt', 'wb') as f:
            f.seek(0)
            f.truncate()
            f.seek(0)
            pickle.dump(self.records, f)

    def get_strings(self):
        """
        :return: строка с таблицей рекордов
        """
        result = ''
        result += 'Records: \n'
        for i in range(len(self.records)):
            result += str(self.records[i][0]) + ': ' + str(self.records[i][1]) + '\n'
        return result

    def check_score(self, score):
        return len(self.records) < 10 or self.records[9] < score
