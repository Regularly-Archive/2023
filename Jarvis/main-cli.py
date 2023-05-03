from speech.async_playsound import playsound_async
from baseJarvisHandler import BaseJarvisHandler
from rich.console import Console
import os, sys

class CliJarvisHandler(BaseJarvisHandler):
    def __init__(self):
        super().__init__(None)
        self.console = Console()

    def onInputFailed(self):
        super().onInputFailed()
        text = '抱歉，我没有听清，请您再说一遍'
        self.tts_engine.speak(text, lang='zh-CN')
        self.console.print(f"🤖 [magenta]{text}")

    def onInputed(self, text):
        super().onInputed(text)
        self.console.print(f'🐛 [white]{text}')

    def onOutputFailed(self):
        super().onOutputFailed()
        text = '网络异常，请您稍后重试，贾维斯将永远为您服务。'
        self.tts_engine.speak(text, lang='zh-CN')
        self.console.print(f"🤖 [magenta]{text}")
        

    def onOutputed(self, text):
        super().onOutputed(text)
        self.console.print(f'🤖 [magenta]{text}', style="magenta")
        self.tts_engine.speak(text, lang='zh-CN')
    
    def onAwake(self):
        super().onAwake()
        playsound_async('.\\resources\\ding.wav')

    def onGreet(self, text):
        super().onGreet(text)
        self.console.print(f'🤖 [magenta]{text}')
        self.tts_engine.speak(text, lang='en-US') 
        self.is_system_ready = True

if __name__ == '__main__':
    jarvis = CliJarvisHandler()
    jarvis.run()


