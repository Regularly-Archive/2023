import sys, logging
import webbrowser
sys.path.append("..")
import requests
from xpinyin import Pinyin
from talk.actionTrigger import trigger
from os import environ as env

pinyin = Pinyin()
logger = logging.getLogger(__name__)

@trigger.route(keywords=['query_weather','查询天气','询问天气','天气查询'])
def report_weather(action):
    ip_info = get_ip()
    if ip_info != None:
        province = ip_info['province']
        cityName = ip_info['cityName']
        cityCode = ip_info['cityCode']
        apiKey = env.get('QWEATHER_API_KEY')
        location = get_location(apiKey, province, cityName, cityCode)
        if location != None:
            weather = get_weather(apiKey, locationCode=location['id'])
            if weather != None:
                now = weather['now']
                temp = now['temp']
                desc = now['text']
                windDir = now['windDir']
                windScale = now['windScale']
                humidity = now['humidity']
                webbrowser.open(weather['fxLink'])
                return f'{cityName}当前气温为{temp}摄氏度、{desc}、{windDir}{windScale}级、相对湿度{humidity}%，您可以在浏览器中查看更多信息'
            else:
                return '抱歉，我暂时无法获取实时天气信息，请您稍后重试'
        else:
            return '抱歉，我暂时无法获取实时天气信息，请您稍后重试'
    else:
        return '抱歉，我暂时无法获取实时天气信息，请您稍后重试'

# 获取本机IP和地理位置
def get_ip():
    try:
        response = requests.get("https://www.ip.cn/api/index?ip=&type=0")
        result = response.json()
        result['province'] = result['address'].split(' ')[2]
        result['cityName'] = result['address'].split(' ')[3].replace('市','')
        result['cityCode'] = pinyin.get_pinyin(result['cityName'],'')
        return result
    except Exception as e:
        logger.error(e, exc_info=True)
        return None

# 获取指定城市天气预报
def get_weather(api_key, locationCode):
    try:
        host = env.get('QWEATHER_HOST_URL')
        url = f"https://{host}/v7/weather/now?key={api_key}&location={locationCode}"
        response = requests.get(url)
        response = response.json()
        if response['code'] == '200':
            return response
        else:
            return None
    except Exception as e:
        logger.error(e, exc_info=True)
        return None


# 获取指定城市代码
def get_location(api_key, province, cityName, cityCode):
    try:
        url = f"https://geoapi.qweather.com/v2/city/lookup?key={api_key}&location={cityCode}"
        response = requests.get(url)
        response = response.json()
        if response['code'] == '200':
            locations = response['location']
            locations = list(filter(lambda x:x['name'] == cityName and x['adm1'] == province, locations))
            if len(locations) > 0:
                return locations[0]
            else:
                return None
    except Exception as e:
        logger.error(e, exc_info=True)
        return None



if __name__ == '__main__':
    report_weather({})