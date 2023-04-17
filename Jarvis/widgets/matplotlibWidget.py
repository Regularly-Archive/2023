import sys
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np  
import pyaudio
import threading
import queue
import matplotlib.lines as line
import matplotlib.animation as animation
from scipy import signal

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        
        # 此处初始化子图一定要在初始化函数之前
        self.fig = plt.figure()
        self.rt_ax = plt.subplot(111, xlim=(0,CHUNK*2), ylim=(-100,100))
        self.rt_ax.patch.set_alpha(0.5)
        plt.axis('off')
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.setStyleSheet(f"background-color: transparent; ")
        

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()
        self.initariateV()
        self.setStyleSheet(f"background-color: transparent; ")
        
    # 初始化成员变量
    def initariateV(self):
        self.p = None
        self.q = queue.Queue()
        self.t = None
        self.ad_rdy_ev = None
        self.stream = None
        self.window = None
        self.ani = None
        self.rt_line = line.Line2D([],[])  # 直线对象
        self.rt_x_data=np.arange(0,CHUNK*2,1) 
        self.rt_data=np.full((CHUNK*2, ), 0) 
        self.rt_line.set_xdata(self.rt_x_data)# 初始化横坐标
        self.rt_line.set_ydata(self.rt_data) # 初始化纵坐标
    
    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=15, height=15, dpi=100)
        self.layout.addWidget(self.mpl)
    
    # 开始录制触发函数
    def startAudio(self, *args, **kwargs):
        # self.mpl.fig.suptitle('波形曲线')
        self.ani = animation.FuncAnimation(self.mpl.fig, self.plot_update,
                              init_func=self.plot_init, 
                              frames=1,
                              interval=30,
                              blit=True)
        # 其实animation方法的实质是开启了一个线程更新图像
        
        #麦克风开始获取音频
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK,
                stream_callback=self.callback)
        self.stream.start_stream()
        
        # 正态分布数组，与音频数据做相关运算可保证波形图两端固定
        self.window = signal.hamming(CHUNK*2)
        
        # 初始化线程
        self.ad_rdy_ev=threading.Event()  # 线程事件变量
        self.t = threading.Thread(target=self.read_audio_thead,  
                  args=(self.q, self.stream, self.ad_rdy_ev))  # 在线程t中添加函数read_audio_thead
        self.t.start() # 线程开始运行
        self.mpl.draw()
    
	# animation的更新函数
    def plot_update(self, i):
        self.rt_line.set_xdata(self.rt_x_data)
        self.rt_line.set_ydata(self.rt_data)
        return self.rt_line,
    
    # animation的初始化函数
    def plot_init(self):
        self.mpl.rt_ax.add_line(self.rt_line)
        return self.rt_line,
    
    #pyaudio的回调函数
    def callback(self, in_data, frame_count, time_info, status):
        global ad_rdy_ev
        self.q.put(in_data)
        return (None, pyaudio.paContinue)
    
    
    def read_audio_thead(self, q, stream, ad_rdy_ev):
    # 获取队列中的数据
        while stream.is_active():
            self.ad_rdy_ev.wait(timeout=0.1) # 线程事件，等待0.1s
            if not q.empty():
                data=q.get()
                while not q.empty(): # 将多余的数据扔掉，不然队列会越来越长
                    q.get()
                self.rt_data = np.frombuffer(data,np.dtype('<i2'))
                self.rt_data = self.rt_data * self.window   # 这样做的目的是将曲线的两端固定，以免出现曲线整体发生波动
            self.ad_rdy_ev.clear()
    
    def endAudio(self):
        # 停止获取音频信息
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # 清空队列
        while not self.q.empty(): 
            self.q.get()
        # 重新初始化变量
        self.initariateV()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.setFixedSize(150, 75)
    ui.startAudio()
    ui.show()
    sys.exit(app.exec_())
