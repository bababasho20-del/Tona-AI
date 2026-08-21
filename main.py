# Tona AI Standalone V2
# Independent AI-first version; no external TA/indicator engines.
# Strategy reference: main_V15_FIXED.py.
# AI models: Gemini/Groq. Runtime: Python standard library.
# Environment: TELEGRAM_TOKEN, CHAT_ID, GROQ_API_KEY, GEMINI_API_KEY.
# Optional: GROQ_MODEL, GEMINI_MODEL, SIGNAL_CHECK_INTERVAL, MONITORING_INTERVAL, INITIAL_BALANCE.

import os, json, time, logging, threading, urllib.request, urllib.parse, urllib.error, html, re
from datetime import datetime

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

# ----------------------------- Flask / Gunicorn -----------------------------
# Render runs this module with: gunicorn main:app
# Gunicorn owns the HTTP port; the bot background loops run inside the single worker.
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/ping")
def ping():
    return jsonify({
        "ok": True,
        "service": "Tona AI Standalone V2",
        "scanner": True,
        "time": datetime.utcnow().isoformat()
    })

START_LOCK = threading.Lock()
STARTED = False

def start_background_threads():
    global STARTED
    with START_LOCK:
        if STARTED:
            return
        STARTED = True

        logger.info("=" * 70)
        logger.info("🚀 Tona AI Standalone V2 starting")
        logger.info("🧠 AI-only analysis: Gemini=%s Groq=%s", bool(GEMINI_API_KEY), bool(GROQ_API_KEY))
        logger.info("📡 Strategy: 15m VPT + SuperTrend | 5m/1h/4h confirmation/context")
        logger.info("📊 Scanner interval: %ss | Monitor interval: %ss", SIGNAL_CHECK_INTERVAL, MONITORING_INTERVAL)

        if not TELEGRAM_TOKEN:
            logger.warning("⚠️ TELEGRAM_TOKEN غير موجود")
        if not (GROQ_API_KEY or GEMINI_API_KEY):
            logger.warning("⚠️ لا يوجد مفتاح AI")

        load_state()

        threading.Thread(
            target=signal_scanner,
            daemon=True,
            name="Scanner"
        ).start()

        threading.Thread(
            target=monitor_positions,
            daemon=True,
            name="Monitor"
        ).start()

        if TELEGRAM_TOKEN:
            threading.Thread(
                target=telegram_polling,
                daemon=True,
                name="TelegramPolling"
            ).start()

        logger.info("✅ جميع الخيوط الأساسية بدأت")

# Gunicorn imports main:app inside its single worker.
# Starting here ensures Scanner/Monitor/Telegram are started when the worker loads.
start_background_threads()

if __name__ == "__main__":
    # Local development only. Production uses Gunicorn.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
