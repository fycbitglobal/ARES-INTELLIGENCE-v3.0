import asyncio
import logging
import time
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from app.core.config import Config
from app.clients.telegram import TelegramClient
from app.clients.binance import BinanceClient

# ==========================================
# ⚙️ CONFIGURATION & CONSTANTS
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = Config()
config.BOT_TOKEN = "BOT_TOKEN"
config.OUTPUT_CHANNEL = "@fycbitusa"

# 🐋 BALİNA AYARLARI
COIN_LIMITS = {"BTCUSDT": 2_000_000, "ETHUSDT": 1_000_000, "DEFAULT": 1_500_000}
MIN_CLUSTER_TRADES = 3
MIN_CLUSTER_VOLUME = 5_000_000
CLUSTER_WINDOW = 300

# ==========================================
# 🛠️ DATA MODELS
# ==========================================
@dataclass
class TradeEvent:
    exchange: str
    symbol: str
    price: float
    value: float
    side: str
    timestamp: float

@dataclass
class SignalCluster:
    symbol: str
    total_volume: float = 0.0
    trade_count: int = 0
    exchanges: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)

# ==========================================
# 🧠 MODÜL 1: PRO SIGNAL ENGINE (Filtering & Clustering)
# ==========================================
class SignalEngine:
    def __init__(self):
        self.active_clusters: Dict[str, SignalCluster] = {}

    def process_event(self, event: TradeEvent) -> Optional[str]:
        limit = COIN_LIMITS.get(event.symbol, COIN_LIMITS["DEFAULT"])
        if event.value < limit: return None

        now = time.time()
        if event.symbol not in self.active_clusters or (now - self.active_clusters[event.symbol].start_time) > CLUSTER_WINDOW:
            self.active_clusters[event.symbol] = SignalCluster(symbol=event.symbol, start_time=now)
        
        cluster = self.active_clusters[event.symbol]
        cluster.total_volume += event.value
        cluster.trade_count += 1
        if event.exchange not in cluster.exchanges: cluster.exchanges.append(event.exchange)

        if cluster.trade_count >= MIN_CLUSTER_TRADES and cluster.total_volume >= MIN_CLUSTER_VOLUME:
            strength = "ULTRA STRONG" if cluster.total_volume > 20_000_000 else "STRONG"
            side_emoji = "🟢" if event.side == "BUY" else "🔴"
            msg = (
                f"💎 *INSTITUTIONAL CLUSTER DETECTED* 💎\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🪙 **Asset:** `{event.symbol}`\n"
                f"💪 **Sinyal Gücü:** `{strength}`\n"
                f"💰 **Toplam Hacim:** `${cluster.total_volume:,.0f}`\n"
                f"📦 **İşlem Sayısı:** `{cluster.trade_count} Trade`\n"
                f"↕️ **Yön:** {side_emoji} `{event.side}`\n"
                f"🌍 **Borsalar:** `{', '.join(cluster.exchanges)}`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ *Sadece yüksek hacimli kurumsal hareketler raporlanır.*"
            )
            del self.active_clusters[event.symbol]
            return msg
        return None

# ==========================================
# 📈 MODÜL 2: TECHNICAL ANALYSIS & CHARTING
# ==========================================
class TechAnalysisEngine:
    def __init__(self, client):
        self.client = client

    async def get_metrics(self, symbol: str):
        # 1 Günlük Veri
        df_1d = await self.client.get_historical_klines(symbol, '1d')
        # 4 Saatlik Veri (Grafik için)
        df_4h = await self.client.get_historical_klines(symbol, '4h')
        
        # İndikatörler
        df_1d['RSI'] = ta.rsi(df_1d['close'], length=14)
        macd = ta.macd(df_1d['close'])
        bb = ta.bbands(df_1d['close'], length=20)
        atr = ta.atr(df_1d['high'], df_1d['low'], df_1d['close'])
        
        last = df_1d.iloc[-1]
        return {
            "price": last['close'], "rsi": last['RSI'], 
            "macd": "Pozitif" if last['MACD'] > last['MACD_S'] else "Negatif",
            "support": df_1d['low'].min(), "resistance": df_1d['high'].max(),
            "bb_u": last['BBU'], "bb_m": last['BBM'], "bb_l": last['BBL'],
            "sl": last['close'] - (atr.iloc[-1] * 2), "tp": last['close'] + (atr.iloc[-1] * 3),
            "df_4h": df_4h
        }

    def create_dark_chart(self, symbol: str, df: pd.DataFrame):
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True)
        mc = mpf.make_marketcolors(up='green', down='red', edge='inherit', wick='inherit', volume='in')
        s = mpf.set_style(mpf.style_generic)
        s.update(facecolor='#000000', edgecolor='#333333', gridcolor='#111111')
        path = f"charts/{symbol}_4h.png"
        mpf.plot(df, type='candle', style=s, marketcolors=mc, title=f"{symbol} 4H", savefig=path)
        return path

