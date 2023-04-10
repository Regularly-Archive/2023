from aip import AipSpeech
import speech_recognition as sr
import time


class BaiduASR:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.recoginzer = sr.Recognizer()

    def recognize_file(self, filePath: str, lang: str = 'zh-cn'):
        with open(filePath, 'rb') as f:
            audio_data = f.read()
            result = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
            if result['err_msg'] == 'success.':
                return result['result'][0]
            else:
                return ''

    def recoginze(self, keep_audio_file: bool = False):
        with sr.Microphone(sample_rate=16000) as source:
            self.recoginzer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recoginzer.listen(source, timeout=15, phrase_time_limit=2)

            if keep_audio_file and audio != None:
                timestamp = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
                file_name = f"./{timestamp}.wav"
                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

            if audio != None:
                audio_data = audio.get_wav_data()
                result = self.client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
                if result['err_msg'] == 'success.':
                    return result['result'][0]
                else:
                    return ''


if __name__ == '__main__':
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    baiduasr = BaiduASR(APP_ID, API_KEY, SECRET_KEY)
    result = baiduasr.recoginze(True)
    print(result)
