import sys
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPalette, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PIL import Image, ImageDraw, ImageQt
from widgets.circleButton import CircleButton
import pyttsx3
from speech.speech2text import BaiduASR, PaddleSpeechASR
from speech.wakeword import PicoWakeWord
from speech.text2speech import Pyttsx3TTS, BaiduTTS, PaddleSpeechTTS
from talk.openai import ChatGPTBot
from talk.qingyunke import QinYunKeBot
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from aiohttp import ClientSession
import asyncio
from playsound import playsound
from conf.constants import welcome
import requests

# 初始化环境变量
load_dotenv(find_dotenv())

# 百度语音 
BAIDU_ASR_APP_ID = env.get("BAIDU_ASR_APP_ID")
BAIDU_ASR_API_KEY = env.get("BAIDU_ASR_API_KEY")
BAIDU_ASR_SECRET_KEY = env.get("BAIDU_ASR_SECRET_KEY")

# PICOVOICE
PICOVOICE_API_KEY = env.get("PICOVOICE_API_KEY")

# OpenAI
OPENAI_API_ENDPOINT = env.get("OPENAI_API_ENDPOINT")
OPENAI_API_KEY = env.get("OPENAI_API_KEY")

# 初始化引擎
# tts = BaiduTTS(BAIDU_ASR_APP_ID, BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY)
tts = PaddleSpeechTTS()
picowakeword = PicoWakeWord(PICOVOICE_API_KEY, 'Jarvis_en_windows_v2_1_0.ppn')
#baiduasr = BaiduASR(BAIDU_ASR_APP_ID, BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY)
baiduasr = PaddleSpeechASR()
# bot = GBT3Bot(ClientSession(), OPENAI_API_KEY, OPENAI_API_ENDPOINT)
session = requests.session()
bot = ChatGPTBot(session, OPENAI_API_KEY, OPENAI_API_ENDPOINT + '/v1/chat/completions')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        desktop = QApplication.desktop()
        print("屏幕宽:" + str(desktop.width()))
        print("屏幕高:" + str(desktop.height()))
        self.setFixedSize(1366, 768)
        # 填充背景图片
        palette = QPalette()
        background = QPixmap("background.jpg")
        palette.setBrush(QPalette.Background,QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)
        # 设置窗口为全屏
        # self.showFullScreen()
        self.label = QLabel('Hey Jarvis!', self)
        self.label.move(50, 50)
        self.label.setStyleSheet("color:blue")
        self.label.setStyleSheet("background-color:transparent")   
        # 设置窗口背景色为半透明的黑色
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")
        # 创建一个 QLabel 对象，用于显示钢铁侠的图片
        # self.label = QLabel(self)
        # # 加载钢铁侠的图片
        # image = Image.open("ironman.png")
        # # 将图片裁切为圆形
        # image = make_circle(image)
        # # 将图片转为 QPixmap 对象
        # pixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
        # # 将图片显示在 QLabel 上
        # self.label.setPixmap(pixmap)
        # # 设置 QLabel 的位置和大小，使其居中显示
        # self.label.setGeometry((self.width() - pixmap.width()) // 2, (self.height() - pixmap.height()) // 2, pixmap.width(), pixmap.height())
        # # 将 QLabel 的背景设置为透明
        # self.label.setStyleSheet("background-color: transparent;")
        # 创建一个带有波纹效果的圆形，用于显示麦克风输入声音的提示
        # self.circle = CircleWidget(self)
        # self.circle.setGeometry(self.label.geometry())
        # 创建一个滚动的 QLabel，用于显示字幕
        self.sub_label = QLabel(self)
        self.sub_label.setStyleSheet("color: white; font-size: 24px;")
        self.sub_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.sub_label.setFixedHeight(75)
        self.sub_label.setFixedWidth(self.width())
        self.sub_label.setFont(QFont("Source Code Pro",9))
        self.sub_label.move(0, self.height() - self.sub_label.height())
        self.sub_label.setText("Hello, sir. It's Jarvis here. How can I assist you?")
        # 启动一个定时器，用于更新字幕和波纹的状态
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_subtitle_and_circle)
        # self.timer.start(1000)
        # 手动唤醒开关
        self.awake_button = CircleButton(self, 99)
        self.awake_button.move(self.width() / 2 - 52, 559)
        self.awake_button.setCursor(Qt.PointingHandCursor)
        # 显示窗口
        self.show()
    def set_sub_label(self, text):
        self.sub_label.setText(text)

    def switch_power_status(self):
        self.awake_button.switch_power_status()

    def update_subtitle_and_circle(self):
        # 模拟语音识别和贾维斯返回的信息
        subtitle = "Hello, sir. It's Jarvis here. How can I assist you?"
        # 获取当前字幕的位置
        x = self.sub_label.pos().x()
        # 计算下一帧的位置
        x -= 5
        # 如果字幕已经移动到屏幕左侧，就将位置重置到屏幕右侧
        if x < -self.sub_label.width():
            x = self.width()
        # 设置字幕的位置
        self.sub_label.move(x, self.sub_label.pos().y())
        # 设置字幕的文本
        self.sub_label.setText(subtitle)
        # 模拟麦克风输入声音
        is_speaking = time.time() % 2 < 1
        # 更新波纹的状态
        self.circle.set_is_speaking(is_speaking)
