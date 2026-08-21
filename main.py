# -*- coding: utf-8 -*-
"""
Tona AI Pure V1
نسخة تجريبية مستقلة - محرك التحليل الوحيد هو Gemini/Groq.
لا تعتمد على مكتبات مؤشرات أو محركات خارجية أو pandas/numpy/ta.
# -*- coding: utf-8 -*-
"""
Tona AI Standalone V2

هدف النسخة:
- نسخة مستقلة بالكامل من البوت العملاق، بدون محركات تحليل خارجية أو مكتبات TA.
- المصدر المرجعي لسلوك استراتيجية الدخول هو main_V15_FIXED.py.
- الحسابات الفنية التي كانت تُنفذ برمجياً في البوت العملاق أصبحت تعليمات صريحة
  لنماذج Gemini/Groq. البوت نفسه يقتصر على جلب البيانات الخام، تشغيل النموذج،
  إدارة الحالة، Telegram، والمراقبة.
- لا تستخدم pandas/numpy/ta أو Prometheus/Chronos/Oracle/Supabase/Gist وغيرها.

متغيرات البيئة:
TELEGRAM_TOKEN, CHAT_ID
GROQ_API_KEY و/أو GEMINI_API_KEY
GROQ_MODEL (افتراضي: openai/gpt-oss-120b)
GEMINI_MODEL (افتراضي: gemini-3.5-flash)
SIGNAL_CHECK_INTERVAL (افتراضي 60)
MONITORING_INTERVAL (افتراضي 300)
INITIAL_BALANCE (افتراضي 10000)

هذه النسخة تداول افتراضي فقط؛ لا ترسل أوامر فتح/إغلاق إلى منصة تداول.
"""

import os, json, time, logging, threading, urllib.request, urllib.parse, urllib.error, html, re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ----------------------------- Logging -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s",
)
logger = logging.getLogger("TonaAIStandalone")

# ----------------------------- Config -----------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
SIGNAL_CHECK_INTERVAL = int(os.getenv("SIGNAL_CHECK_INTERVAL", "60"))
MONITORING_INTERVAL = int(os.getenv("MONITORING_INTERVAL", "300"))
INITIAL_BALANCE = float(os.getenv("INITIAL_BALANCE", "10000"))
HTTP_TIMEOUT = 15

ASSETS = {
    "oil": {"label": "النفط الخام", "symbol": "USOIL_USDT", "base": "Min15", "st_mult": 2.5},
    "silver": {"label": "الفضة", "symbol": "SILVER_USDT", "base": "Min15", "st_mult": 2.2},
}
TIMEFRAMES = {
    "5m": ("Min5", 120),
    "15m": ("Min15", 200),
    "1h": ("Min60", 120),
    "4h": ("Hour4", 120),
}

STATE_LOCK = threading.RLock()
POSITION_FILES = {a: f"current_position_{a}.json" for a in ASSETS}
TRADE_FILES = {a: f"trades_history_{a}.json" for a in ASSETS}
POSITIONS = {"oil": None, "silver": None}
LAST_SIGNAL = {"oil": {"signal": "WAIT", "time": 0}, "silver": {"signal": "WAIT", "time": 0}}
LAST_UPDATE_ID = None

# ----------------------------- HTTP helpers -----------------------------
def http_json(url, method="GET", payload=None, headers=None, timeout=HTTP_TIMEOUT):
    data = None
    hdr = {"User-Agent": "TonaAIStandalone/2.0", "Accept": "application/json"}
    if headers:
        hdr.update(headers)
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        hdr["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdr, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", errors="replace")
        return json.loads(raw)

# ----------------------------- MEXC raw market data -----------------------------
def get_mexc_candles(symbol, interval="Min15", limit=200):
    """مطابق لمسار MEXC في البوت الأصلي، لكن بدون requests/pandas."""
    url = f"https://contract.mexc.com/api/v1/contract/kline/{urllib.parse.quote(symbol)}?interval={urllib.parse.quote(interval)}&limit={limit}"
    try:
        obj = http_json(url)
        if not obj.get("success") or "data" not in obj:
            logger.warning("[MEXC] استجابة غير صالحة %s/%s", symbol, interval)
            return None
        raw = obj["data"]
        keys = ("close", "high", "low", "open", "vol")
        if any(k not in raw for k in keys):
            return None
        n = min(*(len(raw[k]) for k in keys))
        if n < 5:
            return None
        return {
            "closes": [float(x) for x in raw["close"][:n]],
            "highs": [float(x) for x in raw["high"][:n]],
            "lows": [float(x) for x in raw["low"][:n]],
            "opens": [float(x) for x in raw["open"][:n]],
            "volumes": [float(x) for x in raw["vol"][:n]],
        }
    except Exception as e:
        logger.error("[MEXC] %s %s: %s", symbol, interval, e)
        return None


def fetch_market(asset):
    cfg = ASSETS[asset]
    result = {}
    for name, (interval, limit) in TIMEFRAMES.items():
        result[name] = get_mexc_candles(cfg["symbol"], interval, limit)
    return result

# ----------------------------- Local state -----------------------------
def load_state():
    global POSITIONS
    with STATE_LOCK:
        for asset, path in POSITION_FILES.items():
            try:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        POSITIONS[asset] = json.load(f)
            except Exception as e:
                logger.warning("[STATE] تعذر تحميل %s: %s", path, e)


def save_position(asset):
    path = POSITION_FILES[asset]
    with STATE_LOCK:
        pos = POSITIONS.get(asset)
        if pos is None:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                pass
            return
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(pos, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)


def load_trades(asset):
    try:
        with open(TRADE_FILES[asset], "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_trade(asset, trade):
    path = TRADE_FILES[asset]
    rows = load_trades(asset)
    rows.append(trade)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(rows[-1000:], f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

# ----------------------------- AI Strategy Contract -----------------------------
SYSTEM_PROMPT = r"""
أنت Tona AI، محرك التحليل والاستراتيجية في بوت تداول مستقل.
مهمتك تنفيذ قواعد الاستراتيجية المرجعية بدقة، ثم تقديم تحليل شامل باللغة العربية.
لا تخترع أي بيانات. كل قرار يجب أن يستند فقط إلى بيانات الشموع الخام المرسلة لك.

