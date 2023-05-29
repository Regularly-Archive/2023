import speech_recognition as sr
from pathlib import Path
import os, json, time
import sys
from conf.appConstants import ASREngineProvider
import importlib


class BaiduASR:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        aip = None
        try:
            aip = importlib.import_module('aip')
        except ImportError as e:
            print("baidu-aip is required, run 'pip install baidu-aip' first")
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = aip.AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.recoginzer = sr.Recognizer()

    def recognize_file(self, filePath: str, lang: str = 'zh-cn'):
        with open(filePath, 'rb') as f:
            audio_data = f.read()
            result = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
            if result['err_msg'] == 'success.':
                return result['result'][0]
            else:
                return ''

    def recoginze(self, keep_audio_file: bool = False, timeout=120):
        with sr.Microphone(sample_rate=16000) as source:
            self.recoginzer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recoginzer.listen(source, timeout=timeout, phrase_time_limit=None)

            timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
            file_name = f"{timestamp}.wav"
            file_name = os.path.join(Path.home(), file_name)

            if keep_audio_file and audio != None:
                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

            if audio != None:
                audio_data = audio.get_wav_data()
                result = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
                if result['err_msg'] == 'success.':
                    return result['result'][0]
                else:
                    return ''

class PaddleSpeechASR:

    def __init__(self):
        paddlespeech = None
        try:
            paddlespeech = importlib.import_module('paddlespeech.cli.asr.infer')
        except ImportError as e:
             print("paddlespeech is required, run 'pip install paddlespeech' first")           
        self.recoginzer = sr.Recognizer()
        self.executor = paddlespeech.ASRExecutor()

    def recognize_file(self, filePath: str, lang: str = 'zh'):
        return self.executor(audio_file=filePath, lang=lang)

    def recoginze(self, keep_audio_file: bool = True, timeout=60, phrase_time_limit=None):
        with sr.Microphone(sample_rate=16000) as source:
            self.recoginzer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recoginzer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
            file_name = f"./{timestamp}.wav"
            file_name = os.path.join(Path.home(), file_name)
            
            if keep_audio_file and audio != None:

                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

            if audio != None:
                return self.executor(audio_file=file_name)

class WhisperASR:
    def __init__(self, model_name="base"):
        whisper = None
        try:
            whisper = importlib.import_module('whisper')
        except ImportError as e:
            print("openai-whisper is required, run 'pip install openai-whisper' first")
        self.model = whisper.load_model(model_name)
        self.recoginzer = sr.Recognizer()

    def recognize_file(self, filePath: str):
        result = self.model.transcribe(filePath, fp16="False")
        return result["text"]

    def recoginze(self, keep_audio_file: bool = True, timeout=120):
        with sr.Microphone(sample_rate=16000) as source:
            self.recoginzer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recoginzer.listen(source, timeout=timeout, phrase_time_limit=None)

            timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
            file_name = f"{timestamp}.wav"
            file_name = os.path.join(Path.home(), file_name)

            if keep_audio_file and audio != None:
                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

            if audio != None:
                return self.recognize_file(file_name)

# 语音识别引擎工厂类
class ASREngineFactory:

    @staticmethod
    def create(config, type):
        if type == ASREngineProvider.Baidu:
            return BaiduASR(config['BAIDU_APP_ID'], config['BAIDU_API_KEY'], config['BAIDU_SECRET_KEY'])
        elif type == ASREngineProvider.PaddleSpeech:
            return PaddleSpeechASR()
        elif type == ASREngineProvider.OpenAIWhisper:
            return WhisperASR()
    