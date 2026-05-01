from aiogram import Bot

class TelegramClient:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send(self, channel: str, message: str):
        await self.bot.send_message(channel, message)