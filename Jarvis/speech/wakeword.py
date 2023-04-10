import pvporcupine
import pyaudio
import struct


class PicoWakeWord:
    def __init__(self, PICOVOICE_API_KEY, keyword_path):
        self.PICOVOICE_API_KEY = PICOVOICE_API_KEY
        self.keyword_path = keyword_path
        self.porcupine = pvporcupine.create(
            access_key=self.PICOVOICE_API_KEY,
            keyword_paths=[self.keyword_path]
        )
        self.myaudio = pyaudio.PyAudio()
        self.stream = self.myaudio.open(
            input_device_index=0,
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect_wake_word(self):
        audio_obj = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, audio_obj)
        keyword_idx = self.porcupine.process(audio_obj_unpacked)
        return keyword_idx


if __name__ == '__main__':
    PICOVOICE_API_KEY = ''
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, '*.ppn')
    while True:
        keyword_idx = picowakeword.detect_wake_word()
        if keyword_idx >=0:
            print("我听到了！")