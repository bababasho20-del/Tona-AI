# Tona AI Standalone - AI-first signal bot
# IMPORTANT: This file is intentionally independent from the large bot.
# No TA/pandas/numpy/indicator packages are used.
# Signal discovery mirrors the reference V15 logic; AI is called only AFTER BUY/SELL.
# Required env: TELEGRAM_TOKEN, CHAT_ID, GROQ_API_KEY and/or GEMINI_API_KEY.
# Optional: GROQ_MODEL, GEMINI_MODEL, PORT, SCANNER_INTERVAL

import os
import json
import time
import math
import html
import logging
import threading
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

from flask import Flask, request, jsonify

# ----------------------------- logging -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s",
)
log = logging.getLogger("TonaAI")

# ----------------------------- environment -----------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
PORT = int(os.getenv("PORT", "10000"))
SCANNER_INTERVAL = int(os.getenv("SCANNER_INTERVAL", "60"))

# Reference strategy values from main_V15_FIXED.py.
STRATEGY = {
    "oil": {
        "symbol": "USOIL_USDT",
        "base": "Min15",
        "st_mult": 1.5,
        "st_period": 100,
        "vpt_len": 10,
        "confirmation_bars": 1,
        "sl_atr": 2.0,
        "tp_atr": 3.0,
    },
    "silver": {
        "symbol": "SILVER_USDT",
        "base": "Min15",
        "st_mult": 2.2,
        "st_period": 100,
        "vpt_len": 10,
        "confirmation_bars": 1,
        "sl_atr": 2.0,
        "tp_atr": 3.0,
    },
}

# Prevent duplicate scanner calls inside one process.
scan_lock = threading.Lock()
started = False
last_notified_signal = {"oil": None, "silver": None}

