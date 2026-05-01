import websockets
import json

class BinanceClient:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url

    async def stream_trades(self, symbol="btcusdt"):
        url = f"{self.ws_url}/{symbol}@trade"

        async with websockets.connect(url) as ws:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)

                qty = float(data["q"])
                price = float(data["p"])
                value = qty * price

                yield {
                    "symbol": symbol,
                    "price": price,
                    "value": value
                }