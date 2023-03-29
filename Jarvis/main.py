import speech_recognition as sr
import pyttsx3
import cv2

# 初始化语音识别和语音合成客户端
r = sr.Recognizer()
engine = pyttsx3.init()

# 语音识别函数
def recognize_speech():
    with sr.Microphone() as source:
        print('Please speak:')
        audio = r.listen(source)
    try:
        text = r.recognize_sphinx(audio, language='en-US')
        print('You said:', text)
        return text
    except Exception as e:
        print('Error:', e)
        return ''

# 语音合成函数
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 图像识别函数
def recognize_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# 主程序
print('你好，请问有什么可以帮助您的？')
# speak('你好，请问有什么可以帮助您的？')
while True:
    text = recognize_speech()
    if text == '退出':
        break
    elif text == '打开相机':
        # speak('好的，请看摄像头')
        print('好的，请看摄像头')
        recognize_image()
    elif text == '你叫什么名字':
        print('我是小助手')
        # speak('我是小助手')
    else:
        print('对不起，我不明白您的意思，请您再说一遍。')
        # speak('对不起，我不明白您的意思，请您再说一遍。')