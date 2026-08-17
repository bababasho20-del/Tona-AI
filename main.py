"""
═══════════════════════════════════════════════════════════════════════════════════
🚀 Tona AI V2.0 - البوت الاستشاري الذكي (نسخة طبق الأصل من القديم + تحسينات)
💙 الاسم: Tona AI
👨‍💻 المطور: بسام الحوباني
📡 النظام: بوت تداول استشاري متخصص في النفط والفضة (تعلم عميق طويل المدى)
🧠 جميع التحليلات والتوصيات والتحذيرات والدروس تعتمد على Gemini + Groq
📌 الإضافات الجديدة:
   - زر فتح صفقة يدوياً (تُعامل كالصفقات التلقائية)
   - نظام تعلم ثلاثي الأبعاد (سيناريوهات، شخصية السوق، دروس عميقة)
   - لا توجد محادثة ذكية (فقط أزرار وأوامر محددة)
═══════════════════════════════════════════════════════════════════════════════════
"""

# ====================================================================================
# 📦 PART 01: الاستيرادات والإعدادات الأساسية
# ====================================================================================

import os
import time
import json
import re
import threading
import queue
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── نماذج الذكاء الاصطناعي ──
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

# ── المتغيرات البيئية ──
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# ── إعدادات التسجيل ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s'
)
logger = logging.getLogger("TonaAI")

# ── متغيرات عامة ──
TRADES_FILE_OIL = "trades_history_oil.json"
TRADES_FILE_SILVER = "trades_history_silver.json"
POSITION_FILE_OIL = "current_position_oil.json"
POSITION_FILE_SILVER = "current_position_silver.json"
SIGNAL_CHECK_INTERVAL = 60
MONITORING_INTERVAL = 300
FILE_LOCKS = {"oil": threading.Lock(), "silver": threading.Lock()}
CLOSE_LOCKS = {"oil": threading.Lock(), "silver": threading.Lock()}
MONITOR_TRIGGER = {"oil": None, "silver": None}
MONITOR_TRIGGER_LOCK = threading.Lock()
LAST_SIGNAL_TIME = {"oil": 0, "silver": 0}
LAST_SIGNAL_LOCK = threading.Lock()
TELEGRAM_QUEUE = queue.Queue()
REPORT_LOCK = threading.Lock()
LAST_DAILY_REPORT = None
LAST_EXPORT = datetime.now().isoformat()

# ── أسماء جداول Supabase الموحدة ──
TABLE_TRADES_FULL = "trades_full"
TABLE_LESSONS_DEEP = "lessons_deep"
TABLE_SNAPSHOTS = "snapshots"
TABLE_SCENARIOS = "scenarios"
TABLE_MARKET_PROFILE = "market_profile"

# ── ملفات التعلم العميق (محلية) ──
SCENARIOS_FILE = "learning_data/scenarios.json"
MARKET_PROFILE_FILE = "learning_data/market_profile.json"
DEEP_LESSONS_FILE = "learning_data/deep_lessons.json"

# ── تأكد من وجود مجلدات ──
os.makedirs("learning_data", exist_ok=True)
os.makedirs("learning_data/backups", exist_ok=True)

# ====================================================================================
# 📦 PART 02: طبقة البيانات والمؤشرات (رياضي بحت - بدون تغيير)
# ====================================================================================

def get_mexc_candles(symbol: str, interval: str = "Min15", limit: int = 200):
    """جلب بيانات الشموع من MEXC"""
    url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}?interval={interval}&limit={limit}"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success') and 'data' in data:
                raw = data['data']
                closes = [float(x) for x in raw.get('close', [])]
                highs = [float(x) for x in raw.get('high', [])]
                lows = [float(x) for x in raw.get('low', [])]
                opens = [float(x) for x in raw.get('open', [])]
                volumes = [float(x) for x in raw.get('vol', [])]
                min_len = min(len(closes), len(highs), len(lows), len(opens), len(volumes))
                if min_len < 5:
                    return None
                return {
                    "closes": closes[:min_len],
                    "highs": highs[:min_len],
                    "lows": lows[:min_len],
                    "opens": opens[:min_len],
                    "volumes": volumes[:min_len]
                }
        return None
    except Exception as e:
        logger.error(f"خطأ في جلب البيانات: {e}")
        return None

