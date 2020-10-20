import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
import os
from subprocess import run

d = open('programm.txt', mode='wt')
cmd = [ 'echo', 'arg1', 'arg2' ]

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ide.ui', self)
        self.pushButton.clicked.connect(self.compile)

    def compile(self):
        doc = self.textEdit1.document()
        block = doc.begin()
        lines = [block.text()]
        for i in range(1, doc.blockCount()):
            block = block.next()
        lines.append(block.text())
        lines = self.textEdit1.toPlainText().split('\n')
        d.write('from time import sleep' + '\n')

        for _ in lines:
            print(_)
            d.write(_)
            d.write('\n')
        d.write('sleep(100)')
        d.close()
        os.rename(r'programm.txt', r'programm.py')
        os.system('python programm.py')
        self.labebl.display(run("pwd", capture_output=True).stdout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
