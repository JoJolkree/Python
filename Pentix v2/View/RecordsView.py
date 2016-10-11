from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


class RecordsView(QWidget):
    def __init__(self, records):
        """
        Виджет, отображающий таблицу рекордов
        :param records: таблица рекордов (Records)
        """
        super().__init__()
        self.records = records
        self.label = QLabel(self.records.get_strings())
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 0, 0)
        self.setLayout(self.grid)
        self.timer = QBasicTimer()
        self.timer.start(700, self)

    def timerEvent(self, e):
        """
        Реакция на срабатываение таймера
        :param e: QTimerEvent
        :return: None
        """
        self.label.setText(self.records.get_strings())
        self.update()
