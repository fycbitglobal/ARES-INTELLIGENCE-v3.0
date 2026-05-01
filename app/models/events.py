from dataclasses import dataclass

@dataclass
class WhaleEvent:
    symbol: str
    price: float
    qty: float
    value: float
    source: str