import sys
sys.path.append("..")
from talk.actionTrigger import trigger
import datetime

@trigger.route(keywords=['查询时间','询问时间'])
def report_time(input):
    now = datetime.datetime.now()
    prefix = '下午' if now.hour > 12 else '上午'
    formated = now.strftime('%H时%M分')
    return f'当前时间是{prefix}{formated}'