=== الاستراتيجية المرجعية التي يجب الحفاظ عليها ===
1) الفريم الأساسي للإشارة هو 15m.
2) تستخدم الاستراتيجية VPT + SuperTrend بالشكل التالي:
   VPT:
   vpt[0]=0. لكل شمعة i من 1 إلى النهاية:
   vpt[i] = vpt[i-1] + volume[i] * ((close[i]-close[i-1]) / close[i])
   (المقام هو close الحالي، كما في النسخة المرجعية).

   VPT/SuperTrend التحويلي المرجعي:
   - spread السعر = الانحراف المعياري السكاني المتحرك لـ(high-low) بطول 28.
   - smooth_vpt = متوسط VPT المتحرك بطول 14.
   - v_diff = VPT - smooth_vpt.
   - v_spread = الانحراف المعياري السكاني المتحرك لـ v_diff بطول 28.
   - shadow = ((VPT-smooth_vpt)/v_spread) * price_spread.
   - out = high + shadow إذا shadow>0، وإلا low + shadow.
   - VPT EMA بطول 10 على out (alpha=2/(10+1)).

   SuperTrend المرجعي:
   - المصدر = (high+low)/2.
   - ATR يستخدم RMA/Wilder بطول 100.
   - st_multiplier للنفط 2.5 وللفضة 2.2.
   - up = source - multiplier*ATR، down = source + multiplier*ATR.
   - تحديث up/down/trend بنفس منطق SuperTrend التقليدي المرجعي.
3) إشارة BUY فقط عندما:
   previous VPT_EMA <= previous SuperTrend AND current VPT_EMA > current SuperTrend
   مع تحقق شمعة تأكيد واحدة على الأقل (اتجاه SuperTrend الحالي ثابت).
