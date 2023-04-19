import functools
import webbrowser
import datetime

def trigger(keywords):
    def outerWrapper(func):
        def wrapper(*args, **kwargs):
            if args[0] in keywords:
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

if __name__ == '__main__':
    input = '打开百度'
    open_browser(input)
    input = '几点了'
    get_time(input)


