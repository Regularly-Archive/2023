import functools
import webbrowser
import datetime
import jieba

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

def has_trigger(func):
    decorators = [d.__class__ for d in functools.wraps(func).decorator_list]
    return trigger in decorators


@trigger(keywords=['打开百度', '百度'])
def open_browser(input):
    webbrowser.open('https://www.baidu.com/')

@trigger(keywords=['当前时间', '几点了'])
def get_time(input):
    now = datetime.datetime.now()
    prefix = '下午' if now.hour > 12 else '下午'
    time = now.strftime('%H时%M分')
    print(f'当前时间是{prefix}{time}')

@trigger(keywords=['搜索', '检索', '查询'])
def search(input):
    webbrowser.open(f'https://cn.bing.com/search?q={input}')


if __name__ == '__main__':
    input = '打开百度'
    open_browser(input)
    input = '现在几点了'
    get_time(input)
    input = '检索鬼灭之刃'
    search(input)


