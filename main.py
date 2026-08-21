# -*- coding: utf-8 -*-
"""
Tona AI Pure V1
نسخة تجريبية مستقلة - محرك التحليل الوحيد هو Gemini/Groq.
لا تعتمد على مكتبات مؤشرات أو محركات خارجية أو pandas/numpy/ta.

المبدأ:
MEXC raw candles -> AI strategy engine -> structured decision -> Telegram

الاستراتيجية المرجعية المحفوظة داخل Prompt:
- الأصل: oil / silver
- الفريم الأساسي: 15m
- التأكيدات: 5m / 1h / 4h
- VPT + SuperTrend
- BUY عند crossover مؤكد
- SELL عند crossunder مؤكد
- confirmation_bars = 1
- SL/TP افتراضيان مبنيان على ATR 14:
  BUY: SL = price - 2*ATR, TP = price + 3*ATR
  SELL: SL = price + 2*ATR, TP = price - 3*ATR
- AI يحسب المؤشرات من الشموع الخام داخليًا ولا توجد دوال مؤشرات محلية.
"""

import os, json, time, logging, threading, re, html
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional
import requests
from flask import Flask, request, jsonify

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

PORT = int(os.getenv("PORT", "10000"))
SIGNAL_CHECK_INTERVAL = int(os.getenv("SIGNAL_CHECK_INTERVAL", "60"))
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "45"))
CANDLES_LIMIT = int(os.getenv("CANDLES_LIMIT", "200"))
STATE_FILE = Path(os.getenv("STATE_FILE", "tona_ai_state.json"))

