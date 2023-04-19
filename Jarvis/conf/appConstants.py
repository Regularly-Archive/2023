import random
from enum import IntEnum

welcome_tips = [
    'Welcome home, sir. This is Jarvis, who is your artificial intelligence assistant to help you work and live better.',
    "It's my proud to say that I serve for you, sir, always",
    'Always at your service sir',
]

def welcome():
    return random.choice(welcome_tips)

class JarvisEventType(IntEnum):
    Greet = 0
    Awake = 1
    InputFailed = 2
    Inputed = 3
    OutputFailed = 4
    Outputed = 5
    Idle = 6