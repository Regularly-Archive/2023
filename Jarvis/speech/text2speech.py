import pyttsx3

class Pyttsx3TTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def text_to_speech_pyttsx3(self, text):
        self.engine.say(text)
        self.engine.runAndWait()