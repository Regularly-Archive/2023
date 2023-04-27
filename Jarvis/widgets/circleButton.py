import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from playsound import playsound

class CircleButton(QPushButton):
    def __init__(self, parent=None, radius=50):
        super(CircleButton, self).__init__(parent)
        self.radius = radius
        self.setFixedSize(radius, radius)
        self.is_power_on = False
        self.setStyleSheet(f"background-color: #62feff; border-radius: {self.radius}px;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().button())
        painter.setPen(Qt.NoPen)
        rect = self.rect()
        painter.drawEllipse(rect)

    # def mousePressEvent(self, event):
    #     self.switch_power_status()

    def switch_power_status(self):
        self.is_power_on = not self.is_power_on
        playsound('.\\resources\\switch.mp3', block=False)
        if self.is_power_on:
            self.setStyleSheet(f"background-color: white; border-radius: {self.radius}px;")
        else:
            self.setStyleSheet(f"background-color: #62feff; border-radius: {self.radius}px;")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.resize(400, 400)
    button = CircleButton(widget, radius=100)
    button.move(75, 75)
    widget.show()
    sys.exit(app.exec_())