import aiohttp

class CryptoPanicClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def fetch(self, session: aiohttp.ClientSession):
        url = f"https://cryptopanic.com/api/v1/posts?auth_token={self.api_key}&public=true"

        async with session.get(url) as r:
            return await r.json()