# ----------------------------- HTTP helpers -----------------------------
def http_json(url, method="GET", payload=None, headers=None, timeout=20):
    data = None
    hdrs = {"User-Agent": "TonaAI-Standalone/1.0", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    if payload is not None:
        data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, json.loads(raw.decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"error": body}
        raise RuntimeError(f"HTTP {e.code}: {parsed}")
    except Exception as e:
        raise RuntimeError(str(e))

# ----------------------------- MEXC raw candles -----------------------------
def get_mexc_candles(symbol, interval="Min15", limit=200):
    url = (
        "https://contract.mexc.com/api/v1/contract/kline/"
        f"{urllib.parse.quote(symbol)}?interval={urllib.parse.quote(interval)}&limit={limit}"
    )
    status, obj = http_json(url, timeout=10)
    if status != 200 or not obj.get("success") or "data" not in obj:
        return None
    raw = obj["data"]
    keys = ("close", "high", "low", "open", "vol")
    if not all(k in raw for k in keys):
        return None
    n = min(len(raw[k]) for k in keys)
    if n < 5:
        return None
    return {
        "closes": [float(x) for x in raw["close"][:n]],
        "highs": [float(x) for x in raw["high"][:n]],
        "lows": [float(x) for x in raw["low"][:n]],
        "opens": [float(x) for x in raw["open"][:n]],
        "volumes": [float(x) for x in raw["vol"][:n]],
    }

# ----------------------------- exact strategy math -----------------------------
def stdev_population(src, length):
    out = []
    for i in range(len(src)):
        if i < length - 1:
            out.append(0.0)
            continue
        w = [x for x in src[i-length+1:i+1] if math.isfinite(x)]
        if len(w) < 2:
            out.append(0.0)
            continue
        m = sum(w) / len(w)
        out.append(math.sqrt(max(0.0, sum((x-m)**2 for x in w) / len(w))))
    return out

def calculate_vpt_correct(closes, volumes):
    if len(closes) < 2 or len(closes) != len(volumes):
        return None
    vpt = [0.0]
    total = 0.0
    for i in range(1, len(closes)):
        if closes[i] != 0:
            total += volumes[i] * ((closes[i] - closes[i-1]) / closes[i])
        vpt.append(total)
    return vpt

def calculate_atr_rma(highs, lows, closes, length=14):
    n = len(closes)
    if n < length:
        return None
    tr = [0.0] * n
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        tr[i] = max(
            highs[i]-lows[i],
            abs(highs[i]-closes[i-1]),
            abs(lows[i]-closes[i-1]),
        )
    atr = [0.0] * n
    first = sum(tr[:length]) / length
    atr[length-1] = first
    alpha = 1.0 / length
    for i in range(length, n):
        atr[i] = alpha * tr[i] + (1-alpha) * atr[i-1]
    for i in range(length-1):
        atr[i] = first
    return atr

def calculate_supertrend_vpt(data, st_mult, st_period, vpt_len):
    closes, highs, lows, volumes = (
        data["closes"], data["highs"], data["lows"], data["volumes"]
    )
    n = len(closes)
    if n < st_period + 10:
        return None

    v = calculate_vpt_correct(closes, volumes)
    if not v:
        return None

    spread = stdev_population([highs[i]-lows[i] for i in range(n)], 28)
    smooth = []
    for i in range(n):
        w = v[max(0, i-13):i+1]
        smooth.append(sum(w)/len(w))
    vdiff = [v[i]-smooth[i] for i in range(n)]
    vspread = stdev_population(vdiff, 28)

    out = []
    for i in range(n):
        vs = vspread[i] if vspread[i] != 0 else 1.0
        shadow = ((v[i]-smooth[i]) / vs) * spread[i]
        out.append(highs[i]+shadow if shadow > 0 else lows[i]+shadow)

    alpha = 2.0/(vpt_len+1)
    vpt_ema = [out[0]]
    for i in range(1, n):
        vpt_ema.append(alpha*out[i] + (1-alpha)*vpt_ema[-1])

    atr = calculate_atr_rma(highs, lows, closes, st_period)
    if atr is None:
        return None

    src = [(highs[i]+lows[i])/2 for i in range(n)]
    up = [0.0]*n
    down = [0.0]*n
    trend = [1]*n
    st = [0.0]*n

    for i in range(n):
        up_level = src[i] - st_mult*atr[i]
        down_level = src[i] + st_mult*atr[i]
        if i == 0:
            up[i], down[i], trend[i], st[i] = up_level, down_level, 1, up_level
            continue
        up[i] = max(up_level, up[i-1]) if src[i-1] > up[i-1] else up_level
        down[i] = min(down_level, down[i-1]) if src[i-1] < down[i-1] else down_level
        if src[i] > down[i-1]:
            trend[i] = 1
        elif src[i] < up[i-1]:
            trend[i] = -1
        else:
            trend[i] = trend[i-1]
        st[i] = up[i] if trend[i] == 1 else down[i]
    return st, trend, vpt_ema

def detect_signal(asset, data):
    cfg = STRATEGY[asset]
    result = calculate_supertrend_vpt(data, cfg["st_mult"], cfg["st_period"], cfg["vpt_len"])
    if result is None:
        return "WAIT", None
    st, trend, vpt = result
    if len(vpt) < 3 or len(st) < 3 or len(trend) < 3:
        return "WAIT", None

    prev_vpt, prev_st = vpt[-2], st[-2]
    cur_vpt, cur_st = vpt[-1], st[-1]
    crossover = prev_vpt <= prev_st and cur_vpt > cur_st
    crossunder = prev_vpt >= prev_st and cur_vpt < cur_st

    confirmation_ok = False
    if crossover or crossunder:
        confirmation_ok = True
        current_trend = trend[-1]
        for i in range(1, cfg["confirmation_bars"]+1):
            if len(trend) > i and trend[-i] != current_trend:
                confirmation_ok = False
                break

    signal = "BUY" if crossover and confirmation_ok else "SELL" if crossunder and confirmation_ok else "WAIT"
    atr_series = calculate_atr_rma(data["highs"], data["lows"], data["closes"], 14)
    atr = atr_series[-1] if atr_series else None
    price = data["closes"][-1]
    levels = {}
    if atr and atr > 0:
        if signal == "BUY":
            levels = {"sl": price - atr*cfg["sl_atr"], "tp": price + atr*cfg["tp_atr"]}
        elif signal == "SELL":
            levels = {"sl": price + atr*cfg["sl_atr"], "tp": price - atr*cfg["tp_atr"]}
        levels["rr"] = cfg["tp_atr"]/cfg["sl_atr"]
    log.info(
        f"🔍 [{cfg['base']}] {asset}: VPT={vpt[-1]:.6f}, ST={st[-1]:.6f}, "
        f"crossover={crossover}, crossunder={crossunder}"
    )
    return signal, {"price": price, "atr": atr, "levels": levels, "trend": trend[-1]}

# ----------------------------- AI payload -----------------------------
def compact_candles(data, count):
    n = len(data["closes"])
    start = max(0, n-count)
    return [
        [round(data["opens"][i], 6), round(data["highs"][i], 6),
         round(data["lows"][i], 6), round(data["closes"][i], 6),
         round(data["volumes"][i], 4)]
        for i in range(start, n)
    ]

AI_SYSTEM = """أنت Tona AI، محلل تداول فني. لا تخترع إشارة من عندك.
ستصلك إشارة مؤكدة مسبقاً من Scanner مبني على VPT + SuperTrend.
مهمتك بعد وجود الإشارة فقط: إجراء تحليل فني شامل ودقيق وشرح التوصية.
حلل 5m و15m و1h و4h، الاتجاه، الزخم، الحجم، VPT، SuperTrend، RSI، MACD،
ADX، ATR، Bollinger، Stochastic، VWAP، الدعم والمقاومة، المخاطر وRR.
لا تغيّر BUY/SELL إلى إشارة معاكسة. إذا وجدت تعارضاً قوياً اذكره بوضوح.
أخرج JSON فقط بالمفاتيح:
signal, confidence, trend, summary, timeframes, indicators, support, resistance,
risk, sl, tp, rr, recommendation.
"""

def build_ai_payload(asset, signal, trigger, frames):
    # Deliberately compact: AI is called only after a real signal.
    obj = {
        "asset": asset,
        "signal_from_scanner": signal,
        "price": round(trigger["price"], 8),
        "scanner_atr": round(trigger["atr"], 8) if trigger["atr"] else None,
        "scanner_sl": round(trigger["levels"].get("sl", 0), 8),
        "scanner_tp": round(trigger["levels"].get("tp", 0), 8),
        "scanner_rr": trigger["levels"].get("rr"),
        "frames": {
            "5m": compact_candles(frames["5m"], 40),
            "15m": compact_candles(frames["15m"], 80),
            "1h": compact_candles(frames["1h"], 30),
            "4h": compact_candles(frames["4h"], 30),
        },
        "format": "[open,high,low,close,volume], oldest-to-newest"
    }
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

# ----------------------------- AI providers -----------------------------
def groq_analyze(user_text):
    if not GROQ_API_KEY:
        return None
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": AI_SYSTEM},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.2,
        "max_completion_tokens": 900,
    }
    status, obj = http_json(
        "https://api.groq.com/openai/v1/chat/completions",
        method="POST",
        payload=payload,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        timeout=45,
    )
    return obj["choices"][0]["message"]["content"]

