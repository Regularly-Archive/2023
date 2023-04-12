import requests

class QinYunKeBot:

    def __init__(self, url='http://api.qingyunke.com/api.php?key=free&appid=0&msg={query}'):
        self.url = url

    def ask(self, query):
        r = requests.get(self.url.format(query=query))
        return r.json()
