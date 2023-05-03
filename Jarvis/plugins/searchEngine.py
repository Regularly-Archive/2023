import sys
import logging
sys.path.append('..')
import webbrowser
import requests
from pathlib import Path
import os, sys, json
sys.path.append("..")
from talk.actionTrigger import trigger
from speech.async_playsound import playsound_async

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'
download_folder = os.path.join(Path.home(), 'download')

logger = logging.getLogger('searchEngine')

@trigger.route(keywords=['搜索','检索','查询'])
def search(action):
    entities = list(sorted(action['entities'], key=lambda x:x['confidence'], reverse=True))
    query = entities[0]['value']
    webbrowser.open(f'https://bing.com/search?q={query}')
    return f'已为您检索到关于{query}的内容，请在浏览器中查看。'

@trigger.route(keywords=['播放音乐','搜索音乐'])
def search_music(action):
    entities = list(sorted(action['entities'], key=lambda x:x['confidence'], reverse=True))
    query = entities[0]['value']
    try:
        response = session.get(f'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={query}&type=1&offset=0&total=true&limit=2')
        response.raise_for_status()
        payload = json.loads(response.content)
        if payload['code'] == 200 and len(payload['result']['songs']) > 0:
            song_id = payload['result']['songs'][0]['id']
            song_name = payload['result']['songs'][0]['name']
            song_artist = payload['result']['songs'][0]['artists'][0]['name']
            response = session.get(f'http://music.163.com/song/media/outer/url?id={song_id}',allow_redirects=False)
            if response.status_code == 302:
                musicUrl = response.headers['Location']
                if musicUrl == 'http://music.163.com/404':
                    return '抱歉，没有为您找到相关歌曲'
                response = session.get(musicUrl)
                if not os.path.exists(download_folder):
                    os.mkdir(download_folder)
                musicFile = os.path.join(download_folder, f'{song_id}.mp3')
                with open(musicFile, 'wb')as fp:
                    fp.write(response.content)
                    logger.info(f'{musicFile} 保存成功!')   
                playsound_async(musicFile)
                return f'已为您找到{song_artist}的《{song_name}》'
        else:
            return '抱歉，没有为您找到相关歌曲'
    except Exception as e:
        print(e)
        return '抱歉，没有为您找到相关歌曲'
