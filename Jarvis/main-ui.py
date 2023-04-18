import sys
import time
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPalette, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QLCDNumber
from PIL import Image, ImageDraw, ImageQt
from widgets.circleButton import CircleButton
from widgets.matplotlibWidget import MatplotlibWidget
from widgets.typeWriterLabel import TypeWriterLabel
from baseJarvisHandler import BaseJarvisHandler
from playsound import playsound
import json, datetime
from conf.appConstants import JarvisEventType

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
        # 顶部数字时钟区域
        self.clock_label = QLCDNumber(self)
        self.clock_label.setSegmentStyle(QLCDNumber.Filled)
        self.clock_label.setStyleSheet("border: 0px solid black; color: white;")
        self.clock_label.setDigitCount(20)
        self.clock_label.setFixedHeight(35.5)
        self.clock_label.setFixedWidth(self.width())
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.display(self.current_time)
        self.clock_label.move(int((self.width() - self.clock_label.width()) / 2), 10)
        # 顶部数字时钟定时器
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.refresh_system_clock)
        self.clock_timer.start(1000)
        # 底部字幕区域
        self.sub_label = TypeWriterLabel("", self)
        self.sub_label.setStyleSheet("color: white; font-size: 24px; border: 0px solid black;")
        self.sub_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.sub_label.setFixedHeight(75)
        self.sub_label.setFixedWidth(self.width())
        self.sub_label.setFont(QFont("Source Code Pro",9))
        self.sub_label.move(0, self.height() - self.sub_label.height())
        self.sub_label.setBackgroundColor(QColor(255, 255, 255, 0))  # 设置背景
        # 手动唤醒开关
        self.awake_button = CircleButton(self, 99)
        self.awake_button.move(self.width() / 2 - 52, 559)
        self.awake_button.setCursor(Qt.PointingHandCursor)
        self.awake_button.clicked.connect(self.manual_awake)
        # 声纹展示区域
        self.wave_plot = MatplotlibWidget(self)
        self.wave_plot.setFixedSize(150, 75)
        self.wave_plot.startAudio()
        self.wave_plot.setAttribute(Qt.WA_TranslucentBackground)
        self.wave_plot.show()
        # 显示窗口
        self.thread.signal.connect(self.handle_signal)
        self.thread.start()
        self.show()
        
    def set_sub_label(self, text):
        self.sub_label.setText(text)

    def switch_power_status(self):
        self.awake_button.switch_power_status()

    def refresh_system_clock(self):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.display(self.current_time)

    def handle_signal(self, data):
        payload = json.loads(data)
        if payload['evt'] == JarvisEventType.Awake:
            self.switch_power_status()
            self.set_sub_label(payload['text'])
        elif payload['evt'] == JarvisEventType.Idle:
            self.set_sub_label('')
        else:
            self.set_sub_label(payload['text'])

    def manual_awake(self):
        self.handler.awake_by_manual()

class UiJarvisHandler(BaseJarvisHandler):
    def __init__(self, window):
        super().__init__(None)
        self.signal = None

    def onGreet(self, text):
        super().onGreet(text)
        payload = {'evt': JarvisEventType.Greet, 'text': text }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))
    
    def onInputFailed(self):
        super().onInputFailed()
        text = '抱歉，我没有听清，请您再说一遍'
        payload = {'evt': JarvisEventType.InputFailed, 'text': text }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))
        self.tts_engine.speak(text)

    def onInputed(self, text):
        super().onInputed(text)
        payload = {'evt': JarvisEventType.Inputed, 'text': text }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))

    def onOutputFailed(self):
        super().onInputFailed()
        text = "No reply from ChatGPT"
        payload = {'evt': JarvisEventType.OutputFailed, 'text': text }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))
        self.tts_engine.speak(text)

    def onOutputed(self, text):
        super().onOutputed(text)

        payload = {'evt': JarvisEventType.Outputed, 'text': text }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))
        self.tts_engine.speak(text)
    
    def onAwake(self):
        super().onAwake()
        playsound('.\\resources\\ding.wav')
        payload = {'evt': JarvisEventType.Awake, 'text': '正在聆听...' }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))

    def onIdle(self):
        super().onIdle()
        payload = {'evt': JarvisEventType.Idle, 'text': '' }
        if self.signal != None:
            self.signal.emit(json.dumps(payload))

    def set_signal(self, signal):
        self.signal = signal

class Worker(QThread):

    signal = pyqtSignal(str)

    def __init__(self, parent=None, handler=None):
        super(Worker, self).__init__(parent)
        self.handler = handler
        self.handler.set_signal(self.signal)
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self.handler.run()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())