"""
═══════════════════════════════════════════════════════════════════════════════════
🚀 Tona AI V2.0 FINAL - البوت الاستشاري الذكي (نسخة Render)
💙 الاسم: Tona AI
👨‍💻 المطور: بسام الحوباني
📡 النظام: بوت تداول استشاري متخصص في النفط والفضة (تعلم عميق طويل المدى)
🧠 جميع التحليلات والتوصيات والتحذيرات والدروس تعتمد على Gemini + Groq
📌 تم إصلاح جميع الأخطاء وإزالة نظام المحادثة الذكي والاحتفاظ بالأزرار
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

# ── أسماء جداول Supabase (إذا توفرت) ──
TABLE_TRADES_FULL = "trades_full"
TABLE_LESSONS_DEEP = "lessons_deep"
TABLE_SNAPSHOTS = "snapshots"

# ── ملفات التعلم العميق (محلية) ──
SCENARIOS_FILE = "learning_data/scenarios.json"
MARKET_PROFILE_FILE = "learning_data/market_profile.json"
DEEP_LESSONS_FILE = "learning_data/deep_lessons.json"
SNAPSHOTS_FILE = "learning_data/snapshots.json"

# ── تأكد من وجود مجلدات ──
os.makedirs("learning_data", exist_ok=True)
os.makedirs("learning_data/backups", exist_ok=True)

# ====================================================================================
# 📦 PART 02: طبقة البيانات والمؤشرات (من البوت الأصلي V13.0)
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


def stdev_pop(src, length):
    """الانحراف المعياري للسكان"""
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


def rma(data, period):
    """RMA (Wilder's MA)"""
    if not data or len(data) < period:
        return None
    alpha = 1.0 / period
    res = [sum(data[:period]) / period]
    for x in data[period:]:
        res.append(alpha * x + (1 - alpha) * res[-1])
    return res


def calculate_rsi_7(src, length=7):
    """حساب RSI باستخدام RMA"""
    if not src or len(src) < length:
        return None
    deltas = [src[i] - src[i-1] for i in range(1, len(src))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
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


def ema(data, period):
    """EMA"""
    if not data or len(data) < period:
        return None
    alpha = 2.0 / (period + 1)
    res = [data[0]]
    for x in data[1:]:
        res.append(alpha * x + (1 - alpha) * res[-1])
    return res


def calculate_macd_full(src):
    """MACD (12,26,9)"""
    if not src or len(src) < 35:
        return None, None, None
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
    """ATR باستخدام RMA (14)"""
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
    atr_series = rma(tr, 14)
    if atr_series is None:
        return None
    return atr_series[-1]


def calculate_atr_series(data, period=14):
    """سلسلة ATR كاملة"""
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    if not highs or not lows or not closes or len(closes) < period:
        return None
    n = len(closes)
    tr = [0.0] * n
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
    return rma(tr, period)


def calculate_adx_14(data):
    """ADX باستخدام RMA"""
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    if not closes or not highs or not lows or len(closes) < 20:
        return None
    n = len(closes)
    tr = [0.0] * n
    plus_dm = [0.0] * n
    minus_dm = [0.0] * n
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        up = highs[i] - highs[i-1]
        down = lows[i-1] - lows[i]
        plus_dm[i] = up if up > down and up > 0 else 0.0
        minus_dm[i] = down if down > up and down > 0 else 0.0
    tr_smooth = rma(tr, 14)
    plus_smooth = rma(plus_dm, 14)
    minus_smooth = rma(minus_dm, 14)
    if tr_smooth is None or plus_smooth is None or minus_smooth is None:
        return None
    min_len = min(len(tr_smooth), len(plus_smooth), len(minus_smooth))
    tr_smooth = tr_smooth[:min_len]
    plus_smooth = plus_smooth[:min_len]
    minus_smooth = minus_smooth[:min_len]
    plus_di = [100 * x / y if y != 0 else 0 for x, y in zip(plus_smooth, tr_smooth)]
    minus_di = [100 * x / y if y != 0 else 0 for x, y in zip(minus_smooth, tr_smooth)]
    dx = [100 * abs(p - m) / (p + m) if (p + m) != 0 else 0 for p, m in zip(plus_di, minus_di)]
    adx_result = rma(dx, 14)
    if adx_result is None:
        return None
    return adx_result[-1] if adx_result else None


def calculate_vpt_correct(closes, volumes):
    """VPT باستخدام السعر الحالي في المقام"""
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

    v = calculate_vpt_correct(closes, volumes)
    if v is None or len(v) != n:
        return None

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


def calculate_bollinger_bands(closes, length=20, mult=2):
    """Bollinger Bands"""
    if not closes or len(closes) < 2:
        return None, None, None
    if len(closes) < length:
        actual_len = len(closes)
        basis = [sum(closes) / actual_len] * actual_len
        dev = stdev_pop(closes, actual_len)
    else:
        basis = []
        for i in range(len(closes)):
            if i < length - 1:
                basis.append(sum(closes[:i+1]) / (i+1))
            else:
                basis.append(sum(closes[i-length+1:i+1]) / length)
        dev = stdev_pop(closes, length)
    if basis is None or dev is None:
        return None, None, None
    min_len = min(len(basis), len(dev))
    basis = basis[:min_len]
    dev = dev[:min_len]
    upper = [b + (mult * d) for b, d in zip(basis, dev)]
    lower = [b - (mult * d) for b, d in zip(basis, dev)]
    return upper, basis, lower


def calculate_stochastic(highs, lows, closes, length=14, smooth_k=3):
    """Stochastic"""
    if not closes or not highs or not lows or len(closes) < length + smooth_k:
        return None
    stoch_raw = []
    for i in range(len(closes)):
        if i < length - 1:
            stoch_raw.append(50.0)
            continue
        window_high = max(highs[i-length+1:i+1])
        window_low = min(lows[i-length+1:i+1])
        denom = window_high - window_low
        if denom != 0:
            stoch_raw.append(((closes[i] - window_low) / denom * 100))
        else:
            stoch_raw.append(50.0)
    smooth_values = []
    for i in range(len(stoch_raw)):
        if i < smooth_k - 1:
            smooth_values.append(50.0)
        else:
            smooth_values.append(sum(stoch_raw[i-smooth_k+1:i+1]) / smooth_k)
    return smooth_values


def calculate_vwap(data):
    """VWAP"""
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    volumes = data.get("volumes", [])
    if not closes or not highs or not lows or not volumes or len(closes) != len(volumes):
        return None
    vwap_values = []
    cum_pv = 0.0
    cum_vol = 0.0
    for i in range(len(closes)):
        typical = (highs[i] + lows[i] + closes[i]) / 3.0
        cum_pv += typical * volumes[i]
        cum_vol += volumes[i]
        if cum_vol != 0:
            vwap_values.append(cum_pv / cum_vol)
        else:
            vwap_values.append(closes[i])
    return vwap_values


def calculate_macd_histogram(src):
    """MACD Histogram فقط"""
    if not src or len(src) < 35:
        return None
    f = ema(src, 12)
    s = ema(src, 26)
    if f is None or s is None:
        return None
    min_len = min(len(f), len(s))
    f = f[:min_len]
    s = s[:min_len]
    macd = [f_i - s_i for f_i, s_i in zip(f, s)]
    sig = ema(macd, 9)
    if sig is None:
        return None
    min_len = min(len(macd), len(sig))
    macd = macd[:min_len]
    sig = sig[:min_len]
    return [m - si for m, si in zip(macd, sig)]


# ====================================================================================
# 📦 PART 03: استراتيجية الدخول (VPT + SuperTrend)
# ====================================================================================

def generate_raw_signal(asset_type: str) -> Dict:
    """توليد إشارة خام من VPT + SuperTrend"""
    symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
    data = get_mexc_candles(symbol, interval="Min15", limit=200)
    if not data or not data.get("closes") or len(data["closes"]) < 10:
        return {"signal": "WAIT", "price": 0, "sl": 0, "tp": 0, "rr": 0}

    closes = data["closes"]
    price = closes[-1]

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

    atr = calculate_atr_14(data)
    if signal != "WAIT" and atr is not None and atr > 0:
        sl_mult = 2.0
        tp_mult = 3.0
        sl_dist = atr * sl_mult
        tp_dist = atr * tp_mult
        if signal == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
        else:
            sl = price + sl_dist
            tp = price - tp_dist
        rr = tp_mult / sl_mult if sl_mult > 0 else 0
    else:
        sl = tp = 0
        rr = 0

    return {"signal": signal, "price": price, "sl": sl, "tp": tp, "rr": rr}


# ====================================================================================
# 📦 PART 04: حساب التقييم الشامل (Comprehensive Score) من البوت الأصلي
# ====================================================================================

def calculate_comprehensive_score(analysis: Dict, asset_type: str, open_trade: Optional[Dict] = None) -> Dict:
    """حساب التقييم الشامل - نسخة معدلة من PART 16"""
    if not analysis or not isinstance(analysis, dict):
        return {"score": 50, "grade": "محايد", "grade_emoji": "⚪", "details": [], "context": "neutral"}

    price = analysis.get('price', 0)
    if price <= 0:
        return {"score": 50, "grade": "محايد", "grade_emoji": "⚪", "details": [], "context": "neutral"}

    indicators = analysis.get('indicators', {})
    if not indicators:
        return {"score": 50, "grade": "محايد", "grade_emoji": "⚪", "details": [], "context": "neutral"}

    # استخراج البيانات مع تحقق
    trend_data = indicators.get('trend', {})
    bullish_count = trend_data.get('bullish_count', 0) or 0
    adx = trend_data.get('adx', 20) or 20

    momentum = indicators.get('momentum', {})
    rsi = momentum.get('rsi', 50) or 50
    macd_hist = momentum.get('macd_hist', 0) or 0
    stoch = momentum.get('stoch', 50) or 50

    volatility = indicators.get('volatility', {})
    bb_pos = volatility.get('bb_position', 0.5) or 0.5
    atr_pct = volatility.get('atr_percent', 1.0) or 1.0
    vwap_dev = volatility.get('vwap_deviation', 0) or 0

    volume = indicators.get('volume', {})
    vol_ratio = volume.get('ratio', 1.0) or 1.0

    sr = indicators.get('support_resistance', {})
    s1 = sr.get('s1', price * 0.98) or (price * 0.98)
    r1 = sr.get('r1', price * 1.02) or (price * 1.02)
    pivot = sr.get('pivot', price) or price

    sentiment = indicators.get('sentiment', {})
    fear_greed = sentiment.get('fear_greed', 50) or 50

    # حساب الدرجات الفرعية
    trend_score = 65 if bullish_count >= 2 and adx > 25 else 55 if bullish_count >= 2 else 45 if adx > 25 else 35
    if adx is None: adx = 20

    if rsi < 30:
        momentum_score = 70
    elif rsi > 70:
        momentum_score = 30
    elif 40 <= rsi <= 60 and abs(macd_hist) < 0.3:
        momentum_score = 50
    elif rsi < 40:
        momentum_score = 40
    else:
        momentum_score = 60

    volatility_score = 50
    if atr_pct > 2.5:
        volatility_score = 60
    elif atr_pct < 0.5:
        volatility_score = 40
    if bb_pos < 0.15:
        volatility_score = min(volatility_score + 10, 65)
    elif bb_pos > 0.85:
        volatility_score = max(volatility_score - 10, 35)

    volume_score = 65 if vol_ratio >= 1.5 else 55 if vol_ratio >= 1.0 else 45 if vol_ratio >= 0.6 else 35
    if vol_ratio is None: vol_ratio = 1.0

    sr_score = 65 if price <= s1 * 1.003 else 35 if price >= r1 * 0.997 else 50
    if price is None: price = 0

    sentiment_score = 75 if fear_greed <= 20 else 65 if fear_greed <= 35 else 50 if fear_greed <= 55 else 35 if fear_greed <= 75 else 25
    if fear_greed is None: fear_greed = 50

    divergence_score = 50  # بدون تباعد

    # أوزان
    weights = {
        'trend': 0.25,
        'momentum': 0.20,
        'volatility': 0.15,
        'volume': 0.15,
        'sr': 0.15,
        'sentiment': 0.05,
        'divergence': 0.05
    }
    total_weight = sum(weights.values())
    if total_weight != 1.0:
        weights = {k: v/total_weight for k, v in weights.items()}

    final_score = (
        trend_score * weights['trend'] +
        momentum_score * weights['momentum'] +
        volatility_score * weights['volatility'] +
        volume_score * weights['volume'] +
        sr_score * weights['sr'] +
        sentiment_score * weights['sentiment'] +
        divergence_score * weights['divergence']
    )
    final_score = round(final_score, 2)

    if final_score >= 70:
        grade = "إيجابي قوي"
        grade_emoji = "🟢"
        context = "bullish"
    elif final_score >= 60:
        grade = "إيجابي"
        grade_emoji = "🟡"
        context = "bullish"
    elif final_score >= 45:
        grade = "محايد"
        grade_emoji = "⚪"
        context = "neutral"
    elif final_score >= 35:
        grade = "سلبي"
        grade_emoji = "🟠"
        context = "bearish"
    else:
        grade = "سلبي قوي"
        grade_emoji = "🔴"
        context = "bearish"

    details = [
        f"📈 الاتجاه: درجة {trend_score:.0f}",
        f"⚡ الزخم: درجة {momentum_score:.0f}",
        f"🌊 التقلب: درجة {volatility_score:.0f}",
        f"📊 الحجم: درجة {volume_score:.0f}",
        f"🛡️ الدعم/المقاومة: درجة {sr_score:.0f}",
        f"🧠 المشاعر: درجة {sentiment_score:.0f}"
    ]

    if open_trade:
        trade_type = open_trade.get('type', 'unknown')
        entry_price = open_trade.get('entry_price', 0)
        if entry_price > 0:
            pnl = ((price - entry_price) / entry_price * 100) if trade_type == 'BUY' else ((entry_price - price) / entry_price * 100)
            details.append(f"💼 الصفقة المفتوحة: {trade_type} | {pnl:+.2f}%")

    return {
        "score": final_score,
        "grade": grade,
        "grade_emoji": grade_emoji,
        "details": details,
        "context": context,
        "metrics": {
            "price": price,
            "rsi": rsi,
            "adx": adx,
            "vol_ratio": vol_ratio,
            "fear_greed": fear_greed,
            "bullish_count": bullish_count,
            "support": s1,
            "resistance": r1,
            "atr_percent": atr_pct,
            "bb_position": bb_pos
        }
    }


# ====================================================================================
# 📦 PART 05: نواة الذكاء الاصطناعي (AICore) - مع احتياطي قوي
# ====================================================================================

class AICore:
    """المحرك الذكي للبوت - مع منطق احتياطي قوي"""

    def __init__(self):
        self.gemini_model = None
        self.groq_model = "openai/gpt-oss-120b"

        if GEMINI_AVAILABLE and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-3.5-flash')
                logger.info("✅ Gemini 3.5 Flash جاهز")
            except Exception as e:
                logger.error(f"❌ فشل تهيئة Gemini: {e}")
        else:
            logger.warning("⚠️ Gemini غير متوفر")

        if GROQ_API_KEY:
            logger.info("✅ Groq API جاهز")
        else:
            logger.warning("⚠️ Groq API غير متوفر")

    def _call_gemini(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        if not self.gemini_model:
            return None
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens, "temperature": 0.3}
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.error(f"❌ Gemini فشل: {e}")
        return None

    def _call_groq(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        if not GROQ_API_KEY:
            return None
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.groq_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                if content:
                    return content.strip()
        except Exception as e:
            logger.error(f"❌ Groq فشل: {e}")
        return None

    def _call_model(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        response = self._call_gemini(prompt, max_tokens)
        if response:
            return response
        response = self._call_groq(prompt, max_tokens)
        if response:
            return response
        return None

    def analyze_market(self, asset: str, data: Dict, open_trade: Optional[Dict] = None) -> Dict:
        """تحليل شامل للسوق باستخدام AI + احتياطي رياضي"""
        closes = data.get("closes", [])
        if not closes:
            return {"error": "لا توجد بيانات"}

        price = closes[-1]

        # حساب المؤشرات الرياضية
        rsi_values = calculate_rsi_7(closes)
        rsi = rsi_values[-1] if rsi_values else 50

        macd_line, sig_line, hist = calculate_macd_full(closes)
        macd = hist[-1] if hist else 0

        adx = calculate_adx_14(data) or 20

        # تحليل الفريمات
        timeframes = {}
        for tf, interval in [("5m", "Min5"), ("15m", "Min15"), ("1h", "Min60"), ("4h", "Hour4")]:
            tf_data = get_mexc_candles("USOIL_USDT" if asset == "oil" else "SILVER_USDT", interval, 100)
            if tf_data and tf_data.get("closes"):
                st_result = calculate_supertrend_vpt_correct(tf_data, st_mult=2.5 if asset == "oil" else 2.2)
                if st_result:
                    _, trend, _ = st_result
                    timeframes[tf] = "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد"
                else:
                    tf_closes = tf_data["closes"]
                    if len(tf_closes) >= 20:
                        sma_short = sum(tf_closes[-5:]) / 5
                        sma_long = sum(tf_closes[-20:]) / 20
                        if sma_short > sma_long * 1.003:
                            timeframes[tf] = "صاعد"
                        elif sma_short < sma_long * 0.997:
                            timeframes[tf] = "هابط"
                        else:
                            timeframes[tf] = "محايد"
                    else:
                        timeframes[tf] = "محايد"
            else:
                timeframes[tf] = "محايد"

        bullish_count = sum(1 for t in timeframes.values() if t == "صاعد")
        bearish_count = sum(1 for t in timeframes.values() if t == "هابط")
        total_frames = len(timeframes)

        # بناء الكائن الكامل للتحليل (مثل البوت الأصلي)
        analysis = {
            "price": price,
            "asset": asset,
            "indicators": {
                "trend": {
                    "bullish_count": bullish_count,
                    "adx": adx,
                    "current_trend": "صاعد" if bullish_count >= 3 else "هابط" if bearish_count >= 3 else "محايد"
                },
                "momentum": {
                    "rsi": rsi,
                    "macd_hist": macd,
                    "stoch": 50
                },
                "volatility": {
                    "atr_percent": 1.0,
                    "bb_position": 0.5,
                    "vwap_deviation": 0
                },
                "volume": {
                    "ratio": 1.0
                },
                "support_resistance": {
                    "s1": price * 0.98,
                    "r1": price * 1.02,
                    "pivot": price
                },
                "sentiment": {
                    "fear_greed": 50
                }
            },
            "timeframes": {tf: {"trend": v} for tf, v in timeframes.items()}
        }

        # حساب التقييم الشامل الرياضي
        comp_score = calculate_comprehensive_score(analysis, asset, open_trade)

        # بناء الـ Prompt لـ AI
        prompt = f"""أنت خبير تحليل أسواق مالية متخصص في النفط والفضة. قم بتحليل السوق التالي وأجب بالصيغة المطلوبة فقط.

═══════════════════════════════════════
📊 بيانات السوق:
═══════════════════════════════════════
• الأصل: {asset}
• السعر الحالي: ${price:.2f}
• RSI (7): {rsi:.1f}
• ADX (14): {adx:.1f}
• MACD Histogram: {macd:.4f}
• الفريمات الصاعدة: {bullish_count}/{total_frames}
• الفريمات الهابطة: {bearish_count}/{total_frames}
• التقييم الرياضي: {comp_score['score']:.0f}% ({comp_score['grade']})

═══════════════════════════════════════
المطلوب (أجب بالصيغة التالية فقط):
═══════════════════════════════════════
التقييم: [ممتاز/جيد/متوسط/ضعيف/سيئ]
الدرجة: [0-100]
الأسباب: [3 أسباب على الأقل، مفصولة بفواصل]
نصيحة: [نصيحة مختصرة]
مستوى الخطر: [1/2/3]  (1=منخفض، 2=متوسط، 3=مرتفع)
"""

        if open_trade:
            entry = open_trade.get('entry_price', 0)
            trade_type = open_trade.get('type', 'BUY')
            profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" else ((entry - price) / entry * 100)
            prompt += f"\n• الصفقة المفتوحة: {trade_type} | {profit_pct:+.2f}%"

        response = self._call_model(prompt, max_tokens=400)

        # بناء النتيجة مع الاحتياطي الرياضي
        result = {
            "evaluation": comp_score['grade'],
            "score": comp_score['score'],
            "reasons": comp_score['details'][:3] if comp_score['details'] else [],
            "advice": "",
            "risk_level": 1,
            "comprehensive": comp_score  # نمرر التقييم الرياضي بالكامل
        }

        if response:
            eval_match = re.search(r'التقييم:\s*(.+)', response)
            if eval_match:
                result["evaluation"] = eval_match.group(1).strip()

            score_match = re.search(r'الدرجة:\s*(\d+)', response)
            if score_match:
                try:
                    result["score"] = min(100, max(0, int(score_match.group(1))))
                except:
                    pass

            reasons_match = re.search(r'الأسباب:\s*(.+)', response, re.DOTALL)
            if reasons_match:
                reasons_text = reasons_match.group(1).strip()
                reasons = [r.strip() for r in re.split(r'[،،,]', reasons_text) if r.strip()]
                if reasons:
                    result["reasons"] = reasons[:5]

            advice_match = re.search(r'نصيحة:\s*(.+)', response)
            if advice_match:
                result["advice"] = advice_match.group(1).strip()

            risk_match = re.search(r'مستوى الخطر:\s*(\d+)', response)
            if risk_match:
                try:
                    result["risk_level"] = min(3, max(1, int(risk_match.group(1))))
                except:
                    pass

        # تأكد من وجود أسباب ونصيحة
        if not result["reasons"]:
            result["reasons"] = comp_score['details'][:3] if comp_score['details'] else [f"RSI: {rsi:.1f}", f"ADX: {adx:.1f}", f"{bullish_count}/{total_frames} صاعدة"]
        if not result["advice"]:
            if bullish_count >= 3:
                result["advice"] = "الاتجاه العام صاعد، فكر في صفقات شراء مع إدارة المخاطر."
            elif bearish_count >= 3:
                result["advice"] = "الاتجاه العام هابط، فكر في صفقات بيع أو الانتظار."
            else:
                result["advice"] = "السوق في حالة تذبذب، انتظر حتى تظهر إشارة واضحة."

        logger.info(f"✅ تحليل {asset}: score={result['score']}, risk={result['risk_level']}")
        return result

    def generate_alert(self, asset: str, open_trade: Dict, current_data: Dict) -> Dict:
        """تحليل الخطر للصفقة المفتوحة باستخدام AI + منطق رياضي"""
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

        closes = current_data.get("closes", [])
        rsi_val = calculate_rsi_7(closes)
        rsi_val = rsi_val[-1] if rsi_val else 50
        macd_line, sig_line, hist = calculate_macd_full(closes)
        macd_val = hist[-1] if hist else 0
        atr = calculate_atr_14(current_data) or 0

        # حساب المسافات إلى SL و TP
        dist_to_sl = 0
        dist_to_tp = 0
        if sl > 0 and entry > 0:
            if trade_type == "BUY":
                dist_to_sl = (price - sl) / entry * 100
                dist_to_tp = (tp - price) / entry * 100 if tp > 0 else 0
            else:
                dist_to_sl = (sl - price) / entry * 100
                dist_to_tp = (price - tp) / entry * 100 if tp > 0 else 0

        # حساب المستوى رياضيًا (منطق البوت الأصلي)
        level = 1
        if dist_to_sl < 0.5:
            level = 3
        elif dist_to_sl < 1.0:
            level = 2
        elif abs(profit_pct) > 5:
            level = 2
        elif (trade_type == "BUY" and rsi_val > 70) or (trade_type == "SELL" and rsi_val < 30):
            level = 2

        # استدعاء AI لصياغة الرسالة
        prompt = f"""أنت خبير إدارة مخاطر. قم بكتابة رسالة تحذيرية مختصرة للصفقة التالية.

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
• MACD: {macd_val:.4f}
• ATR: ${atr:.2f} ({atr/price*100 if price > 0 else 0:.2f}%)

═══════════════════════════════════════
مستوى الخطر المحسوب: {level}/3

المطلوب:
اكتب رسالة تحذيرية مختصرة (لا تتجاوز سطرين) توضح سبب الخطر والإجراء المناسب.
"""

        response = self._call_model(prompt, max_tokens=150)
        if response:
            message = response.strip()
        else:
            # رسائل احتياطية من البوت الأصلي
            if level == 3:
                message = f"🚨 خطر داهم! الصفقة قريبة جداً من وقف الخسارة ({dist_to_sl:.1f}%). أنصح بالإغلاق فوراً."
            elif level == 2:
                message = f"⚠️ خطر متوسط. راقب الصفقة عن كثب، قد تحتاج للإغلاق قريباً."
            else:
                message = "🟢 الخطر منخفض، استمر في مراقبة الصفقة."

        action = "close" if level == 3 else "notify"
        return {"level": level, "message": message, "action": action}

    def extract_deep_lesson(self, trade_data: Dict, market_context: str) -> Dict:
        """استخلاص درس عميق وسيناريو باستخدام AI + احتياطي"""
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
            # احتياطي قوي
            if profit > 0:
                lesson = "الصفقات الرابحة تحدث عندما تتوافق المؤشرات مع الاتجاه العام."
                scenario = "ارتفع السعر بعد الدخول بفضل زخم صاعد قوي."
                condition = "RSI > 50 و ADX > 25 و الاتجاه صاعد."
                advice = "استمر في استخدام هذه الشروط للدخول."
            else:
                lesson = "الصفقات الخاسرة تحدث عندما تتعارض المؤشرات مع الاتجاه العام."
                scenario = "انعكس السعر بعد الدخول بسبب ضعف الزخم."
                condition = "RSI < 50 أو ADX < 20 أو الاتجاه هابط."
                advice = "تجنب الدخول عندما تكون المؤشرات ضعيفة."
            return {"lesson": lesson, "scenario": scenario, "condition": condition, "advice": advice}

        result = {}
        lesson_match = re.search(r'الدرس:\s*(.+)', response)
        result["lesson"] = lesson_match.group(1).strip() if lesson_match else "درس غير معروف"
        scenario_match = re.search(r'السيناريو:\s*(.+)', response)
        result["scenario"] = scenario_match.group(1).strip() if scenario_match else ""
        condition_match = re.search(r'الشرط:\s*(.+)', response)
        result["condition"] = condition_match.group(1).strip() if condition_match else ""
        advice_match = re.search(r'النصيحة:\s*(.+)', response)
        result["advice"] = advice_match.group(1).strip() if advice_match else ""

        return result

    def update_market_profile(self, asset: str, recent_trades: List[Dict]) -> str:
        """تحديث وصف شخصية السوق باستخدام AI + احتياطي"""
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
        return "تعذر تحديث شخصية السوق حالياً."

    def generate_intelligence_report(self, asset: str, trades: List[Dict], market_profile: str) -> str:
        """توليد تقرير استخباراتي باستخدام AI + احتياطي"""
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
        return "تعذر توليد التقرير الاستخباراتي حالياً."


# ====================================================================================
# 📦 PART 06: نظام التعلم العميق (إدارة السيناريوهات وشخصية السوق والدروس)
# ====================================================================================

def load_scenarios() -> List[Dict]:
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
    try:
        with open(SCENARIOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ السيناريوهات: {e}")
        return False


def load_market_profile() -> Dict:
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
    try:
        with open(MARKET_PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ شخصية السوق: {e}")
        return False


def load_deep_lessons() -> List[str]:
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
    try:
        with open(DEEP_LESSONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(lessons, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ الدروس العميقة: {e}")
        return False


def add_scenario(scenario: Dict) -> bool:
    scenarios = load_scenarios()
    condition = scenario.get('condition', '')
    for s in scenarios:
        if s.get('condition', '') == condition:
            s['occurrences'] = s.get('occurrences', 0) + 1
            s['last_updated'] = datetime.now().isoformat()
            save_scenarios(scenarios)
            return True
    scenario['id'] = f"sc_{int(time.time())}"
    scenario['occurrences'] = 1
    scenario['last_updated'] = datetime.now().isoformat()
    scenarios.append(scenario)
    save_scenarios(scenarios)
    return True


def add_deep_lesson(lesson: str) -> bool:
    lessons = load_deep_lessons()
    for existing in lessons:
        if len(existing) > 10 and len(lesson) > 10:
            if existing[:30] == lesson[:30]:
                return False
    lessons.append(lesson)
    if len(lessons) > 50:
        lessons = lessons[-50:]
    save_deep_lessons(lessons)
    return True


# ====================================================================================
# 📦 PART 07: إدارة الملفات والبيانات
# ====================================================================================

def get_trades_file(asset_type: str) -> str:
    return TRADES_FILE_OIL if asset_type == "oil" else TRADES_FILE_SILVER


def get_position_file(asset_type: str) -> str:
    return POSITION_FILE_OIL if asset_type == "oil" else POSITION_FILE_SILVER


def safe_file_operation(asset_type: str, operation, *args, **kwargs):
    lock = FILE_LOCKS[asset_type]
    with lock:
        return operation(*args, **kwargs)


def load_trades_history(asset_type: str) -> Dict:
    file = get_trades_file(asset_type)
    default = {"trades": [], "last_cleanup": datetime.now().isoformat()}
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'trades' in data:
                    return data
    except Exception as e:
        logger.error(f"❌ فشل تحميل {asset_type}: {e}")
    return default


def save_trades_history(asset_type: str, history: Dict) -> bool:
    file = get_trades_file(asset_type)
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ {asset_type}: {e}")
        return False


def get_current_open_trade(asset_type: str) -> Optional[Dict]:
    file = get_position_file(asset_type)
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                trade = json.load(f)
                if trade and trade.get('status') == 'open':
                    return trade
    except Exception as e:
        logger.error(f"❌ فشل قراءة {asset_type}: {e}")
    return None


def save_current_trade(asset_type: str, trade: Dict) -> bool:
    file = get_position_file(asset_type)
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(trade, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ {asset_type}: {e}")
        return False


def delete_current_trade(asset_type: str) -> bool:
    file = get_position_file(asset_type)
    try:
        if os.path.exists(file):
            os.remove(file)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حذف {asset_type}: {e}")
        return False


# ====================================================================================
# 📦 PART 08: المدير التنفيذي (TradingCore) مع المحاسبة المدمجة
# ====================================================================================

class AccountingSystem:
    INITIAL_CAPITAL = 100.0
    ENTRY_AMOUNT = 1.0
    LEVERAGE = 200.0

    @classmethod
    def calculate_profit_dollars(cls, entry_price, exit_price, trade_type):
        if entry_price is None or entry_price == 0:
            return 0.0
        if trade_type == "BUY":
            price_change = (exit_price - entry_price) / entry_price
        else:
            price_change = (entry_price - exit_price) / entry_price
        return price_change * cls.ENTRY_AMOUNT * cls.LEVERAGE

    @classmethod
    def format_profit(cls, profit_dollars):
        if profit_dollars is None:
            return "⚖️ متعادلة: $0.00"
        if profit_dollars > 0:
            return f"✅ ربح: +${profit_dollars:.2f}"
        elif profit_dollars < 0:
            return f"❌ خسارة: -${abs(profit_dollars):.2f}"
        return "⚖️ متعادلة: $0.00"


class TradingCore:
    def __init__(self, ai_core: AICore):
        self.ai_core = ai_core
        self.accounting = AccountingSystem()

    def open_trade(self, asset_type: str, signal_data: Dict, source: str = "auto") -> bool:
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

        # توليد توصية ذكية باستخدام AI
        recommendation = self._generate_recommendation(asset_type, signal_data, trade)

        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        signal_label = "شراء 🟢" if signal == "BUY" else "بيع 🔴"
        msg = f"📊 **توصية Tona AI - {asset_label}**\n"
        msg += f"🎯 {signal_label} عند ${safe_price(price)}\n"
        msg += f"🛡️ وقف الخسارة: ${safe_price(sl)}\n"
        msg += f"🎯 الهدف: ${safe_price(tp)}\n"
        msg += f"📊 RR: {rr:.2f}\n"
        if source == "manual":
            msg += "📌 تم الفتح يدوياً\n"
        msg += "\n" + recommendation + "\n"
        msg += "\n💙 Tona AI: سأراقب الصفقة وأحذرك عند الحاجة."
        queue_telegram_message(msg)

        with MONITOR_TRIGGER_LOCK:
            MONITOR_TRIGGER[asset_type] = {"reason": "new_trade", "time": time.time()}

        logger.info(f"✅ تم فتح صفقة {asset_type} ({signal}) بـ ${price:.2f}")
        return True

    def _generate_recommendation(self, asset_type: str, signal_data: Dict, trade: Dict) -> str:
        """توليد نص توصية ذكي باستخدام AI"""
        price = signal_data.get('price', 0)
        signal = signal_data.get('signal', 'WAIT')
        sl = signal_data.get('sl', 0)
        tp = signal_data.get('tp', 0)
        rr = signal_data.get('rr', 0)

        # جلب تحليل السوق
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        data = get_mexc_candles(symbol, "Min15", 200)
        if not data:
            return "⚠️ لا توجد بيانات كافية للتوصية."

        analysis = self.ai_core.analyze_market(asset_type, data, None)
        if not analysis or 'error' in analysis:
            return "⚠️ تعذر الحصول على تحليل السوق."

        score = analysis.get('score', 50)
        evaluation = analysis.get('evaluation', 'متوسط')
        reasons = analysis.get('reasons', [])
        advice = analysis.get('advice', '')
        risk = analysis.get('risk_level', 1)

        msg = f"🧠 **تحليل Tona AI:**\n"
        msg += f"📊 التقييم: {evaluation} ({score}/100)\n"
        msg += f"⚠️ مستوى الخطر: {risk}/3\n"
        if reasons:
            msg += "📋 الأسباب:\n"
            for r in reasons[:3]:
                msg += f"   • {r}\n"
        if advice:
            msg += f"💡 النصيحة: {advice}\n"

        return msg

    def close_trade(self, asset_type: str, reason: str, current_price: Optional[float] = None) -> bool:
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
                            "adx": calculate_adx_14(data) or 20,
                            "trend": "صاعد" if sum(1 for tf in ["Min5","Min15","Min60","Hour4"] if (d := get_mexc_candles("USOIL_USDT" if asset_type == "oil" else "SILVER_USDT", tf, 100)) and (st := calculate_supertrend_vpt_correct(d, st_mult=2.5 if asset_type == "oil" else 2.2)) and st[1][-1] == 1) >= 3 else "هابط" if sum(1 for tf in ["Min5","Min15","Min60","Hour4"] if (d := get_mexc_candles("USOIL_USDT" if asset_type == "oil" else "SILVER_USDT", tf, 100)) and (st := calculate_supertrend_vpt_correct(d, st_mult=2.5 if asset_type == "oil" else 2.2)) and st[1][-1] == -1) >= 3 else "محايد"
                        }
                    break

            if not trade_found:
                logger.error(f"❌ لم يُعثر على الصفقة {trade_id} في السجل")
                return False

            save_trades_history(asset_type, history)
            delete_current_trade(asset_type)

            with MONITOR_TRIGGER_LOCK:
                MONITOR_TRIGGER[asset_type] = None

            # التعلم من الصفقة باستخدام AI
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

            if lesson_result.get('lesson') and lesson_result['lesson'] != "درس غير معروف":
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
# 📦 PART 09: نظام التحذير والمراقبة المتقدم (من البوت الأصلي مع AI)
# ====================================================================================

def check_sl_tp_hit(asset_type: str, current_price: float, open_trade: Dict, trading_core: TradingCore) -> bool:
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
    else:
        if sl is not None and current_price >= sl:
            trading_core.close_trade(asset_type, "Hit Stop Loss", current_price)
            return True
        if tp is not None and current_price <= tp:
            trading_core.close_trade(asset_type, "Hit Take Profit", current_price)
            return True
    return False


def check_distance_warning(asset_type: str, current_price: float, open_trade: Dict, ai_core: AICore):
    """تحذير الاقتراب من SL (مرة واحدة)"""
    entry = open_trade.get('entry_price', current_price)
    sl = open_trade.get('sl', entry)
    if sl == entry or sl == 0:
        return

    total_distance = abs(entry - sl)
    current_distance = abs(current_price - sl)
    distance_pct = current_distance / total_distance if total_distance > 0 else 1.0

    if distance_pct <= 0.33:
        # التحقق من عدم تكرار التحذير
        warnings_sent = open_trade.get('warnings_sent', [])
        if "distance_sl" in warnings_sent:
            return

        # توليد رسالة ذكية
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        prompt = f"""اكتب رسالة تحذيرية مختصرة لصفقة {asset_label} تقترب من وقف الخسارة.

السعر الحالي: ${current_price:.2f}
وقف الخسارة: ${sl:.2f}
المسافة المتبقية: {distance_pct*100:.1f}%

اكتب رسالة لا تتجاوز سطرين، توضح الوضع وتقدم نصيحة."""
        response = ai_core._call_model(prompt, max_tokens=100)
        if response:
            msg = f"⚠️ **تحذير {asset_label}**\n{response}"
        else:
            msg = f"⚠️ **تحذير {asset_label}**\n"
            msg += f"الصفقة تقترب من وقف الخسارة!\n"
            msg += f"💰 السعر الحالي: ${safe_price(current_price)} | وقف الخسارة: ${safe_price(sl)}\n"
            msg += f"📉 المسافة المتبقية: {distance_pct*100:.1f}%\n"
            msg += "\n💡 **توصية Tona AI:** راقب الصفقة عن كثب، قد تحتاج للإغلاق."

        queue_telegram_message(msg)
        open_trade['warnings_sent'] = warnings_sent + ["distance_sl"]
        save_current_trade(asset_type, open_trade)


def check_trend_reversal_warnings(asset_type: str, current_analysis: Dict, open_trade: Dict, ai_core: AICore):
    """تحذير انعكاس الاتجاه (3 مستويات) - من البوت الأصلي مع AI"""
    if not open_trade or not current_analysis:
        return

    last_state = open_trade.get("last_analysis", {})
    if not last_state:
        open_trade["last_analysis"] = _extract_analysis_state(current_analysis)
        save_current_trade(asset_type, open_trade)
        return

    current_state = _extract_analysis_state(current_analysis)

    prev_rsi = last_state.get("rsi", 50)
    curr_rsi = current_state.get("rsi", 50)
    prev_adx = last_state.get("adx", 20)
    curr_adx = current_state.get("adx", 20)
    prev_macd = last_state.get("macd", 0)
    curr_macd = current_state.get("macd", 0)
    prev_vwap = last_state.get("vwap", 0)
    curr_vwap = current_state.get("vwap", 0)
    prev_vol = last_state.get("volume_ratio", 1.0)
    curr_vol = current_state.get("volume_ratio", 1.0)
    prev_score = last_state.get("comprehensive_score", 50)
    curr_score = current_state.get("comprehensive_score", 50)
    prev_trends = last_state.get("timeframes", {})
    curr_trends = current_state.get("timeframes", {})
    prev_false_score = last_state.get("false_signal_score", 0)
    curr_false_score = current_state.get("false_signal_score", 0)

    rsi_change = curr_rsi - prev_rsi
    adx_change = curr_adx - prev_adx
    macd_change = curr_macd - prev_macd
    vwap_change = curr_vwap - prev_vwap
    vol_change = curr_vol - prev_vol
    score_change = curr_score - prev_score
    false_score_change = curr_false_score - prev_false_score

    changed_frames = []
    for tf in ["5m", "15m", "1h", "4h"]:
        if tf in prev_trends and tf in curr_trends:
            if prev_trends[tf] != curr_trends[tf]:
                changed_frames.append(tf)
    changed_count = len(changed_frames)

    level = 0
    reasons = []

    if abs(rsi_change) > 15:
        level = max(level, 2)
        reasons.append(f"تغير حاد في RSI: {rsi_change:+.1f}")
    elif abs(rsi_change) > 8:
        level = max(level, 1)
        reasons.append(f"تغير ملحوظ في RSI: {rsi_change:+.1f}")

    if abs(adx_change) > 10:
        level = max(level, 2)
        reasons.append(f"تغير حاد في ADX: {adx_change:+.1f}")
    elif abs(adx_change) > 5:
        level = max(level, 1)
        reasons.append(f"تغير ملحوظ في ADX: {adx_change:+.1f}")

    if abs(macd_change) > 0.5:
        level = max(level, 2)
        reasons.append(f"تغير حاد في MACD: {macd_change:+.3f}")
    elif abs(macd_change) > 0.1:
        level = max(level, 1)
        reasons.append(f"تغير ملحوظ في MACD: {macd_change:+.3f}")

    if abs(vwap_change) > 0.005:
        level = max(level, 1)
        reasons.append(f"تغير في VWAP: {vwap_change:+.3f}")

    if abs(vol_change) > 0.5:
        level = max(level, 2)
        reasons.append(f"تغير حاد في الحجم: {vol_change:+.1f}x")
    elif abs(vol_change) > 0.2:
        level = max(level, 1)
        reasons.append(f"تغير ملحوظ في الحجم: {vol_change:+.1f}x")

    if abs(score_change) > 10:
        level = max(level, 2)
        reasons.append(f"تغير حاد في التقييم: {score_change:+.1f}%")
    elif abs(score_change) > 5:
        level = max(level, 1)
        reasons.append(f"تغير ملحوظ في التقييم: {score_change:+.1f}%")

    if changed_count >= 2:
        level = max(level, 2 if changed_count >= 3 else 1)
        reasons.append(f"تغير في {changed_count} فريمات ({', '.join(changed_frames)})")

    if false_score_change > 2:
        level = max(level, 2)
        reasons.append(f"زيادة في مؤشرات الإشارة الخادعة: +{false_score_change}")

    if level == 0:
        open_trade["last_analysis"] = current_state
        save_current_trade(asset_type, open_trade)
        return

    warnings_sent = open_trade.get('warnings_sent', [])
    warning_key = f"trend_reversal_{level}"
    if warning_key in warnings_sent:
        open_trade["last_analysis"] = current_state
        save_current_trade(asset_type, open_trade)
        return

    # توليد رسالة تحذيرية باستخدام AI
    asset_label = "النفط" if asset_type == "oil" else "الفضة"
    prompt = f"""اكتب رسالة تحذيرية من المستوى {level} لصفقة {asset_label} بسبب انعكاس محتمل في الاتجاه.

الأسباب:
{chr(10).join('• ' + r for r in reasons)}

السعر الحالي: ${current_analysis.get('price', 0):.2f}

اكتب رسالة مختصرة (لا تتجاوز 3 أسطر) توضح الوضع وتقدم توصية واضحة (استمر، راقب، اغلق)."""
    response = ai_core._call_model(prompt, max_tokens=150)

    if response:
        msg = f"⚠️ **تحذير من المستوى {level} - {asset_label}**\n{response}"
    else:
        # رسائل احتياطية من البوت الأصلي
        level_labels = {1: "انعكاس ضعيف", 2: "انعكاس متوسط", 3: "انعكاس قوي"}
        label = level_labels.get(level, "تحذير")
        msg = f"⚠️ **تحذير من المستوى {level}** {label} - {asset_label}\n"
        msg += "🔍 أسباب التحذير:\n"
        for r in reasons[:3]:
            msg += f"   • {r}\n"
        if level == 3:
            msg += "🚨 **توصية Tona AI:** أنصح بشدة بإغلاق الصفقة فوراً."
        elif level == 2:
            msg += "💡 **توصية Tona AI:** راقب الصفقة عن كثب، قد تحتاج للإغلاق قريباً."
        else:
            msg += "💡 **توصية Tona AI:** كن حذراً، هناك تغير طفيف في الاتجاه."

    queue_telegram_message(msg)
    open_trade['warnings_sent'] = warnings_sent + [warning_key]
    open_trade["last_analysis"] = current_state
    save_current_trade(asset_type, open_trade)

    if level == 3:
        trading_core.close_trade(asset_type, f"انعكاس قوي: {reasons[0] if reasons else ''}", current_analysis.get('price', 0))


def check_memory_warning(asset_type: str, current_analysis: Dict, open_trade: Dict, ai_core: AICore):
    """تحذير الذاكرة الاستباقي - من البوت الأصلي مع AI"""
    if not open_trade or not current_analysis:
        return

    warnings_sent = open_trade.get('warnings_sent', [])
    if "memory_warning" in warnings_sent:
        return

    # جلب اللقطات
    snapshots = []
    try:
        if os.path.exists(SNAPSHOTS_FILE):
            with open(SNAPSHOTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                snapshots = data.get('snapshots', [])[-50:]
    except Exception as e:
        logger.warning(f"⚠️ فشل جلب اللقطات: {e}")

    if len(snapshots) < 5:
        return

    # استخراج المؤشرات الحالية
    indicators = current_analysis.get('indicators', {})
    momentum = indicators.get('momentum', {})
    trend_data = indicators.get('trend', {})
    volatility = indicators.get('volatility', {})
    volume = indicators.get('volume', {})

    current_rsi = momentum.get('rsi', 50)
    current_adx = trend_data.get('adx', 20)
    current_macd = momentum.get('macd_hist', 0)
    current_vol_ratio = volume.get('ratio', 1.0)
    current_bb_pos = volatility.get('bb_position', 0.5)
    current_price = current_analysis.get('price', 0)

    # حساب متوسط المؤشرات في اللقطات الخاسرة
    losing_snapshots = []
    for snap in snapshots:
        if snap.get('profit_dollars', 0) < 0:
            losing_snapshots.append(snap)

    if len(losing_snapshots) < 3:
        return

    avg_rsi = sum(s.get('rsi', 0) for s in losing_snapshots) / len(losing_snapshots)
    avg_adx = sum(s.get('adx', 0) for s in losing_snapshots) / len(losing_snapshots)
    avg_macd = sum(s.get('macd', 0) for s in losing_snapshots) / len(losing_snapshots)
    avg_vol = sum(s.get('volume_ratio', 0) for s in losing_snapshots) / len(losing_snapshots)

    # حساب التشابه
    similarity = 0
    total_weight = 0

    if abs(current_rsi - avg_rsi) < 10:
        similarity += 0.2
    total_weight += 0.2

    if abs(current_adx - avg_adx) < 10:
        similarity += 0.15
    total_weight += 0.15

    if abs(current_macd - avg_macd) < 0.2:
        similarity += 0.15
    total_weight += 0.15

    if abs(current_vol_ratio - avg_vol) < 0.3:
        similarity += 0.15
    total_weight += 0.15

    similarity_percent = (similarity / total_weight) * 100 if total_weight > 0 else 0

    if similarity_percent >= 75:
        # توليد رسالة ذكية
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        prompt = f"""اكتب رسالة تذكير لصفقة {asset_label} تتشابه مع الخسائر السابقة.

التشابه: {similarity_percent:.0f}%
RSI الحالي: {current_rsi:.0f} (متوسط الخسائر: {avg_rsi:.0f})
ADX الحالي: {current_adx:.0f} (متوسط الخسائر: {avg_adx:.0f})
الحجم الحالي: {current_vol_ratio:.1f}x (متوسط الخسائر: {avg_vol:.1f}x)

اكتب رسالة تحذيرية مختصرة (لا تتجاوز سطرين)."""
        response = ai_core._call_model(prompt, max_tokens=100)
        if response:
            msg = f"🧠 **تذكير بالذاكرة - {asset_label}**\n{response}"
        else:
            msg = f"🧠 **تذكير بالذاكرة - {asset_label}**\n"
            msg += f"🔍 تتشابه المؤشرات الحالية بنسبة {similarity_percent:.0f}% مع الخسائر السابقة.\n"
            msg += f"📊 RSI: {current_rsi:.0f} (المتوسط في الخسائر: {avg_rsi:.0f})\n"
            msg += f"📊 ADX: {current_adx:.0f} (المتوسط في الخسائر: {avg_adx:.0f})\n"
            msg += f"📊 الحجم: {current_vol_ratio:.1f}x (المتوسط في الخسائر: {avg_vol:.1f}x)\n"
            msg += "\n💡 **توصية Tona AI:** أنصح بالمراقبة المكثفة، قد تكون الصفقة في منطقة خطر مشابهة للخسائر السابقة."

        queue_telegram_message(msg)
        open_trade['warnings_sent'] = warnings_sent + ["memory_warning"]
        save_current_trade(asset_type, open_trade)


def _extract_analysis_state(analysis: Dict) -> Dict:
    """استخراج حالة التحليل للمقارنة"""
    if not analysis:
        return {}
    state = {
        "timeframes": {},
        "rsi": 50,
        "adx": 20,
        "macd": 0,
        "volume_ratio": 1.0,
        "vwap": 0,
        "comprehensive_score": 50,
        "false_signal_score": 0
    }
    timeframes = analysis.get('timeframes', {})
    for tf in ["5m", "15m", "1h", "4h"]:
        if tf in timeframes and isinstance(timeframes.get(tf), dict):
            state["timeframes"][tf] = timeframes[tf].get('trend', 'محايد')

    tf_15m = timeframes.get('15m', {})
    state["rsi"] = tf_15m.get('rsi', 50)
    state["adx"] = tf_15m.get('adx', 20)
    state["macd"] = tf_15m.get('macd', 0)
    state["volume_ratio"] = tf_15m.get('volume_ratio', 1.0)
    state["vwap"] = tf_15m.get('vwap', 0)
    state["comprehensive_score"] = analysis.get('comprehensive_score', {}).get('score', 50)
    return state


def monitor_loop(trading_core: TradingCore):
    """حلقة المراقبة الرئيسية مع التحذيرات المتقدمة"""
    logger.info("🔄 [Monitor] بدأ التشغيل")
    while True:
        try:
            for asset_type in ["oil", "silver"]:
                open_trade = get_current_open_trade(asset_type)
                if not open_trade:
                    continue

                symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
                data = get_mexc_candles(symbol, "Min1", 10)
                if not data or not data.get("closes"):
                    continue

                current_price = data["closes"][-1]

                # التحقق من ضرب SL/TP
                if check_sl_tp_hit(asset_type, current_price, open_trade, trading_core):
                    continue

                # جلب التحليل الشامل
                analysis, _ = perform_comprehensive_analysis(asset_type, data, open_trade)
                if not analysis:
                    continue

                # التحذيرات
                check_distance_warning(asset_type, current_price, open_trade, trading_core.ai_core)
                check_trend_reversal_warnings(asset_type, analysis, open_trade, trading_core.ai_core)
                check_memory_warning(asset_type, analysis, open_trade, trading_core.ai_core)

                # حفظ لقطة
                save_snapshot(asset_type, open_trade, analysis, current_price)

                # تحليل الخطر عبر AI
                current_data = {
                    "price": current_price,
                    "closes": data["closes"],
                    "highs": data["highs"],
                    "lows": data["lows"],
                    "volumes": data["volumes"]
                }
                alert = trading_core.ai_core.generate_alert(asset_type, open_trade, current_data)
                if alert["level"] >= 2:
                    if "warnings_log" not in open_trade:
                        open_trade["warnings_log"] = []
                    open_trade["warnings_log"].append({
                        "level": alert["level"],
                        "message": alert["message"],
                        "timestamp": datetime.now().isoformat()
                    })
                    save_current_trade(asset_type, open_trade)

                if alert["level"] == 3:
                    msg = f"🚨 **تحذير المستوى 3 - {asset_type}**\n{alert['message']}\n💰 السعر الحالي: ${safe_price(current_price)}\n⚠️ سيتم إغلاق الصفقة تلقائياً."
                    queue_telegram_message(msg)
                    trading_core.close_trade(asset_type, f"تحذير مستوى 3: {alert['message'][:50]}", current_price)
                elif alert["level"] == 2:
                    msg = f"⚠️ **تحذير المستوى 2 - {asset_type}**\n{alert['message']}\n💰 السعر الحالي: ${safe_price(current_price)}"
                    queue_telegram_message(msg)

            time.sleep(5)

        except Exception as e:
            logger.error(f"❌ [Monitor] خطأ: {e}")
            time.sleep(10)


def save_snapshot(asset_type: str, open_trade: Dict, analysis: Dict, current_price: float):
    """حفظ لقطة في الملف المحلي"""
    try:
        snapshots_data = {"snapshots": []}
        if os.path.exists(SNAPSHOTS_FILE):
            with open(SNAPSHOTS_FILE, 'r', encoding='utf-8') as f:
                snapshots_data = json.load(f)

        snapshot = {
            "trade_id": open_trade.get('trade_id', ''),
            "asset_type": asset_type,
            "timestamp": datetime.now().isoformat(),
            "price": current_price,
            "rsi": analysis.get('indicators', {}).get('momentum', {}).get('rsi', 50),
            "adx": analysis.get('indicators', {}).get('trend', {}).get('adx', 20),
            "macd": analysis.get('indicators', {}).get('momentum', {}).get('macd_hist', 0),
            "volume_ratio": analysis.get('indicators', {}).get('volume', {}).get('ratio', 1.0),
            "profit_dollars": open_trade.get('profit_dollars', 0),
            "trend": analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')
        }

        snapshots_data["snapshots"].append(snapshot)
        if len(snapshots_data["snapshots"]) > 200:
            snapshots_data["snapshots"] = snapshots_data["snapshots"][-200:]

        with open(SNAPSHOTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(snapshots_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"❌ فشل حفظ اللقطة: {e}")


def perform_comprehensive_analysis(asset_type: str, data: Dict, open_trade: Optional[Dict] = None) -> tuple:
    """بناء كامل للتحليل الشامل (مشابه للبوت الأصلي)"""
    if not data:
        return None, "بيانات غير كافية"

    closes = data.get("closes", [])
    if not closes:
        return None, "بيانات غير كافية"

    price = closes[-1]

    rsi = calculate_rsi_7(closes)
    rsi = rsi[-1] if rsi else 50

    macd_hist = calculate_macd_histogram(closes)
    macd = macd_hist[-1] if macd_hist else 0

    adx = calculate_adx_14(data) or 20

    atr = calculate_atr_14(data) or 0

    # Bollinger
    upper, basis, lower = calculate_bollinger_bands(closes)
    bb_upper = upper[-1] if upper else price * 1.02
    bb_middle = basis[-1] if basis else price
    bb_lower = lower[-1] if lower else price * 0.98

    # الفريمات
    timeframes = {}
    for tf, interval in [("5m", "Min5"), ("15m", "Min15"), ("1h", "Min60"), ("4h", "Hour4")]:
        tf_data = get_mexc_candles("USOIL_USDT" if asset_type == "oil" else "SILVER_USDT", interval, 100)
        if tf_data and tf_data.get("closes"):
            st_result = calculate_supertrend_vpt_correct(tf_data, st_mult=2.5 if asset_type == "oil" else 2.2)
            if st_result:
                _, trend, _ = st_result
                timeframes[tf] = {"trend": "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد"}
            else:
                tf_closes = tf_data["closes"]
                if len(tf_closes) >= 20:
                    sma_short = sum(tf_closes[-5:]) / 5
                    sma_long = sum(tf_closes[-20:]) / 20
                    if sma_short > sma_long * 1.003:
                        timeframes[tf] = {"trend": "صاعد"}
                    elif sma_short < sma_long * 0.997:
                        timeframes[tf] = {"trend": "هابط"}
                    else:
                        timeframes[tf] = {"trend": "محايد"}
                else:
                    timeframes[tf] = {"trend": "محايد"}
        else:
            timeframes[tf] = {"trend": "محايد"}

    bullish = sum(1 for tf in timeframes.values() if tf.get('trend') == 'صاعد')
    bearish = sum(1 for tf in timeframes.values() if tf.get('trend') == 'هابط')

    analysis = {
        "price": price,
        "asset": asset_type,
        "indicators": {
            "trend": {
                "bullish_count": bullish,
                "adx": adx,
                "current_trend": "صاعد" if bullish >= 3 else "هابط" if bearish >= 3 else "محايد"
            },
            "momentum": {
                "rsi": rsi,
                "macd_hist": macd,
                "stoch": 50
            },
            "volatility": {
                "atr_percent": (atr / price * 100) if price > 0 else 0,
                "bb_position": (price - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5,
                "vwap_deviation": 0
            },
            "volume": {
                "ratio": 1.0
            },
            "support_resistance": {
                "s1": price * 0.98,
                "r1": price * 1.02,
                "pivot": price
            },
            "sentiment": {
                "fear_greed": 50
            }
        },
        "timeframes": timeframes,
        "comprehensive_score": calculate_comprehensive_score(analysis, asset_type, open_trade)
    }

    report = f"📊 تحليل {asset_type}\n💰 السعر: ${price:.2f}\n📊 التقييم: {analysis['comprehensive_score']['score']:.0f}% ({analysis['comprehensive_score']['grade']})"
    return analysis, report


# ====================================================================================
# 📦 PART 10: بوابة المستخدم (معدل - مع بدء الخيوط عند أول طلب)
# ====================================================================================

app = Flask(__name__)
CORS(app)

AI_CORE = AICore()
TRADING_CORE = TradingCore(AI_CORE)

# --- متغيرات للتحكم في بدء الخيوط الخلفية ---
_BACKGROUND_THREADS_STARTED = False
_BACKGROUND_THREADS_LOCK = threading.Lock()

def start_background_threads():
    """بدء الخيوط الخلفية (يتم استدعاؤها عند أول طلب)"""
    global _BACKGROUND_THREADS_STARTED
    with _BACKGROUND_THREADS_LOCK:
        if _BACKGROUND_THREADS_STARTED:
            return
        logger.info("🔄 بدء تشغيل الخيوط الخلفية (بعد أول طلب)...")
        
        # بدء Scanner
        scanner_thread = threading.Thread(target=signal_scanner, args=(TRADING_CORE,), name="Scanner", daemon=True)
        scanner_thread.start()
        logger.info("✅ Scanner بدأ بنجاح")
        
        # بدء Monitor
        monitor_thread = threading.Thread(target=monitor_loop, args=(TRADING_CORE,), name="Monitor", daemon=True)
        monitor_thread.start()
        logger.info("✅ Monitor بدأ بنجاح")
        
        _BACKGROUND_THREADS_STARTED = True
        logger.info("✅ جميع الخيوط الخلفية بدأت بنجاح")


@app.route('/')
def home():
    start_background_threads()  # بدء الخيوط عند أول طلب
    return "🚀 Tona AI V2.0 - البوت الاستشاري الذكي", 200


@app.route('/ping')
def ping():
    start_background_threads()  # بدء الخيوط عند أول طلب
    return "Bot is alive!", 200


@app.route('/webhook', methods=['POST'])
def webhook():
    start_background_threads()  # بدء الخيوط عند أول طلب
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


def _send_telegram_message_direct(text: str, chat_id: str) -> bool:
    if not TELEGRAM_TOKEN or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }, timeout=15)
        return resp.status_code == 200
    except Exception as e:
        logger.error(f"❌ استثناء في الإرسال: {e}")
        return False


def queue_telegram_message(text: str, chat_id: str = None):
    if not text or text.strip() == "":
        return False
    target = chat_id or CHAT_ID
    if not target:
        return False
    if len(text) > 4096:
        parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for part in parts:
            _send_telegram_message_direct(part, target)
        return True
    return _send_telegram_message_direct(text, target)


def send_main_menu(chat_id: str):
    keyboard = [
        ["🛢️ تحليل النفط", "🥈 تحليل الفضة"],
        ["🔍 وضع الصفقة الحالية", "📊 تقرير الأداء"],
        ["📌 فتح صفقة يدوياً", "🧠 تقرير التعلم العميق"],
        ["📰 تقرير استخباراتي", "❌ إغلاق الصفقة"]
    ]

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
    text = """🚀 **Tona AI V2.0** - المستشار الذكي

💙 أنا هنا لمساعدتك في تحليل النفط والفضة.

📌 استخدم الأزرار أو اكتب /start للقائمة."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "reply_markup": reply_markup,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception as e:
        logger.error(f"❌ فشل إرسال القائمة: {e}")


def analyze_timeframes(asset_type: str) -> Dict[str, str]:
    result = {}
    symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
    st_mult = 2.5 if asset_type == "oil" else 2.2
    timeframes = {"5m": "Min5", "15m": "Min15", "1h": "Min60", "4h": "Hour4"}

    for name, interval in timeframes.items():
        try:
            data = get_mexc_candles(symbol, interval, 200)
            if not data or not data.get("closes") or len(data["closes"]) < 50:
                result[name] = "محايد ⚪"
                continue
            st_result = calculate_supertrend_vpt_correct(data, st_mult=st_mult, st_period=100, vpt_len=10)
            if st_result is None:
                closes = data["closes"]
                if len(closes) >= 20:
                    sma_short = sum(closes[-5:]) / 5
                    sma_long = sum(closes[-20:]) / 20
                    if sma_short > sma_long * 1.003:
                        result[name] = "صاعد 📈"
                    elif sma_short < sma_long * 0.997:
                        result[name] = "هابط 📉"
                    else:
                        result[name] = "محايد ⚪"
                else:
                    result[name] = "محايد ⚪"
                continue
            st_line_arr, trend, _ = st_result
            if not trend or len(trend) == 0:
                result[name] = "محايد ⚪"
                continue
            result[name] = "صاعد 📈" if trend[-1] == 1 else "هابط 📉" if trend[-1] == -1 else "محايد ⚪"
        except Exception as e:
            logger.warning(f"⚠️ فشل تحليل {name} لـ {asset_type}: {e}")
            result[name] = "محايد ⚪"
    return result


def handle_analysis(asset_type: str, chat_id: str):
    logger.info(f"🔍 [handle_analysis] بدء تحليل {asset_type} لـ {chat_id}")
    try:
        queue_telegram_message(f"🔍 جاري التحليل الشامل لـ {'النفط' if asset_type == 'oil' else 'الفضة'}...", chat_id)
    except:
        pass

    try:
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        data = get_mexc_candles(symbol, "Min15", 200)
        if not data or not data.get("closes"):
            queue_telegram_message(f"⚠️ تعذر جلب بيانات {'النفط' if asset_type == 'oil' else 'الفضة'}", chat_id)
            return

        open_trade = get_current_open_trade(asset_type)
        ai_analysis = AI_CORE.analyze_market(asset_type, data, open_trade)

        if 'error' in ai_analysis:
            queue_telegram_message(f"⚠️ {ai_analysis['error']}", chat_id)
            return

        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        analysis_text = ai_analysis.get('ai_analysis_text', '')
        score = ai_analysis.get('score', 50)
        evaluation = ai_analysis.get('evaluation', 'متوسط')
        risk = ai_analysis.get('risk_level', 1)
        price = ai_analysis.get('full_analysis', {}).get('price', 0)

        if price == 0 and data and data.get("closes"):
            price = data["closes"][-1]

        # إذا كان النص التحليلي فارغاً، ننشئ نصاً احتياطياً
        if not analysis_text:
            full = ai_analysis.get('full_analysis', {})
            rsi = full.get('rsi', 50)
            adx = full.get('adx', 20)
            macd = full.get('macd', 0)
            atr = full.get('atr', 0)
            atr_pct = (atr / price * 100) if price > 0 else 0
            timeframes = full.get('timeframes', {})
            bullish = sum(1 for tf in timeframes.values() if tf.get('trend') == 'صاعد')
            bearish = sum(1 for tf in timeframes.values() if tf.get('trend') == 'هابط')
            support = full.get('indicators', {}).get('support_resistance', {}).get('s1', price * 0.98 if price > 0 else 0)
            resistance = full.get('indicators', {}).get('support_resistance', {}).get('r1', price * 1.02 if price > 0 else 0)

            analysis_text = f"⚠️ لم يتمكن النموذج من توليد تحليل نصي. إليك ملخص المؤشرات:\n"
            analysis_text += f"• السعر: ${price:.2f}\n" if price > 0 else "• السعر: غير متوفر\n"
            analysis_text += f"• RSI: {rsi:.1f}\n"
            analysis_text += f"• ADX: {adx:.1f}\n"
            analysis_text += f"• MACD: {macd:.4f}\n"
            analysis_text += f"• ATR: ${atr:.2f} ({atr_pct:.2f}%)\n"
            analysis_text += f"• الفريمات: {bullish} صاعدة / {bearish} هابطة\n"
            if support > 0 and resistance > 0:
                analysis_text += f"• الدعم: ${support:.2f} | المقاومة: ${resistance:.2f}\n"
            analysis_text += f"• التقييم العام: {evaluation} ({score}/100)\n"
            analysis_text += "\n💡 يُرجى المحاولة مرة أخرى للحصول على تحليل نصي من النموذج."

        price_str = f"${price:.2f}" if price > 0 else "غير متوفر"
        msg = f"📊 **تحليل {asset_label} الشامل**\n"
        msg += f"💰 السعر: {price_str} | التقييم: {evaluation} ({score}/100) | الخطر: {risk}/3\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        msg += f"🧠 **تحليل Tona AI:**\n{analysis_text}"

        if open_trade:
            entry = open_trade.get('entry_price', 0)
            trade_type = open_trade.get('type', 'BUY')
            profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" and entry > 0 else ((entry - price) / entry * 100) if entry > 0 else 0
            msg += f"\n\n📈 **الصفقة المفتوحة:** {trade_type} @ ${safe_price(entry)} | {profit_pct:+.2f}%"
            msg += f"\n🛡️ وقف الخسارة: ${safe_price(open_trade.get('sl'))}"
            msg += f"\n🎯 الهدف: ${safe_price(open_trade.get('tp'))}"

        msg += "\n\n💙 Tona AI: أنا هنا لمساعدتك!"

        logger.info(f"✅ تم بناء التحليل لـ {asset_type} (طول: {len(msg)})")
        queue_telegram_message(msg, chat_id)

    except Exception as e:
        logger.error(f"❌ [handle_analysis] استثناء: {e}")
        import traceback
        logger.error(traceback.format_exc())
        queue_telegram_message(f"⚠️ حدث خطأ أثناء التحليل: {str(e)[:100]}", chat_id)


def handle_position_status(chat_id: str):
    try:
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
            sl = trade.get('sl')
            tp = trade.get('tp')

            symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
            data = get_mexc_candles(symbol, "Min1", 5)
            current_price = data["closes"][-1] if data and data.get("closes") else entry

            profit_pct = ((current_price - entry) / entry * 100) if trade_type == "BUY" else ((entry - current_price) / entry * 100)
            profit_dollars = AccountingSystem.calculate_profit_dollars(entry, current_price, trade_type)

            msg += f"🛢️ **{asset_label}**\n"
            msg += f"   • النوع: {trade_type}\n"
            msg += f"   • الدخول: ${safe_price(entry)}\n"
            msg += f"   • الحالي: ${safe_price(current_price)}\n"
            msg += f"   • الربح/خسارة: {profit_pct:+.2f}% (${profit_dollars:+.2f})\n"
            msg += f"   • وقف الخسارة: ${safe_price(sl)}\n"
            msg += f"   • الهدف: ${safe_price(tp)}\n"
            msg += f"   • RR: {trade.get('rr', 0):.2f}\n"
            msg += f"   • المصدر: {'يدوي' if trade.get('source') == 'manual' else 'تلقائي'}\n\n"

        if not has_trade:
            msg += "🔄 لا توجد صفقات مفتوحة حالياً.\n"
            msg += "💡 يمكنك فتح صفقة يدوياً عبر زر '📌 فتح صفقة يدوياً'"

        queue_telegram_message(msg, chat_id)

    except Exception as e:
        logger.error(f"❌ [handle_position_status] خطأ: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)


def handle_manual_open(chat_id: str):
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
    try:
        parts = text.split()
        if len(parts) < 4:
            queue_telegram_message("⚠️ الصيغة غير صحيحة. استخدم: `فتح صفقة [نفط/فضة] [شراء/بيع] [السعر]`", chat_id)
            return

        asset_str = parts[2]
        type_str = parts[3]
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

        success = TRADING_CORE.open_trade(asset_type, signal_data, source="manual")
        if success:
            queue_telegram_message(f"✅ تم فتح صفقة {asset_str} يدوياً ({type_str}) عند ${safe_price(price)}", chat_id)
        else:
            queue_telegram_message(f"⚠️ فشل فتح صفقة {asset_str}. تأكد من عدم وجود صفقة مفتوحة.", chat_id)

    except Exception as e:
        logger.error(f"❌ فشل فتح يدوي: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)


def handle_performance_report(chat_id: str):
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

            wins = [t for t in closed if (t.get('profit_dollars', 0) or 0) > 0]
            losses = [t for t in closed if (t.get('profit_dollars', 0) or 0) <= 0]
            profit = sum((t.get('profit_dollars', 0) or 0) for t in closed)
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
    try:
        lessons = load_deep_lessons()
        scenarios = load_scenarios()
        profile = load_market_profile()

        msg = "🧠 **تقرير التعلم العميق**\n"
        msg += "━" * 30 + "\n\n"

        msg += "📊 **شخصية السوق الحالية:**\n"
        msg += f"🛢️ النفط: {profile.get('oil', 'لا توجد بيانات')[:200]}\n\n"
        msg += f"🥈 الفضة: {profile.get('silver', 'لا توجد بيانات')[:200]}\n\n"
        msg += f"📅 آخر تحديث: {profile.get('last_updated', 'غير معروف')}\n\n"

        msg += "📚 **الدروس المستفادة:**\n"
        if lessons:
            for i, lesson in enumerate(lessons[-10:], 1):
                msg += f"   {i}. {lesson[:100]}\n"
        else:
            msg += "   ℹ️ لا توجد دروس مسجلة بعد\n"
        msg += "\n"

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
    try:
        queue_telegram_message("📰 جاري توليد التقرير الاستخباراتي...", chat_id)

        oil_history = load_trades_history("oil")
        silver_history = load_trades_history("silver")
        all_trades = oil_history.get('trades', []) + silver_history.get('trades', [])
        closed_trades = [t for t in all_trades if t.get('status') == 'closed']

        if len(closed_trades) < 3:
            queue_telegram_message("⚠️ لا توجد بيانات كافية لتوليد تقرير استخباراتي (يحتاج 3 صفقات على الأقل)", chat_id)
            return

        profile = load_market_profile()
        market_context = f"النفط: {profile.get('oil', '')}\nالفضة: {profile.get('silver', '')}"

        report = AI_CORE.generate_intelligence_report("النفط والفضة", closed_trades, market_context)
        queue_telegram_message(f"📰 **تقرير استخباراتي**\n\n{report}", chat_id)

    except Exception as e:
        logger.error(f"❌ فشل التقرير الاستخباراتي: {e}")
        queue_telegram_message(f"⚠️ حدث خطأ: {str(e)[:100]}", chat_id)


def close_trade_manual(asset_type: Optional[str], chat_id: str):
    if asset_type:
        open_trade = get_current_open_trade(asset_type)
        if not open_trade:
            queue_telegram_message(f"⚠️ لا توجد صفقة {asset_type} مفتوحة", chat_id)
            return
        TRADING_CORE.close_trade(asset_type, "أمر يدوي من المستخدم")
        queue_telegram_message(f"✅ تم إغلاق صفقة {asset_type} يدوياً", chat_id)
    else:
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


def handle_message(text: str, chat_id: str):
    clean_text = text.strip()
    logger.info(f"📩 [handle_message] رسالة من {chat_id}: '{clean_text}'")

    if clean_text in ["/start", "قائمة", "منيو", "/menu"]:
        send_main_menu(chat_id)
        return

    if clean_text in ["🛢️ تحليل النفط", "نفط", "oil"]:
        logger.info("🔍 [handle_message] بدء تحليل النفط")
        handle_analysis("oil", chat_id)
        return

    if clean_text in ["🥈 تحليل الفضة", "فضة", "silver"]:
        logger.info("🔍 [handle_message] بدء تحليل الفضة")
        handle_analysis("silver", chat_id)
        return

    if clean_text in ["🔍 وضع الصفقة الحالية", "وضع الصفقة", "حالة"]:
        handle_position_status(chat_id)
        return

    if clean_text in ["📌 فتح صفقة يدوياً", "فتح يدوي"]:
        handle_manual_open(chat_id)
        return

    if clean_text in ["📊 تقرير الأداء", "إحصائيات"]:
        handle_performance_report(chat_id)
        return

    if clean_text in ["🧠 تقرير التعلم العميق", "تقرير التعلم"]:
        handle_learning_report(chat_id)
        return

    if clean_text in ["📰 تقرير استخباراتي", "استخبارات"]:
        handle_intelligence_report(chat_id)
        return

    if clean_text in ["❌ إغلاق النفط", "أغلق النفط"]:
        close_trade_manual("oil", chat_id)
        return

    if clean_text in ["❌ إغلاق الفضة", "أغلق الفضة"]:
        close_trade_manual("silver", chat_id)
        return

    if clean_text in ["❌ إغلاق الصفقة", "إغلاق"]:
        close_trade_manual(None, chat_id)
        return

    if clean_text.startswith("فتح صفقة"):
        handle_manual_open_command(clean_text, chat_id)
        return

    queue_telegram_message(f"💙 Tona AI: أمر غير معروف. استخدم الأزرار أو اكتب /start للقائمة.", chat_id)


def safe_price(value, default="N/A"):
    if value is None:
        return default
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return default
        
# ====================================================================================
# 📦 PART 11: التشغيل الرئيسي (معدل - مع إزالة بدء الخيوط المباشر)
# ====================================================================================

import os
import time
import threading
import logging
from datetime import datetime
import requests

def cleanup_stuck_trades(trading_core: TradingCore):
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
            except Exception as e:
                logger.error(f"❌ فشل تنظيف {asset_type}: {e}")


def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)


def set_webhook() -> bool:
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN غير موجود")
        return False

    render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if not render_url:
        service_name = os.environ.get('RENDER_SERVICE_NAME', '')
        render_url = f"https://{service_name}.onrender.com" if service_name else os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
        if render_url:
            render_url = f"https://{render_url}"

    if not render_url:
        logger.error("❌ RENDER_EXTERNAL_URL غير موجود - لا يمكن تسجيل Webhook")
        return False

    webhook_url = f"{render_url}/webhook"
    logger.info(f"🔗 محاولة تسجيل Webhook: {webhook_url}")

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        resp = requests.post(url, json={
            "url": webhook_url,
            "allowed_updates": ["message"]
        }, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data.get('ok', False):
                logger.info(f"✅ Webhook مسجل بنجاح: {webhook_url}")
                return True
            else:
                logger.error(f"❌ فشل تسجيل Webhook: {data}")
                return False
        else:
            logger.error(f"❌ خطأ في تسجيل Webhook: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        logger.error(f"❌ استثناء في تسجيل Webhook: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 Tona AI V2.0 FINAL - البوت الاستشاري الذكي (بدء الخيوط عند أول طلب)")
    logger.info("💙 الاسم: Tona AI")
    logger.info("👨‍💻 المطور: بسام الحوباني")
    logger.info("🧠 جميع التحليلات والتوصيات تعتمد على Gemini + Groq")
    logger.info("=" * 60)

    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN غير موجود!")
    else:
        logger.info(f"✅ TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10]}...")

    if not CHAT_ID:
        logger.error("❌ CHAT_ID غير موجود!")
    else:
        logger.info(f"✅ CHAT_ID: {CHAT_ID}")

    os.makedirs("learning_data", exist_ok=True)
    os.makedirs("learning_data/backups", exist_ok=True)

    cleanup_stuck_trades(TRADING_CORE)

    if set_webhook():
        logger.info("✅ Webhook مسجل بنجاح")
    else:
        logger.warning("⚠️ فشل تسجيل Webhook - تأكد من TELEGRAM_TOKEN و RENDER_EXTERNAL_URL")

    # تشغيل خادم Flask (الخيوط ستبدأ عند أول طلب)
    flask_thread = threading.Thread(target=run_flask, name="Flask", daemon=True)
    flask_thread.start()
    logger.info("🌐 خادم Flask يعمل (الخيوط الخلفية ستُبدأ عند أول طلب)")

    # إرسال رسالة تأكيد بدء التشغيل
    if CHAT_ID and TELEGRAM_TOKEN:
        try:
            test_msg = "🚀 **Tona AI V2.0 FINAL** جاهز للعمل!\n\n💙 أنا هنا لمساعدتك في تحليل النفط والفضة.\n\n📌 استخدم الأزرار أو اكتب /start للقائمة."
            _send_telegram_message_direct(test_msg, CHAT_ID)
            logger.info("📨 تم إرسال رسالة تأكيد بدء التشغيل")
        except Exception as e:
            logger.error(f"❌ فشل إرسال رسالة التأكيد: {e}")

    logger.info("✅ الخادم يعمل - انتظر أول طلب لبدء الخيوط الخلفية.")
    logger.info("💙 Tona AI: أنا هنا لمساعدتك في تحليل النفط والفضة!")

    while True:
        time.sleep(1)
        
# ====================================================================================
# 📦 PART 12: التشغيل الرئيسي
# ====================================================================================

def cleanup_stuck_trades(trading_core: TradingCore):
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
            except Exception as e:
                logger.error(f"❌ فشل تنظيف {asset_type}: {e}")


def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)


def set_webhook() -> bool:
    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN غير موجود")
        return False

    render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if not render_url:
        service_name = os.environ.get('RENDER_SERVICE_NAME', '')
        render_url = f"https://{service_name}.onrender.com" if service_name else os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
        if render_url:
            render_url = f"https://{render_url}"

    if not render_url:
        logger.error("❌ RENDER_EXTERNAL_URL غير موجود - لا يمكن تسجيل Webhook")
        return False

    webhook_url = f"{render_url}/webhook"
    logger.info(f"🔗 محاولة تسجيل Webhook: {webhook_url}")

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        resp = requests.post(url, json={
            "url": webhook_url,
            "allowed_updates": ["message"]
        }, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data.get('ok', False):
                logger.info(f"✅ Webhook مسجل بنجاح: {webhook_url}")
                return True
            else:
                logger.error(f"❌ فشل تسجيل Webhook: {data}")
                return False
        else:
            logger.error(f"❌ خطأ في تسجيل Webhook: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        logger.error(f"❌ استثناء في تسجيل Webhook: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 Tona AI V2.0 FINAL - البوت الاستشاري الذكي")
    logger.info("💙 الاسم: Tona AI")
    logger.info("👨‍💻 المطور: بسام الحوباني")
    logger.info("🧠 جميع التحليلات والتوصيات تعتمد على Gemini + Groq")
    logger.info("=" * 60)

    if not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN غير موجود!")
    else:
        logger.info(f"✅ TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10]}...")

    if not CHAT_ID:
        logger.error("❌ CHAT_ID غير موجود!")
    else:
        logger.info(f"✅ CHAT_ID: {CHAT_ID}")

    os.makedirs("learning_data", exist_ok=True)
    os.makedirs("learning_data/backups", exist_ok=True)

    cleanup_stuck_trades(TRADING_CORE)

    if set_webhook():
        logger.info("✅ Webhook مسجل بنجاح")
    else:
        logger.warning("⚠️ فشل تسجيل Webhook - تأكد من TELEGRAM_TOKEN و RENDER_EXTERNAL_URL")

    flask_thread = threading.Thread(target=run_flask, name="Flask", daemon=True)
    flask_thread.start()
    logger.info("🌐 خادم Flask يعمل")

    if CHAT_ID and TELEGRAM_TOKEN:
        try:
            test_msg = "🚀 **Tona AI V2.0 FINAL** جاهز للعمل!\n\n💙 أنا هنا لمساعدتك في تحليل النفط والفضة.\n\n📌 استخدم الأزرار أو اكتب /start للقائمة."
            _send_telegram_message_direct(test_msg, CHAT_ID)
            logger.info("📨 تم إرسال رسالة تأكيد بدء التشغيل")
        except Exception as e:
            logger.error(f"❌ فشل إرسال رسالة التأكيد: {e}")

    scanner_thread = threading.Thread(target=signal_scanner, args=(TRADING_CORE,), name="Scanner", daemon=True)
    scanner_thread.start()
    logger.info("✅ Thread Scanner بدأ")

    monitor_thread = threading.Thread(target=monitor_loop, args=(TRADING_CORE,), name="Monitor", daemon=True)
    monitor_thread.start()
    logger.info("✅ Thread Monitor بدأ")

    logger.info("✅ جميع الخيوط تعمل - Tona AI جاهز!")
    logger.info("💙 Tona AI: أنا هنا لمساعدتك في تحليل النفط والفضة!")

    while True:
        time.sleep(1)
