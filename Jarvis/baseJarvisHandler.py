from speech.speech2text import PaddleSpeechASR
from speech.wakeword import PicoWakeWord
from speech.pyaduio_player import PyAudioPlayer
from speech.text2speech import PaddleSpeechTTS
from talk.openai import ChatGPTBot
from talk.contentCorrector import ChatGPTCorrector
from talk.intentExtractor import ChatGPTExtractor
from os import environ as env
from conf.appConstants import welcome
from conf.appConfig import load_config_from_env
import requests
import logging, time
from talk.actionTrigger import trigger
import os, sys, importlib

class BaseJarvisHandler:

    def __init__(self, env_file=''):
        self.manual_awake = False
        self.logger = logging.getLogger('BaseJarvisHandler')
        self.logger.setLevel(logging.INFO)
        self.config = load_config_from_env(env_file)
        self.tts_engine = PaddleSpeechTTS()
        self.awake_engine = PicoWakeWord(self.config['PICOVOICE_API_KEY'], 'Jarvis_en_windows_v2_1_0.ppn')
        self.asr_engine = PaddleSpeechASR()
        self.session = requests.session()
        self.audio_player = PyAudioPlayer()
        self.chat_bot = ChatGPTBot(
            self.session, 
            self.config['OPENAI_API_KEY'], 
            self.config['OPENAI_API_ENDPOINT'] + '/v1/chat/completions',
            self.config['OPENAI_API_PROMPT'])
        self.chineses_corrector = ChatGPTCorrector(
            self.config['OPENAI_API_KEY'], 
            self.config['OPENAI_API_ENDPOINT'] + '/v1/chat/completions',
        )
        self.semantic_extractor = ChatGPTExtractor(
            self.config['OPENAI_API_KEY'], 
            self.config['OPENAI_API_ENDPOINT'] + '/v1/chat/completions',
        )
        self.trigger = trigger
        self.load_plugins()
    
    def onGreet(self, text):
        self.logger.info(f"Jarvis greet you with '{text}'")

    def onInputFailed(self):
        self.logger.info(f"Jarvis can't recognize what you said")
        self.manual_awake = False

    def onInputed(self, text):
        self.logger.info(f"Jarvis had recognized follwing information '{text}'")
        self.manual_awake = False

    def onOutputFailed(self):
        self.logger.info(f"Jarvis can't response due to unknow reason")

    def onOutputed(self, text):
        self.logger.info(f"Jarvis had responsed follwing information '{text}'")
    
    def onAwake(self):
        self.logger.info(f"Jarvis had beed awaked with awake word")

    def onIdle(self):
        self.logger.info(f"Jarvis is idle now")
        if self.manual_awake:
            self.manual_awake = False
    
    def awake_by_manual(self):
        self.manual_awake = True
    
    def load_plugins(self, plugin_folder='plugins'):
        sys.path.append(f'./{plugin_folder}')
        for file in os.listdir(f'./{plugin_folder}'):  
            fileName = os.path.splitext(file)[0] 
            importlib.import_module(fileName)

        
    def run(self):
        if self.config['PLAY_WELCOME_VOICE']:
            tips = welcome()
            self.onGreet(tips)
        while True:
            wake_word_index = self.awake_engine.detect_wake_word()
            if wake_word_index >= 0 or self.manual_awake:
                self.onAwake()
                input = self.asr_engine.recoginze(keep_audio_file=True, timeout=60)
                if input == None or input == '':
                    self.onInputFailed()
                    continue
                else:
                    # 当开启中文纠错特性时，对输入内容进行纠正
                    if self.config['ENABLE_CHINESE_CORRECT']:
                        input = self.chineses_corrector.correct(input)
                    self.onInputed(input)
                    # 当开启语义理解特性时，对输入意图进行分析
                    output = None
                    if self.config['ENABLE_SEMANTIC_ANALYSIS']:
                        action = self.semantic_extractor.extract(input)
                        output = self.trigger.execute(action=action)
                        if output == None:
                            output = self.chat_bot.ask(input)
                    else:
                        output = self.chat_bot.ask(input)
                    if output== None or output == '':
                        self.onOutputFailed()
                        continue
                    else:
                        self.onOutputed(output)
                
        
            
    