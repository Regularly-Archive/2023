from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QFrame
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QPalette
from PyQt5.QtCore import QTimer, QSize
import sys

class TypeWriterLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self._background_color = QColor(255, 255, 255, 100)  # 半透明背景色
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_text)
        self._text = ''
        self._index = 0
        self.setStyleSheet('')
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        painter.setBrush(self._background_color)
        painter.drawRect(self.rect())  # 绘制背景
        painter.setPen(self.palette().color(QPalette.WindowText))
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self._text)
        text_height = font_metrics.height()
        x = (self.width() - text_width) / 2
        y = (self.height() - text_height) / 2 + font_metrics.ascent()
        painter.drawText(x, y, self._text[:self._index])
        
    def setText(self, text):
        self._text = text
        self._index = 0
        self._timer.start(100)
        
    def stop(self):
        self._timer.stop()
        
    def setBackgroundColor(self, color):
        self._background_color = color
        
    def sizeHint(self):
        return QSize(100, 30)
    
    def update_text(self):
        self._index += 1
        if self._index > len(self._text):
            self._timer.stop()
            self._index = len(self._text)
        self.update()
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setFixedSize(800,640)
    label = TypeWriterLabel('Hello, world!', parent=widget)
    label.setText('Hello, world!')
    label.setFixedWidth(480)
    label.setBackgroundColor(QColor(0, 0, 0, 0))  # 设置背景色
    widget.show()
    sys.exit(app.exec_())