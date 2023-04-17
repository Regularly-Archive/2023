from speech.speech2text import PaddleSpeechASR
from speech.wakeword import PicoWakeWord
from speech.text2speech import PaddleSpeechTTS
from talk.openai import ChatGPTBot
from os import environ as env
from conf.appConstants import welcome
from conf.appConfig import load_config_from_env
import requests
import logging

class BaseJarvisHandler:

    def __init__(self, env_file=''):
        self.logger = logging.getLogger('BaseJarvisHandler')
        self.logger.setLevel(logging.DEBUG)
        self.config = load_config_from_env(env_file)
        self.tts_engine = PaddleSpeechTTS()
        self.awake_engine = PicoWakeWord(self.config['PICOVOICE_API_KEY'], 'Jarvis_en_windows_v2_1_0.ppn')
        self.asr_engine = PaddleSpeechASR()
        self.session = requests.session()
        self.chat_bot = ChatGPTBot(self.session, self.config['OPENAI_API_KEY'], self.config['OPENAI_API_ENDPOINT'] + '/v1/chat/completions')
    
    def onGreet(self, text):
        self.logger.info(f"Jarvis greet you with '{text}'")

    def onInputFailed(self):
        self.logger.info(f"Jarvis can't recognize what you said")

    def onInputed(self, text):
        self.logger.info(f"Jarvis had recognized follwing information '{text}'")

    def onOutputFailed(self):
        self.logger.info(f"Jarvis can't response due to unknow reason")

    def onOutputed(self, text):
        self.logger.info(f"Jarvis had responsed follwing information '{text}'")
    
    def onAwake(self):
        self.logger.info(f"Jarvis had beed awaked with awake word")

    def run(self):
        if self.config['PLAY_WELCOME_VOICE']:
            tips = welcome()
            self.tts_engine.speak(tips)
            self.onGreet(tips)
        while True:
            wake_word_index = self.awake_engine.detect_wake_word()
            if wake_word_index >= 0:
                self.onAwake()
                input = self.asr_engine.recoginze(keep_audio_file=True, timeout=60)
                if input == None or input == '':
                    self.onInputFailed()
                else:
                    output = self.chat_bot.ask(input)
                    if output== None or output == '':
                        self.onOutputFailed()
                    else:
                        self.onOutputed(output)
        
            
    