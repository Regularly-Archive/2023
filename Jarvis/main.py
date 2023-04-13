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


# 主程序
async def main():
    tips = welcome()
    # tts.speak(tips)
    print('Jarvis: ' + tips)
    while True:
        wake_word_index = picowakeword.detect_wake_word()
        if wake_word_index >= 0:
            playsound('.\\resources\\ding.wav')
            # tts.speak(welcome())
            input = baiduasr.recoginze(keep_audio_file=True, timeout=60)
            if input == None or input == '':
                tts.speak('没听清，请再说一遍')
            else:
                print('I: ' + input)
                data = bot.ask(input)
                choices = data.get("choices")
                if not choices:
                    print("No reply from gpt3")
                else:
                    message = choices[0]["message"]["content"]
                    print('Jarvis: ' + message)
                    tts.speak(message)
                    

if __name__ == '__main__':
    asyncio.run(main())
            
    