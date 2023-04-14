import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QPoint
class Circle:
    def __init__(self, center, max_radius, max_alpha, duration):
        self.center = center
        self.max_radius = max_radius
        self.max_alpha = max_alpha
        self.duration = duration
        self.radius = 0
        self.alpha = 0
        self.elapsed_time = 0

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            return False
        self.radius = self.max_radius * self.elapsed_time / self.duration
        self.alpha = self.max_alpha * (1 - self.elapsed_time / self.duration)
        return True
    
    def draw(self, painter):
        painter.setPen(QColor(255, 255, 255, 100))
        painter.setBrush(QBrush(QColor(255, 255, 255, self.alpha)))
        painter.drawEllipse(250 - self.radius, 250 - self.radius, self.radius, self.radius)

class CircleWidget(QWidget):
    def __init__(self, parent, center, max_radius, max_alpha, duration, max_count):
        super().__init__(parent)
        # 初始化变量
        self.color = QColor(255, 255, 255, 100)
        self.center = center
        self.max_radius = max_radius
        self.max_alpha = max_alpha
        self.duration = duration
        self.max_count = max_count
        self.circles = []
        self.count = 0
        self.is_speaking = False
        # 启动一个定时器，用于更新波纹的状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_circle)
        self.timer.start(self.duration)
    def set_is_speaking(self, is_speaking):
        self.is_speaking = is_speaking
    def paintEvent(self, event):
        painter = QPainter(self)
        for circle in self.circles:
            circle.draw(painter)
    def update_circle(self):
        dt = self.timer.interval() / 1000
        if self.count >= self.max_count:
            self.timer.stop()
            return
        circle = Circle(self.center, self.max_radius, self.max_alpha, self.duration)
        if circle.update(dt):
            self.circles.append(circle)
        else:
            self.count += 1
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(400, 400)
    widget.setObjectName("MainWindow")
    widget.setStyleSheet("#MainWindow{background-color:black}")
    center = QPoint(200,100)
    max_radius = 100
    max_alpha = 255
    duration = 10  # seconds
    max_count = 20
    circle = CircleWidget(widget, center, max_radius, max_alpha, duration, max_count)
    circle.move(100, 100)
    circle.set_is_speaking(True)
    widget.show()
    sys.exit(app.exec_())