MEXC_SYMBOLS = {"oil": "USOIL_USDT", "silver": "SILVER_USDT"}
ASSET_NAMES = {"oil": "النفط", "silver": "الفضة"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TonaAI")
logger.setLevel(logging.INFO)
if not logger.handlers:
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s"))
    logger.addHandler(sh)
    try:
        fh = RotatingFileHandler("tona_ai.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
        fh.setFormatter(sh.formatter)
        logger.addHandler(fh)
    except Exception:
        pass

app = Flask(__name__)
STATE_LOCK = threading.Lock()
SEND_LOCK = threading.Lock()
LAST_SCAN = {"oil": 0.0, "silver": 0.0}
RUNNING = True

# ---------------- STATE ----------------
def load_state():
    if not STATE_FILE.exists():
        return {"trades": {}, "history": [], "last_ai": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("تعذر قراءة state")
        return {"trades": {}, "history": [], "last_ai": {}}

STATE = load_state()

def save_state():
    tmp = STATE_FILE.with_suffix(".tmp")
    with STATE_LOCK:
        tmp.write_text(json.dumps(STATE, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(STATE_FILE)

# ---------------- MEXC RAW DATA ----------------
def get_mexc_candles(asset: str, interval: str = "Min15", limit: int = CANDLES_LIMIT) -> Optional[Dict[str, list]]:
    symbol = MEXC_SYMBOLS[asset]
    url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}"
    try:
        r = requests.get(url, params={"interval": interval, "limit": limit},
                          headers={"User-Agent": "Tona-AI-Pure/1.0"}, timeout=12)
        r.raise_for_status()
        body = r.json()
        if not body.get("success") or not body.get("data"):
            logger.warning("MEXC رد غير صالح %s %s: %s", asset, interval, body)
            return None
        d = body["data"]
        keys = ["time", "open", "high", "low", "close", "vol"]
        n = min(len(d.get(k, [])) for k in keys[1:])
        if n < 30:
            return None
        out = {
            "time": [int(x) for x in d.get("time", [])[:n]],
            "opens": [float(x) for x in d["open"][:n]],
            "highs": [float(x) for x in d["high"][:n]],
            "lows": [float(x) for x in d["low"][:n]],
            "closes": [float(x) for x in d["close"][:n]],
            "volumes": [float(x) for x in d["vol"][:n]],
        }
        return out
    except Exception as e:
        logger.error("MEXC error %s/%s: %s", asset, interval, e)
        return None

def compact_candles(data: Dict[str,list], max_rows: int = 160):
    # نرسل بيانات خام كافية للنموذج، مع الحفاظ على حجم الطلب.
    n = len(data["closes"])
    start = max(0, n - max_rows)
    rows = []
    for i in range(start, n):
        rows.append({
            "t": data["time"][i],
            "o": round(data["opens"][i], 6),
            "h": round(data["highs"][i], 6),
            "l": round(data["lows"][i], 6),
            "c": round(data["closes"][i], 6),
            "v": round(data["volumes"][i], 6),
        })
    return rows

# ---------------- AI ----------------
SYSTEM_PROMPT = r"""
أنت Tona AI، محرك التحليل الوحيد في نظام تداول تجريبي.
لا تستخدم أي مصدر خارجي أو مؤشرات محسوبة مسبقاً. احسب ما تحتاجه بنفسك من الشموع الخام.
يجب أن تتبع استراتيجية الدخول المرجعية التالية حرفياً:

1) الفريم الأساسي 15m.
2) الاستراتيجية هي VPT + SuperTrend.
3) VPT يحسب من تغير السعر والحجم، ثم يتم تنعيمه، ويقارن بخط SuperTrend.
4) BUY فقط إذا حدث crossover: كان VPT <= SuperTrend في الشمعة السابقة ثم أصبح VPT > SuperTrend في الحالية.
5) SELL فقط إذا حدث crossunder: كان VPT >= SuperTrend في السابقة ثم أصبح VPT < SuperTrend في الحالية.
6) يلزم تأكيد شمعة واحدة confirmation_bars=1: اتجاه SuperTrend في آخر شمعة يجب أن يطابق اتجاهه الحالي.
7) إذا لم يتحقق الشرط بدقة فالقرار WAIT، ولا تخترع إشارة من الاتجاه العام.
8) استخدم 5m و1h و4h كتأكيد سياقي، لكن لا تحولها إلى بديل عن شرط الإشارة الأساسي.
9) ATR(14) يستخدم فقط لتقدير SL/TP في الإشارة المؤكدة:
   BUY: SL=price-2*ATR, TP=price+3*ATR
   SELL: SL=price+2*ATR, TP=price-3*ATR
10) إذا كانت البيانات غير كافية، decision=WAIT وdata_quality منخفضة.
11) لا تدّعي أنك اتصلت بسوق أو مصدر غير البيانات المرسلة لك.
12) أعد JSON صالحاً فقط، بلا Markdown.

JSON schema:
{
 "decision":"BUY|SELL|WAIT",
 "confidence":0-100,
 "strategy_signal":"BUY|SELL|WAIT",
 "strategy_reason":"...",
 "current_price":number,
 "atr14":number,
 "sl":number,
 "tp":number,
 "rr":number,
 "data_quality":"high|medium|low",
 "timeframe_summary":{"15m":"bullish|bearish|neutral","5m":"bullish|bearish|neutral","1h":"bullish|bearish|neutral","4h":"bullish|bearish|neutral"},
 "analysis":"تحليل عربي مختصر",
 "risk":"low|medium|high",
 "warnings":["..."]
}
"""

def extract_json(text: str) -> Optional[dict]:
    if not text:
        return None
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                obj = json.loads(m.group(0))
                return obj if isinstance(obj, dict) else None
            except Exception:
                return None
    return None

def call_gemini(prompt: str) -> Optional[str]:
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.15, "maxOutputTokens": 1400}
    }
    try:
        r = requests.post(url, params={"key": GEMINI_API_KEY}, json=payload, timeout=AI_TIMEOUT)
        if r.status_code != 200:
            logger.error("Gemini HTTP %s: %s", r.status_code, r.text[:500])
            return None
        parts = r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
        if text:
            logger.info("🧠 Gemini نجح")
            return text.strip()
    except Exception as e:
        logger.error("Gemini exception: %s", e)
    return None

def call_groq(prompt: str) -> Optional[str]:
    if not GROQ_API_KEY:
        return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 1400,
        "response_format": {"type": "json_object"}
    }
    try:
        r = requests.post(url, headers={"Authorization": f"Bearer {GROQ_API_KEY}",
                                         "Content-Type": "application/json"},
                          json=payload, timeout=AI_TIMEOUT)
        if r.status_code != 200:
            logger.error("Groq HTTP %s: %s", r.status_code, r.text[:500])
            return None
        text = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        if text:
            logger.info("🧠 Groq نجح")
            return text.strip()
    except Exception as e:
        logger.error("Groq exception: %s", e)
    return None

def ai_analyze(asset: str, frames: Dict[str, Dict], open_trade: Optional[dict] = None) -> Optional[dict]:
    payload = {
        "asset": ASSET_NAMES[asset],
        "asset_code": asset,
        "reference_strategy": "VPT + SuperTrend; 15m base; confirmation=1; ATR14 SL=2x TP=3x",
        "frames": {tf: compact_candles(data) for tf, data in frames.items() if data},
        "open_trade": open_trade
    }
    prompt = SYSTEM_PROMPT + "\n\nحلل البيانات التالية. التزم بالـJSON فقط:\n" + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # Gemini لا يحتاج system endpoint منفصلاً في هذا التصميم.
    for name, fn in (("Gemini", call_gemini), ("Groq", call_groq)):
        raw = fn(prompt)
        obj = extract_json(raw)
        if obj:
            obj["_model"] = name
            return obj
        if raw:
            logger.warning("%s أعاد نصاً غير JSON", name)
    return None

# ---------------- TELEGRAM ----------------
def tg(method: str, payload: dict):
    if not TELEGRAM_TOKEN:
        return None
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}",
                          json=payload, timeout=15)
        return r.json()
    except Exception as e:
        logger.error("Telegram %s error: %s", method, e)
        return None