4) إشارة SELL فقط عندما:
   previous VPT_EMA >= previous SuperTrend AND current VPT_EMA < current SuperTrend
   مع تحقق شمعة تأكيد واحدة على الأقل.
5) إذا لم يتحقق crossover/crossunder المؤكد فالقرار WAIT.
6) لا تحول تحيزاً عاماً أو توقعاً إلى BUY/SELL إذا لم يتحقق شرط الاستراتيجية.
7) 5m و1h و4h للتأكيد والسياق فقط، ولا تستبدل 15m كفريم إشارة.
8) ATR14 يستخدم لإدارة الصفقة المرجعية:
   BUY: SL=price-2*ATR14 و TP=price+3*ATR14.
   SELL: SL=price+2*ATR14 و TP=price-3*ATR14.
   RR المستهدف 3/2=1.5.
9) إذا كانت البيانات غير كافية أو الحساب غير مؤكد، استخدم WAIT واذكر السبب.

=== التحليل الذكي ===
بعد تحديد signal وفق القواعد السابقة، حلل الاتجاه والزخم والتقلب والحجم والدعم/المقاومة
والفريمات الأخرى والأخبار فقط إذا كانت البيانات متاحة. لا تخترع أخباراً.

=== الإخراج الإلزامي ===
أعد JSON صالحاً فقط، بلا Markdown وبلا نص قبله أو بعده:
{
 "signal":"BUY|SELL|WAIT",
 "confidence":0-100,
 "price":number,
 "atr14":number|null,
 "sl":number|null,
 "tp":number|null,
 "rr":number|null,
 "strategy_check":{
   "vpt_previous":number|null,"st_previous":number|null,
   "vpt_current":number|null,"st_current":number|null,
   "crossover":true|false,"crossunder":true|false,
   "confirmation_ok":true|false
 },
 "trend":"صاعد|هابط|محايد",
 "risk":"منخفض|متوسط|مرتفع",
 "support":number|null,
 "resistance":number|null,
 "summary":"...",
 "analysis":"تحليل عربي مفصل وقصير بما يكفي لتيليجرام"
}
"""


def market_payload(asset, market):
    cfg = ASSETS[asset]
    # نحافظ على البيانات الخام ولا نحسب مؤشرات خارجية.
    return {
        "asset": asset,
        "label": cfg["label"],
        "symbol": cfg["symbol"],
        "strategy_parameters": {"base_timeframe": "15m", "st_multiplier": cfg["st_mult"], "st_period": 100, "vpt_len": 10, "confirmation_bars": 1, "sl_atr_mult": 2.0, "tp_atr_mult": 3.0},
        "timeframes": market,
    }

# ----------------------------- AI Providers -----------------------------
def groq_call(system, user):
    if not GROQ_API_KEY:
        return None
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {"model": GROQ_MODEL, "temperature": 0.1, "messages": [{"role":"system","content":system},{"role":"user","content":user}]}
    try:
        obj = http_json(url, "POST", payload, {"Authorization": f"Bearer {GROQ_API_KEY}"}, 35)
        return obj["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error("[AI/Groq] فشل الطلب: %s", e)
        return None


def gemini_call(system, user):
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(GEMINI_MODEL)}:generateContent?key={urllib.parse.quote(GEMINI_API_KEY)}"
    payload = {"systemInstruction":{"parts":[{"text":system}]},"contents":[{"role":"user","parts":[{"text":user}]}],"generationConfig":{"temperature":0.1,"responseMimeType":"application/json"}}
    try:
        obj = http_json(url, "POST", payload, timeout=35)
        return obj["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logger.error("[AI/Gemini] فشل الطلب: %s", e)
        return None


def extract_json(text):
    if not text:
        return None
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


def ai_analyze(asset, market, mode="scanner", position=None):
    payload = market_payload(asset, market)
    if position:
        payload["open_position"] = position
    user = json.dumps({"mode": mode, "market": payload}, ensure_ascii=False, separators=(",", ":"))

    raw = None
    provider = None
    if GROQ_API_KEY:
        raw = groq_call(SYSTEM_PROMPT, user)
        provider = "Groq"
    if not raw and GEMINI_API_KEY:
        raw = gemini_call(SYSTEM_PROMPT, user)
        provider = "Gemini"
    if not raw:
        return None
    result = extract_json(raw)
    if not result:
        logger.error("[AI] %s أعاد نصاً غير JSON", provider)
        return None
    result["provider"] = provider
    result["raw_model_response"] = raw
    return result

# ----------------------------- Telegram -----------------------------
def telegram(method, payload=None):
    if not TELEGRAM_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    try:
        return http_json(url, "POST", payload or {}, {"Content-Type":"application/json"}, 15)
    except Exception as e:
        logger.error("[Telegram] %s: %s", method, e)
        return None


def send_message(text, chat_id=None):
    cid = chat_id or CHAT_ID
    if not cid:
        logger.warning("[Telegram] لا يوجد CHAT_ID")
        return False
    result = telegram("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML"})
    return bool(result and result.get("ok"))


def menu(chat_id):
    kb = {"keyboard":[["🛢️ تحليل النفط","🥈 تحليل الفضة"],["🔍 وضع الصفقة الحالية","📊 تقرير الأداء"],["🔍 تحليل الصفقة الأخيرة","🧠 تحليل عميق"],["❌ إغلاق الصفقة"]],"resize_keyboard":True}
    telegram("sendMessage", {"chat_id":chat_id,"text":"<b>🤖 Tona AI Standalone V2</b>\n\nمحرك التحليل يعتمد على Gemini/Groq والبيانات الخام فقط.","parse_mode":"HTML","reply_markup":kb})

# ----------------------------- Formatting -----------------------------
def fmt_num(x, digits=4):
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return "—"


def format_analysis(asset, result, manual=True):
    label = ASSETS[asset]["label"]
    sig = str(result.get("signal", "WAIT")).upper()
    emoji = "🟢 BUY" if sig == "BUY" else "🔴 SELL" if sig == "SELL" else "⚪ WAIT"
    lines = [
        f"📊 <b>تحليل {label}</b>",
        f"💰 السعر: <b>${fmt_num(result.get('price'), 2)}</b>",
        f"🎯 الإشارة: <b>{emoji}</b>",
        f"🧠 الثقة: <b>{fmt_num(result.get('confidence'), 0)}%</b>",
        f"⚠️ الخطر: <b>{html.escape(str(result.get('risk','غير معروف')))}</b>",
    ]
    if sig in ("BUY", "SELL"):
        lines += [f"🛑 SL: ${fmt_num(result.get('sl'),2)}", f"🎯 TP: ${fmt_num(result.get('tp'),2)}", f"📐 RR: {fmt_num(result.get('rr'),2)}"]
    lines += ["━━━━━━━━━━━━━━━━", "🧠 <b>Tona AI:</b>", html.escape(str(result.get("analysis") or result.get("summary") or "لا يوجد تحليل نصي."))]
    return "\n".join(lines)

# ----------------------------- Trading state -----------------------------
def current_position(asset):
    with STATE_LOCK:
        return dict(POSITIONS[asset]) if POSITIONS[asset] else None


def profit_pct(pos, price):
    if not pos or not pos.get("entry_price"):
        return 0.0
    entry = float(pos["entry_price"])
    return ((price-entry)/entry*100) if pos["type"] == "BUY" else ((entry-price)/entry*100)


def close_position(asset, reason, price=None):
    with STATE_LOCK:
        pos = POSITIONS.get(asset)
        if not pos:
            return False
        close_price = float(price or pos.get("last_price") or pos["entry_price"])
        pp = profit_pct(pos, close_price)
        trade = dict(pos)
        trade.update({"exit_price":close_price,"exit_time":datetime.utcnow().isoformat(),"profit_pct":pp,"reason":reason,"status":"CLOSED"})
        save_trade(asset, trade)
        POSITIONS[asset] = None
        save_position(asset)
    logger.info("[Trade] أغلقت %s %s عند %.5f بسبب %s (%.2f%%)", asset, trade["type"], close_price, reason, pp)
    return True


def maybe_open_or_reverse(asset, result):
    sig = str(result.get("signal","WAIT")).upper()
    if sig not in ("BUY","SELL"):
        return False
    price = float(result.get("price") or 0)
    if price <= 0:
        return False
    with STATE_LOCK:
        pos = POSITIONS.get(asset)
        if pos:
            if pos.get("type") == sig:
                logger.info("[Scanner] تجاهل %s المكرر: توجد صفقة %s", asset, sig)
                return False
            close_position(asset, f"إشارة معاكسة ({sig})", price)
        POSITIONS[asset] = {
            "asset":asset,"type":sig,"entry_price":price,"sl":result.get("sl"),"tp":result.get("tp"),
            "rr":result.get("rr"),"confidence":result.get("confidence"),"entry_time":datetime.utcnow().isoformat(),
            "last_price":price,"provider":result.get("provider"),"status":"OPEN"
        }
        save_position(asset)
    logger.info("🚨 [Scanner] إشارة مؤكدة لـ %s: %s", asset, sig)
    send_message(format_analysis(asset, result, False) + "\n\n✅ <b>تم فتح صفقة افتراضية.</b>")
    return True

# ----------------------------- Analysis entrypoint -----------------------------
def analyze_and_send(asset, is_manual=False, chat_id=None):
    try:
        logger.info("🔎 [Analyze] بدء %s | manual=%s", asset, is_manual)
        market = fetch_market(asset)
        if not market.get("15m"):
            logger.error("[Analyze] بيانات 15m غير متاحة لـ %s", asset)
            if is_manual: send_message("⚠️ تعذر جلب بيانات السوق حالياً.", chat_id)
            return None
        result = ai_analyze(asset, market, "manual" if is_manual else "scanner", current_position(asset))
        if not result:
            if is_manual: send_message("⚠️ تعذر الحصول على تحليل من Gemini/Groq حالياً.", chat_id)
            return None
        # حماية أساسية: لا نقبل إلا الإشارات المحددة في عقد الاستراتيجية.
        if str(result.get("signal","WAIT")).upper() not in ("BUY","SELL","WAIT"):
            result["signal"] = "WAIT"
        logger.info("🧠 [AI] %s | provider=%s | signal=%s | confidence=%s", asset, result.get("provider"), result.get("signal"), result.get("confidence"))
        if is_manual:
            send_message(format_analysis(asset, result, True), chat_id)
        else:
            maybe_open_or_reverse(asset, result)
        return result
    except Exception as e:
        logger.exception("[Analyze] خطأ في %s: %s", asset, e)
        if is_manual: send_message("⚠️ حدث خطأ أثناء التحليل.", chat_id)
        return None

# ----------------------------- Scanner -----------------------------
def signal_scanner():
    logger.info("📡 [Scanner] بدأ التشغيل | interval=%ss | assets=oil,silver", SIGNAL_CHECK_INTERVAL)
    while True:
        started = time.time()
        logger.info("📡 [Scanner] دورة فحص جديدة بدأت")
        for asset in ASSETS:
            try:
                analyze_and_send(asset, False, None)
            except Exception as e:
                logger.exception("[Scanner] خطأ في %s: %s", asset, e)
        elapsed = time.time() - started
        logger.info("📡 [Scanner] انتهت الدورة خلال %.1fs", elapsed)
        time.sleep(max(1, SIGNAL_CHECK_INTERVAL - elapsed))

# ----------------------------- Position monitor -----------------------------
def monitor_positions():
    logger.info("👁️ [Monitor] بدأ التشغيل | interval=%ss", MONITORING_INTERVAL)
    while True:
        started = time.time()
        for asset in ASSETS:
            try:
                pos = current_position(asset)
                if not pos:
                    continue
                market = fetch_market(asset)
                data = market.get("15m")
                if not data:
                    continue
                price = data["closes"][-1]
                pos["last_price"] = price
                save_position(asset)
                sl, tp = pos.get("sl"), pos.get("tp")
                hit = None
                if sl is not None and tp is not None:
                    if pos["type"] == "BUY":
                        if price <= float(sl): hit = "SL"
                        elif price >= float(tp): hit = "TP"
                    else:
                        if price >= float(sl): hit = "SL"
                        elif price <= float(tp): hit = "TP"
                if hit:
                    close_position(asset, f"تم الوصول إلى {hit}", price)
                    send_message(f"🔔 <b>{ASSETS[asset]['label']}</b>\nتم إغلاق الصفقة الافتراضية بسبب {hit}.\nالسعر: ${price:.4f}")
                    continue
                # AI monitoring: يستخدم النموذج لتقييم صحة الصفقة، لا لتغيير قواعد الدخول السابقة.
                result = ai_analyze(asset, market, "monitor", pos)
                if result:
                    logger.info("[Monitor/AI] %s signal=%s confidence=%s", asset, result.get("signal"), result.get("confidence"))
                    analysis = str(result.get("analysis") or "")
                    # لا نغلق تلقائياً بسبب رأي AI؛ الإغلاق التلقائي هنا SL/TP فقط.
                    if result.get("risk") == "مرتفع" and analysis:
                        send_message(f"⚠️ <b>تحذير AI — {ASSETS[asset]['label']}</b>\n{html.escape(analysis[:1500])}")
            except Exception as e:
                logger.exception("[Monitor] خطأ في %s: %s", asset, e)
        elapsed = time.time() - started
        time.sleep(max(5, MONITORING_INTERVAL - elapsed))

# ----------------------------- Telegram commands -----------------------------
def stats_text():
    out = ["📊 <b>تقرير الأداء</b>"]
    total = 0; wins = 0
    for asset in ASSETS:
        rows = load_trades(asset)
        total += len(rows); wins += sum(1 for r in rows if float(r.get("profit_pct",0)) > 0)
        out.append(f"• {ASSETS[asset]['label']}: {len(rows)} صفقة")
    out.append(f"\n📈 الإجمالي: {total}\n🏆 رابحة: {wins}")
    if total: out.append(f"🎯 نسبة الفوز: {wins/total*100:.1f}%")
    return "\n".join(out)


def position_text():
    rows=[]
    for asset in ASSETS:
        p=current_position(asset)
        if not p:
            rows.append(f"• {ASSETS[asset]['label']}: لا توجد صفقة")
        else:
            rows.append(f"• {ASSETS[asset]['label']}: {p['type']} | دخول ${p['entry_price']:.4f} | SL ${float(p['sl']):.4f} | TP ${float(p['tp']):.4f}")
    return "🔍 <b>وضع الصفقات الحالية</b>\n"+"\n".join(rows)


def handle_text(text, chat_id):
    t = text.strip()
    if t in ("/start","/menu","قائمة","منيو","القائمة"):
        menu(chat_id); return
    if t in ("🛢️ تحليل النفط","نفط","oil","تحليل النفط"):
        send_message("🔍 جاري تحليل النفط بواسطة AI...", chat_id); threading.Thread(target=analyze_and_send,args=("oil",True,chat_id),daemon=True,name="Manual-Oil").start(); return
    if t in ("🥈 تحليل الفضة","فضة","silver","تحليل الفضة"):
        send_message("🔍 جاري تحليل الفضة بواسطة AI...", chat_id); threading.Thread(target=analyze_and_send,args=("silver",True,chat_id),daemon=True,name="Manual-Silver").start(); return
    if t in ("🔍 وضع الصفقة الحالية","حالة","check","وضع الصفقة"):
        send_message(position_text(), chat_id); return
    if t in ("📊 تقرير الأداء","stats","الإحصائيات"):
        send_message(stats_text(), chat_id); return
    if t in ("❌ إغلاق النفط","إغلاق النفط"):
        p=current_position("oil");
        if p: close_position("oil","أمر يدوي",p.get("last_price")); send_message("✅ تم إغلاق صفقة النفط.",chat_id)
        else: send_message("لا توجد صفقة نفط مفتوحة.",chat_id)
        return
    if t in ("❌ إغلاق الفضة","إغلاق الفضة"):
        p=current_position("silver");
        if p: close_position("silver","أمر يدوي",p.get("last_price")); send_message("✅ تم إغلاق صفقة الفضة.",chat_id)
        else: send_message("لا توجد صفقة فضة مفتوحة.",chat_id)
        return
    if t in ("❌ إغلاق الصفقة","إغلاق","close"):
        send_message(position_text()+"\n\nأرسل: إغلاق النفط أو إغلاق الفضة",chat_id); return
    # أي سؤال آخر يذهب مباشرة للنموذج مع بيانات السوق عند الحاجة.
    threading.Thread(target=answer_chat,args=(t,chat_id),daemon=True,name="AI-Chat").start()


def answer_chat(text, chat_id):
    market = {a: fetch_market(a) for a in ASSETS}
    prompt = "أجب بالعربية وباختصار. لا تختلق بيانات. إذا كان السؤال عن السوق استخدم البيانات المرفقة فقط.\n" + json.dumps({"question":text,"markets":market,"positions":POSITIONS},ensure_ascii=False)
    raw = groq_call("أنت Tona AI. لا تخترع بيانات.", prompt) or gemini_call("أنت Tona AI. لا تخترع بيانات.", prompt)
    if raw:
        send_message(html.escape(raw[:3500]), chat_id)
    else:
        send_message("⚠️ لا يتوفر نموذج AI حالياً.", chat_id)

# ----------------------------- Telegram polling -----------------------------
def telegram_polling():
    global LAST_UPDATE_ID
    logger.info("📨 [Telegram] بدأ polling")
    while True:
        try:
            params = {"timeout":25}
            if LAST_UPDATE_ID is not None: params["offset"] = LAST_UPDATE_ID + 1
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?" + urllib.parse.urlencode(params)
            obj = http_json(url, timeout=35)
            for upd in obj.get("result", []):
                LAST_UPDATE_ID = upd.get("update_id", LAST_UPDATE_ID)
                msg = upd.get("message") or upd.get("edited_message")
                if not msg or not msg.get("text"): continue
                chat = msg.get("chat",{}).get("id")
                threading.Thread(target=handle_text,args=(msg["text"],str(chat)),daemon=True,name="TelegramHandler").start()
        except Exception as e:
            logger.error("[Telegram] polling: %s", e)
            time.sleep(3)

# ----------------------------- Health server (stdlib only) -----------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"ok":True,"service":"Tona AI Standalone V2","time":datetime.utcnow().isoformat(),"scanner":True},ensure_ascii=False).encode()
        self.send_response(200); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *args): return


def health_server():
    port=int(os.getenv("PORT","10000"))
    server=ThreadingHTTPServer(("0.0.0.0",port),HealthHandler)
    logger.info("🌐 [Health] listening on :%s",port)
    server.serve_forever()

# ----------------------------- Main -----------------------------
def main():
    logger.info("="*70)
    logger.info("🚀 Tona AI Standalone V2 starting")
    logger.info("🧠 AI-only analysis: Gemini=%s Groq=%s", bool(GEMINI_API_KEY), bool(GROQ_API_KEY))
    logger.info("📡 Strategy: 15m VPT + SuperTrend | 5m/1h/4h confirmation/context")
    logger.info("📊 Scanner interval: %ss | Monitor interval: %ss", SIGNAL_CHECK_INTERVAL, MONITORING_INTERVAL)
    if not TELEGRAM_TOKEN: logger.warning("⚠️ TELEGRAM_TOKEN غير موجود")
    if not (GROQ_API_KEY or GEMINI_API_KEY): logger.warning("⚠️ لا يوجد مفتاح AI")
    load_state()
    threading.Thread(target=signal_scanner,daemon=True,name="Scanner").start()
    threading.Thread(target=monitor_positions,daemon=True,name="Monitor").start()
    if TELEGRAM_TOKEN:
        threading.Thread(target=telegram_polling,daemon=True,name="TelegramPolling").start()
    threading.Thread(target=health_server,daemon=True,name="HealthServer").start()
    logger.info("✅ جميع الخيوط الأساسية بدأت")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()

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