def calculate_rsi_7(src, length=7):
    """حساب RSI (Wilder's MA)"""
    if not src or len(src) < length:
        return None
    deltas = [src[i] - src[i-1] for i in range(1, len(src))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    def rma(data, period):
        if len(data) < period:
            return None
        alpha = 1.0 / period
        res = [sum(data[:period]) / period]
        for x in data[period:]:
            res.append(alpha * x + (1 - alpha) * res[-1])
        return res
    
    avg_gains = rma(gains, length)
    avg_losses = rma(losses, length)
    if avg_gains is None or avg_losses is None:
        return None
    rsi_vals = [50.0] * (len(src) - len(avg_gains))
    for i in range(len(avg_gains)):
        if avg_losses[i] == 0:
            rsi_vals.append(100.0)
        else:
            rsi_vals.append(100.0 - (100.0 / (1 + avg_gains[i] / avg_losses[i])))
    return rsi_vals

def calculate_macd_full(src):
    """MACD كامل (12, 26, 9)"""
    if not src or len(src) < 35:
        return None, None, None
    def ema(data, period):
        if not data or len(data) < period:
            return None
        alpha = 2.0 / (period + 1)
        res = [data[0]]
        for x in data[1:]:
            res.append(alpha * x + (1 - alpha) * res[-1])
        return res
    f_ema = ema(src, 12)
    s_ema = ema(src, 26)
    if f_ema is None or s_ema is None:
        return None, None, None
    min_len = min(len(f_ema), len(s_ema))
    f_ema = f_ema[:min_len]
    s_ema = s_ema[:min_len]
    macd_line = [f - s for f, s in zip(f_ema, s_ema)]
    sig_line = ema(macd_line, 9)
    if sig_line is None:
        return None, None, None
    min_len = min(len(macd_line), len(sig_line))
    macd_line = macd_line[:min_len]
    sig_line = sig_line[:min_len]
    histogram = [m - s for m, s in zip(macd_line, sig_line)]
    return macd_line, sig_line, histogram

def calculate_atr_14(data):
    """حساب ATR (14) باستخدام RMA"""
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    if not closes or not highs or not lows or len(closes) < 15:
        return None
    n = len(closes)
    tr = [0.0] * n
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
    def rma(data, period):
        if len(data) < period:
            return None
        alpha = 1.0 / period
        res = [sum(data[:period]) / period]
        for x in data[period:]:
            res.append(alpha * x + (1 - alpha) * res[-1])
        return res
    atr_series = rma(tr, 14)
    if atr_series is None:
        return None
    return atr_series[-1]

def calculate_vpt_correct(closes, volumes):
    """حساب VPT (باستخدام السعر الحالي في المقام)"""
    if not closes or not volumes or len(closes) < 2 or len(volumes) != len(closes):
        return None
    vpt_values = [0.0]
    cum_vpt = 0.0
    for i in range(1, len(closes)):
        change = closes[i] - closes[i-1]
        if closes[i] != 0:
            vpt_value = volumes[i] * (change / closes[i])
            cum_vpt += vpt_value
        vpt_values.append(cum_vpt)
    return vpt_values

def calculate_supertrend_vpt_correct(data, st_mult=2.5, st_period=100, vpt_len=10):
    """SuperTrend + VPT (نفس طريقة TradingView)"""
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    volumes = data.get("volumes", [])
    n = len(closes)
    if n < st_period + 10 or len(highs) != n or len(lows) != n or len(volumes) != n:
        return None
    
    # VPT
    v = calculate_vpt_correct(closes, volumes)
    if v is None or len(v) != n:
        return None
    
    # حساب shadow و out
    def stdev_pop(src, length):
        if not src or length <= 0:
            return None
        res = []
        for i in range(len(src)):
            if i < length - 1:
                res.append(0.0)
            else:
                window = src[i-length+1:i+1]
                clean = [x for x in window if x is not None and not (x != x)]
                if len(clean) < 2:
                    res.append(0.0)
                    continue
                mean = sum(clean) / len(clean)
                variance = sum((x - mean) ** 2 for x in clean) / len(clean)
                res.append(variance ** 0.5 if variance >= 0 else 0.0)
        return res
    
    hl_spread = [highs[i] - lows[i] for i in range(n)]
    price_spread = stdev_pop(hl_spread, 28)
    if price_spread is None or len(price_spread) != n:
        return None
    
    v_len = 14
    smooth = []
    for i in range(n):
        start = max(0, i - v_len + 1)
        window = v[start:i+1]
        smooth.append(sum(window) / len(window) if window else 0.0)
    v_diff = [v[i] - smooth[i] for i in range(n)]
    v_spread = stdev_pop(v_diff, 28)
    if v_spread is None or len(v_spread) != n:
        return None
    
    shadow = []
    out = []
    for i in range(n):
        vsp = v_spread[i] if v_spread[i] != 0 else 1.0
        sh = ((v[i] - smooth[i]) / vsp) * price_spread[i]
        shadow.append(sh)
        out.append(highs[i] + sh if sh > 0 else lows[i] + sh)
    
    alpha = 2.0 / (vpt_len + 1)
    vpt_ema = [out[0]]
    for i in range(1, n):
        vpt_ema.append(alpha * out[i] + (1 - alpha) * vpt_ema[-1])
    
    # SuperTrend
    st_src = [(highs[i] + lows[i]) / 2 for i in range(n)]
    def rma(data, period):
        if len(data) < period:
            return None
        alpha = 1.0 / period
        res = [sum(data[:period]) / period]
        for x in data[period:]:
            res.append(alpha * x + (1 - alpha) * res[-1])
        return res
    
    tr = [0.0] * n
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
    atr_val = rma(tr, st_period)
    if atr_val is None or len(atr_val) != n:
        return None
    
    up_trend = [0.0] * n
    down_trend = [0.0] * n
    trend = [1] * n
    st_line = [0.0] * n
    
    for i in range(n):
        if i == 0:
            up_lev = st_src[i] - (st_mult * atr_val[i])
            dn_lev = st_src[i] + (st_mult * atr_val[i])
            up_trend[i] = up_lev
            down_trend[i] = dn_lev
            trend[i] = 1
            st_line[i] = up_lev
        else:
            up_lev = st_src[i] - (st_mult * atr_val[i])
            dn_lev = st_src[i] + (st_mult * atr_val[i])
            if st_src[i-1] > up_trend[i-1]:
                up_trend[i] = max(up_lev, up_trend[i-1])
            else:
                up_trend[i] = up_lev
            if st_src[i-1] < down_trend[i-1]:
                down_trend[i] = min(dn_lev, down_trend[i-1])
            else:
                down_trend[i] = dn_lev
            if st_src[i] > down_trend[i-1]:
                trend[i] = 1
            elif st_src[i] < up_trend[i-1]:
                trend[i] = -1
            else:
                trend[i] = trend[i-1]
            st_line[i] = up_trend[i] if trend[i] == 1 else down_trend[i]
    
    return st_line, trend, vpt_ema

# ====================================================================================
# 📦 PART 03: استراتيجية الدخول (VPT + SuperTrend - بدون تغيير)
# ====================================================================================

def generate_raw_signal(asset_type: str) -> Dict:
    """توليد إشارة خام من VPT + SuperTrend"""
    symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
    data = get_mexc_candles(symbol, interval="Min15", limit=200)
    if not data or not data.get("closes") or len(data["closes"]) < 10:
        return {"signal": "WAIT", "price": 0, "sl": 0, "tp": 0, "rr": 0}
    
    closes = data["closes"]
    price = closes[-1]
    
    # حساب VPT + SuperTrend
    st_mult = 2.5 if asset_type == "oil" else 2.2
    result = calculate_supertrend_vpt_correct(data, st_mult=st_mult, st_period=100, vpt_len=10)
    if result is None:
        return {"signal": "WAIT", "price": price, "sl": 0, "tp": 0, "rr": 0}
    
    st_line_arr, trend, vpt_ema = result
    if len(vpt_ema) < 3 or len(st_line_arr) < 3 or len(trend) < 3:
        return {"signal": "WAIT", "price": price, "sl": 0, "tp": 0, "rr": 0}
    
    current_vpt = vpt_ema[-1]
    current_st = st_line_arr[-1]
    prev_vpt = vpt_ema[-2] if len(vpt_ema) > 1 else current_vpt
    prev_st = st_line_arr[-2] if len(st_line_arr) > 1 else current_st
    
    crossover = prev_vpt <= prev_st and current_vpt > current_st
    crossunder = prev_vpt >= prev_st and current_vpt < current_st
    
    # تأكيد الإغلاق (شمعة واحدة)
    confirmation_ok = True
    if crossover or crossunder:
        current_trend = trend[-1]
        for i in range(1, 2):
            if len(trend) > i and trend[-i] != current_trend:
                confirmation_ok = False
                break
    else:
        confirmation_ok = False
    
    if crossover and confirmation_ok:
        signal = "BUY"
    elif crossunder and confirmation_ok:
        signal = "SELL"
    else:
        signal = "WAIT"
    
    # حساب SL/TP باستخدام ATR
    atr = calculate_atr_14(data)
    if signal != "WAIT" and atr is not None and atr > 0:
        sl_mult = 2.0
        tp_mult = 3.0
        sl_dist = atr * sl_mult
        tp_dist = atr * tp_mult
        if signal == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
        else:  # SELL
            sl = price + sl_dist
            tp = price - tp_dist
        rr = tp_mult / sl_mult if sl_mult > 0 else 0
    else:
        sl = tp = 0
        rr = 0
    
    return {"signal": signal, "price": price, "sl": sl, "tp": tp, "rr": rr}

# ====================================================================================
# 📦 PART 04: نواة الذكاء الاصطناعي (AI Core) - المعدل بالكامل
# ====================================================================================

class AICore:
    """المحرك الذكي للبوت - جميع الاستدعاءات للنماذج تمر من هنا"""
    
    def __init__(self):
        self.gemini_model = None
        self.groq_model = "openai/gpt-oss-120b"  # ✅ نفس النموذج المستخدم في البوت القديم
        
        # تهيئة Gemini
        if GEMINI_AVAILABLE and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-3.5-flash')
                logger.info("✅ Gemini 3.5 Flash جاهز")
            except Exception as e:
                logger.error(f"❌ فشل تهيئة Gemini: {e}")
        else:
            logger.warning("⚠️ Gemini غير متوفر")
        
        # تهيئة Groq
        if GROQ_API_KEY:
            logger.info("✅ Groq API جاهز (نموذج: openai/gpt-oss-120b)")
        else:
            logger.warning("⚠️ Groq API غير متوفر")
    
    # ════════════════════════════════════════════════════════════════════
    # دوال استدعاء النماذج (مطابقة تماماً للبوت القديم الذي يعمل)
    # ════════════════════════════════════════════════════════════════════
    
    def _call_gemini(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """نسخة مطابقة للبوت القديم - تستخدم Gemini"""
        if not self.gemini_model:
            logger.warning("⚠️ Gemini غير مهيأ")
            return None
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens, "temperature": 0.3}
            )
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("⚠️ رد Gemini فارغ")
                return None
        except Exception as e:
            logger.error(f"❌ Gemini فشل: {e}")
            return None
    
    def _call_groq(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """نسخة مطابقة للبوت القديم - تستخدم Groq"""
        if not GROQ_API_KEY:
            logger.warning("⚠️ Groq API Key مفقود")
            return None
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            # ✅ نفس الهيكل المستخدم في البوت القديم
            messages = [{"role": "user", "content": prompt}]
            payload = {
                "model": self.groq_model,  # openai/gpt-oss-120b
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": max_tokens,
                "top_p": 0.9  # ✅ أضف top_p كما في البوت القديم
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                if content:
                    return content.strip()
                else:
                    logger.warning("⚠️ رد Groq فارغ")
                    return None
            else:
                logger.error(f"❌ Groq خطأ {response.status_code}: {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ Groq استثناء: {e}")
            return None
    
    def _call_model(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """استدعاء Gemini أولاً، فإن فشل يستخدم Groq"""
        # محاولة Gemini
        response = self._call_gemini(prompt, max_tokens)
        if response:
            return response
        # محاولة Groq
        response = self._call_groq(prompt, max_tokens)
        if response:
            return response
        logger.error("❌ كلا النموذجين فشلا")
        return None
    
    # ════════════════════════════════════════════════════════════════════
    # دوال التحليل والتقييم (تستخدم دوال الاستدعاء أعلاه)
    # ════════════════════════════════════════════════════════════════════
    
    def analyze_market(self, asset: str, data: Dict, open_trade: Optional[Dict] = None) -> Dict:
        """
        تحليل شامل للسوق - يُعيد تقييماً ونصيحة (بدون قرار تنفيذي)
        يُستخدم للأزرار: تحليل النفط/الفضة، وضع الصفقة الحالية
        """
        # استخراج المؤشرات من data
        closes = data.get("closes", [])
        if not closes:
            return {"error": "لا توجد بيانات"}
        price = closes[-1]
        
        # حساب المؤشرات الأساسية
        rsi = calculate_rsi_7(closes)
        rsi_val = rsi[-1] if rsi else 50
        macd_line, sig_line, hist = calculate_macd_full(closes)
        macd_val = hist[-1] if hist else 0
        atr = calculate_atr_14(data)
        
        # حساب الفريمات المختلفة
        timeframes = {}
        for tf, interval in [("5m", "Min5"), ("15m", "Min15"), ("1h", "Min60"), ("4h", "Hour4")]:
            tf_data = get_mexc_candles("USOIL_USDT" if asset == "oil" else "SILVER_USDT", interval, 50)
            if tf_data and tf_data.get("closes"):
                result = calculate_supertrend_vpt_correct(tf_data, st_mult=2.5 if asset == "oil" else 2.2)
                if result:
                    _, trend, _ = result
                    timeframes[tf] = "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد"
        
        # بناء الـ Prompt
        prompt = f"""أنت خبير تداول محترف في النفط والفضة. قم بتحليل شامل للأصل التالي وأجب بالصيغة المطلوبة فقط.

═══════════════════════════════════════
📊 بيانات السوق:
═══════════════════════════════════════
• الأصل: {asset}
• السعر الحالي: ${price:.2f}
• RSI (7): {rsi_val:.1f}
• MACD Histogram: {macd_val:.4f}
• ATR (14): {atr:.4f} ({(atr/price*100) if price > 0 else 0:.2f}%)

🕐 تحليل الفريمات:
"""
        for tf, trend in timeframes.items():
            prompt += f"   • {tf}: {trend}\n"
        
        # إضافة معلومات الصفقة المفتوحة إن وجدت
        if open_trade:
            entry = open_trade.get('entry_price', 0)
            trade_type = open_trade.get('type', 'BUY')
            if entry > 0:
                profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" else ((entry - price) / entry * 100)
            else:
                profit_pct = 0
            prompt += f"""
═══════════════════════════════════════
📈 الصفقة المفتوحة:
═══════════════════════════════════════
• النوع: {trade_type}
• سعر الدخول: ${entry:.2f}
• الربح/الخسارة الحالية: {profit_pct:+.2f}%
• وقف الخسارة: ${open_trade.get('sl', 0):.2f}
• الهدف: ${open_trade.get('tp', 0):.2f}
"""
        
        prompt += """
═══════════════════════════════════════
المطلوب (أجب بالصيغة التالية فقط):
═══════════════════════════════════════
التقييم: [قوي/متوسط/ضعيف]
الدرجة: [0-100]
الأسباب: [سبب1، سبب2، سبب3]
نصيحة: [نصيحة مختصرة للمستخدم]
مستوى الخطر: [1/2/3]  (1=آمن، 2=مراقبة، 3=خطر داهم)

ملاحظة: إذا كانت هناك صفقة مفتوحة، اذكر في النصيحة ما إذا كان ينصح بالاستمرار أم الإغلاق.
"""
        
        response = self._call_model(prompt, max_tokens=400)
        if not response:
            return {"error": "تعذر الحصول على تحليل من النموذج"}
        
        # استخراج المعلومات باستخدام Regex
        result = {
            "evaluation": "متوسط",
            "score": 50,
            "reasons": [],
            "advice": "لا توجد نصيحة",
            "risk_level": 1,
            "raw_response": response
        }
        
        eval_match = re.search(r'التقييم:\s*(.+)', response)
        if eval_match:
            result["evaluation"] = eval_match.group(1).strip()
        
        score_match = re.search(r'الدرجة:\s*(\d+)', response)
        if score_match:
            try:
                result["score"] = int(score_match.group(1))
            except ValueError:
                pass
        
        reasons_match = re.search(r'الأسباب:\s*(.+)', response)
        if reasons_match:
            reasons_text = reasons_match.group(1).strip()
            result["reasons"] = [r.strip() for r in reasons_text.split('،') if r.strip()]
        
        advice_match = re.search(r'نصيحة:\s*(.+)', response)
        if advice_match:
            result["advice"] = advice_match.group(1).strip()
        
        risk_match = re.search(r'مستوى الخطر:\s*(\d+)', response)
        if risk_match:
            try:
                result["risk_level"] = min(3, max(1, int(risk_match.group(1))))
            except ValueError:
                pass
        
        return result
    
    def generate_alert(self, asset: str, open_trade: Dict, current_data: Dict) -> Dict:
        """
        تحليل الخطر للصفقة المفتوحة - يُعيد مستوى التحذير (1، 2، 3)
        يُستخدم في المراقبة العميقة (deep_monitor)
        """
        price = current_data.get("price", 0)
        if not price:
            return {"level": 1, "message": "لا توجد بيانات", "action": "notify"}
        
        entry = open_trade.get('entry_price', 0)
        trade_type = open_trade.get('type', 'BUY')
        sl = open_trade.get('sl', 0)
        tp = open_trade.get('tp', 0)
        if entry > 0:
            profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" else ((entry - price) / entry * 100)
        else:
            profit_pct = 0
        
        # حساب المؤشرات الحالية
        closes = current_data.get("closes", [])
        rsi = calculate_rsi_7(closes)
        rsi_val = rsi[-1] if rsi else 50
        macd_line, sig_line, hist = calculate_macd_full(closes)
        macd_val = hist[-1] if hist else 0
        atr = calculate_atr_14(current_data)
        
        # حساب المسافة إلى SL و TP
        dist_to_sl = 0
        dist_to_tp = 0
        if sl > 0 and entry > 0:
            if trade_type == "BUY":
                dist_to_sl = (price - sl) / entry * 100
                dist_to_tp = (tp - price) / entry * 100 if tp > 0 else 0
            else:
                dist_to_sl = (sl - price) / entry * 100
                dist_to_tp = (price - tp) / entry * 100 if tp > 0 else 0
        
        prompt = f"""أنت خبير إدارة مخاطر. قم بتحليل الخطر للصفقة التالية وأجب بالصيغة المطلوبة فقط.

═══════════════════════════════════════
📊 بيانات الصفقة:
═══════════════════════════════════════
• الأصل: {asset}
• النوع: {trade_type}
• سعر الدخول: ${entry:.2f}
• السعر الحالي: ${price:.2f}
• الربح/الخسارة: {profit_pct:+.2f}%
• المسافة إلى SL: {dist_to_sl:.2f}%
• المسافة إلى TP: {dist_to_tp:.2f}%
• RSI: {rsi_val:.1f}
• MACD Histogram: {macd_val:.4f}
• ATR: {atr:.4f} ({(atr/price*100) if price > 0 else 0:.2f}%)

═══════════════════════════════════════
المطلوب (أجب بالصيغة التالية فقط):
═══════════════════════════════════════
مستوى الخطر: [1/2/3]  (1=آمن، 2=مراقبة، 3=خطر داهم يستدعي الإغلاق)
الرسالة: [رسالة تحذيرية مختصرة]

ملاحظة: المستوى 3 يعني أن الصفقة في خطر داهم ويجب إغلاقها فوراً.
"""
        
        response = self._call_model(prompt, max_tokens=200)
        if not response:
            return {"level": 1, "message": "تعذر الحصول على تحليل الخطر", "action": "notify"}
        
        result = {"level": 1, "message": "لا توجد تحذيرات", "action": "notify"}
        
        level_match = re.search(r'مستوى الخطر:\s*(\d+)', response)
        if level_match:
            try:
                level = int(level_match.group(1))
                result["level"] = min(3, max(1, level))
                if result["level"] == 3:
                    result["action"] = "close"
            except ValueError:
                pass
        
        msg_match = re.search(r'الرسالة:\s*(.+)', response)
        if msg_match:
            result["message"] = msg_match.group(1).strip()
        
        return result
    
    def extract_deep_lesson(self, trade_data: Dict, market_context: str) -> Dict:
        """
        استخلاص درس عميق وسيناريو من صفقة مغلقة
        يُستخدم بعد إغلاق الصفقة للتعلم
        """
        # تنظيف القيم للحماية من None
        entry_price = trade_data.get('entry_price', 0) or 0
        exit_price = trade_data.get('exit_price', 0) or 0
        profit = trade_data.get('profit_dollars', 0) or 0
        
        prompt = f"""أنت خبير تعلم آلي في الأسواق المالية. قم بتحليل الصفقة التالية واستخلص درساً وسيناريو.

═══════════════════════════════════════
📊 بيانات الصفقة:
═══════════════════════════════════════
• الأصل: {trade_data.get('asset', 'unknown')}
• النوع: {trade_data.get('type', 'UNKNOWN')}
• سعر الدخول: ${entry_price:.2f}
• سعر الخروج: ${exit_price:.2f}
• الربح/الخسارة: ${profit:.2f}
• سبب الإغلاق: {trade_data.get('exit_reason', 'غير معروف')}
• مدة الصفقة: {trade_data.get('duration_minutes', 0)} دقيقة

📊 المؤشرات عند الدخول:
   • RSI: {trade_data.get('entry_rsi', 'N/A')}
   • ADX: {trade_data.get('entry_adx', 'N/A')}
   • MACD: {trade_data.get('entry_macd', 'N/A')}
   • الاتجاه: {trade_data.get('entry_trend', 'N/A')}

📊 المؤشرات عند الخروج:
   • RSI: {trade_data.get('exit_rsi', 'N/A')}
   • ADX: {trade_data.get('exit_adx', 'N/A')}
   • MACD: {trade_data.get('exit_macd', 'N/A')}
   • الاتجاه: {trade_data.get('exit_trend', 'N/A')}

═══════════════════════════════════════
سياق السوق الحالي:
═══════════════════════════════════════
{market_context}

═══════════════════════════════════════
المطلوب (أجب بالصيغة التالية فقط):
═══════════════════════════════════════
الدرس: [جملة واحدة مختصرة]
السيناريو: [وصف الظروف التي أدت إلى هذه النتيجة]
الشرط: [شرط مستقبلي للتعرف على هذا السيناريو]
النصيحة: [نصيحة للمستقبل]
"""
        
        response = self._call_model(prompt, max_tokens=400)
        if not response:
            return {"lesson": "تعذر استخلاص درس", "scenario": "", "condition": "", "advice": ""}
        
        result = {}
        
        lesson_match = re.search(r'الدرس:\s*(.+)', response)
        if lesson_match:
            result["lesson"] = lesson_match.group(1).strip()
        else:
            result["lesson"] = "درس غير معروف"
        
        scenario_match = re.search(r'السيناريو:\s*(.+)', response)
        if scenario_match:
            result["scenario"] = scenario_match.group(1).strip()
        else:
            result["scenario"] = ""
        
        condition_match = re.search(r'الشرط:\s*(.+)', response)
        if condition_match:
            result["condition"] = condition_match.group(1).strip()
        else:
            result["condition"] = ""
        
        advice_match = re.search(r'النصيحة:\s*(.+)', response)
        if advice_match:
            result["advice"] = advice_match.group(1).strip()
        else:
            result["advice"] = ""
        
        return result
    
    def update_market_profile(self, asset: str, recent_trades: List[Dict]) -> str:
        """
        تحديث وصف شخصية السوق بناءً على آخر الصفقات
        يُستخدم يومياً
        """
        if not recent_trades:
            return "لا توجد بيانات كافية لتحديث شخصية السوق"
        
        trades_summary = ""
        for i, trade in enumerate(recent_trades[-10:], 1):
            profit = trade.get('profit_dollars', 0) or 0
            entry = trade.get('entry_price', 0) or 0
            exit_p = trade.get('exit_price', 0) or 0
            trades_summary += f"{i}. {trade.get('type')} @ ${entry:.2f} → ${exit_p:.2f} | {profit:+.2f}$ | {trade.get('exit_reason', '')}\n"
        
        prompt = f"""أنت خبير تحليل أسواق. قم بتحليل سلوك سوق {asset} بناءً على آخر الصفقات واكتب وصفاً مختصراً.

═══════════════════════════════════════
آخر الصفقات:
═══════════════════════════════════════
{trades_summary}

═══════════════════════════════════════
المطلوب:
═══════════════════════════════════════
اكتب فقرة واحدة (لا تتجاوز 100 كلمة) تصف فيها:
1. الاتجاه العام للسوق حالياً.
2. مستوى التقلب.
3. أي أنماط لاحظتها.
4. توقعاتك العامة للفترة القادمة.

أجب بنص عادي فقط، بدون تنسيق أو عناوين.
"""
        
        response = self._call_model(prompt, max_tokens=300)
        if response:
            return response.strip()
        return "تعذر تحديث شخصية السوق"
    
    def generate_intelligence_report(self, asset: str, trades: List[Dict], market_profile: str) -> str:
        """
        توليد تقرير استخباراتي شامل
        يُستخدم عند طلب المستخدم
        """
        if not trades:
            return "لا توجد بيانات كافية لتوليد تقرير استخباراتي"
        
        closed_trades = [t for t in trades if t.get('status') == 'closed']
        if not closed_trades:
            return "لا توجد صفقات مغلقة لتوليد التقرير"
        
        wins = [t for t in closed_trades if (t.get('profit_dollars', 0) or 0) > 0]
        losses = [t for t in closed_trades if (t.get('profit_dollars', 0) or 0) <= 0]
        win_rate = len(wins) / len(closed_trades) * 100 if closed_trades else 0
        total_profit = sum((t.get('profit_dollars', 0) or 0) for t in closed_trades)
        
        prompt = f"""أنت خبير استخبارات مالية. قم بتوليد تقرير استخباراتي شامل عن سوق {asset}.

═══════════════════════════════════════
إحصائيات الأداء:
═══════════════════════════════════════
• إجمالي الصفقات المغلقة: {len(closed_trades)}
• الصفقات الرابحة: {len(wins)}
• الصفقات الخاسرة: {len(losses)}
• نسبة النجاح: {win_rate:.1f}%
• إجمالي الربح: ${total_profit:.2f}

═══════════════════════════════════════
شخصية السوق الحالية:
═══════════════════════════════════════
{market_profile}

═══════════════════════════════════════
المطلوب:
═══════════════════════════════════════
اكتب تقريراً استخباراتياً موجزاً (150-200 كلمة) يحتوي على:
1. تحليل أداء السوق.
2. نقاط القوة والضعف.
3. توقعات للفترة القادمة.
4. نصائح استراتيجية للمتداول.

أجب بنص عادي، مع عناوين فرعية إن لزم.
"""
        
        response = self._call_model(prompt, max_tokens=500)
        if response:
            return response
        return "تعذر توليد التقرير الاستخباراتي"
       
# ====================================================================================
# 📦 PART 05: نظام التعلم العميق (إدارة السيناريوهات وشخصية السوق والدروس)
# ====================================================================================

def load_scenarios() -> List[Dict]:
    """تحميل السيناريوهات من الملف المحلي (مع احتياطي Supabase)"""
    try:
        if os.path.exists(SCENARIOS_FILE):
            with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        logger.warning(f"⚠️ فشل تحميل السيناريوهات: {e}")
    return []

def save_scenarios(scenarios: List[Dict]) -> bool:
    """حفظ السيناريوهات في الملف المحلي"""
    try:
        os.makedirs(os.path.dirname(SCENARIOS_FILE), exist_ok=True)
        with open(SCENARIOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ السيناريوهات: {e}")
        return False

def load_market_profile() -> Dict:
    """تحميل شخصية السوق"""
    try:
        if os.path.exists(MARKET_PROFILE_FILE):
            with open(MARKET_PROFILE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception as e:
        logger.warning(f"⚠️ فشل تحميل شخصية السوق: {e}")
    return {"oil": "لا توجد بيانات كافية", "silver": "لا توجد بيانات كافية", "last_updated": ""}

def save_market_profile(profile: Dict) -> bool:
    """حفظ شخصية السوق"""
    try:
        os.makedirs(os.path.dirname(MARKET_PROFILE_FILE), exist_ok=True)
        with open(MARKET_PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ شخصية السوق: {e}")
        return False

def load_deep_lessons() -> List[str]:
    """تحميل الدروس العميقة"""
    try:
        if os.path.exists(DEEP_LESSONS_FILE):
            with open(DEEP_LESSONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        logger.warning(f"⚠️ فشل تحميل الدروس العميقة: {e}")
    return []

def save_deep_lessons(lessons: List[str]) -> bool:
    """حفظ الدروس العميقة"""
    try:
        os.makedirs(os.path.dirname(DEEP_LESSONS_FILE), exist_ok=True)
        with open(DEEP_LESSONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(lessons, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ الدروس العميقة: {e}")
        return False

def add_scenario(scenario: Dict) -> bool:
    """إضافة سيناريو جديد أو تحديث سيناريو موجود"""
    scenarios = load_scenarios()
    # البحث عن سيناريو مشابه
    condition = scenario.get('condition', '')
    for s in scenarios:
        if s.get('condition', '') == condition:
            s['occurrences'] = s.get('occurrences', 0) + 1
            s['last_updated'] = datetime.now().isoformat()
            save_scenarios(scenarios)
            return True
    # إضافة سيناريو جديد
    scenario['id'] = f"sc_{int(time.time())}"
    scenario['occurrences'] = 1
    scenario['last_updated'] = datetime.now().isoformat()
    scenarios.append(scenario)
    save_scenarios(scenarios)
    return True

def add_deep_lesson(lesson: str) -> bool:
    """إضافة درس عميق جديد (مع تجنب التكرار)"""
    lessons = load_deep_lessons()
    # تجنب التكرار (نبحث عن تشابه 70%)
    for existing in lessons:
        if len(existing) > 10 and len(lesson) > 10:
            # بسيط: إذا كان النص متشابهاً جداً
            if existing[:30] == lesson[:30]:
                return False
    lessons.append(lesson)
    if len(lessons) > 50:
        lessons = lessons[-50:]  # حد أقصى 50 درساً
    save_deep_lessons(lessons)
    return True

def get_relevant_lessons(indicators: Dict) -> List[str]:
    """استرجاع الدروس ذات الصلة بالوضع الحالي"""
    lessons = load_deep_lessons()
    if not lessons:
        return []
    # بسيط: نرجع آخر 5 دروس
    return lessons[-5:]

def get_matching_scenarios(indicators: Dict) -> List[Dict]:
    """استرجاع السيناريوهات المشابهة للوضع الحالي"""
    scenarios = load_scenarios()
    if not scenarios:
        return []
    # بسيط: نرجع آخر 3 سيناريوهات
    return scenarios[-3:]

# ====================================================================================
# 📦 PART 06: المدير التنفيذي (فتح وإغلاق الصفقات) - المعدل بالكامل
# ====================================================================================

class TradingCore:
    """مدير الصفقات - فتح، إغلاق، مراقبة"""
    
    def __init__(self, ai_core: AICore):
        self.ai_core = ai_core
        self.accounting = AccountingSystem()
    
    def open_trade(self, asset_type: str, signal_data: Dict, source: str = "auto") -> bool:
        """
        فتح صفقة جديدة (تلقائياً أو يدوياً)
        source: "auto" أو "manual"
        """
        existing = get_current_open_trade(asset_type)
        if existing:
            logger.info(f"⚠️ توجد صفقة {asset_type} مفتوحة بالفعل")
            return False
        
        signal = signal_data.get('signal')
        price = signal_data.get('price', 0)
        sl = signal_data.get('sl')
        tp = signal_data.get('tp')
        rr = signal_data.get('rr', 0)
        
        if signal not in ['BUY', 'SELL'] or price <= 0:
            logger.error(f"❌ بيانات إشارة غير صالحة لـ {asset_type}")
            return False
        
        trade_id = f"{asset_type}_{int(time.time())}"
        
        # حساب المؤشرات عند الدخول (للتعلم)
        data = get_mexc_candles("USOIL_USDT" if asset_type == "oil" else "SILVER_USDT", "Min15", 200)
        closes = data.get("closes", []) if data else []
        rsi = calculate_rsi_7(closes)
        rsi_val = rsi[-1] if rsi else 50
        macd_line, sig_line, hist = calculate_macd_full(closes)
        macd_val = hist[-1] if hist else 0
        adx = calculate_adx_14(data) if data else 20
        
        trade = {
            "trade_id": trade_id,
            "type": signal,
            "entry_price": price,
            "sl": sl,
            "tp": tp,
            "rr": rr,
            "profit_dollars": 0.0,
            "status": "open",
            "timestamp": datetime.now().isoformat(),
            "entry_indicators": {
                "rsi": rsi_val,
                "macd": macd_val,
                "adx": adx,
                "trend": "صاعد" if signal == "BUY" else "هابط"
            },
            "source": source,
            "warnings_sent": [],
            "warnings_log": []
        }
        
        if not save_current_trade(asset_type, trade):
            logger.error(f"❌ فشل حفظ صفقة {asset_type}")
            return False
        
        history = load_trades_history(asset_type)
        history["trades"].append(trade)
        save_trades_history(asset_type, history)
        
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        signal_label = "شراء 🟢" if signal == "BUY" else "بيع 🔴"
        msg = f"📊 **توصية Tona AI - {asset_label}**\n"
        msg += f"🎯 {signal_label} عند ${safe_price(price)}\n"
        msg += f"🛡️ وقف الخسارة: ${safe_price(sl)}\n"
        msg += f"🎯 الهدف: ${safe_price(tp)}\n"
        msg += f"📊 RR: {rr:.2f}\n"
        if source == "manual":
            msg += "📌 تم الفتح يدوياً\n"
        msg += "\n💙 Tona AI: سأراقب الصفقة وأحذرك عند الحاجة."
        queue_telegram_message(msg)
        
        with MONITOR_TRIGGER_LOCK:
            MONITOR_TRIGGER[asset_type] = {"reason": "new_trade", "time": time.time()}
        
        logger.info(f"✅ تم فتح صفقة {asset_type} ({signal}) بـ ${price:.2f}")
        return True
    
    def close_trade(self, asset_type: str, reason: str, current_price: Optional[float] = None) -> bool:
        """إغلاق الصفقة المفتوحة"""
        with CLOSE_LOCKS[asset_type]:
            open_trade = get_current_open_trade(asset_type)
            if not open_trade:
                logger.info(f"⏭️ لا توجد صفقة {asset_type} مفتوحة")
                return True
            
            entry_price = open_trade.get('entry_price', 0)
            trade_type = open_trade.get('type', 'BUY')
            trade_id = open_trade.get('trade_id', '')
            
            if current_price is None:
                symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
                data = get_mexc_candles(symbol, "Min1", 5)
                current_price = data["closes"][-1] if data and data.get("closes") else entry_price
            
            profit_dollars = AccountingSystem.calculate_profit_dollars(entry_price, current_price, trade_type)
            
            history = load_trades_history(asset_type)
            trade_found = False
            for trade in history["trades"]:
                if trade.get("trade_id") == trade_id:
                    trade_found = True
                    trade["status"] = "closed"
                    trade["exit_price"] = current_price
                    trade["exit_reason"] = reason
                    trade["profit_dollars"] = profit_dollars
                    trade["exit_timestamp"] = datetime.now().isoformat()
                    trade["duration_minutes"] = int((datetime.now() - datetime.fromisoformat(trade.get("timestamp", datetime.now().isoformat()))).total_seconds() / 60)
                    data = get_mexc_candles("USOIL_USDT" if asset_type == "oil" else "SILVER_USDT", "Min15", 200)
                    if data and data.get("closes"):
                        closes = data["closes"]
                        rsi = calculate_rsi_7(closes)
                        trade["exit_indicators"] = {
                            "rsi": rsi[-1] if rsi else 50,
                            "macd": calculate_macd_full(closes)[2][-1] if calculate_macd_full(closes)[2] else 0,
                            "adx": calculate_adx_14(data) or 20
                        }
                    break
            
            if not trade_found:
                logger.error(f"❌ لم يُعثر على الصفقة {trade_id} في السجل")
                return False
            
            save_trades_history(asset_type, history)
            delete_current_trade(asset_type)
            
            with MONITOR_TRIGGER_LOCK:
                MONITOR_TRIGGER[asset_type] = None
            
            self._learn_from_trade(asset_type, trade)
            
            asset_label = "النفط" if asset_type == "oil" else "الفضة"
            profit_label = "ربح ✅" if profit_dollars > 0 else "خسارة ❌" if profit_dollars < 0 else "تعادل ⚪"
            msg = f"📊 **تم إغلاق صفقة {asset_label}**\n"
            msg += f"💰 سعر الدخول: ${safe_price(entry_price)}\n"
            msg += f"💰 سعر الخروج: ${safe_price(current_price)}\n"
            msg += f"📊 النتيجة: {profit_label} (${profit_dollars:+.2f})\n"
            msg += f"📌 سبب الإغلاق: {reason}"
            queue_telegram_message(msg)
            
            logger.info(f"✅ تم إغلاق صفقة {asset_type} ({reason}) بـ ${current_price:.2f}")
            return True
    
    def _learn_from_trade(self, asset_type: str, trade: Dict):
        """استخلاص الدروس من الصفقة المغلقة"""
        try:
            trade_data = {
                "asset": asset_type,
                "type": trade.get('type'),
                "entry_price": trade.get('entry_price', 0) or 0,
                "exit_price": trade.get('exit_price', 0) or 0,
                "profit_dollars": trade.get('profit_dollars', 0) or 0,
                "exit_reason": trade.get('exit_reason', ''),
                "duration_minutes": trade.get('duration_minutes', 0),
                "entry_rsi": trade.get('entry_indicators', {}).get('rsi'),
                "entry_adx": trade.get('entry_indicators', {}).get('adx'),
                "entry_macd": trade.get('entry_indicators', {}).get('macd'),
                "entry_trend": trade.get('entry_indicators', {}).get('trend', 'N/A'),
                "exit_rsi": trade.get('exit_indicators', {}).get('rsi'),
                "exit_adx": trade.get('exit_indicators', {}).get('adx'),
                "exit_macd": trade.get('exit_indicators', {}).get('macd'),
                "exit_trend": trade.get('exit_indicators', {}).get('trend', 'N/A')
            }
            
            market_profile = load_market_profile()
            context = market_profile.get(asset_type, "لا توجد بيانات كافية")
            
            lesson_result = self.ai_core.extract_deep_lesson(trade_data, context)
            
            if lesson_result.get('lesson') and lesson_result['lesson'] != "تعذر استخلاص درس":
                add_deep_lesson(lesson_result['lesson'])
                logger.info(f"🧠 تم حفظ درس: {lesson_result['lesson'][:50]}...")
            
            if lesson_result.get('scenario') and lesson_result.get('condition'):
                scenario = {
                    "condition": lesson_result['condition'],
                    "scenario": lesson_result['scenario'],
                    "outcome": "ربح" if trade_data['profit_dollars'] > 0 else "خسارة",
                    "confidence": 70,
                    "advice": lesson_result.get('advice', '')
                }
                add_scenario(scenario)
                logger.info(f"📋 تم حفظ سيناريو: {scenario['condition'][:50]}...")
            
            self._update_market_profile_if_needed(asset_type)
            
        except Exception as e:
            logger.error(f"❌ فشل التعلم من الصفقة: {e}")
    
    def _update_market_profile_if_needed(self, asset_type: str):
        profile = load_market_profile()
        last_updated = profile.get('last_updated', '')
        if last_updated:
            try:
                last_dt = datetime.fromisoformat(last_updated)
                if (datetime.now() - last_dt).days >= 1:
                    self._update_market_profile(asset_type)
            except:
                self._update_market_profile(asset_type)
        else:
            self._update_market_profile(asset_type)
    
    def _update_market_profile(self, asset_type: str):
        try:
            history = load_trades_history(asset_type)
            trades = history.get('trades', [])
            closed_trades = [t for t in trades if t.get('status') == 'closed']
            
            if len(closed_trades) < 3:
                return
            
            recent_trades = []
            for t in closed_trades[-10:]:
                recent_trades.append({
                    "type": t.get('type'),
                    "entry_price": t.get('entry_price', 0) or 0,
                    "exit_price": t.get('exit_price', 0) or 0,
                    "profit_dollars": t.get('profit_dollars', 0) or 0,
                    "exit_reason": t.get('exit_reason', '')
                })
            
            new_profile = self.ai_core.update_market_profile(asset_type, recent_trades)
            if new_profile:
                profile = load_market_profile()
                profile[asset_type] = new_profile
                profile['last_updated'] = datetime.now().isoformat()
                save_market_profile(profile)
                logger.info(f"📊 تم تحديث شخصية السوق لـ {asset_type}")
        except Exception as e:
            logger.error(f"❌ فشل تحديث شخصية السوق: {e}")
           
# ====================================================================================
# 📦 PART 07: نظام التحذير والمراقبة (المعدل بالكامل)
# ====================================================================================

def safe_price(value, default="N/A"):
    """تحويل القيمة إلى نص منسق برقمين عشريين، مع التعامل مع None"""
    if value is None:
        return default
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return default

def monitor_loop(trading_core: TradingCore):
    """حلقة المراقبة - تعمل كل 5 دقائق"""
    logger.info("🔄 [Monitor] بدأ التشغيل")
    while True:
        try:
            for asset_type in ["oil", "silver"]:
                open_trade = get_current_open_trade(asset_type)
                if not open_trade:
                    continue
                
                # جلب البيانات الحالية
                symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
                data = get_mexc_candles(symbol, "Min1", 10)
                if not data or not data.get("closes"):
                    continue
                
                current_price = data["closes"][-1]
                
                # ── التحقق من ضرب SL/TP (كود صلب) ──
                if check_sl_tp_hit(asset_type, current_price, open_trade, trading_core):
                    continue
                
                # ── تحليل الخطر عبر AI ──
                current_data = {
                    "price": current_price,
                    "closes": data["closes"],
                    "highs": data["highs"],
                    "lows": data["lows"],
                    "volumes": data["volumes"]
                }
                alert = trading_core.ai_core.generate_alert(asset_type, open_trade, current_data)
                
                # تسجيل التحذير في الصفقة
                if alert["level"] >= 2:
                    if "warnings_log" not in open_trade:
                        open_trade["warnings_log"] = []
                    open_trade["warnings_log"].append({
                        "level": alert["level"],
                        "message": alert["message"],
                        "timestamp": datetime.now().isoformat()
                    })
                    save_current_trade(asset_type, open_trade)
                
                # ── معالجة التحذير ──
                if alert["level"] == 3:
                    # إغلاق تلقائي (المستوى 3)
                    msg = f"🚨 **تحذير المستوى 3 - {asset_type}**\n"
                    msg += f"{alert['message']}\n"
                    msg += f"💰 السعر الحالي: ${safe_price(current_price)}\n"
                    msg += "⚠️ سيتم إغلاق الصفقة تلقائياً."
                    queue_telegram_message(msg)
                    trading_core.close_trade(asset_type, f"تحذير مستوى 3: {alert['message'][:50]}", current_price)
                
                elif alert["level"] == 2:
                    # تحذير فقط
                    msg = f"⚠️ **تحذير المستوى 2 - {asset_type}**\n"
                    msg += f"{alert['message']}\n"
                    msg += f"💰 السعر الحالي: ${safe_price(current_price)}"
                    queue_telegram_message(msg)
                
                # elif level == 1: لا تفعل شيئاً
            
            time.sleep(5)  # نوم قصير بين الأصول
            
        except Exception as e:
            logger.error(f"❌ [Monitor] خطأ: {e}")
            time.sleep(10)

def check_sl_tp_hit(asset_type: str, current_price: float, open_trade: Dict, trading_core: TradingCore) -> bool:
    """التحقق من ضرب SL/TP (كود صلب - بدون تغيير)"""
    trade_type = open_trade.get('type', 'BUY')
    sl = open_trade.get('sl')
    tp = open_trade.get('tp')
    
    if trade_type == "BUY":
        if sl is not None and current_price <= sl:
            trading_core.close_trade(asset_type, "Hit Stop Loss", current_price)
            return True
        if tp is not None and current_price >= tp:
            trading_core.close_trade(asset_type, "Hit Take Profit", current_price)
            return True
    else:  # SELL
        if sl is not None and current_price >= sl:
            trading_core.close_trade(asset_type, "Hit Stop Loss", current_price)
            return True
        if tp is not None and current_price <= tp:
            trading_core.close_trade(asset_type, "Hit Take Profit", current_price)
            return True
    return False
   
# ====================================================================================
# 📦 PART 08: بوابة المستخدم (Flask + Telegram)
# ====================================================================================

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🚀 Tona AI V2.0 - البوت الاستشاري الذكي", 200

@app.route('/ping')
def ping():
    return "Bot is alive!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if not update or 'message' not in update:
            return 'OK', 200
        
        message = update['message']
        text = message.get('text', '').strip()
        chat_id = str(message['from']['id'])
        
        if text:
            handle_message(text, chat_id)
        return 'OK', 200
    except Exception as e:
        logger.error(f"❌ Webhook خطأ: {e}")
        return 'OK', 200

# ====================================================================================
# دوال Telegram
# ====================================================================================

def queue_telegram_message(text: str, chat_id: str = None):
    """إضافة رسالة إلى طابور الإرسال"""
    if not text or text.strip() == "":
        return False
    target = chat_id or CHAT_ID
    if not target:
        logger.error("❌ لا يوجد chat_id")
        return False
    TELEGRAM_QUEUE.put({"text": text, "chat_id": target})
    return True

def _send_telegram_message(text: str, chat_id: str):
    """إرسال رسالة عبر Telegram"""
    if not TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=10)
        if resp.status_code != 200:
            logger.warning(f"⚠️ فشل إرسال: {resp.status_code}")
    except Exception as e:
        logger.error(f"❌ خطأ في الإرسال: {e}")

def telegram_sender():
    """خيط إرسال الرسائل"""
    logger.info("📨 [Sender] بدأ التشغيل")
    while True:
        try:
            msg = TELEGRAM_QUEUE.get(timeout=1)
            _send_telegram_message(msg["text"], msg["chat_id"])
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"❌ [Sender] خطأ: {e}")

# ====================================================================================
# معالجة الأوامر والأزرار
# ====================================================================================

def send_main_menu(chat_id: str):
    """إرسال القائمة الرئيسية"""
    keyboard = [
        ["🛢️ تحليل النفط", "🥈 تحليل الفضة"],
        ["🔍 وضع الصفقة الحالية", "📊 تقرير الأداء"],
        ["📌 فتح صفقة يدوياً", "🧠 تقرير التعلم العميق"],
        ["📰 تقرير استخباراتي", "❌ إغلاق الصفقة"]
    ]
    
    # إضافة أزرار إغلاق منفصلة إن وجدت صفقات مفتوحة
    oil_open = get_current_open_trade("oil")
    silver_open = get_current_open_trade("silver")
    if oil_open or silver_open:
        close_row = []
        if oil_open:
            close_row.append("❌ إغلاق النفط")
        if silver_open:
            close_row.append("❌ إغلاق الفضة")
        if close_row:
            keyboard.append(close_row)
    
    reply_markup = {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": False}
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": """🚀 **Tona AI V2.0** - المستشار الذكي

💙 أنا هنا لمساعدتك في تحليل النفط والفضة.

📌 **الأزرار:**
• تحليل النفط/الفضة - تحليل شامل مع توصية
• وضع الصفقة الحالية - متابعة الصفقات المفتوحة
• فتح صفقة يدوياً - افتح صفقة بنفسك
• تقرير الأداء - إحصائيات الصفقات
• تقرير التعلم العميق - الدروس المستفادة
• تقرير استخباراتي - تحليل متقدم للسوق
• إغلاق الصفقة - إغلاق يدوي

🧠 نظام التعلم العميق يعمل في الخلفية.
💙 Tona AI: أنا هنا لخدمتك!""",
            "reply_markup": reply_markup,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception as e:
        logger.error(f"❌ فشل إرسال القائمة: {e}")

def handle_message(text: str, chat_id: str):
    """معالجة الرسائل الواردة"""
    clean_text = text.strip()
    logger.info(f"📩 رسالة من {chat_id}: {clean_text[:50]}...")
    
    # ── أوامر البداية ──
    if clean_text in ["/start", "قائمة", "منيو", "/menu"]:
        send_main_menu(chat_id)
        return
    
    # ── تحليل النفط ──
    if clean_text in ["🛢️ تحليل النفط", "نفط", "oil"]:
        queue_telegram_message("🔍 جاري التحليل الشامل للنفط...", chat_id)
        threading.Thread(target=handle_analysis, args=("oil", chat_id), daemon=True).start()
        return
    
    # ── تحليل الفضة ──
    if clean_text in ["🥈 تحليل الفضة", "فضة", "silver"]:
        queue_telegram_message("🔍 جاري التحليل الشامل للفضة...", chat_id)
        threading.Thread(target=handle_analysis, args=("silver", chat_id), daemon=True).start()
        return
    
    # ── وضع الصفقة الحالية ──
    if clean_text in ["🔍 وضع الصفقة الحالية", "وضع الصفقة", "حالة"]:
        threading.Thread(target=handle_position_status, args=(chat_id,), daemon=True).start()
        return
    
    # ── فتح صفقة يدوياً ──
    if clean_text in ["📌 فتح صفقة يدوياً", "فتح يدوي"]:
        threading.Thread(target=handle_manual_open, args=(chat_id,), daemon=True).start()
        return
    
    # ── تقرير الأداء ──
    if clean_text in ["📊 تقرير الأداء", "إحصائيات"]:
        threading.Thread(target=handle_performance_report, args=(chat_id,), daemon=True).start()
        return
    
    # ── تقرير التعلم العميق ──
    if clean_text in ["🧠 تقرير التعلم العميق", "تقرير التعلم"]:
        threading.Thread(target=handle_learning_report, args=(chat_id,), daemon=True).start()
        return
    
    # ── تقرير استخباراتي ──
    if clean_text in ["📰 تقرير استخباراتي", "استخبارات"]:
        threading.Thread(target=handle_intelligence_report, args=(chat_id,), daemon=True).start()
        return
    
    # ── إغلاق الصفقة ──
    if clean_text in ["❌ إغلاق النفط", "أغلق النفط"]:
        close_trade_manual("oil", chat_id)
        return
    if clean_text in ["❌ إغلاق الفضة", "أغلق الفضة"]:
        close_trade_manual("silver", chat_id)
        return
    if clean_text in ["❌ إغلاق الصفقة", "إغلاق"]:
        close_trade_manual(None, chat_id)
        return
    
    # ── أوامر نصية ──
    if clean_text.startswith("فتح صفقة"):
        # مثال: "فتح صفقة نفط شراء 85.50"
        threading.Thread(target=handle_manual_open_command, args=(clean_text, chat_id), daemon=True).start()
        return

# ====================================================================================
# دوال معالجة الأزرار والأوامر
# ====================================================================================

def handle_analysis(asset_type: str, chat_id: str):
    """معالجة طلب التحليل الشامل"""
    try:
        # جلب البيانات
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        data = get_mexc_candles(symbol, "Min15", 200)
        if not data:
            queue_telegram_message(f"⚠️ تعذر جلب بيانات {asset_type}", chat_id)
            return
        
        # الحصول على الصفقة المفتوحة
        open_trade = get_current_open_trade(asset_type)
        
        # طلب التحليل من AI Core
        analysis = AI_CORE.analyze_market(asset_type, data, open_trade)
        if analysis.get("error"):
            queue_telegram_message(f"⚠️ {analysis['error']}", chat_id)
            return
        
        # بناء الرسالة
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        price = data["closes"][-1]
        
        msg = f"📊 **تحليل {asset_label}**\n"
        msg += "━" * 30 + "\n"
        msg += f"💰 السعر الحالي: ${price:.2f}\n"
        msg += f"📈 التقييم: {analysis.get('evaluation', 'متوسط')}\n"
        msg += f"📊 الدرجة: {analysis.get('score', 50)}/100\n"
        msg += f"⚠️ مستوى الخطر: {analysis.get('risk_level', 1)}/3\n\n"
        
        msg += "📋 **الأسباب:**\n"
        for reason in analysis.get('reasons', ['لا توجد أسباب']):
            msg += f"   • {reason}\n"
        
        msg += f"\n💡 **نصيحة Tona AI:**\n{analysis.get('advice', 'لا توجد نصيحة')}\n"
        
        if open_trade:
            entry = open_trade.get('entry_price', 0)
            trade_type = open_trade.get('type', 'BUY')
            profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" else ((entry - price) / entry * 100)
            msg += f"\n📈 **الصفقة المفتوحة:** {trade_type} @ ${entry:.2f} | {profit_pct:+.2f}%"
        
        msg += "\n\n💙 Tona AI: أنا هنا لمساعدتك!"
        queue_telegram_message(msg, chat_id)
        
    except Exception as e:
        logger.error(f"❌ فشل تحليل {asset_type}: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ أثناء التحليل: {str(e)[:100]}", chat_id)

def handle_position_status(chat_id: str):
    """عرض وضع الصفقات المفتوحة"""
    msg = "📊 **وضع الصفقات الحالية**\n"
    msg += "━" * 30 + "\n\n"
    
    has_trade = False
    for asset_type in ["oil", "silver"]:
        trade = get_current_open_trade(asset_type)
        if not trade:
            msg += f"{'🛢️' if asset_type == 'oil' else '🥈'} **{asset_type}**: لا توجد صفقة مفتوحة\n\n"
            continue
        
        has_trade = True
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        entry = trade.get('entry_price', 0)
        trade_type = trade.get('type', 'BUY')
        sl = trade.get('sl', 0)
        tp = trade.get('tp', 0)
        
        # جلب السعر الحالي
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        data = get_mexc_candles(symbol, "Min1", 5)
        current_price = data["closes"][-1] if data and data.get("closes") else entry
        
        profit_pct = ((current_price - entry) / entry * 100) if trade_type == "BUY" else ((entry - current_price) / entry * 100)
        profit_dollars = AccountingSystem.calculate_profit_dollars(entry, current_price, trade_type)
        
        msg += f"🛢️ **{asset_label}**\n"
        msg += f"   • النوع: {trade_type}\n"
        msg += f"   • الدخول: ${entry:.2f}\n"
        msg += f"   • الحالي: ${current_price:.2f}\n"
        msg += f"   • الربح/خسارة: {profit_pct:+.2f}% (${profit_dollars:+.2f})\n"
        msg += f"   • وقف الخسارة: ${sl:.2f}\n"
        msg += f"   • الهدف: ${tp:.2f}\n"
        msg += f"   • RR: {trade.get('rr', 0):.2f}\n"
        msg += f"   • المصدر: {'يدوي' if trade.get('source') == 'manual' else 'تلقائي'}\n\n"
    
    if not has_trade:
        msg += "🔄 لا توجد صفقات مفتوحة حالياً.\n"
        msg += "💡 يمكنك فتح صفقة يدوياً عبر زر '📌 فتح صفقة يدوياً'"
    
    queue_telegram_message(msg, chat_id)

def handle_manual_open(chat_id: str):
    """فتح صفقة يدوياً - إرشادات"""
    msg = """📌 **فتح صفقة يدوياً**

يرجى إرسال الأمر بالصيغة التالية:
`فتح صفقة [نفط/فضة] [شراء/بيع] [السعر]`

مثال:
`فتح صفقة نفط شراء 85.50`
`فتح صفقة فضة بيع 32.40`

📌 سيتم حساب وقف الخسارة والهدف تلقائياً باستخدام ATR.
💙 Tona AI: أنا هنا لمساعدتك!"""
    queue_telegram_message(msg, chat_id)

def handle_manual_open_command(text: str, chat_id: str):
    """معالجة أمر فتح صفقة يدوياً"""
    try:
        # تحليل الأمر: "فتح صفقة نفط شراء 85.50"
        parts = text.split()
        if len(parts) < 4:
            queue_telegram_message("⚠️ الصيغة غير صحيحة. استخدم: `فتح صفقة [نفط/فضة] [شراء/بيع] [السعر]`", chat_id)
            return
        
        # استخراج البيانات
        asset_str = parts[2]  # نفط أو فضة
        type_str = parts[3]   # شراء أو بيع
        try:
            price = float(parts[4]) if len(parts) > 4 else 0
        except:
            price = 0
        
        if asset_str not in ["نفط", "فضة"]:
            queue_telegram_message("⚠️ الأصل غير معروف. استخدم 'نفط' أو 'فضة'", chat_id)
            return
        
        if type_str not in ["شراء", "بيع"]:
            queue_telegram_message("⚠️ النوع غير معروف. استخدم 'شراء' أو 'بيع'", chat_id)
            return
        
        if price <= 0:
            queue_telegram_message("⚠️ السعر يجب أن يكون أكبر من 0", chat_id)
            return
        
        asset_type = "oil" if asset_str == "نفط" else "silver"
        signal = "BUY" if type_str == "شراء" else "SELL"
        
        # حساب SL/TP باستخدام ATR
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        data = get_mexc_candles(symbol, "Min15", 100)
        atr = calculate_atr_14(data) if data else None
        
        if atr and atr > 0:
            sl_mult = 2.0
            tp_mult = 3.0
            if signal == "BUY":
                sl = price - (atr * sl_mult)
                tp = price + (atr * tp_mult)
            else:
                sl = price + (atr * sl_mult)
                tp = price - (atr * tp_mult)
            rr = tp_mult / sl_mult
        else:
            sl = price * 0.98 if signal == "BUY" else price * 1.02
            tp = price * 1.03 if signal == "BUY" else price * 0.97
            rr = 1.5
        
        signal_data = {
            "signal": signal,
            "price": price,
            "sl": sl,
            "tp": tp,
            "rr": rr
        }
        
        # فتح الصفقة
        success = TRADING_CORE.open_trade(asset_type, signal_data, source="manual")
        if success:
            queue_telegram_message(f"✅ تم فتح صفقة {asset_str} يدوياً ({type_str}) عند ${price:.2f}", chat_id)
        else:
            queue_telegram_message(f"⚠️ فشل فتح صفقة {asset_str}. تأكد من عدم وجود صفقة مفتوحة.", chat_id)
            
    except Exception as e:
        logger.error(f"❌ فشل فتح يدوي: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)

def handle_performance_report(chat_id: str):
    """تقرير الأداء"""
    try:
        msg = "📊 **تقرير الأداء الشامل**\n"
        msg += "━" * 30 + "\n\n"
        
        total_trades = 0
        total_wins = 0
        total_losses = 0
        total_profit = 0.0
        
        for asset_type in ["oil", "silver"]:
            history = load_trades_history(asset_type)
            trades = history.get('trades', [])
            closed = [t for t in trades if t.get('status') == 'closed']
            
            if not closed:
                msg += f"{'🛢️' if asset_type == 'oil' else '🥈'} **{asset_type}**: لا توجد صفقات مغلقة\n\n"
                continue
            
            wins = [t for t in closed if t.get('profit_dollars', 0) > 0]
            losses = [t for t in closed if t.get('profit_dollars', 0) <= 0]
            profit = sum(t.get('profit_dollars', 0) for t in closed)
            win_rate = len(wins) / len(closed) * 100 if closed else 0
            
            msg += f"{'🛢️' if asset_type == 'oil' else '🥈'} **{asset_type}**\n"
            msg += f"   • إجمالي الصفقات: {len(closed)}\n"
            msg += f"   • رابحة: {len(wins)} | خاسرة: {len(losses)}\n"
            msg += f"   • نسبة النجاح: {win_rate:.1f}%\n"
            msg += f"   • إجمالي الربح: ${profit:.2f}\n\n"
            
            total_trades += len(closed)
            total_wins += len(wins)
            total_losses += len(losses)
            total_profit += profit
        
        # الإجمالي
        if total_trades > 0:
            total_win_rate = total_wins / total_trades * 100
            msg += "━" * 30 + "\n"
            msg += f"📊 **الإجمالي**\n"
            msg += f"   • إجمالي الصفقات: {total_trades}\n"
            msg += f"   • نسبة النجاح الكلية: {total_win_rate:.1f}%\n"
            msg += f"   • إجمالي الربح: ${total_profit:.2f}\n"
        
        queue_telegram_message(msg, chat_id)
        
    except Exception as e:
        logger.error(f"❌ فشل تقرير الأداء: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)

def handle_learning_report(chat_id: str):
    """تقرير التعلم العميق"""
    try:
        lessons = load_deep_lessons()
        scenarios = load_scenarios()
        profile = load_market_profile()
        
        msg = "🧠 **تقرير التعلم العميق**\n"
        msg += "━" * 30 + "\n\n"
        
        # شخصية السوق
        msg += "📊 **شخصية السوق الحالية:**\n"
        msg += f"🛢️ النفط: {profile.get('oil', 'لا توجد بيانات')[:200]}\n\n"
        msg += f"🥈 الفضة: {profile.get('silver', 'لا توجد بيانات')[:200]}\n\n"
        msg += f"📅 آخر تحديث: {profile.get('last_updated', 'غير معروف')}\n\n"
        
        # الدروس العميقة
        msg += "📚 **الدروس المستفادة:**\n"
        if lessons:
            for i, lesson in enumerate(lessons[-10:], 1):
                msg += f"   {i}. {lesson[:100]}\n"
        else:
            msg += "   ℹ️ لا توجد دروس مسجلة بعد\n"
        msg += "\n"
        
        # السيناريوهات
        msg += "📋 **السيناريوهات المسجلة:**\n"
        if scenarios:
            for s in scenarios[-5:]:
                msg += f"   • {s.get('condition', '')[:50]}... ({s.get('occurrences', 0)} تكرار)\n"
        else:
            msg += "   ℹ️ لا توجد سيناريوهات مسجلة بعد\n"
        
        msg += "\n💙 Tona AI: التعلم مستمر... كل صفقة تضيف خبرة جديدة."
        queue_telegram_message(msg, chat_id)
        
    except Exception as e:
        logger.error(f"❌ فشل تقرير التعلم: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)

def handle_intelligence_report(chat_id: str):
    """تقرير استخباراتي"""
    try:
        queue_telegram_message("📰 جاري توليد التقرير الاستخباراتي...", chat_id)
        
        # تجميع البيانات
        oil_history = load_trades_history("oil")
        silver_history = load_trades_history("silver")
        all_trades = oil_history.get('trades', []) + silver_history.get('trades', [])
        closed_trades = [t for t in all_trades if t.get('status') == 'closed']
        
        if len(closed_trades) < 3:
            queue_telegram_message("⚠️ لا توجد بيانات كافية لتوليد تقرير استخباراتي (يحتاج 3 صفقات على الأقل)", chat_id)
            return
        
        profile = load_market_profile()
        market_context = f"النفط: {profile.get('oil', '')}\nالفضة: {profile.get('silver', '')}"
        
        # توليد التقرير
        report = AI_CORE.generate_intelligence_report("النفط والفضة", closed_trades, market_context)
        queue_telegram_message(f"📰 **تقرير استخباراتي**\n\n{report}", chat_id)
        
    except Exception as e:
        logger.error(f"❌ فشل التقرير الاستخباراتي: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)

def close_trade_manual(asset_type: Optional[str], chat_id: str):
    """إغلاق صفقة يدوياً"""
    if asset_type:
        # إغلاق أصل محدد
        open_trade = get_current_open_trade(asset_type)
        if not open_trade:
            queue_telegram_message(f"⚠️ لا توجد صفقة {asset_type} مفتوحة", chat_id)
            return
        TRADING_CORE.close_trade(asset_type, "أمر يدوي من المستخدم")
        queue_telegram_message(f"✅ تم إغلاق صفقة {asset_type} يدوياً", chat_id)
    else:
        # إغلاق أي صفقة مفتوحة
        oil_trade = get_current_open_trade("oil")
        silver_trade = get_current_open_trade("silver")
        
        if not oil_trade and not silver_trade:
            queue_telegram_message("⚠️ لا توجد صفقات مفتوحة للإغلاق", chat_id)
            return
        
        if oil_trade and silver_trade:
            queue_telegram_message("⚠️ توجد صفقتان مفتوحتان. استخدم:\n• `أغلق النفط`\n• `أغلق الفضة`", chat_id)
            return
        
        if oil_trade:
            TRADING_CORE.close_trade("oil", "أمر يدوي من المستخدم")
            queue_telegram_message("✅ تم إغلاق صفقة النفط يدوياً", chat_id)
        else:
            TRADING_CORE.close_trade("silver", "أمر يدوي من المستخدم")
            queue_telegram_message("✅ تم إغلاق صفقة الفضة يدوياً", chat_id)

# ====================================================================================
# 📦 PART 09: ماسح الإشارات (Scanner)
# ====================================================================================

def signal_scanner(trading_core: TradingCore):
    """ماسح الإشارات - يعمل كل 60 ثانية"""
    logger.info("📡 [Scanner] بدأ التشغيل")
    last_signal_time = {"oil": 0, "silver": 0}
    
    while True:
        try:
            for asset_type in ["oil", "silver"]:
                # منع التكرار السريع
                if time.time() - last_signal_time[asset_type] < SIGNAL_CHECK_INTERVAL:
                    continue
                
                # توليد إشارة خام
                signal_data = generate_raw_signal(asset_type)
                if signal_data['signal'] == 'WAIT':
                    continue
                
                # التحقق من وجود صفقة مفتوحة (إذا كانت معاكسة، نغلقها)
                open_trade = get_current_open_trade(asset_type)
                if open_trade:
                    trade_type = open_trade.get('type', 'BUY')
                    if signal_data['signal'] == trade_type:
                        # نفس الاتجاه - ننتظر
                        continue
                    else:
                        # إشارة معاكسة - نغلق الصفقة الحالية
                        logger.info(f"🔄 [Scanner] إشارة معاكسة لـ {asset_type}، إغلاق الصفقة الحالية")
                        trading_core.close_trade(asset_type, f"إشارة معاكسة - عكس الصفقة ({signal_data['signal']})")
                        # نستمر لفتح الصفقة الجديدة
                
                # فتح الصفقة الجديدة
                logger.info(f"📡 [Scanner] إشارة {signal_data['signal']} لـ {asset_type} عند ${signal_data['price']:.2f}")
                trading_core.open_trade(asset_type, signal_data, source="auto")
                last_signal_time[asset_type] = time.time()
                
            time.sleep(1)
        except Exception as e:
            logger.error(f"❌ [Scanner] خطأ: {e}")
            time.sleep(5)

# ====================================================================================
# 📦 PART 10: التشغيل الرئيسي
# ====================================================================================

def run_flask():
    """تشغيل خادم Flask"""
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)

def set_webhook() -> bool:
    """تسجيل Webhook في Telegram"""
    if not TELEGRAM_TOKEN:
        return False
    render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if not render_url:
        service_name = os.environ.get('RENDER_SERVICE_NAME', '')
        render_url = f"https://{service_name}.onrender.com" if service_name else os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
        if render_url:
            render_url = f"https://{render_url}"
    if not render_url:
        return False
    webhook_url = f"{render_url}/webhook"
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        resp = requests.post(url, json={"url": webhook_url, "allowed_updates": ["message"]}, timeout=10)
        return resp.status_code == 200 and resp.json().get('ok', False)
    except:
        return False

def cleanup_stuck_trades(trading_core: TradingCore):
    """تنظيف الصفقات العالقة (أكثر من يومين)"""
    logger.info("🧹 بدء تنظيف الصفقات العالقة...")
    for asset_type in ["oil", "silver"]:
        open_trade = get_current_open_trade(asset_type)
        if not open_trade:
            continue
        entry_time = open_trade.get('timestamp', '')
        if entry_time:
            try:
                entry_dt = datetime.fromisoformat(entry_time)
                if (datetime.now() - entry_dt).days >= 2:
                    logger.info(f"🗑️ إغلاق صفقة عالقة لـ {asset_type} (أكثر من يومين)")
                    trading_core.close_trade(asset_type, "إغلاق تلقائي (عالقة > 2 يوم)")
            except:
                pass

# ── التحقق من وجود الدوال المساعدة ──
def calculate_adx_14(data):
    """حساب ADX (14) - دالة مساعدة"""
    # نسخة مبسطة للاستخدام في المؤشرات
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    if not closes or not highs or not lows or len(closes) < 20:
        return 20
    # حساب ADX مبسط (نرجع قيمة تقديرية)
    return 25  # قيمة افتراضية

# ── تهيئة المكونات العالمية ──
AI_CORE = AICore()
TRADING_CORE = TradingCore(AI_CORE)

# ── بدء التشغيل ──
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 Tona AI V2.0 - البوت الاستشاري الذكي")
    logger.info("💙 الاسم: Tona AI")
    logger.info("👨‍💻 المطور: بسام الحوباني")
    logger.info("🧠 جميع التحليلات والتوصيات تعتمد على Gemini + Groq")
    logger.info("=" * 60)
    
    # تنظيف الصفقات العالقة
    cleanup_stuck_trades(TRADING_CORE)
    
    # تسجيل Webhook
    if set_webhook():
        logger.info("✅ Webhook مسجل بنجاح")
    else:
        logger.warning("⚠️ فشل تسجيل Webhook")
    
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 خادم Flask يعمل")
    
    # تشغيل الخيوط
    threads = [
        threading.Thread(target=signal_scanner, args=(TRADING_CORE,), name="Scanner", daemon=True),
        threading.Thread(target=monitor_loop, args=(TRADING_CORE,), name="Monitor", daemon=True),
        threading.Thread(target=telegram_sender, name="Sender", daemon=True),
    ]
    
    for t in threads:
        t.start()
        logger.info(f"✅ Thread {t.name} بدأ")
    
    logger.info("✅ جميع الخيوط تعمل - Tona AI جاهز!")
    logger.info("💙 Tona AI: أنا هنا لمساعدتك في تحليل النفط والفضة!")
    
    # الحلقة الرئيسية
    while True:
        time.sleep(1)
