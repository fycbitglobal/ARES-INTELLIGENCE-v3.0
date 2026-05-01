from app.models.events import WhaleEvent

class WhaleDetector:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def detect(self, trade: dict) -> WhaleEvent | None:
        price = float(trade["p"])
        qty = float(trade["q"])
        value = price * qty

        if value < self.threshold:
            return None

        return WhaleEvent(
            symbol="BTCUSDT",
            price=price,
            qty=qty,
            value=value,
            source="binance"
        )