def gemini_analyze(user_text):
    if not GEMINI_API_KEY:
        return None
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(GEMINI_MODEL)}:generateContent?key={urllib.parse.quote(GEMINI_API_KEY)}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": AI_SYSTEM}]},
        "contents": [{"parts": [{"text": user_text}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 900},
    }
    status, obj = http_json(url, method="POST", payload=payload, timeout=45)
    return obj["candidates"][0]["content"]["parts"][0]["text"]

def ai_analyze(user_text):
    # One provider call first; fallback only if the first provider is unavailable.
    if GROQ_API_KEY:
        try:
            log.info("🧠 [AI] Groq request — signal already confirmed")
            return groq_analyze(user_text), "Groq"
        except Exception as e:
            log.error(f"[AI/Groq] {e}")
    if GEMINI_API_KEY:
        try:
            log.info("🧠 [AI] Gemini fallback — signal already confirmed")
            return gemini_analyze(user_text), "Gemini"
        except Exception as e:
            log.error(f"[AI/Gemini] {e}")
    return None, None

# ----------------------------- Telegram -----------------------------
def telegram_call(method, payload):
    if not TELEGRAM_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    return http_json(url, method="POST", payload=payload, timeout=20)

def send_telegram(text, chat_id=None, keyboard=True):
    target = str(chat_id or CHAT_ID).strip()
    if not target or not TELEGRAM_TOKEN:
        log.warning("⚠️ Telegram غير مهيأ: CHAT_ID أو TELEGRAM_TOKEN مفقود")
        return
    payload = {"chat_id": target, "text": text[:4090], "parse_mode": "HTML"}
    if keyboard:
        payload["reply_markup"] = {
            "keyboard": [[{"text":"🛢 تحليل النفط"},{"text":"🥈 تحليل الفضة"}]],
            "resize_keyboard": True
        }
    try:
        telegram_call("sendMessage", payload)
    except Exception as e:
        log.error(f"[Telegram] {e}")

def set_webhook():
    if not TELEGRAM_TOKEN:
        return
    base = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    if not base:
        log.warning("⚠️ RENDER_EXTERNAL_URL غير موجود؛ Telegram webhook لن يُفعّل")
        return
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
    url = f"{base}/telegram/webhook"
    payload = {"url": url, "drop_pending_updates": True}
    if secret:
        payload["secret_token"] = secret
    try:
        telegram_call("deleteWebhook", {"drop_pending_updates": True})
        telegram_call("setWebhook", payload)
        log.info(f"📨 [Telegram] webhook جاهز: {url}")
    except Exception as e:
        log.error(f"[Telegram] webhook setup: {e}")

# ----------------------------- comprehensive analysis -----------------------------
def manual_or_signal_analysis(asset, signal=None, chat_id=None):
    cfg = STRATEGY[asset]
    base = get_mexc_candles(cfg["symbol"], cfg["base"], 200)
    if not base:
        send_telegram(f"⚠️ تعذر جلب بيانات {asset}.", chat_id)
        return

    if signal is None:
        signal, trigger = detect_signal(asset, base)
        if signal == "WAIT":
            # Manual analysis is allowed even without a signal.
            atrs = calculate_atr_rma(base["highs"], base["lows"], base["closes"], 14)
            price = base["closes"][-1]
            trigger = {"price": price, "atr": atrs[-1] if atrs else None,
                       "levels": {}, "trend": 0}
    else:
        _, trigger = detect_signal(asset, base)

    frames = {
        "5m": get_mexc_candles(cfg["symbol"], "Min5", 50),
        "15m": base,
        "1h": get_mexc_candles(cfg["symbol"], "Min60", 35),
        "4h": get_mexc_candles(cfg["symbol"], "Hour4", 35),
    }
    if not all(frames.values()):
        send_telegram("⚠️ تعذر اكتمال بيانات الفريمات الأربعة للتحليل.", chat_id)
        return

    if not trigger:
        trigger = {"price": base["closes"][-1], "atr": None, "levels": {}}
    payload = build_ai_payload(asset, signal or "WAIT", trigger, frames)
    log.info(f"📦 [AI] {asset} analysis payload={len(payload.encode())} bytes")
    text, provider = ai_analyze(payload)
    if not text:
        send_telegram("⚠️ تعذر الحصول على تحليل من نماذج الذكاء الاصطناعي حالياً.", chat_id)
        return

    try:
        parsed = json.loads(text)
        body = (
            f"📊 <b>تحليل {('النفط' if asset=='oil' else 'الفضة')} الشامل</b>\n"
            f"💰 السعر: <b>{trigger['price']}</b>\n"
            f"🚨 إشارة الماسح: <b>{signal or 'WAIT'}</b>\n"
            f"🤖 النموذج: <b>{provider}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>التقييم:</b> {html.escape(str(parsed.get('confidence','غير محدد')))}\n"
            f"<b>الاتجاه:</b> {html.escape(str(parsed.get('trend','غير محدد')))}\n\n"
            f"<b>الملخص:</b>\n{html.escape(str(parsed.get('summary','')))}\n\n"
            f"<b>الدعم:</b> {html.escape(str(parsed.get('support','غير محدد')))}\n"
            f"<b>المقاومة:</b> {html.escape(str(parsed.get('resistance','غير محدد')))}\n"
            f"<b>SL:</b> {html.escape(str(parsed.get('sl', trigger['levels'].get('sl',''))))}\n"
            f"<b>TP:</b> {html.escape(str(parsed.get('tp', trigger['levels'].get('tp',''))))}\n"
            f"<b>RR:</b> {html.escape(str(parsed.get('rr', trigger['levels'].get('rr',''))))}\n"
            f"<b>المخاطر:</b> {html.escape(str(parsed.get('risk','')))}\n\n"
            f"<b>التوصية:</b>\n{html.escape(str(parsed.get('recommendation','')))}"
        )
    except Exception:
        # If a model ignores JSON-only instruction, still deliver its text.
        body = (
            f"📊 <b>تحليل {'النفط' if asset=='oil' else 'الفضة'}</b>\n"
            f"🚨 إشارة الماسح: <b>{signal or 'WAIT'}</b>\n"
            f"🤖 النموذج: <b>{provider}</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"{html.escape(text)}"
        )
    send_telegram(body, chat_id)

# ----------------------------- scanner -----------------------------
def scan_asset(asset):
    cfg = STRATEGY[asset]
    try:
        data = get_mexc_candles(cfg["symbol"], cfg["base"], 200)
        if not data:
            log.warning(f"⚠️ [Scanner] تعذر جلب بيانات {asset}")
            return
        signal, trigger = detect_signal(asset, data)
        if signal == "WAIT":
            log.info(f"⏸️ [Scanner] {asset}: لا توجد إشارة — لا يوجد طلب AI")
            return

        # The signal has already been confirmed by the reference strategy.
        log.info(f"🚨 [Scanner] توجد إشارة مؤكدة لـ {asset}: {signal}")
        if last_notified_signal[asset] == signal:
            log.info(f"⏳ [Scanner] تجاهل إشارة {signal} المكررة لـ {asset}")
            return
        last_notified_signal[asset] = signal
        manual_or_signal_analysis(asset, signal=signal, chat_id=CHAT_ID)
    except Exception as e:
        log.exception(f"[Scanner] خطأ في {asset}: {e}")

def scanner_loop():
    log.info("📡 [Scanner] بدأ التشغيل")
    while True:
        started_at = time.time()
        if scan_lock.acquire(blocking=False):
            try:
                log.info("📡 [Scanner] دورة فحص جديدة")
                # No AI is called unless scan_asset detects BUY/SELL.
                scan_asset("oil")
                scan_asset("silver")
            finally:
                scan_lock.release()
        elapsed = time.time() - started_at
        time.sleep(max(1, SCANNER_INTERVAL - elapsed))

# ----------------------------- Telegram webhook -----------------------------
@app.get("/")
def home():
    return jsonify({"ok": True, "service": "Tona AI Standalone", "ai_only_after_signal": True})

@app.get("/ping")
def ping():
    return "pong", 200

@app.post("/telegram/webhook")
def telegram_webhook():
    update = request.get_json(silent=True) or {}
    try:
        msg = update.get("message") or update.get("edited_message") or {}
        chat = msg.get("chat") or {}
        chat_id = str(chat.get("id", ""))
        text = (msg.get("text") or "").strip()

        if not chat_id:
            return jsonify({"ok": True})

        if text in ("/start", "/help"):
            send_telegram(
                "💙 <b>Tona AI</b>\nاختر التحليل الذي تريد طلبه.\n"
                "الماسح يعمل تلقائياً ولا يستدعي AI إلا عند ظهور إشارة مؤكدة.",
                chat_id
            )
        elif "نفط" in text or text == "/oil":
            threading.Thread(target=manual_or_signal_analysis, args=("oil", None, chat_id),
                             name="ManualOil", daemon=True).start()
        elif "فضة" in text or text == "/silver":
            threading.Thread(target=manual_or_signal_analysis, args=("silver", None, chat_id),
                             name="ManualSilver", daemon=True).start()
        elif text:
            send_telegram("استخدم أزرار تحليل النفط أو الفضة.", chat_id)
    except Exception as e:
        log.error(f"[TelegramWebhook] {e}")
    return jsonify({"ok": True})

# ----------------------------- startup -----------------------------
def start_background():
    global started
    if started:
        return
    started = True
    log.info("🚀 [BOOT] Tona AI Standalone — AI فقط بعد الإشارة")
    log.info("🧠 [AI] لا توجد طلبات AI في دورة Scanner إذا كانت الإشارة WAIT")
    set_webhook()
    threading.Thread(target=scanner_loop, name="Scanner", daemon=True).start()
    log.info("✅ [BOOT] Scanner بدأ")

start_background()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
