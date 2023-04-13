import sys
import speech_recognition as sr
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QProgressBar, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("Jarvis")
        self.setGeometry(100, 100, 400, 400)
        self.setFixedSize(1366, 768)
        self.setStylesSheet("""
            QWidget {
                background: black;
            }
        """)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.label = QLabel(self.central_widget)
        self.label.setGeometry(100, 100, 200, 200)
        self.label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar(self.central_widget)
        self.progress_bar.setGeometry(50, 50, 300, 300)
        self.progress_bar.setFormat("")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 0px solid grey;
                border-radius: 150px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                border-radius: 150px;
                background-color: #00BFFF;
            }
        """)
        self.timer = QTimer(self)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_progress_bar)
        self.show()
    def update_progress_bar(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        if self.progress_bar.value() > 100:
            self.timer.stop()
            self.progress_bar.setValue(0)
    def paintEvent(self, event):
        pass
        # painter = QPainter(self.label.pixmap())
        # painter.setPen(QPen(QColor(255, 0, 0), 5))
        # painter.drawPixmap(self.label.rect(), self.label.pixmap())
        # painter.drawEllipse(self.label.rect())
    def wake_up(self):
        self.timer.start()
        self.label.setText("正在监听")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        self.label.setText("检测到语音")
        try:
            text = r.recognize_google(audio, language='zh-CN')
            print(f"你说了：{text}")
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError as e:
            print(f"请求出错：{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.label.setPixmap(QPixmap("ironman.png").scaled(474, 568, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    window.label.setScaledContents(True)
    window.progress_bar.setValue(0)
    window.progress_bar.hide()
    window.label.mousePressEvent = window.wake_up
    sys.exit(app.exec_())