# ARES-INTELLIGENCE-v3.0
Evet, buna yazılım dünyasında **README.md** denir. Bir projenin "kimlik kartı" gibidir. Eğer bu projeyi GitHub'a yüklersen veya birine sunarsan, insanlar ne yaptığını ve nasıl çalıştırdığını buradan anlar.

Bir Blockchain ve Yazılım Mühendisi olarak, projeni sadece "kod" olarak değil, bir **"Ürün"** olarak sunan, profesyonel, İngilizce ve Türkçe detaylar içeren bir README hazırladım.

Aşağıdaki metni kopyalayıp projenin ana dizinine **`README.md`** adıyla kaydedebilirsin.

---

# 🚀 Ares Intelligence v3.0
### Institutional Market Intelligence & Whale Tracking Platform

**Ares Intelligence**, kripto para piyasalarındaki büyük oyuncuların (balinaların) ve kurumsal yatırımcıların ayak izlerini gerçek zamanlı olarak takip eden, teknik analiz yapan ve yapay zeka destekli piyasa yorumları sunan yüksek performanslı bir istihbarat sistemidir.

---

## 🌟 Temel Özellikler (Key Features)

### 🐋 1. Gelişmiş Balina Takibi (Whale Intelligence)
- **Multi-Exchange Monitoring:** Binance ve diğer büyük borsaların WebSocket akışlarını anlık izler.
- **Whale Scoring (Tier System):** İşlemleri hacmine göre puanlar:
  - `S-TIER (GOD)`: > 10M$
  - `A-TIER (Institutional)`: > 1M$
  - `B-TIER (Whale)`: > 500K$
- **Cluster Detection (Sürü Analizi):** Tekil işlemleri değil, kısa süre içinde gerçekleşen koordineli büyük işlemleri (kurumsal hareketler) tespit eder.
- **Multi-Exchange Confirmation:** Farklı borsalardaki eşzamanlı hareketleri doğrulayarak sinyal gücünü artırır.

### 📈 2. Profesyonel Teknik Analiz (Quant Engine)
- **Timeframe Analysis:** 1 Günlük (1D) trend analizi ve 4 Saatlik (4H) giriş stratejileri.
- **Quantitative Indicators:** RSI, MACD, Bollinger Bands ve ATR (Average True Range) hesaplamaları.
- **Volatility-Based SL/TP:** Sabit yüzdeler yerine ATR bazlı dinamik Stop-Loss ve Take-Profit bölgeleri belirler.
- **Siyah Tema Grafikler:** `mplfinance` ile TradingView standartlarında, kurumsal görünümlü 4 saatlik mum grafikleri üretir.

### 🤖 3. AI & Sabah Bülteni (AI Analyst)
- **AI Sentiment Fusion:** Teknik verileri anlamlandırarak profesyonel piyasa yorumları üretir.
- **Top 10 Alpha List:** Her sabah piyasadaki en güçlü `AL` ve `SAT` veren 10 coin'i skorlayarak listeler.

### 🛠️ 4. Mühendislik Standartları
- **Modular Architecture:** Yeni borsaların kolayca eklenebildiği plugin tabanlı yapı.
- **Flood-Safe System:** Telegram API limitlerini koruyan, sinyalleri birleştiren (Aggregation) yapı.
- **Auto-Reconnect:** Bağlantı kopmalarında otomatik yeniden bağlanma mekanizması.

---

## 🛠️ Kurulum (Installation)

### Gereksinimler
- Python 3.10+
- Telegram Bot Token

### Adımlar
1. **Kodu Klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/ares-intelligence.git
   cd ares-intelligence
   ```

2. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install pandas pandas_ta mplfinance aiogram websockets
   ```

3. **Yapılandırma:**
   `app/core/config.py` dosyasını veya `main.py` içerisindeki ayarları düzenleyin:
   - `BOT_TOKEN`: Telegram Bot Token'ınız.
   - `OUTPUT_CHANNEL`: Mesajların gideceği kanal (örn: `@kanaladi`).

4. **Çalıştırın:**
   ```bash
   python -m app.main
   ```

---

## 📊 Sinyal Gücü Tablosu (Signal Strength)

| Tier | Volume | Meaning | Action |
| :--- | :--- | :--- | :--- |
| **S-Tier** | > 10M$ | God Tier / Market Maker | High Impact |
| **A-Tier** | > 1M$ | Institutional Move | Strong Signal |
| **B-Tier** | > 500K$ | Whale Activity | Moderate Signal |
| **C-Tier** | < 500K$ | Retail/Small Whale | Low Impact |

---

## 📜 Yasal Uyarı (Disclaimer)
*Bu bot tarafından üretilen analizler ve sinyaller tamamen matematiksel verilere ve algoritmalara dayalıdır. **Yatırım tavsiyesi değildir.** Kripto para piyasaları yüksek risk içerir; tüm sorumluluk kullanıcıya aittir.*

---

### 🛠️ Developer
**Developed by [Senin Adın/Kullanıcı Adın]**  
*Blockchain & Software Engineer*

---

### 💡 Mühendislik Notu (Teknik Detay)
Sistem, $O(1)$ zaman karmaşıklığında çalışan bir `Normalization Layer` kullanır. Veriler `TradeEvent` veri sınıfı (dataclass) üzerinden taşınarak bellek yönetimi optimize edilmiştir. Grafik üretim süreci `asynchronous` yapıya uygun olarak optimize edilerek ana akışı engellemez.

---

### Bu README'yi neden böyle hazırladım?
1.  **Yatırımcı Psikolojisi:** "Institutional", "S-Tier", "Quant Engine" gibi terimler kullanarak botun basit bir yazılım değil, profesyonel bir araç olduğunu vurguladım.
2.  **Teknik Detay:** Bir mühendis olarak kullandığın `O(1)` ve `Normalization` gibi terimleri ekledim, böylece kodu inceleyen biri senin uzmanlığını anlar.
3.  **Kullanılabilirlik:** Kurulum adımlarını net bir şekilde belirttim.

**Artık projen hem kod olarak hem de sunum (dokümantasyon) olarak tam anlamıyla profesyonel!** 🚀💎
