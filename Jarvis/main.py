import pyttsx3
from speech.speech2text import BaiduASR
from speech.wakeword import PicoWakeWord
from speech.text2speech import Pyttsx3TTS, BaiduTTS
# from talk.openai import GBT3Bot
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from aiohttp import ClientSession
import asyncio
from playsound import playsound
from conf.constants import welcome

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
tts = BaiduTTS(BAIDU_ASR_APP_ID, BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY)
picowakeword = PicoWakeWord(PICOVOICE_API_KEY, 'Jarvis_en_windows_v2_1_0.ppn')
baiduasr = BaiduASR(BAIDU_ASR_APP_ID, BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY)
# bot = GBT3Bot(ClientSession(), OPENAI_API_KEY, OPENAI_API_ENDPOINT)

# 主程序
async def main():
    print('你好，请问有什么可以帮助您的？')
    tts.speak(welcome())
    while True:
        wake_word_index = picowakeword.detect_wake_word()
        if wake_word_index >= 0:
            playsound('.\\resources\\ding.wav')
            tts.speak(welcome())
            input = baiduasr.recoginze(False)
            if input == None:
                tts.speak('没听清，请再说一遍')
            else:
                tts.speak(input)
                # data = await bot.ask(input)
                # if data != None:
                #     choices = data.get("choices")
                #     content = choices[0]["message"]["content"]
                #     tts.speak(content)

if __name__ == '__main__':
    asyncio.run(main())
            
    