class EventProcessor:
    def __init__(self, ollama, telegram, config):
        self.ollama = ollama
        self.telegram = telegram
        self.config = config

    async def handle_whale(self, session, event):
        raw = f"WHALE DETECTED: {event.value}$ on {event.symbol}"

        ai = await self.ollama.analyze(session, raw)

        msg = (
            "🐋 WHALE ALERT\n\n"
            f"{raw}\n\n"
            f"AI:\n{ai}"
        )

        await self.telegram.send(self.config.OUTPUT_CHANNEL, msg)