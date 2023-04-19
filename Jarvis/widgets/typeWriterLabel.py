from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QFrame
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QPalette
from PyQt5.QtCore import QTimer, QSize
import sys, re

class TypeWriterLabel(QLabel):
    def __init__(self, text='', parent=None, split_length=40):
        super().__init__(text, parent)
        self._background_color = QColor(255, 255, 255, 100)  # 半透明背景色
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_text)
        self._texts = []
        self._char_index = 0
        self._line_index = 0
        self._split_length = split_length
        self.setStyleSheet('')
        
    def paintEvent(self, event):
        if self._line_index >= len(self._texts):
            self._line_index = len(self._texts) - 1
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        painter.setBrush(self._background_color)
        painter.drawRect(self.rect())  # 绘制背景
        painter.setPen(self.palette().color(QPalette.WindowText))
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self._texts[self._line_index])
        text_height = font_metrics.height()
        x = (self.width() - text_width) / 2
        y = (self.height() - text_height) / 2 + font_metrics.ascent()
        painter.drawText(x, y, self._texts[self._line_index][:self._char_index])
        
    def setText(self, text):
        self._texts = self.split_text(text, self._split_length)
        self._char_index = 0
        self._line_index = 0
        self._timer.start(100)
        
    def stop(self):
        self._timer.stop()
        
    def setBackgroundColor(self, color):
        self._background_color = color
        
    def sizeHint(self):
        return QSize(100, 30)
    
    def update_text(self):
        # 如果是最后一页，则直接返回
        if self._line_index >= len(self._texts):
            self._line_index = len(self._texts) - 1
        
        self._char_index += 1
        if self._char_index > len(self._texts[self._line_index]):
            if self._line_index > len(self._texts):
                self._timer.stop()
                self._char_index = len(self._texts[self._line_index])
            else:
                # 如果是最后一页，则直接返回
                self._line_index += 1
                if self._line_index >= len(self._texts):
                    self._line_index = len(self._texts) - 1
                    return
                self._char_index = 0
        self.update()
    
    def split_text(self, text, split_length):
        results = []
        startPos = 0

        if text == None or text == '':
            return []
        
        total_length = len(text)
        if (total_length < split_length):
            return [text]
        
        for i in range(int(total_length / split_length)):
            nextPos = startPos + split_length
            if nextPos >= total_length:
                nextPos = total_length - 1
            results.append(text[startPos:nextPos])
            startPos = nextPos

        return results
        



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