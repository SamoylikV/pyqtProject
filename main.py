import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
import os
from time import sleep
import subprocess


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ide.ui', self)
        self.pushButton.clicked.connect(self.compile)

    def compile(self):
        arr = []
        d = open('programm.txt', mode='wt')
        doc = self.textEdit1.document()
        block = doc.begin()
        lines = [block.text()]
        for i in range(1, doc.blockCount()):
            block = block.next()
        lines.append(block.text())
        lines = self.textEdit1.toPlainText().split('\n')
        for _ in lines:
            # print(_)
            d.write(_)
            d.write('\n')
        d.close()
        os.rename(r'programm.txt', r'programm.py')
        # os.system('python programm.py')
        try:
            a = subprocess.check_output('programm.py', shell=True)
        except Exception:
            print('error')
        print(arr)
        tf = 3
        for _ in a:
            if tf == 3:
                print(_, end='')
                if a.index(_) != 0 and a.index(_) != 1 and a.index(_) != -1 and a.index(_) != -2:
                    if _ == "\r" and a[a.index(_) + 1] == 'n' and a[a.index(_) + 3] == "\r":
                        print()
                        tf = 0
            elif tf < 3:
                tf += 1

        # arr = arr.split("r")
        # print(arr)
        os.remove('programm.py')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
