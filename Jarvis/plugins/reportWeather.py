import re, sys
sys.path.append("..")
import requests
from xpinyin import Pinyin
from talk.actionTrigger import trigger
from os import environ as env

pinyin = Pinyin()

@trigger.route(keywords=['查询天气','询问天气'])
def report_weather(action):
    ip_info = get_ip()
    print(ip_info)
    if ip_info != None:
        cityCode = ip_info['cityCode']
        # apiKey = env.get('OPENWEATHERMAP_API_KEY')
        apiKey = '4780978e1508db0431f40a4bb13ec706'
        weatherInfo = get_weather(api_key=apiKey, city=cityCode)
        print(weatherInfo)
    return None

# 获取本机IP和地理位置
def get_ip():
    try:
        response = requests.get("https://www.ip.cn/api/index?ip=&type=0")
        result = response.json()
        result['cityName'] = result['address'].split(' ')[3].replace('市','')
        result['cityCode'] = pinyin.get_pinyin(result['cityName'],'')
        return result
    except Exception as e:
        return None

# 获取指定城市天气预报
def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    report_weather({})