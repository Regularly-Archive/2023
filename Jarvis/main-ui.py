import sys
import time
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPalette, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PIL import Image, ImageDraw, ImageQt
from widgets.circleButton import CircleButton
from widgets.matplotlibWidget import MatplotlibWidget
from widgets.typeWriterLabel import TypeWriterLabel
from baseJarvisHandler import BaseJarvisHandler
from playsound import playsound

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.handler = UiJarvisHandler(self)
        self.thread = Worker(None, self.handler)
        self.setWindowTitle("J.A.R.V.I.S")
        desktop = QApplication.desktop()
        print(f"screenSize=({str(desktop.width())},{str(desktop.height())})")
        self.setFixedSize(1366, 768)
        # 设置窗口为全屏
        # self.showFullScreen()
        # 填充背景图片
        palette = QPalette()
        background = QPixmap("background.jpg")
        palette.setBrush(QPalette.Background,QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)
        # 底部字幕区域
        self.sub_label = TypeWriterLabel("", self)
        self.sub_label.setStyleSheet("color: white; font-size: 24px;")
        self.sub_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.sub_label.setFixedHeight(75)
        self.sub_label.setFixedWidth(self.width())
        self.sub_label.setFont(QFont("Source Code Pro",9))
        self.sub_label.move(0, self.height() - self.sub_label.height())
        self.sub_label.setText("Hello, sir. It's Jarvis here. How can I assist you?")
        self.sub_label.setBackgroundColor(QColor(255, 255, 255, 0))  # 设置背景
        # 手动唤醒开关
        self.awake_button = CircleButton(self, 99)
        self.awake_button.move(self.width() / 2 - 52, 559)
        self.awake_button.setCursor(Qt.PointingHandCursor)
        # 声纹展示区域
        self.wave_plot = MatplotlibWidget(self)
        self.wave_plot.setFixedSize(150, 75)
        self.wave_plot.startAudio()
        self.wave_plot.show()
        # 显示窗口
        self.thread.start()
        self.show()
        
        
    def set_sub_label(self, text):
        self.sub_label.setText(text)

    def switch_power_status(self):
        self.awake_button.switch_power_status()

class UiJarvisHandler(BaseJarvisHandler):
    def __init__(self, window):
        super().__init__(None)
        self.window = window

    def onInputFailed(self):
        self.tts_engine.speak('抱歉，我没有听清，请您再说一遍')
        self.window.set_sub_label('抱歉，我没有听清，请您再说一遍')

    def onInputed(self, text):
        super().onInputed(text)
        self.window.set_sub_label(text)

    def onOutputFailed(self):
        super().onInputFailed()
        print("Jarvis: No reply from ChatGPT")

    def onOutputed(self, text):
        self.window.set_sub_label(text)
        self.tts_engine.speak(text)
    
    def onAwake(self):
        super().onAwake()
        playsound('.\\resources\\ding.wav')
        self.window.switch_power_status()

class Worker(QThread):
    def __init__(self, parent=None, handler=None):
        super(Worker, self).__init__(parent)
        self.handler = handler
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self.handler.run()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())