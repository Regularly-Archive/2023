import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication

class SystemMonitorWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)
        self.last_net_io_counters = psutil.net_io_counters()

    def initUI(self):
        hbox = QHBoxLayout()

        # 网速监控
        self.speed_icon_label = QLabel()
        self.speed_icon_label.setFixedSize(32, 32)
        self.speed_icon_label.setPixmap(QPixmap("./resources/Network-Speed.png"))
        self.speed_metrics_label = QLabel()
        self.speed_metrics_label.setStyleSheet("color: white; font-size: 16px")
        hbox.addWidget(self.speed_icon_label)
        hbox.addWidget(self.speed_metrics_label)

        # CPU 监控
        self.CPU_icon_label = QLabel()
        self.CPU_icon_label.setFixedSize(32, 32)
        self.CPU_icon_label.setPixmap(QPixmap("./resources/CPU.png"))
        self.CPU_metrics_label = QLabel()
        self.CPU_metrics_label.setStyleSheet("color: white; font-size: 16px")
        hbox.addWidget(self.CPU_icon_label)
        hbox.addWidget(self.CPU_metrics_label)
        
        # 内存监控
        self.Mem_icon_label = QLabel()
        self.Mem_icon_label.setFixedSize(32, 32)
        self.Mem_icon_label.setPixmap(QPixmap("./resources/Mem.png"))
        self.Mem_metrics_label = QLabel()
        self.Mem_metrics_label.setStyleSheet("color: white; font-size: 16px")
        hbox.addWidget(self.Mem_icon_label)
        hbox.addWidget(self.Mem_metrics_label)

        self.memory_label = QLabel()
        self.memory_label.setPixmap(QPixmap("./resources/Mem.png"))
        self.memory_label.setStyleSheet("color: white; font-size: 16px")
        self.cpu_label = QLabel()
        self.cpu_label.setPixmap(QPixmap("./resources/CPU.png"))
        self.cpu_label.setStyleSheet("color: white; font-size: 16px")
        
        self.setLayout(hbox)
        self.setAutoFillBackground(False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def update_metrics(self):
        net_io_counters = psutil.net_io_counters()
        # net_speed = (net_io_counters.bytes_sent + net_io_counters.bytes_recv - self.last_net_io_counters.bytes_sent - self.last_net_io_counters.bytes_recv) / 1024 / 1024
        net_speed = (net_io_counters.bytes_sent - self.last_net_io_counters.bytes_sent) / 1024 / 1024
        self.last_net_io_counters = net_io_counters
        mem_info = psutil.virtual_memory()
        mem_percent = mem_info.percent
        cpu_percent = psutil.cpu_percent(interval=1)
        self.speed_metrics_label.setText("{:.2f} MB/s".format(net_speed))
        self.Mem_metrics_label.setText("{}%".format(mem_percent))
        self.CPU_metrics_label.setText("{}%".format(cpu_percent))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    monitor = SystemMonitorWidget()
    monitor.show()
    sys.exit(app.exec_())