def send_message(chat_id: str, text: str):
    if not chat_id:
        return
    with SEND_LOCK:
        tg("sendMessage", {"chat_id": chat_id, "text": text,
                           "parse_mode": "HTML", "disable_web_page_preview": True})

def esc(s):
    return html.escape(str(s), quote=False)

def format_analysis(asset: str, a: dict, manual=False):
    d = a.get("decision", "WAIT")
    emoji = "🟢" if d == "BUY" else "🔴" if d == "SELL" else "⚪"
    p = a.get("current_price", 0)
    sl, tp = a.get("sl", 0), a.get("tp", 0)
    frames = a.get("timeframe_summary", {})
    return (
        f"📊 <b>تحليل {esc(ASSET_NAMES[asset])}</b>\n"
        f"💰 السعر: <b>${p:.4f}</b>\n"
        f"{emoji} القرار: <b>{esc(d)}</b> | الثقة: <b>{a.get('confidence',0)}/100</b>\n"
        f"🧠 النموذج: {esc(a.get('_model','AI'))}\n"
        f"📐 ATR14: {a.get('atr14',0):.6f}\n"
        f"🛡️ SL: ${sl:.4f} | 🎯 TP: ${tp:.4f} | RR: {a.get('rr',0):.2f}\n"
        f"📈 15m: {esc(frames.get('15m','-'))} | 5m: {esc(frames.get('5m','-'))} | "
        f"1h: {esc(frames.get('1h','-'))} | 4h: {esc(frames.get('4h','-'))}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔎 <b>سبب الاستراتيجية:</b> {esc(a.get('strategy_reason','-'))}\n\n"
        f"🧠 <b>تحليل Tona AI:</b>\n{esc(a.get('analysis','-'))}\n\n"
        f"⚠️ المخاطر: {esc(a.get('risk','-'))}\n"
        + (f"🚨 تحذيرات: {esc(' | '.join(map(str,a.get('warnings',[]))))}\n" if a.get('warnings') else "")
        + "💙 Tona AI"
    )

