import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie #Show GIF FIle

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()

        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0, 0]
        self.to_xy = xy
        self.to_xy_diff = [0, 0]
        self.speed = 60
        self.direction = [0, 0] # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None

        self.setupUi()
        self.show()

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        #FramlessWindowHint = Remove FramelessWindowHint
        #if object's location is on top -> WindowStaysOnTopHint
        #else FramlessWindowHint
        self.setWindowFlags(flags)
        #Settings Save
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #NoSystemBackground, TranslucentBackground -> transparent

        label = QtWidgets.QLabel(centralWidget)
            #Make The loation for label

        movie = QMovie(self.img_path)
            #loading the GIF file
        label.setMovie(movie)
            #GIF Setting
        movie.start()
        #Start GIF
        movie.stop()
        #Stop GIF

        w = int(movie.frameRect().size().width() * self.size)
        #width
        h = int(movie.frameRect().size().height() * self.size)
        #height
        movie.setScaledSize(QtCore.QSize(w, h))
        #Set the GIF file

        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)
        #GIF window size location

    # 마우스 놓았을 때
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.to_xy_diff == [0, 0] and self.from_xy_diff == [0, 0]:
            pass
        else:
            self.walk_diff(self.from_xy_diff, self.to_xy_diff, self.speed, restart=True)

    # 마우스 눌렀을 때
    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.localPos = a0.localPos()

    # 드래그 할 때
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        self.timer.stop()
        self.xy = [(a0.globalX() - self.localPos.x()), (a0.globalY() - self.localPos.y())]
        self.move(*self.xy)

    def walk(self, from_xy, to_xy, speed=60):
        self.from_xy = from_xy
        #GIF source 
        self.to_xy = to_xy
        #GIF Destination
        self.speed = speed
        #GIF speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    # 초기 위치로부터의 상대적 거리를 이용한 walk
    def walk_diff(self, from_xy_diff, to_xy_diff, speed=60, restart=False):
        self.from_xy_diff = from_xy_diff
        self.to_xy_diff = to_xy_diff
        self.from_xy = [self.xy[0] + self.from_xy_diff[0], self.xy[1] + self.from_xy_diff[1]]
        self.to_xy = [self.xy[0] + self.to_xy_diff[0], self.xy[1] + self.to_xy_diff[1]]
        self.speed = speed
        if restart:
            self.timer.start()
        else:
            self.timer.timeout.connect(self.__walkHandler)
            self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
            #set the location by left
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1
            #set the location by right

        if self.direction[0] == 0:
            self.xy[0] -= 1
            #move to left
        else:
            self.xy[0] += 1
            #move to right

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
            #set the location by left
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1
            #set the location by right

        if self.direction[1] == 0:
            self.xy[1] -= 1
            #move to left
        else:
            self.xy[1] += 1
            #move to right

        self.move(*self.xy)
        #Move!

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s = Sticker('./amongus/left.gif', xy=[-80, 200], on_top=False)

    s1 = Sticker('./amongus/red_vent.gif', xy=[780, 1020], size=0.3, on_top=True)

    s2 = Sticker('./amongus/orange.gif', xy=[1200, 1020], size=0.3, on_top=True)


    s3 = Sticker('./amongus/blue_green.gif', xy=[400, 920], size=1.0, on_top=True)

    s4 = Sticker('./amongus/mint.gif', xy=[1000, 950], size=0.2, on_top=True)
    # s4.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=120)

    s5 = Sticker('./amongus/brown.gif', xy=[200, 1010], size=0.75, on_top=True)

    s6 = Sticker('./amongus/yellow.gif', xy=[1850, 800], size=0.75, on_top=True)
    s6.walk(from_xy=[0, 800], to_xy=[1850, 800], speed=240)

    s7 = Sticker('./amongus/magenta.gif', xy=[1500, 900], size=0.5, on_top=True)
    s7.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=180)

    sys.exit(app.exec_())
