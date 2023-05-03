import logging
import sys
sys.path.append("..")
from talk.actionTrigger import trigger
import datetime, requests, random

logger = logging.getLogger(__name__)

@trigger.route(keywords=['查询时间','询问时间','时间查询'])
def report_time(input):
    now = datetime.datetime.now()
    prefix = '上午'
    if now.hour >= 0 and now.hour < 6:
        prefix = '凌晨'
    elif now.hour >= 6 and now.hour < 9:
        prefix = '早上'
    elif now.hour >= 9 and now.hour < 12:
        prefix = '上午'
    elif now.hour >= 12 and now.hour < 18:
        prefix = '下午'
    elif now.hour >= 18 and now.hour <= 23:
        prefix = '晚上'
    formated = now.strftime('%H时%M分')
    return f'当前时间是{prefix}{formated}'


@trigger.route(keywords=['查询日期','询问日期','日期查询'])
def report_date(input):
    now = datetime.datetime.now()
    week_list = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    formated = now.strftime('%Y年%m月%d日')
    week_day = week_list[now.weekday()]
    history = today_on_history()
    if history != None:
        return f'今天是{formated}，{week_day}。{history}。'
    else:
        return f'今天是{formated}，{week_day}。'


def today_on_history():
    try:
        response = requests.get('https://www.ipip5.com/today/api.php?type=json')
        payload = response.json()
        event = random.choice(payload['result'])
        event_year = event['year']
        event_date = payload['today']
        event_desc = event['title']
        return f'历史上的今天: {event_year}年{event_date}, {event_desc}'
    except Exception as e:
        logger.error(e, exc_info=True)
        return None
    