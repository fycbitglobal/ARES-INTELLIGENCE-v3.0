import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    CRYPTO_PANIC_API: str = os.getenv("CRYPTO_PANIC_API", "")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
    MODEL: str = os.getenv("MODEL", "qwen2.5")
    OUTPUT_CHANNEL: str = os.getenv("OUTPUT_CHANNEL", "@channel")

    WHALE_THRESHOLD_USDT: float = 100_000
