import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.core.config import Config
from app.clients.telegram import TelegramClient

# ==========================================
# 🛠️ PRO DATA MODELS
# ==========================================
@dataclass
class TradeEvent:
    exchange: str
    symbol: str
    price: float
    value: float
    side: str
    timestamp: float
    score: float = 0.0
    tier: str = "C"

@dataclass
class Cluster:
    symbol: str
    total_volume: float = 0.0
    trade_count: int = 0
    start_time: float = field(default_factory=time.time)
    exchanges: List[str] = field(default_factory=list)

# ==========================================
# 🧠 PRO SIGNAL ENGINE (Scoring & Clustering)
# ==========================================
class SignalEngine:
    def __init__(self):
        self.clusters: Dict[str, Cluster] = {}
        self.cluster_window = 300  # 5 Dakikalık pencere
        self.confirmation_threshold = 2 # Kaç borsa onaylamalı?

    def calculate_score(self, value: float) -> tuple:
        """İşlemi değerine göre puanlar ve Tier atar."""
        if value >= 10_000_000: return 100, "S-TIER (GOD)"
        if value >= 1_000_000: return 70, "A-TIER (INSTITUTIONAL)"
        if value >= 500_000: return 40, "B-TIER (WHALE)"
        return 10, "C-TIER (SHARK)"

    def detect_cluster(self, event: TradeEvent) -> Optional[Cluster]:
        """Sinyalleri kümeleyerek kurumsal hareketleri tespit eder."""
        now = time.time()
        symbol = event.symbol
        
        if symbol not in self.clusters or (now - self.clusters[symbol].start_time) > self.cluster_window:
            self.clusters[symbol] = Cluster(symbol=symbol, start_time=now)
        
        cluster = self.clusters[symbol]
        cluster.total_volume += event.value
        cluster.trade_count += 1
        if event.exchange not in cluster.exchanges:
            cluster.exchanges.append(event.exchange)
        
        return cluster

# ==========================================
# 🌐 MULTI-EXCHANGE & ON-CHAIN MANAGER
# ==========================================
class IntelligenceManager:
    def __init__(self, telegram_client, config):
        self.telegram = telegram_client
        self.config = config
        self.engine = SignalEngine()
        self.cooldowns = {} # Flood Safe için

    async def process_signal(self, event: TradeEvent):
        # 1. Puanlama
        score, tier = self.engine.calculate_score(event.value)
        event.score = score
        event.tier = tier

        # 2. Kümeleme ve Kurumsal Analiz
        cluster = self.engine.detect_cluster(event)
        
        # 3. Multi-Exchange Confirmation (Sinyal Gücü)
        confirmation_multiplier = len(cluster.exchanges)
        final_score = event.score * (1 + (confirmation_multiplier * 0.2)) # Her ek borsa %20 güç katar

        # 4. Flood Safe Check
        last_alert = self.cooldowns.get(event.symbol, 0)
        if time.time() - last_alert < 10: # Aynı coin için 10sn bekle
            return

        # 5. Smart Money & Cluster Alert logic
        is_institutional = cluster.trade_count >= 3 and confirmation_multiplier >= 2
        
        # 🚀 MESSAGE CONSTRUCTION
        emoji = "💎" if is_institutional else "🐋"
        side_emoji = "🟢" if event.side == "BUY" else "🔴"
        
        msg = (
            f"{emoji} *{tier} SIGNAL DETECTED* {emoji}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🪙 **Asset:** `{event.symbol}`\n"
            f"🏢 **Exchange:** `{event.exchange}`\n"
            f"💰 **Value:** `${event.value:,.0f}`\n"
            f"↕️ **Side:** {side_emoji} `{event.side}`\n"
            f"📊 **Price:** `{event.price}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **Signal Strength:** `{final_score:.1f}/100`\n"
            f"👥 **Cluster:** `{cluster.trade_count} trades in 5m`\n"
            f"🌍 **Confirmed by:** `{', '.join(cluster.exchanges)}`\n"
            f"⚠️ **Type:** {'INSTITUTIONAL MOVEMENT' if is_institutional else 'SINGLE WHALE'}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 [Chart]({f'https://www.tradingview.com/chart/?symbol=BINANCE:{event.symbol}'})"
        )

        await self.telegram.send(self.config.OUTPUT_CHANNEL, msg)
        self.cooldowns[event.symbol] = time.time()

# ==========================================
# 🚀 MAIN ENGINE (Orchestrator)
# ==========================================
async def main():
    logging.basicConfig(level=logging.INFO)
    config = Config()
    config.BOT_TOKEN = "8647623541:AAEXP5hSkJb1FtmRLdN8g8RxL3iYKDI4vV0"
    config.OUTPUT_CHANNEL = "@fycbitusa"

    telegram = TelegramClient(config.BOT_TOKEN)
    intel_manager = IntelligenceManager(telegram, config)

    # Borsa Client'ları (Binance, Bybit, OKX vb.)
    # Not: Her borsa için TradeEvent döndüren Client yazılmalıdır.
    from app.clients.binance import BinanceClient
    binance = BinanceClient("wss://stream.binance.com:9443/ws")

    async def run_exchange(client, name):
        while True:
            try:
                async for trade in client.stream_trades():
                    # Veriyi TradeEvent formatına dönüştür (Normalization)
                    event = TradeEvent(
                        exchange=name,
                        symbol=trade['symbol'].upper(),
                        price=float(trade['price']),
                        value=float(trade['value']),
                        side="BUY" if not trade.get('is_buyer_maker') else "SELL",
                        timestamp=time.time()
                    )
                    await intel_manager.process_signal(event)
            except Exception as e:
                logging.error(f"Connection error {name}: {e}")
                await asyncio.sleep(5)

    # Parallel execution of all exchanges
    await asyncio.gather(
        run_exchange(binance, "Binance"),
        # run_exchange(bybit, "Bybit"), # BybitClient eklendiğinde açılır
        # run_exchange(okx, "OKX"),     # OKXClient eklendiğinde açılır
    )

if __name__ == "__main__":
    asyncio.run(main())
