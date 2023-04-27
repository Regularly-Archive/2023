import asyncio
import wave
import pyaudio
import time
import numpy as np
import os
import subprocess
from pydub import AudioSegment

# 一种利用黑科技实现的单例模式
# 其实还可以使用导出一个实例的经典做法:)
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class PyAudioPlayer:

    def __init__(self):
        self.audio = None
        self.stream = None
        self.is_paused = False
        self.is_stoped = False
        self.rate = None
        self.channels = None
        self.file_name = None
    
    # 播放音乐
    async def play(self, file_name):
        self.file_name = file_name
        
        if not os.path.exists(self.file_name):
            raise FileNotFoundError(f'文件 {self.file_name} 不存在')

        file_suffix = self.file_name.split('.')[-1]
        if file_suffix not in ['mp3', 'wav']:
            raise Exception(f'不支持的音频格式：{file_suffix}')

        self.audio = pyaudio.PyAudio()

        if file_suffix == 'wav':
            wf = wave.open(self.file_name, 'rb')
            self.rate = wf.getframerate()
            self.channels = wf.getnchannels()
            data = wf.readframes(1024)
        else:
            song = AudioSegment.from_mp3(self.file_name)
            raw_data = song._data
            self.rate = song.frame_rate
            self.channels = song.channels
            data = np.frombuffer(raw_data, dtype=np.int16)

        # 打开音频输出流
        self.stream = self.audio.open(
            format=self.audio.get_format_from_width(2),
            channels=self.channels,
            rate=self.rate,
            output=True
        )
        
        # 正式播放音频
        while not self.is_stoped:
            # 如果已暂停，则不播放
            if self.is_paused:
                time.sleep(0.1)
                continue

            # 写入音频数据
            self.stream.write(data)

            # 读取下一块音频数据
            if file_suffix == 'wav':
                data = wf.readframes(1024)
            else:
                raw_data = song._data
                data = np.frombuffer(raw_data, dtype=np.int16)

            # 检测是否到达音频文件结尾
            if len(data) == 0:
                break

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    # 暂停播放
    def pause(self):
        self.is_paused = True

    # 恢复播放
    def resume(self):
        self.is_paused = False

    # 停止播放
    def stop(self):
        self.is_stoped = True



if __name__ == '__main__':
    async def play_sound(filePath):
        player = PyAudioPlayer()
        await player.play(file_name=filePath)
        player.stop() 

    loop = asyncio.get_event_loop()
    loop.run_until_complete(play_sound('./resources/ding.wav'))