def make_circle(image):
    # 创建一个新的白色图像，大小与原图像相同
    mask = Image.new("RGBA", image.size, (255, 255, 255, 0))
    # 创建一个 ImageDraw 对象，用于绘制圆形
    draw = ImageDraw.Draw(mask)
    # 计算圆形的半径和中心点坐标
    cx, cy = image.size[0] // 2, image.size[1] // 2
    r = min(cx, cy)
    # 绘制圆形
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
    # 将图像与掩码合并
    return Image.composite(image, mask, mask)
class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化变量
        self.radius = 0
        self.color = QColor(255, 255, 255, 0)
        self.is_speaking = False
        # 启动一个定时器，用于更新波纹的状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_circle)
        self.timer.start(30)
    def set_is_speaking(self, is_speaking):
        self.is_speaking = is_speaking
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.color, 2))
        painter.setBrush(QBrush(self.color))
        cx, cy = self.width() // 2, self.height() // 2
        painter.drawEllipse(cx - self.radius, cy - self.radius, 2 * self.radius, 2 * self.radius)
    def update_circle(self):
        if self.is_speaking:
            # 如果正在输入声音，就让波纹扩散
            self.radius += 5
            if self.radius > min(self.width(), self.height()):
                self.radius = 0
        else:
            # 如果没有输入声音，就让波纹逐渐消失
            alpha = self.color.alpha() - 10
            if alpha <= 0:
                alpha = 0
            self.color.setAlpha(0)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    tips = welcome()
    tts.speak(tips)
    window.set_sub_label(tips)
    print('Jarvis: ' + tips)
    # while True:
    #     wake_word_index = picowakeword.detect_wake_word()
    #     if wake_word_index >= 0:
    #         window.switch_power_status()
    #         playsound('.\\resources\\ding.wav')
    #         tts.speak(welcome())
    #         input = baiduasr.recoginze(keep_audio_file=True, timeout=60)
    #         if input == None or input == '':
    #             output = '没听清，请再说一遍'
    #             window.set_sub_label(output)
    #             tts.speak('没听清，请再说一遍')
    #         else:
    #             print('I: ' + input)
    #             data = bot.ask(input)
    #             choices = data.get("choices")
    #             if not choices:
    #                 print("No reply from gpt3")
    #             else:
    #                 message = choices[0]["message"]["content"]
    #                 print('Jarvis: ' + message)
    #                 tts.speak(message)
    sys.exit(app.exec_())