# ==========================================
# 🤖 MODÜL 3: AI ANALYST & DAILY REPORTS
# ==========================================
class AIAnalyst:
    async def generate_commentary(self, symbol, data):
        # AI Simülasyonu (Gerçek API ile bağlanabilir)
        return f"Analiz sonucunda {symbol} için 1 günlük grafikte güçlü bir trend gözlemleniyor. RSI {data['rsi']:.2f} seviyesinde olup, MACD'nin {data['macd']} olması orta vadeli yönün yukarı/aşağı olduğunu gösteriyor."

    async def get_top_lists(self, tech_engine):
        coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT"]
        buys, sells = [], []
        for c in coins:
            d = await tech_engine.get_metrics(c)
            score = 0
            if d['rsi'] < 40: score += 1
            if d['macd'] == "Pozitif": score += 1
            if score >= 2: buys.append(c) elif score <= 0: sells.append(c)
        return buys[:10], sells[:10]

# ==========================================
# 🚀 MAIN ORCHESTRATOR (Sistemi Yöneten)
# ==========================================
class AresIntelligence:
    def __init__(self):
        self.telegram = TelegramClient(config.BOT_TOKEN)
        self.binance = BinanceClient(config.BINANCE_WS_URL)
        self.signal_engine = SignalEngine()
        self.tech_engine = TechAnalysisEngine(self.binance)
        self.ai_analyst = AIAnalyst()

    async def handle_whale(self, event: TradeEvent):
        msg = self.signal_engine.process_event(event)
        if msg: await self.telegram.send(config.OUTPUT_CHANNEL, msg)

    async def send_morning_report(self):
        symbol = "BTCUSDT"
        data = await self.tech_engine.get_metrics(symbol)
        chart = self.tech_engine.create_dark_chart(symbol, data['df_4h'])
        comment = await self.ai_analyst.generate_commentary(symbol, data)
        buys, sells = await self.ai_analyst.get_top_lists(self.tech_engine)
        
        report = (
            f"🚀 *{symbol} Teknik Analiz Raporu*\n\n"
            f"💰 Fiyat: `{data['price']}`\n📈 RSI: `{data['rsi']:.2f}`\n📊 MACD: `{data['macd']}`\n"
            f"📉 Destek: `{data['support']:.2f}` | 📈 Direnç: `{data['resistance']:.2f}`\n"
            f"🛑 Stop: `{data['sl']:.2f}` | 💸 Take: `{data['tp']:.2f}`\n\n"
            f"🧠 *AI Yorum:* _{comment}_\n\n"
            f"☀️ *TOP 10 LİSTESİ*\n🟢 AL: {', '.join(buys)}\n🔴 SAT: {', '.join(sells)}"
        )
        await self.telegram.send_photo(config.OUTPUT_CHANNEL, chart, caption=report)

    async def run(self):
        logger.info("🚀 Ares Intelligence v3.0 Aktif!")
        
        # 1. Balina Takibi (Real-time)
        async def whale_task():
            while True:
                try:
                    async for trade in self.binance.stream_trades():
                        event = TradeEvent("Binance", trade['symbol'].upper(), float(trade['price']), 
                                           float(trade['value']), "BUY" if not trade.get('is_buyer_maker') else "SELL", time.time())
                        await self.handle_whale(event)
                except Exception as e:
                    logger.error(f"Whale Task Error: {e}")
                    await asyncio.sleep(5)

        # 2. Sabah Raporu (Daily)
        async def report_task():
            while True:
                # Test için 1 saatte bir, gerçekte 86400 saniye
                await asyncio.sleep(3600) 
                await self.send_morning_report()

        await asyncio.gather(whale_task(), report_task())

if __name__ == "__main__":
    try:
        asyncio.run(AresIntelligence().run())
    except KeyboardInterrupt:
        pass
