<<<<<<< HEAD
from speech.async_playsound import playsound_async
=======
from playsound import playsound
>>>>>>> c7fea3a575162a6d7d6fbea88863de6ca38ba703
from baseJarvisHandler import BaseJarvisHandler

class CliJarvisHandler(BaseJarvisHandler):
    def __init__(self):
        super().__init__(None)

    def onInputFailed(self):
        self.tts_engine.speak('抱歉，我没有听清，请您再说一遍')

    def onInputed(self, text):
        super().onInputed(text)
        print(f'I: {text}')

    def onOutputFailed(self):
        super().onInputFailed()
        print("Jarvis: No reply from ChatGPT")

    def onOutputed(self, text):
        print(f'Jarvis: {text}')
        self.tts_engine.speak(text)
    
    def onAwake(self):
        super().onAwake()
        playsound_async('.\\resources\\ding.wav')

if __name__ == '__main__':
    jarvis = CliJarvisHandler()
    jarvis.run()


