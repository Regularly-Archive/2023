import random
from enum import IntEnum

welcome_tips = [
    # 'Welcome home, sir.',
    # "For you, sir, always",
    # 'Always at your service, sir',
    "Allow me to introduce myself. I'm JARVIS, a virtual artificial intelligence, and I'm here to assist you with a variety of tasks as best as I can. 24 hours a day, seven days a week. Importing all preferences from home interface. Begin systems check."
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