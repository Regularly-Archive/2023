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
    
    def normalize(self, message):
        message = message.replace("\n", "，")
        message = message.replace('"', "，")
        message = message.replace('\r', "，")
        return message

    def ask(self, query):
        if self.prompt != None and self.prompt != '':
             query = self.prompt + query
        self.data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}]
        }
        r = self.session.post(self.api_url, headers=self.headers, json=self.data)
        data = r.json()
        choices = data.get("choices")
        if not choices:
            return None
        else:
            message = choices[0]["message"]["content"]
            message = self.normalize(message)
            return message
    
