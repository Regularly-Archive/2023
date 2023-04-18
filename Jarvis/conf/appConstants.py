import random
from enum import IntEnum

welcome_tips = [
    'Welcome home sir',
    'For you sir, always',
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