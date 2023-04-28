from aip import AipSpeech
import pyttsx3
import os
from pathlib import Path
from paddlespeech.cli.tts.infer import TTSExecutor
import threading
from .async_playsound import playsound_async
from .pyaduio_player import PyAudioPlayer
import asyncio


class BaiduTTS:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.audio_player = PyAudioPlayer()

    def speak(self, text="", speed=5, volume=5, person=3):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': speed,
            'vol': volume,
            'per': person
        })
        
        filePath = os.path.join(Path.home(), "audio.mp3")
        if not isinstance(result, dict):
            with open(filePath, "wb") as f:
                f.write(result)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.audio_player.play(filePath))
        else:
            print("语音合成失败", result)
        
class Pyttsx3TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text="", speed=100, volume=0.6, person=0):
        self.engine.setProperty('rate', speed)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices') 
        if person > len(voices) - 1:
            person = 0
        self.engine.setProperty('voice',voices[person].id)
        self.engine.say(text)
        self.engine.runAndWait()

class PaddleSpeechTTS:

    def __init__(self):
        self.executor = TTSExecutor()
        self.audio_player = PyAudioPlayer()

    def speak(self, text="", lang='mix', model='fastspeech2_male'):
        filePath = os.path.join(Path.home(), "output.mp3")
        self.executor(text=text, output=filePath, am=model, lang=lang)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.audio_player.play(filePath))

if __name__ == "__main__":
    APP_ID = '32200779'
    API_KEY = 'WTsdQmg4RIptppSAXA2og5cj'
    SECRET_KEY = 'qTN2xoKMjl8pvdlPDHYm7GnsN02C1W2r'
    tts = BaiduTTS(APP_ID, API_KEY, SECRET_KEY)
    tts.speak('欢迎使用延长自助终端管理系统')
    tts = PaddleSpeechTTS()
    tts.speak('欢迎使用延长自助终端管理系统')