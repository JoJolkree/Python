import sys
from PyQt5.QtWidgets import QApplication

from View.View import View


def main():
    """
    Точка входа в приложение
    :return: None
    """
    app = QApplication(sys.argv)
    qb = View()
    qb.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
