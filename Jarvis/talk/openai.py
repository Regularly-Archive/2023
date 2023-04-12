from aiohttp import ClientSession

class GPT3Bot:
    def __init__(self, session, openai_api_key, openai_api_endpoint='https://api.openai.com/v1/completions'):
            self.api_key = openai_api_key
            self.api_url = openai_api_endpoint
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            self.session = session

    async def ask(self, query):
        self.data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}]
        }
        r = await self.session.post(self.api_url, headers=self.headers, json=self.data)
        return await r.json()