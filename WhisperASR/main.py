import speech_recognition as sr
from pathlib import Path
import os, json, time
import whisper


class WhisperASR:
    def __init__(self, model_name="base"):
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


asr = WhisperASR()
print('--------开始识别--------')
text = asr.recoginze()
print('--------识别结束--------')
print(text)