# ---------------- MARKET ANALYSIS / SCANNER ----------------
def collect_frames(asset: str):
    intervals = {"15m": "Min15", "5m": "Min5", "1h": "Min60", "4h": "Hour4"}
    frames = {}
    for tf, interval in intervals.items():
        frames[tf] = get_mexc_candles(asset, interval, CANDLES_LIMIT)
        if frames[tf]:
            logger.info("📥 %s %s: %d شمعة", asset, tf, len(frames[tf]["closes"]))
        else:
            logger.warning("📥 %s %s: لا توجد بيانات", asset, tf)
    return frames

def get_open_trade(asset):
    with STATE_LOCK:
        return dict(STATE.get("trades", {}).get(asset) or {}) or None

def open_trade(asset, decision, a):
    trade = {
        "asset": asset, "type": decision,
        "entry_price": a["current_price"], "sl": a.get("sl", 0), "tp": a.get("tp", 0),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": a.get("_model"), "confidence": a.get("confidence", 0)
    }
    with STATE_LOCK:
        STATE.setdefault("trades", {})[asset] = trade
    save_state()
    return trade

def close_trade(asset, reason, price=None):
    with STATE_LOCK:
        t = STATE.setdefault("trades", {}).pop(asset, None)
        if not t:
            return None
        t["close_price"] = price
        t["close_reason"] = reason
        t["closed_at"] = datetime.utcnow().isoformat() + "Z"
        STATE.setdefault("history", []).append(t)
    save_state()
    return t

def evaluate(asset: str, manual=False, chat_id=None):
    logger.info("🔎 [Scanner] بدء فحص %s | manual=%s", asset, manual)
    frames = collect_frames(asset)
    if not frames.get("15m") or len(frames["15m"]["closes"]) < 30:
        msg = f"⚠️ لا توجد بيانات 15m كافية لتحليل {ASSET_NAMES[asset]}."
        if manual: send_message(chat_id, msg)
        return None

    trade = get_open_trade(asset)
    result = ai_analyze(asset, frames, trade)
    if not result:
        logger.error("❌ [AI] لم يتم الحصول على JSON صالح لـ %s", asset)
        if manual: send_message(chat_id, "⚠️ تعذر الحصول على تحليل صالح من Gemini/Groq. راجع السجل.")
        return None

    STATE.setdefault("last_ai", {})[asset] = result
    save_state()

    decision = result.get("decision", "WAIT")
    strategy_signal = result.get("strategy_signal", decision)
    # الحماية: القرار التنفيذي لا يتجاوز إشارة الاستراتيجية التي أعادها AI.
    if decision not in ("BUY","SELL","WAIT") or strategy_signal not in ("BUY","SELL","WAIT"):
        decision = strategy_signal = "WAIT"

    if not manual:
        if strategy_signal == "WAIT":
            logger.info("⏳ [Scanner] %s: لا توجد إشارة مؤكدة", asset)
            return result
        if trade and trade.get("type") == strategy_signal:
            logger.info("⏳ [Scanner] %s: إشارة %s مكررة، الصفقة موجودة", asset, strategy_signal)
            return result
        if trade and trade.get("type") != strategy_signal:
            close_trade(asset, f"إشارة معاكسة {strategy_signal}", result.get("current_price"))
        open_trade(asset, strategy_signal, result)
        logger.info("🚨 [Scanner] إشارة %s مؤكدة لـ %s | price=%s", strategy_signal, asset, result.get("current_price"))

    if manual:
        send_message(chat_id, format_analysis(asset, result, True))
    else:
        # إرسال الإشارة المؤكدة فقط
        send_message(os.getenv("TELEGRAM_CHAT_ID",""), format_analysis(asset, result))
    return result

def scanner_loop():
    logger.info("📡 [Scanner] بدأ التشغيل — AI ONLY — كل %ss", SIGNAL_CHECK_INTERVAL)
    while RUNNING:
        cycle = time.time()
        logger.info("📡 [Scanner] دورة فحص جديدة بدأت")
        for asset in ("oil", "silver"):
            try:
                evaluate(asset, manual=False)
            except Exception:
                logger.exception("❌ [Scanner] خطأ في %s", asset)
        elapsed = time.time() - cycle
        sleep_for = max(1, SIGNAL_CHECK_INTERVAL - elapsed)
        logger.info("📡 [Scanner] انتهاء الدورة، النوم %ss", int(sleep_for))
        time.sleep(sleep_for)

