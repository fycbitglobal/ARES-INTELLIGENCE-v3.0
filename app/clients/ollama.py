import aiohttp

class OllamaClient:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    async def analyze(self, session, text: str):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Analyze crypto market impact (BULLISH/BEARISH)."},
                {"role": "user", "content": text}
            ],
            "stream": False
        }

        async with session.post(self.url, json=payload) as r:
            if r.status != 200:
                return text
            data = await r.json()
            return data["message"]["content"]