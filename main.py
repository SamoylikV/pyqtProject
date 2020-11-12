import sys, random
from score import MyWidget
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import simpleaudio as sa


class Tetris(QMainWindow):
    """
    Класс игры
    """

    def __init__(self):
        super().__init__()
        self.main_window()

    def main_window(self):
        """
        создание главного окна
        """
        self.tetrist_list = tetrist_list(self)
        self.setCentralWidget(self.tetrist_list)

        self.statusbar = self.statusBar()
        self.tetrist_list.to_Statubar[str].connect(self.statusbar.showMessage)

        self.tetrist_list.start()

        self.resize(180, 380)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)
        self.setWindowTitle('Tetris')
        self.show()
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)


class tetrist_list(QFrame):
    """
    поле игры
    """
    to_Statubar = pyqtSignal(str)
    tetrist_list_Width = 10
    tetrist_list_Height = 20
    Speed = 150

    def __init__(self, parent):
        super().__init__(parent)

        self.init_tetrist_list()

    def init_tetrist_list(self):

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.tetrist_list = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clear_tetrist_list()

    def figure_Type(self, x, y):
        '''
        определяет тип фигуры в данном блоке.
        '''
        return self.tetrist_list[(y * tetrist_list.tetrist_list_Width) + x]

    def set_Size(self, x, y, shape):
        '''
        задаём размер поля
        '''
        self.tetrist_list[(y * tetrist_list.tetrist_list_Width) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // tetrist_list.tetrist_list_Width

    def squareHeight(self):
        return self.contentsRect().height() // tetrist_list.tetrist_list_Height

    def start(self):
        """
        начало игры
        """
        if self.isPaused:
            return

        wave_obj = sa.WaveObject.from_wave_file("theme.wav")
        play_obj = wave_obj.play()

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clear_tetrist_list()

        self.to_Statubar.emit(str(self.numLinesRemoved))

        self.next_Figure()
        self.timer.start(tetrist_list.Speed, self)

    def pause(self):
        """
        функция паузы
        """
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.to_Statubar.emit("paused")

        else:
            self.timer.start(tetrist_list.Speed, self)
            self.to_Statubar.emit(str(self.numLinesRemoved))

        self.update()

    def paintEvent(self, event):
        """
        отрисовка фигурок
        :param event:
        """
        painter = QPainter(self)
        rect = self.contentsRect()

        tetrist_listTop = rect.bottom() - tetrist_list.tetrist_list_Height * self.squareHeight()

        for i in range(tetrist_list.tetrist_list_Height):
            for j in range(tetrist_list.tetrist_list_Width):
                shape = self.figure_Type(j, tetrist_list.tetrist_list_Height - i - 1)

                if shape != figure_list.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    tetrist_listTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != figure_list.NoShape:

            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                tetrist_listTop + (tetrist_list.tetrist_list_Height - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def keyPressEvent(self, event):
        """
        обработка нажатий на клавиатурру для поворота фигурок
        """
        if not self.isStarted or self.curPiece.shape() == figure_list.NoShape:
            super(tetrist_list, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        # рисование упавших вниз частей.

        elif key == Qt.Key_Left:
            self.figure_Move(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.figure_Move(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.figure_Move(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.figure_Move(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(tetrist_list, self).keyPressEvent(event)

    def timerEvent(self, event):
        """
        фсоздаём новую фигуру и передвигаем падающую
        """

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.next_Figure()
            else:
                self.oneLineDown()

        else:
            super(tetrist_list, self).timerEvent(event)

    def clear_tetrist_list(self):
        """
        очистка поля путём помещения путой фигуры
        """
        for i in range(tetrist_list.tetrist_list_Height * tetrist_list.tetrist_list_Width):
            self.tetrist_list.append(figure_list.NoShape)

    def dropDown(self):
        """
        функция ускоренного спуска фигурок
        """
        newY = self.curY

        while newY > 0:

            if not self.figure_Move(self.curPiece, self.curX, newY - 1):
                break

            newY -= 1

        self.figure_Down()

    def oneLineDown(self):

        if not self.figure_Move(self.curPiece, self.curX, self.curY - 1):
            self.figure_Down()

    def figure_Down(self):
        """
        вызывается после достижения фигурки низ
        """
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.set_Size(x, y, self.curPiece.shape())

        self.line_Remove()

        if not self.isWaitingAfterLine:
            self.next_Figure()

    def line_Remove(self):
        """
        вызывается при сборе полной линии от края до края поля и удаляет ее
        """
        numFullLines = 0
        rowsToRemove = []

        for i in range(tetrist_list.tetrist_list_Height):

            n = 0
            for j in range(tetrist_list.tetrist_list_Width):
                if not self.figure_Type(j, i) == figure_list.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, tetrist_list.tetrist_list_Height):
                for l in range(tetrist_list.tetrist_list_Width):
                    self.set_Size(l, k, self.figure_Type(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.to_Statubar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.set_Shape(figure_list.NoShape)
            self.update()

    def call_score(self, score_val):
        """
        Показывает счёт
        """

        dialog = MyWidget(score_val, self)
        dialog.exec_()

    def next_Figure(self):
        """
        создаёт новую фигуру, а если для неё нет места, то пройгрыш
        """
        self.curPiece = Shape()
        self.curPiece.set_Random_Figure()
        self.curX = tetrist_list.tetrist_list_Width // 2 + 1
        self.curY = tetrist_list.tetrist_list_Height - 1 + self.curPiece.minY()

        if not self.figure_Move(self.curPiece, self.curX, self.curY):
            wave_obj = sa.WaveObject.from_wave_file("lose.wav")
            play_obj = wave_obj.play()
            self.to_Statubar.emit("Game over")
            self.call_score(int(self.numLinesRemoved))
            self.curPiece.set_Shape(figure_list.NoShape)
            self.timer.stop()
            self.isStarted = False
            # app = QApplication(sys.argv)
            # ex = MyWidget(self)
            # ex.exec_()
            # sys.exit(app.exec())

    def figure_Move(self, next_Figure, newX, newY):
        """
        перемещаем фигуру когда фигура не аходится на краю доски
        """
        for i in range(4):

            x = newX + next_Figure.x(i)
            y = newY - next_Figure.y(i)

            if x < 0 or x >= tetrist_list.tetrist_list_Width or y < 0 or y >= tetrist_list.tetrist_list_Height:
                return False

            if self.figure_Type(x, y) != figure_list.NoShape:
                return False

        self.curPiece = next_Figure
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def drawSquare(self, painter, x, y, shape):

        """
            Создание фигур по квадратам
        """

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class figure_list(object):
    """
    Фигуры
    """
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    """
    Фигуры
    """

    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = figure_list.NoShape

        self.set_Shape(figure_list.NoShape)

    def shape(self):
        return self.pieceShape

    def set_Shape(self, shape):
        """
        инициализация фигуры
        """

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def set_Random_Figure(self):
        """
        выбор случайной фигуры
        """
        self.set_Shape(random.randint(1, 7))

    """
    методы для работы с координатами
    """

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotateLeft(self):
        """
        поворот фигуры влево
        """

        if self.pieceShape == figure_list.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotateRight(self):
        """
        поворот фигуры вправо
        """
        if self.pieceShape == figure_list.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':
    # запуск
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