# ---------------- TELEGRAM WEBHOOK ----------------
def telegram_update(update):
    msg = update.get("message") or {}
    chat = msg.get("chat", {})
    chat_id = str(chat.get("id", ""))
    text = (msg.get("text") or "").strip()
    if not chat_id:
        return
    if text in ("/start", "/help"):
        send_message(chat_id,
            "💙 <b>Tona AI Pure</b>\n\n"
            "🧠 المحرك التحليلي: Gemini/Groq فقط\n"
            "📡 /oil — تحليل النفط\n"
            "🥈 /silver — تحليل الفضة\n"
            "📊 /status — الصفقات الحالية\n"
            "🔍 /scan — فحص فوري")
    elif text == "/oil":
        threading.Thread(target=evaluate, args=("oil", True, chat_id), daemon=True).start()
    elif text == "/silver":
        threading.Thread(target=evaluate, args=("silver", True, chat_id), daemon=True).start()
    elif text == "/scan":
        threading.Thread(target=lambda: (evaluate("oil", True, chat_id), evaluate("silver", True, chat_id)), daemon=True).start()
    elif text == "/status":
        t1, t2 = get_open_trade("oil"), get_open_trade("silver")
        send_message(chat_id, "📊 <b>الحالة</b>\n" +
                     (f"🛢️ النفط: {t1['type']} @ {t1['entry_price']}\n" if t1 else "🛢️ النفط: لا توجد صفقة\n") +
                     (f"🥈 الفضة: {t2['type']} @ {t2['entry_price']}\n" if t2 else "🥈 الفضة: لا توجد صفقة\n"))

@app.post("/webhook")
def webhook():
    try:
        telegram_update(request.get_json(silent=True) or {})
    except Exception:
        logger.exception("Webhook error")
    return jsonify({"ok": True})

@app.get("/")
def home():
    return "Tona AI Pure V1 is running", 200

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "ai": {"gemini": bool(GEMINI_API_KEY), "groq": bool(GROQ_API_KEY)},
        "scanner": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

# ---------------- STARTUP ----------------
def validate_config():
    missing = []
    if not TELEGRAM_TOKEN: missing.append("TELEGRAM_TOKEN")
    if not GEMINI_API_KEY and not GROQ_API_KEY: missing.append("GEMINI_API_KEY أو GROQ_API_KEY")
    if missing:
        logger.warning("⚠️ متغيرات ناقصة: %s", ", ".join(missing))
    else:
        logger.info("✅ إعدادات AI وTelegram موجودة")

def set_webhook():
    if not TELEGRAM_TOKEN:
        return
    base = os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    if not base:
        host = os.getenv("RENDER_EXTERNAL_HOSTNAME", "")
        base = f"https://{host}" if host else ""
    if not base:
        logger.warning("⚠️ لا يوجد RENDER_EXTERNAL_URL؛ لن يتم تسجيل webhook")
        return
    res = tg("setWebhook", {"url": base + "/webhook", "allowed_updates": ["message"]})
    logger.info("🔗 Webhook: %s", res)

def main():
    validate_config()
    logger.info("🚀 Tona AI Pure V1 starting")
    logger.info("🧠 Architecture: RAW MEXC -> Gemini/Groq -> JSON -> Telegram")
    logger.info("🚫 No pandas/numpy/ta/external strategy engines")
    save_state()
    threading.Thread(target=scanner_loop, name="AI-Scanner", daemon=True).start()
    logger.info("✅ [BOOT] Scanner thread started")
    set_webhook()
    app.run(host="0.0.0.0", port=PORT, threaded=True, use_reloader=False)

if __name__ == "__main__":
    main()
