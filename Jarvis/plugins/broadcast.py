import sys
# sys.path.append("..")
# from talk.actionTrigger import trigger
import datetime, requests, random
import feedparser

playlist = {
    '余生皆假期': 'https://hayami.typlog.io/feed/audio.xml',
    '机核网': 'http://feed.tangsuanradio.com/gadio.xml',
    '一席': 'http://www.ximalaya.com/album/242812.xml',
    '半瓶醋': 'https://getpodcast.xyz/data/163/1082007.xml',
    '随机波动': 'https://feeds.fireside.fm/stovol/rss'
}

# @trigger.route(keywords=['broadcasting'])
def play_it(action):
    try:
        # entities = list(sorted(action['entities'], key=lambda x:x['confidence'], reverse=True))
        # query = entities[0]['value']
        query = '随机波动'
        if query in playlist:
            rss_url = playlist[query]
            response = requests.get(rss_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            latest = feed.entries[0]
            title = latest['title']
            link = list(filter(lambda x:x['type'] == 'audio/mpeg', latest['links']))[0]
            print(title, link['href'])
        else:
            return '抱歉，没有为你找到相关的节目'
        
    except Exception as ex:
        pass


if  __name__ == '__main__':
    play_it({})