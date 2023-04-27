from playsound import playsound
import threading

def playsound_async(filePath):
    t = threading.Thread(target=playsound, args=(filePath,))
    t.start()
