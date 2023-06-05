import speech_recognition as sr
from pathlib import Path
import os, sys, json, time, wave
import numpy as np
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

class SherpaASR:
      
      def __init__(self, model_path='./resources/models/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23/'):
        self.recoginzer = sr.Recognizer()
        self.model_path = model_path

      def create_recognizer(self, model_path):
          sherpa_ncnn = None
          try:
            sherpa_ncnn = importlib.import_module('sherpa_ncnn')
            recognizer = sherpa_ncnn.Recognizer(
                tokens=f"{model_path}/tokens.txt",
                encoder_param=f"{model_path}/encoder_jit_trace-pnnx.ncnn.param",
                encoder_bin=f"{model_path}/encoder_jit_trace-pnnx.ncnn.bin",
                decoder_param=f"{model_path}/decoder_jit_trace-pnnx.ncnn.param",
                decoder_bin=f"{model_path}/decoder_jit_trace-pnnx.ncnn.bin",
                joiner_param=f"{model_path}/joiner_jit_trace-pnnx.ncnn.param",
                joiner_bin=f"{model_path}/joiner_jit_trace-pnnx.ncnn.bin",
                num_threads=4,
            )
            return recognizer
          except ImportError as e:
            print("sherpa-ncnn is required, run 'pip install sherpa-ncnn' first")

      def recoginze_file(self, filePath: str):
          sherpa_recognizer = self.create_recognizer(self.model_path)
          with wave.open(filePath) as f:
            num_samples = f.getnframes()
            samples = f.readframes(num_samples)
            samples_int16 = np.frombuffer(samples, dtype=np.int16)
            samples_float32 = samples_int16.astype(np.float32)
            samples_float32 = samples_float32 / 32768

            sherpa_recognizer.accept_waveform(sherpa_recognizer.sample_rate, samples_float32)

            tail_paddings = np.zeros(int(sherpa_recognizer.sample_rate * 0.5), dtype=np.float32)
            sherpa_recognizer.accept_waveform(sherpa_recognizer.sample_rate, tail_paddings)

            sherpa_recognizer.input_finished()

            return sherpa_recognizer.text

      def recoginze(self, keep_audio_file: bool = True, timeout=60, phrase_time_limit=None):
          with sr.Microphone(sample_rate=16000) as source:
            self.recoginzer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recoginzer.listen(source, timeout=120, phrase_time_limit=None)

            timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
            file_name = f"{timestamp}.wav"
            file_name = os.path.join(Path.home(), file_name)

            if keep_audio_file and audio != None:
                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

            if audio != None:
                return self.recoginze_file(file_name)
        
    



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
        elif type == ASREngineProvider.Sherpa:
            return SherpaASR(config['SHERPA_MODEL_PATH'])
    