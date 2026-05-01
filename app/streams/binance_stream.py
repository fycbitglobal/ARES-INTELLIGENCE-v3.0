from app.clients.binance import BinanceClient
from app.services.whale_detector import WhaleDetector

class BinanceStream:
    def __init__(self, detector, processor, session):
        self.client = BinanceClient()
        self.detector = detector
        self.processor = processor
        self.session = session

    async def run(self):
        async for trade in self.client.stream_trades():

            event = self.detector.detect(trade)
            if not event:
                continue

            await self.processor.handle_whale(self.session, event)