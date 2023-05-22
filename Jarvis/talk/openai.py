import requests

class ChatGPTBot:
    def __init__(self, session, openai_api_key, openai_api_endpoint='https://api.openai.com/v1/completions', prompt=""):
            self.api_key = openai_api_key
            self.api_url = openai_api_endpoint
            self.prompt = prompt
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            self.session = session

    def ask(self, query):
        try:
            if self.prompt != None and self.prompt != '':
                query = self.prompt + query
            self.data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    # {"role": "system", "content": self.prompt},
                    # {"role": "assistant", "content": "你可以从信息检索、天气查询、日期查询、时间查询、设备控制、音乐查询、打开应用这些分类中选取最合适的意图。"},
                    {"role": "user", "content": query}
                ]
            }
            r = self.session.post(self.api_url, headers=self.headers, json=self.data)
            data = r.json()
            choices = data.get("choices")
            if not choices:
                return None
            else:
                message = choices[0]["message"]["content"]
                return message
        except Exception as e:
            return None
    
