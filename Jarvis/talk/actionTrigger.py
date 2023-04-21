import functools
import webbrowser
import datetime
import jieba
from types import FunctionType

def trigger(keywords):
    def outerWrapper(func):
        def wrapper(*args, **kwargs):
            words = jieba.cut(args[0], cut_all=False)
            print(list(words))
            for word in words:
                if word in keywords:
                    return func(*args, **kwargs)      
        return wrapper
    return outerWrapper


 
    # f 指的是一个函数
    def add_url_to_map(self,url,f):
        self.url_map[url] = f

def has_trigger(func):
    decorators = [d.__class__ for d in functools.wraps(func).decorator_list]
    return trigger in decorators

class ActionTrigger:

    triggers_map = {}

    def __init__(self, jarvisHandler):
        self.jarvisHandler = jarvisHandler

    def router(intent):
        def decorator(func: FunctionType):
            ActionTrigger.register_trigger(intent, func)
        return decorator
    
    def register_trigger(intent, func):
        ActionTrigger.triggers_map[intent] = func

    def execute(action):
        intent = action['intent']
        ActionTrigger.triggers_map[intent](action)

    @router(intent='打开浏览器')
    def open_browser(self, action):
        webbrowser.open('https://bing.com')

    @router(intent='查询时间')
    def get_time(input):
        now = datetime.datetime.now()
        prefix = '下午' if now.hour > 12 else '下午'
        current_time = now.strftime('%H时%M分')
        current_time = f'当前时间是：{prefix}{current_time}'
        print(current_time)
        return current_time

    @router(intent='检索信息')
    def search(action):
        entities = list(sorted(action.entities, key=lambda x:x['confidence'], reverse=True))
        webbrowser.open(f'https://bing.com/search?q={entities[0]}')
        return f'已为您检索到关于{entities[0]}的内容'
        

        






@trigger(keywords=['打开百度', '百度'])
def open_browser(input):
    webbrowser.open('https://www.baidu.com/')

@trigger(keywords=['询问时间'])
def get_time(input):
    now = datetime.datetime.now()
    prefix = '下午' if now.hour > 12 else '下午'
    time = now.strftime('%H时%M分')
    print(f'当前时间是{prefix}{time}')

@trigger(keywords=['搜索', '检索', '查询'])
def search(input):
    webbrowser.open(f'https://cn.bing.com/search?q={input}')

def playmusic(input):
    pass

    #http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=孤勇者&type=1&offset=0&total=true&limit=2
    #http://music.163.com/song/media/outer/url?id=（将id号）.mp3


if __name__ == '__main__':
    input = '打开百度'
    open_browser(input)
    input = '现在几点了'
    get_time(input)
    input = '检索鬼灭之刃'
    search(input)

    trigger = ActionTrigger(None)
    trigger.execute(None)


