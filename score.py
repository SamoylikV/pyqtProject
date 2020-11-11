import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog


class MyWidget(QDialog):
    def __init__(self, score_val, parent=None):
        super(MyWidget, self).__init__(parent)
        # super().__init__()
        uic.loadUi("score.ui", self)
        self.con = sqlite3.connect("LeaderBoard.db")
        self.pushButton.clicked.connect(self.add_elem)
        self.modified = {}
        self.titles = None
        self.score_val = score_val
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM small_table", ).fetchall()
        print(result)
        if len(result) > 0:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}

    def add_elem(self):
        name = str(self.lineEdit.text())
        print(name)
        cur = self.con.cursor()
        cur.execute('''INSERT INTO small_table(name,score) VALUES(?,?)''', (name, self.score_val))
        self.con.commit()
        self.update_result()
        #kot



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
