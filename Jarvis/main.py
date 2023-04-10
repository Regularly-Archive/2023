import pyttsx3
from speech.speech2text import BaiduASR
from speech.wakeword import PicoWakeWord
from speech.text2speech import Pyttsx3TTS
from dotenv import load_dotenv, find_dotenv
from os import environ as env

# 初始化环境变量
load_dotenv(find_dotenv())
BAIDU_ASR_APP_ID = env.get("BAIDU_ASR_APP_ID")
BAIDU_ASR_API_KEY = env.get("BAIDU_ASR_API_KEY")
BAIDU_ASR_SECRET_KEY = env.get("BAIDU_ASR_SECRET_KEY")
PICOVOICE_API_KEY = env.get("PICOVOICE_API_KEY")

# 初始化语音合成引擎
tts = Pyttsx3TTS()
picowakeword = PicoWakeWord(PICOVOICE_API_KEY, 'Jarvis_en_windows_v2_1_0.ppn')
baiduasr = BaiduASR(BAIDU_ASR_APP_ID, BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY)

# 主程序
print('你好，请问有什么可以帮助您的？')
while True:
    wake_word_index = picowakeword.detect_wake_word()
    if wake_word_index >= 0:
        tts.speak('我在')
        result = baiduasr.recoginze(False)
        if result == None:
            tts.speak('没听清，请再说一遍')
        else:
            tts.speak(result)
            
    