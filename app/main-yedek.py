import asyncio
import logging
from app.core.config import Config
from app.clients.telegram import TelegramClient
from app.clients.binance import BinanceClient

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config()

# 🔥 ANA AYARLAR
config.BOT_TOKEN = "8647623541:AAEXP5hSkJb1FtmRLdN8g8RxL3iYKDI4vV0"
config.OUTPUT_CHANNEL = "@fycbit"
config.BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

# 🐋 COIN BAZLI LİMİTLER (Dolar cinsinden)
# Buraya istediğin coinleri ekleyebilirsin. 
# Eğer coin burada yoksa, aşağıdaki DEFAULT_LIMIT geçerli olur.
COIN_LIMITS = {
    "BTCUSDT": 1_000_000,   # BTC için 1 Milyon $
    "ETHUSDT": 500_000,     # ETH için 500 Bin $
    "SOLUSDT": 200_000,     # SOL için 200 Bin $
    "BNBUSDT": 200_000,     # BNB için 200 Bin $
    "XRPUSDT": 100_000,     # XRP için 100 Bin $
    "ADAUSDT": 100_000,     # ADA için 100 Bin $
    "DOGEUSDT": 50_000,     # DOGE için 50 Bin $
}

# 🛡️ VARSAYILAN LİMİT (Listede olmayan coinler için geçerli olan limit)
DEFAULT_LIMIT = 1_000_000 

async def main():
    print("🚀 Gelişmiş Balina Takip Botu Başlatıldı...")
    print(f"⚙️ Coin bazlı limitler aktif. Varsayılan limit: ${DEFAULT_LIMIT:,}")

    telegram = TelegramClient(config.BOT_TOKEN)
    binance = BinanceClient(config.BINANCE_WS_URL)

    try:
        async for trade in binance.stream_trades():
            symbol = trade['symbol'].upper()
            value = trade['value']
            
            # 🎯 Bu coin için geçerli limiti belirle
            # Eğer coin COIN_LIMITS içinde varsa onu al, yoksa DEFAULT_LIMIT'i al.
            limit = COIN_LIMITS.get(symbol, DEFAULT_LIMIT)

            # 🛡️ FİLTRE: İşlem değeri belirlenen limitin altındaysa atla
            if value < limit:
                continue 

            # 🟢/🔴 Alış mı Satış mı? (Binance is_buyer_maker mantığı)
            # is_buyer_maker True ise -> SATIŞ (Sell)
            # is_buyer_maker False ise -> ALIŞ (Buy)
            side = "🔴 SELL (SATIŞ)" if trade.get('is_buyer_maker') else "🟢 BUY (ALIŞ)"
            
            # Mesaj formatı (TradingView linki de eklendi!)
            tv_link = f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}"
            
            msg = (
                f"🚨 *WHALE DETECTED* 🚨\n\n"
                f"🪙 Pair: *{symbol}*\n"
                f"💰 Value: *${value:,.0f}*\n"
                f"↕️ Side: *{side}*\n"
                f"📊 Price: `{trade['price']}`\n\n"
                f"📈 [Grafiği Gör]({tv_link})"
            )

            try:
                await telegram.send(config.OUTPUT_CHANNEL, msg)
                print(f"✅ {side} Yakalandı: {symbol} - ${value:,.0f} (Limit: ${limit:,})")
            except Exception as e:
                logger.error(f"❌ Mesaj gönderilemedi: {e}")
                if "Forbidden" in str(e):
                    print("🛑 HATA: Bot kanal yöneticisi değil!")
                    break

    except Exception as e:
        logger.error(f"⚠️ Genel bir hata oluştu: {e}")
    finally:
        if hasattr(telegram, 'bot'):
            await telegram.bot.session.close()
            print("🔌 Bağlantılar kapatıldı.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Program kullanıcı tarafından kapatıldı.")
