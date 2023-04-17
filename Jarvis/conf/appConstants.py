from inspect import classify_class_attrs
import random
from enum import Enum

welcome_tips = [
    'Welcome home sir',
    'For you sir, always',
    'Always at your service sir',
]

def welcome():
    return random.choice(welcome_tips)

class JarvisEventType(Enum):
    Awake = 0
    Greet = 1
    Inputed = 2
    InputFailed = 3
    Outputed = 4
    OutputFailed = 5
    Idle = 6

