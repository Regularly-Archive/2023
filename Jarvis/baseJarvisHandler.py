from speech.speech2text import ASREngineFactory
from speech.wakeword import PicoWakeWord
from speech.pyaduio_player import PyAudioPlayer
from speech.text2speech import TTSEngineFactory
from talk.openai import ChatGPTBot
from talk.contentCorrector import ChatGPTCorrector
from talk.intentExtractor import ChatGPTExtractor
from os import environ as env
from conf.appConstants import welcome, TTSEngineProvider, ASREngineProvider
from conf.appConfig import load_config_from_env
import requests
import logging, time
from rich.logging import RichHandler
from talk.actionTrigger import trigger
import os, sys, importlib, asyncio, click
from logging import handlers

class BaseJarvisHandler:

    def __init__(self, env_file=''):
        self.manual_awake = False
        self.is_system_ready = False
        self.init_logging()
        self.config = load_config_from_env(env_file)
        self.tts_engine = TTSEngineFactory.create(self.config, TTSEngineProvider.Edge)
        self.awake_engine = PicoWakeWord(self.config['PICOVOICE_API_KEY'], 'Jarvis_en_windows_v2_1_0.ppn')
        self.asr_engine = ASREngineFactory.create(self.config, ASREngineProvider.Sherpa)
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
        self.logger.info(f"Jarvis greet you with: {text}.")

    def onInputFailed(self):
        self.logger.info(f"Jarvis can't recognize what you said.")
        self.manual_awake = False

    def onInputed(self, text):
        self.logger.info(f"Jarvis had recognized follwing information: {text}.")
        self.manual_awake = False

    def onOutputFailed(self):
        self.logger.info(f"Jarvis can't response due to unknow reason.")

    def onOutputed(self, text):
        self.logger.info(f"Jarvis had responsed follwing information: {text}.")
    
    def onAwake(self):
        self.logger.info(f"Jarvis had beed awaked with awake word.")

    def onIdle(self):
        self.logger.info(f"Jarvis is idle now.")
        if self.manual_awake:
            self.manual_awake = False
    
    def awake_by_manual(self):
        self.manual_awake = True
    
    def load_plugins(self, plugin_folder='plugins'):
        sys.path.append(f'./{plugin_folder}')
        for file in os.listdir(f'./{plugin_folder}'):  
            fileName = os.path.splitext(file)[0] 
            fileExt = os.path.splitext(file)[1]
            if fileExt == '.py':
                importlib.import_module(fileName)

    def play_sound_async(self, file_name):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.audio_player.play(file_name=file_name))

    def init_logging(self):
        format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        # 日志输出到文件
        formatter = logging.Formatter(format)
        file_handler = handlers.TimedRotatingFileHandler(filename='./logs/Jarvis.log', when='D')
        file_handler.setFormatter(formatter)
        # 日志输出到终端
        rich_handler = RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])
        logging.basicConfig(level=logging.INFO, format=format, datefmt="[%X]", handlers=[file_handler, rich_handler])
        self.logger = logging.getLogger('BaseJarvisHandler')
        self.logger.setLevel(logging.INFO)

    def run(self):
        if self.config['PLAY_WELCOME_VOICE']:
            tips = welcome()
            self.onGreet(tips)
        while self.is_system_ready:
            wake_word_index = self.awake_engine.detect_wake_word()
            if wake_word_index >= 0 or self.manual_awake:
                self.onAwake()
                input = self.asr_engine.recoginze(keep_audio_file=True, timeout=120)
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
                
        
            
    