import sys
sys.path.append("..")
from talk.actionTrigger import trigger

@trigger.route(keywords=['查询天气','询问天气'])
def report_weather(action):
    return f'抱歉，我还不会查询天气呢'