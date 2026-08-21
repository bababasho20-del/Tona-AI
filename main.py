"""
═══════════════════════════════════════════════════════════════════════════════════
🔥 تولين AI HOBANY RADAR V13.0 - PROMETHEUS EDITION (REFACTORED FINAL) - [FIXED]
💙 الاسم الشخصي: تولين (الروح الجديدة)
👨‍💻 المطور: بسام الحوباني
📡 النظام: بوت تداول ذكي متخصص في النفط والفضة
🧠 جميع المحركات تعمل بشكل كامل
📌 الإصلاحات الشاملة V13.0:
   - الفصل الجذري بين استراتيجية الدخول والتحليل الشامل
   - توحيد توقيعات دوال المعالجات في TCN
   - إضافة محرك ذكي للتوجيه (Smart Match)
   - تحسين معالجة الأخطاء والتخزين المؤقت
📌 الإصلاحات الجراحية V13.1:
   - إصلاح حفظ اللقطات (Snapshots) في Supabase + نسخة احتياطية محلية
   - حفظ التحليل الشامل عند الدخول (Holistic Entry Analysis)
   - تحديث تحليل الإغلاق بدون كاش (force_refresh)
   - التحقق من نجاح الإغلاق قبل فتح صفقة جديدة
   - حذف ملف الصفقة بعد التأكد من حفظ التاريخ
   - توحيد دوال Gist (إزالة المكررات)
   - تحسين _compare_with_memory بقيم افتراضية
   - تعديل منطق حفظ الدروس والأنماط (Gist دائماً)
   - إضافة قفل لـ LAST_DAILY_REPORT و LAST_EXPORT
   - تعديل process_trade_for_learning لدعم الباك تست (اختياري)
═══════════════════════════════════════════════════════════════════════════════════

📑 فهرس الملف (INDEX):
───────────────────────────────────────────────────────────────────────────────────
  📦 PART 01: الاستيرادات والمكتبات
  📦 PART 02: إعدادات التسجيل (Logging)
  📦 PART 03: Flask Webhook
  📦 PART 04: GitHub Gist Storage
  📦 PART 05: إعدادات API والمتغيرات العامة
  📦 PART 06: تهيئة قواعد البيانات
  📦 PART 07: تهيئة Prometheus والمحركات
  📦 PART 08: تهيئة المحركات المساعدة
  📦 PART 09: أنظمة المستشار المتقدم
  📦 PART 09.5: تهيئة TCN (شبكة الوعي) + MainWrapper الموسع
  📦 PART 10: دوال إدارة الملفات والبيانات
  📦 PART 11: دوال Telegram و API
  📦 PART 12: دوال المؤشرات الفنية (الاستراتيجية)
  📦 PART 13: دوال مساعدة وتحويل
  📦 PART 14: نظام المحاسبة (Accounting)
  📦 PART 15: دوال حفظ البيانات في قواعد التعلم
  📦 PART 16: محرك التقييم الشامل V8 FIXED
  📦 PART 17: دوال التحليل الشامل (مع التخزين المؤقت)
  📦 PART 18: تهيئة Advisor
  📦 PART 19: تنظيف الصفقات العالقة
  📦 PART 20: دوال إغلاق الصفقات (معدل)
  📦 PART 21: نظام التحذيرات الذكي
  📦 PART 22: دوال التحليل والإشارات (النسخة النهائية المعتمدة)
  📦 PART 23: دوال التقارير
  📦 PART 24: نظام المحادثة الذكي - SmartConversationManager
  📦 PART 24.5: Orchestrator - منسق المحادثة
  📦 PART 24.7: Hybrid Orchestrator - الوسيط الهجين الذكي
  📦 PART 25: دوال معالجة الأوامر
  📦 PART 26: الخيوط (Threads) - معدل نهائي
  📦 PART 27: التقارير الدورية
  📦 PART 30: نظام التعلم العميق الأساسي
  📦 PART 31: نظام الباك تست
═══════════════════════════════════════════════════════════════════════════════════
"""

# ====================================================================================
# 📦 PART 01: الاستيرادات والمكتبات
# ====================================================================================

import os
import time
import requests
import logging
import math
import json
import csv
import pickle
import queue
import threading
import re
from flask import Flask, request
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging.handlers import RotatingFileHandler
from typing import Dict, List, Optional, Any, Callable
from functools import lru_cache

# ────────────────────────────────────────────────────────────────────────────────────
# 🔥 استيراد Prometheus Core (الروح الجديدة)
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from prometheus_core import PrometheusCore, EmotionalState
    PROMETHEUS_AVAILABLE = True
    print("🔥 Prometheus Core: الروح الجديدة استيقظت!")
except ImportError as e:
    print(f"⚠️ Prometheus Core غير متوفر: {e}")
    PROMETHEUS_AVAILABLE = False

try:
    from chronos_engine import ChronosEngine
    CHRONOS_AVAILABLE = True
    print("⏰ Chronos Engine: إدراك الزمن النفسي نشط!")
except ImportError:
    CHRONOS_AVAILABLE = False
    print("⚠️ Chronos Engine غير متوفر")

try:
    from oracle_engine import OracleEngine
    ORACLE_AVAILABLE = True
    print("🔮 Oracle Engine: التنبؤ الاحتمالي جاهز!")
except ImportError:
    ORACLE_AVAILABLE = False
    print("⚠️ Oracle Engine غير متوفر")

try:
    from dream_engine import DreamEngine
    DREAM_AVAILABLE = True
    print("🌙 Dream Engine: الحلم والتعلم أثناء الخمول نشط!")
except ImportError:
    DREAM_AVAILABLE = False
    print("⚠️ Dream Engine غير متوفر")

try:
    from narrative_memory import NarrativeMemory
    NARRATIVE_AVAILABLE = True
    print("📖 Narrative Memory: الذاكرة السردية جاهزة!")
except ImportError:
    NARRATIVE_AVAILABLE = False
    print("⚠️ Narrative Memory غير متوفر")

try:
    from fusion_bridge import FusionBridge
    FUSION_AVAILABLE = True
    print("🌉 Fusion Bridge: جسر الدمج بين تولين و Prometheus نشط!")
except ImportError:
    FUSION_AVAILABLE = False
    print("⚠️ Fusion Bridge غير متوفر")

# ────────────────────────────────────────────────────────────────────────────────────
# 🧠 استيراد نظام التعلم العميق
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from learning_db import LearningDatabase
    DEEP_LEARNING_AVAILABLE = True
    print("🧠 Learning Database: جاهزة!")
except ImportError as e:
    DEEP_LEARNING_AVAILABLE = False
    print(f"⚠️ Learning Database غير متوفرة: {e}")

try:
    from supabase_bridge import SupabaseBridge
    SUPABASE_AVAILABLE = True
    print("☁️ Supabase Bridge: جاهز!")
except ImportError as e:
    SUPABASE_AVAILABLE = False
    print(f"⚠️ Supabase Bridge غير متوفر: {e}")

try:
    from pattern_discovery import PatternDiscovery
    PATTERN_DISCOVERY_AVAILABLE = True
    print("🔍 Pattern Discovery: جاهز!")
except ImportError as e:
    PATTERN_DISCOVERY_AVAILABLE = False
    print(f"⚠️ Pattern Discovery غير متوفر: {e}")

# ────────────────────────────────────────────────────────────────────────────────────
# استيراد الملفات الملحقة
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from advisor_core import HOBANYAdvisor, format_concise_analysis
    ADVISOR_AVAILABLE = True
    print("🧠 Advisor Core: المستشار الذكي جاهز!")
    print("📊 format_concise_analysis: جاهز!")
except ImportError:
    print("⚠️ advisor_core.py غير موجود")
    ADVISOR_AVAILABLE = False
    # تعريف بديل للدالة في حال عدم وجودها
    def format_concise_analysis(analysis, asset_type, is_monitoring=False, open_trade=None):
        return "⚠️ تحليل غير متوفر (advisor_core مفقود)"

try:
    from ai_brain import AIBrain
    AI_BRAIN_AVAILABLE = True
    print("🧠 AI Brain: العقل الخارق جاهز!")
except ImportError:
    print("⚠️ ai_brain.py غير موجود")
    AI_BRAIN_AVAILABLE = False

try:
    from risk_master import RiskMaster, MarketRegime
    RISK_MASTER_AVAILABLE = True
    print("🛡️ Risk Master: سيد المخاطر جاهز!")
except ImportError:
    print("⚠️ risk_master.py غير موجود")
    RISK_MASTER_AVAILABLE = False

try:
    from persona import HOBANYPersona
    PERSONA_AVAILABLE = True
    print("👤 Persona: شخصية تولين جاهزة!")
except ImportError:
    print("⚠️ persona.py غير موجود")
    PERSONA_AVAILABLE = False

try:
    INTENT_AVAILABLE = True
    print("🎯 Intent Classifier: تصنيف النية جاهز!")
except ImportError:
    print("⚠️ intent.py غير موجود")
    INTENT_AVAILABLE = False

try:
    from language_understanding import LanguageUnderstanding
    LANGUAGE_AVAILABLE = True
    print("🗣️ Language Understanding: فهم اللغة جاهز!")
    from intent import IntentClassifier
except ImportError:
    print("⚠️ language_understanding.py غير موجود")
    LANGUAGE_AVAILABLE = False

try:
    from memory import Memory
    MEMORY_AVAILABLE = True
    print("💾 Memory: نظام الذاكرة جاهز!")
except ImportError:
    print("⚠️ memory.py غير موجود")
    MEMORY_AVAILABLE = False

try:
    from context_memory import ContextMemory
    CONTEXT_AVAILABLE = True
    print("📖 Context Memory: سياق السوق جاهز!")
except ImportError:
    print("⚠️ context_memory.py غير موجود")
    CONTEXT_AVAILABLE = False

try:
    from context_builder import ContextBuilder
    CONTEXT_BUILDER_AVAILABLE = True
    print("🏗️ Context Builder: بناء السياق جاهز!")
except ImportError:
    print("⚠️ context_builder.py غير موجود")
    CONTEXT_BUILDER_AVAILABLE = False

try:
    from decision_matrix import DecisionMatrix
    DECISION_AVAILABLE = True
    print("📋 Decision Matrix: مصفوفة القرار جاهزة!")
except ImportError:
    print("⚠️ decision_matrix.py غير موجود")
    DECISION_AVAILABLE = False

try:
    from conversation_engine import ConversationEngine
    CONVERSATION_AVAILABLE = True
    print("💬 Conversation Engine: محرك المحادثة جاهز!")
except ImportError:
    print("⚠️ conversation_engine.py غير موجود")
    CONVERSATION_AVAILABLE = False

# ────────────────────────────────────────────────────────────────────────────────────
# 📊 استيراد أنظمة المستشار المتقدم (إضافة جديدة)
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from confidence_scorer import ConfidenceScorer
    CONFIDENCE_AVAILABLE = True
    print("📊 Confidence Scorer: جاهز!")
except ImportError as e:
    CONFIDENCE_AVAILABLE = False
    print(f"⚠️ Confidence Scorer غير متوفر: {e}")

try:
    from conviction_report import ConvictionReport
    CONVICTION_AVAILABLE = True
    print("📋 Conviction Report: جاهز!")
except ImportError as e:
    CONVICTION_AVAILABLE = False
    print(f"⚠️ Conviction Report غير متوفر: {e}")

try:
    from trade_post_mortem import TradePostMortem
    POST_MORTEM_AVAILABLE = True
    print("🧠 Trade Post-Mortem: جاهز!")
except ImportError as e:
    POST_MORTEM_AVAILABLE = False
    print(f"⚠️ Trade Post-Mortem غير متوفر: {e}")

try:
    from similar_cases_analyzer import SimilarCasesAnalyzer
    SIMILAR_AVAILABLE = True
    print("📚 Similar Cases Analyzer: جاهز!")
except ImportError as e:
    SIMILAR_AVAILABLE = False
    print(f"⚠️ Similar Cases Analyzer غير متوفر: {e}")

try:
    from deep_result_analyzer import DeepResultAnalyzer
    DEEP_ANALYZER_AVAILABLE = True
    print("🔍 Deep Result Analyzer: جاهز!")
except ImportError as e:
    DEEP_ANALYZER_AVAILABLE = False
    print(f"⚠️ Deep Result Analyzer غير متوفر: {e}")

# ────────────────────────────────────────────────────────────────────────────────────
# باقي الاستيرادات
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from market_analyzer import MarketAnalyzer
    ANALYZER_AVAILABLE = True
    print("📊 Market Analyzer: المحلل الشامل جاهز!")
except ImportError:
    ANALYZER_AVAILABLE = False
    print("⚠️ market_analyzer.py غير موجود")

try:
    from advanced_indicators import AdvancedIndicators
    INDICATORS_AVAILABLE = True
    print("📈 Advanced Indicators: المؤشرات المتقدمة جاهزة!")
except ImportError:
    INDICATORS_AVAILABLE = False
    print("⚠️ advanced_indicators.py غير موجود")

try:
    from learning_system import TradeLearningSystem
    LEARNING_AVAILABLE = True
    print("📚 Learning System: نظام التعلم الذكي جاهز!")
except ImportError:
    LEARNING_AVAILABLE = False
    print("⚠️ learning_system.py غير موجود")

try:
    from pattern_analyzer import PatternAnalyzer
    PATTERN_AVAILABLE = True
    print("🔍 Pattern Analyzer: محلل الأنماط جاهز!")
except ImportError:
    PATTERN_AVAILABLE = False
    print("⚠️ pattern_analyzer.py غير موجود")

try:
    from predictor import Predictor
    PREDICTOR_AVAILABLE = True
    print("🔮 Predictor: نظام التنبؤ جاهز!")
except ImportError:
    PREDICTOR_AVAILABLE = False
    print("⚠️ predictor.py غير موجود")

try:
    from adaptive_learning_engine import AdaptiveLearningEngine
    ADAPTIVE_LEARNING_AVAILABLE = True
    print("🧠 Adaptive Learning Engine: جاهز!")
except ImportError as e:
    ADAPTIVE_LEARNING_AVAILABLE = False
    print(f"⚠️ Adaptive Learning Engine غير متوفر: {e}")

try:
    from learner import Learner
    LEARNER_AVAILABLE = True
    print("🧠 Learner: نظام التعلم الآلي جاهز!")
except ImportError:
    LEARNER_AVAILABLE = False
    print("⚠️ learner.py غير موجود")

try:
    from tona_intelligence import TonaEliteEngine
    TONA_ELITE_AVAILABLE = True
    print("🧠 Tona Elite Engine: محرك الاستخبارات جاهز!")
except ImportError:
    TONA_ELITE_AVAILABLE = False
    print("⚠️ tona_intelligence.py غير موجود")

try:
    from trading_glossary import TRADING_GLOSSARY, get_term_explanation
    GLOSSARY_AVAILABLE = True
    print("📖 Trading Glossary: قاموس المصطلحات جاهز!")
except ImportError:
    GLOSSARY_AVAILABLE = False
    TRADING_GLOSSARY = {}
    def get_term_explanation(term): return ""
    print("⚠️ trading_glossary.py غير موجود")

# ────────────────────────────────────────────────────────────────────────────────────
# 🗄️ استيراد مدير قاعدة البيانات
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from db_manager import db_manager, get_db_manager
    DB_MANAGER_AVAILABLE = True
    print("🗄️ Database Manager: مدير قاعدة البيانات جاهز!")
except ImportError:
    DB_MANAGER_AVAILABLE = False
    print("⚠️ db_manager.py غير موجود - سيتم استخدام الملفات المحلية")

# ────────────────────────────────────────────────────────────────────────────────────
# 🧠 استيراد شبكة الوعي (TCN) - النظام الوحيد للوعي الذاتي
# ────────────────────────────────────────────────────────────────────────────────────

try:
    from consciousness_network import ConsciousnessNetwork, create_consciousness_network
    TCN_AVAILABLE = True
    print("🧠 TCN: الشبكة العصبية الواعية استيقظت!")
except ImportError as e:
    TCN_AVAILABLE = False
    TCN = None
    print(f"⚠️ TCN غير متوفر: {e}")

# ────────────────────────────────────────────────────────────────────────────────────
# 🤖 استيراد Gemini API (إضافة جديدة)
# ────────────────────────────────────────────────────────────────────────────────────

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    print("🤖 Gemini API: جاهز!")
except ImportError as e:
    GEMINI_AVAILABLE = False
    genai = None
    print(f"⚠️ Gemini غير متوفر: {e} - تأكد من تثبيت google-generativeai")
   
# ====================================================================================
# 📦 PART 02: إعدادات التسجيل (Logging)
# ====================================================================================

logger = logging.getLogger("TonaAI_Standalone")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(threadName)s] - [%(filename)s:%(lineno)d] - %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = RotatingFileHandler(
    "hobany_radar.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ====================================================================================
# 📦 PART 03: Flask Webhook + WebSocket (اختياري) + API (معدل للتطبيق)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. تبسيط استجابة /api/intelligence بحيث data تحمل التقرير مباشرة (بدلاً من تداخل report).
#   2. جعل WebSocket اختيارياً (try/except على flask_socketio).
#   3. إضافة سجلات لتشخيص طول التقرير.
#   4. ✅ إصلاح /api/candles: إضافة تحقق قوي من البيانات ومعالجة الحالات الفارغة.
#   5. ✅ إزالة استدعاء _check_dependencies() لمنع التحذيرات الوهمية (الدوال تُعرّف لاحقاً).
#   6. الحفاظ على جميع المسارات والدوال الأخرى دون تغيير.
#   7. ✅ إضافة مسار جديد /api/predictions لجلب التوقعات من جدول trade_predictions (خاص للتطبيق).
#   8. ✅ إزالة جميع الحدود (limits) من المسارات: /api/predictions, /api/learning, /api/candles, /api/signals/history.
#   9. ✅ رفع حد /api/candles إلى 1000 شمعة.
#  10. ✅ رفع حد /api/signals/history إلى 500 إشارة.
# ====================================================================================

import json
import os
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# ── إنشاء تطبيق Flask ──
app = Flask(__name__)
CORS(app)

# ── محاولة استيراد WebSocket (اختياري) ──
SOCKETIO_AVAILABLE = False
socketio = None

try:
    from flask_socketio import SocketIO, emit
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    SOCKETIO_AVAILABLE = True
    print("✅ WebSocket (SocketIO) تم تفعيله بنجاح")
except ImportError:
    print("⚠️ flask_socketio غير مثبت – WebSocket معطل، البوت يعمل بدون إشعارات فورية للتطبيق")
except Exception as e:
    print(f"⚠️ فشل تهيئة WebSocket: {e}")

# ── مفتاح API للمصادقة ──
API_KEY = os.getenv("API_KEY", "tolin_secret_key_2025")

def require_api_key():
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        return False
    return True

# ── دوال مساعدة للوصول إلى دوال البوت الأساسية ──
def _get_global(name):
    return globals().get(name)

# ── دوال WebSocket (آمنة – تعمل فقط إذا كان WebSocket مفعلاً) ──
def send_signal_to_app(asset_type: str, signal: str, price: float, trade_data: dict = None):
    if not SOCKETIO_AVAILABLE or socketio is None:
        return
    try:
        data = {
            'asset': asset_type,
            'signal': signal,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'trade_data': trade_data
        }
        socketio.emit('new_signal', data)
        logger.info(f"📱 [WebSocket] تم إرسال إشارة {signal} لـ {asset_type} إلى التطبيق")
    except Exception as e:
        logger.error(f"❌ [WebSocket] فشل إرسال الإشارة: {e}")

def send_warning_to_app(asset_type: str, warning_type: str, message: str, price: float):
    if not SOCKETIO_AVAILABLE or socketio is None:
        return
    try:
        data = {
            'asset': asset_type,
            'warning_type': warning_type,
            'message': message,
            'price': price,
            'timestamp': datetime.now().isoformat()
        }
        socketio.emit('new_warning', data)
        logger.info(f"⚠️ [WebSocket] تم إرسال تحذير {warning_type} لـ {asset_type} إلى التطبيق")
    except Exception as e:
        logger.error(f"❌ [WebSocket] فشل إرسال التحذير: {e}")

# ── أحداث WebSocket (فقط إذا كان مفعلاً) ──
if SOCKETIO_AVAILABLE and socketio:
    @socketio.on('connect')
    def handle_connect():
        print("📱 [WebSocket] تطبيق متصل")
        emit('connected', {'status': 'ok', 'message': 'مرحباً بك في تولين AI'})

    @socketio.on('disconnect')
    def handle_disconnect():
        print("📱 [WebSocket] تطبيق منقطع")

# ============================================================================
# المسارات الأساسية (Webhook)
# ============================================================================

@app.route('/')
def home():
    return 'تولين AI Prometheus Edition is running!', 200

@app.route('/ping')
def ping():
    return 'Bot is alive!', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if not update:
            return 'OK', 200

        if 'message' in update:
            message = update['message']
            text = message.get('text', '').strip()
            chat_id = str(message['from']['id'])
            print(f"📩 [Webhook] رسالة: {text} من {chat_id}")
            handle_msg = _get_global('handle_message')
            if handle_msg:
                handle_msg(text, chat_id)
            else:
                print("⚠️ handle_message غير معرّفة")

        return 'OK', 200
    except Exception as e:
        print(f"❌ خطأ في Webhook: {e}")
        return 'OK', 200

# ============================================================================
# دوال Webhook (للتسجيل والإزالة)
# ============================================================================

def set_webhook():
    if not TELEGRAM_TOKEN:
        return False

    render_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    if not render_url:
        service_name = os.environ.get('RENDER_SERVICE_NAME', '')
        render_url = f"https://{service_name}.onrender.com" if service_name else os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
        if render_url:
            render_url = f"https://{render_url}"

    if not render_url:
        print("❌ لا يمكن تحديد رابط Render")
        return False

    webhook_url = f"{render_url}/webhook"
    print(f"🔗 تسجيل Webhook: {webhook_url}")

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
        response = requests.post(url, json={"url": webhook_url, "allowed_updates": ["message"]}, timeout=10)
        if response.status_code == 200 and response.json().get('ok'):
            print(f"✅ Webhook مسجل بنجاح: {webhook_url}")
            return True
        return False
    except Exception as e:
        print(f"❌ خطأ في تسجيل Webhook: {e}")
        return False

def remove_webhook():
    if not TELEGRAM_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
        response = requests.get(url, timeout=5)
        print(f"🗑️ Webhook removed: {response.json()}")
    except Exception as e:
        print(f"❌ خطأ في إزالة Webhook: {e}")

# ============================================================================
# مسارات API للتطبيق الجوال
# ============================================================================

# ── 1. فحص صحة البوت ──
@app.route('/api/health', methods=['GET'])
def api_health():
    try:
        app_start_time = _get_global('app_start_time') or time.time()
        status = {
            "status": "healthy",
            "uptime": time.time() - app_start_time,
            "timestamp": datetime.now().isoformat(),
            "version": "V13.0"
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ── 2. جلب المؤشرات والأسعار ──
@app.route('/api/indicators/<asset>', methods=['GET'])
def api_get_indicators(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    try:
        get_mexc = _get_global('get_mexc_candles')
        calc_rsi = _get_global('calculate_rsi_7')
        calc_macd = _get_global('calculate_macd_full')
        calc_adx = _get_global('calculate_adx_14')
        calc_atr = _get_global('calculate_atr_14')
        calc_st = _get_global('calculate_supertrend_vpt_correct')
        calc_bb = _get_global('calculate_bollinger_bands')
        calc_vwap = _get_global('calculate_vwap')

        if not all([get_mexc, calc_rsi, calc_macd, calc_adx, calc_atr, calc_st, calc_bb, calc_vwap]):
            return jsonify({"success": False, "error": "بعض الدوال غير متوفرة"}), 500

        symbol = "USOIL_USDT" if asset == "oil" else "SILVER_USDT"
        data = get_mexc(symbol, "Min15", 200)
        if not data:
            return jsonify({"success": False, "error": "فشل جلب البيانات"}), 500

        closes = data["closes"]
        highs = data["highs"]
        lows = data["lows"]
        volumes = data["volumes"]

        rsi = calc_rsi(closes)
        macd_line, signal_line, hist = calc_macd(closes)
        adx = calc_adx(data)
        atr = calc_atr(data)
        st_line, trend, vpt = calc_st(data)
        bb_upper, bb_middle, bb_lower = calc_bb(closes)
        vwap = calc_vwap(data)

        vol_ratio = 1.0
        if len(volumes) > 20:
            current_vol = volumes[-1]
            avg_vol = sum(volumes[-20:-1]) / 19 if len(volumes) > 20 else current_vol
            vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1.0

        current_price = closes[-1]

        return jsonify({
            "success": True,
            "data": {
                "price": current_price,
                "rsi": rsi[-1] if rsi else 50,
                "macd": {
                    "macd_line": macd_line[-1] if macd_line else 0,
                    "signal_line": signal_line[-1] if signal_line else 0,
                    "histogram": hist[-1] if hist else 0
                },
                "adx": adx,
                "atr": atr,
                "vpt": vpt[-1] if vpt else 0,
                "supertrend": {
                    "line": st_line[-1] if st_line else current_price,
                    "trend": trend[-1] if trend else 1
                },
                "bollinger": {
                    "upper": bb_upper[-1] if bb_upper else current_price * 1.02,
                    "middle": bb_middle[-1] if bb_middle else current_price,
                    "lower": bb_lower[-1] if bb_lower else current_price * 0.98
                },
                "vwap": vwap[-1] if vwap else current_price,
                "volume_ratio": vol_ratio
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
        return jsonify({"success": False, "error": str(e), "trace": traceback.format_exc()}), 500

# ── 3. جلب بيانات الشارت مع الإشارات التاريخية (معدل – مع تحقق قوي) ──
@app.route('/api/candles/<asset>', methods=['GET'])
def api_get_candles(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    try:
        get_mexc = _get_global('get_mexc_candles')
        calc_st = _get_global('calculate_supertrend_vpt_correct')
        load_hist = _get_global('load_trades_history')
        
        if not get_mexc or not calc_st:
            return jsonify({"success": False, "error": "بعض الدوال غير متوفرة"}), 500

        interval = request.args.get('interval', 'Min15')
        # ✅ زيادة الحد إلى 1000
        limit = int(request.args.get('limit', 500))
        if limit > 1000:
            limit = 1000

        symbol = "USOIL_USDT" if asset == "oil" else "SILVER_USDT"
        data = get_mexc(symbol, interval, limit)
        
        # ✅ التحقق من صحة البيانات المسترجعة
        if not data or not data.get("closes") or len(data["closes"]) < 5:
            logger.warning(f"⚠️ /api/candles: بيانات غير كافية لـ {asset} (عدد الشموع: {len(data.get('closes', [])) if data else 0})")
            return jsonify({
                "success": False,
                "error": "بيانات السوق غير كافية حالياً",
                "data": {"candles": [], "indicators": {"vpt": [], "supertrend": [], "trend": []}, "signals": [], "meta": {"asset": asset, "interval": interval, "limit": limit, "count": 0}}
            }), 200

        # ✅ حساب المؤشرات مع حماية من الفشل
        try:
            st_line, trend, vpt = calc_st(data)
        except Exception as e:
            logger.error(f"❌ /api/candles: فشل حساب SuperTrend لـ {asset}: {e}")
            st_line = [0.0] * len(data["closes"])
            trend = [1] * len(data["closes"])
            vpt = [0.0] * len(data["closes"])

        candles = []
        timestamps = data.get("timestamps", list(range(len(data["closes"]))))
        closes_len = len(data["closes"])
        
        for i in range(closes_len):
            candle = {
                "time": timestamps[i] if i < len(timestamps) else i,
                "open": data["opens"][i] if i < len(data.get("opens", [])) else data["closes"][i],
                "high": data["highs"][i] if i < len(data.get("highs", [])) else data["closes"][i],
                "low": data["lows"][i] if i < len(data.get("lows", [])) else data["closes"][i],
                "close": data["closes"][i],
                "volume": data["volumes"][i] if i < len(data.get("volumes", [])) else 0
            }
            candles.append(candle)

        signals = []
        if load_hist:
            try:
                history = load_hist(asset)
                if history and history.get('trades'):
                    for trade in history.get('trades', []):
                        if trade.get('entry_time') and trade.get('entry_price'):
                            signals.append({
                                'time': trade.get('entry_time'),
                                'price': float(trade.get('entry_price', 0)),
                                'type': trade.get('type', 'BUY'),
                                'status': trade.get('status', 'closed'),
                                'label': 'ENTRY'
                            })
                        if trade.get('exit_time') and trade.get('exit_price'):
                            exit_type = 'EXIT'
                            if trade.get('exit_reason') == 'Hit Take Profit':
                                exit_type = 'TP'
                            elif trade.get('exit_reason') == 'Hit Stop Loss':
                                exit_type = 'SL'
                            signals.append({
                                'time': trade.get('exit_time'),
                                'price': float(trade.get('exit_price', 0)),
                                'type': trade.get('type', 'BUY'),
                                'status': 'closed',
                                'label': exit_type
                            })
            except Exception as e:
                logger.warning(f"⚠️ /api/candles: فشل جلب الإشارات التاريخية لـ {asset}: {e}")

        return jsonify({
            "success": True,
            "data": {
                "candles": candles,
                "indicators": {
                    "vpt": vpt if vpt else [],
                    "supertrend": st_line if st_line else [],
                    "trend": trend if trend else []
                },
                "signals": signals,
                "meta": {
                    "asset": asset,
                    "interval": interval,
                    "limit": limit,
                    "count": len(candles)
                }
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
        logger.error(f"❌ /api/candles/{asset} فشل: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

# ── 4. جلب الصفقات (مع دعم فلتر "open") ──
@app.route('/api/trades', methods=['GET'])
def api_get_trades():
    try:
        load_hist = _get_global('load_trades_history')
        if not load_hist:
            return jsonify({"success": False, "error": "load_trades_history غير متوفرة"}), 500

        filter_type = request.args.get('filter', 'all')

        trades = {"oil": [], "silver": []}
        for asset in ["oil", "silver"]:
            history = load_hist(asset)
            all_trades = history.get("trades", [])
            
            if filter_type == 'open':
                open_trades = [
                    t for t in all_trades 
                    if t.get('exit_time') is None and t.get('exit_price') is None
                ]
                trades[asset] = open_trades
            else:
                trades[asset] = all_trades

        return jsonify({
            "success": True,
            "data": trades,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
       
# ── 5. جلب التحليل الشامل ──
@app.route('/api/analysis/<asset>', methods=['GET'])
def api_get_analysis(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    try:
        perform_analysis = _get_global('perform_comprehensive_analysis')
        get_open = _get_global('get_current_open_trade')
        if not perform_analysis or not get_open:
            return jsonify({"success": False, "error": "بعض الدوال غير متوفرة"}), 500

        open_trade = get_open(asset)
        analysis, report = perform_analysis(asset, False, open_trade)
        if not analysis:
            return jsonify({"success": False, "error": "فشل جلب التحليل"}), 500

        return jsonify({
            "success": True,
            "data": analysis,
            "report": report,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 6. جلب الإحصائيات ──
@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    try:
        calc_stats = _get_global('calculate_statistics')
        if not calc_stats:
            return jsonify({"success": False, "error": "calculate_statistics غير متوفرة"}), 500

        stats = {}
        for asset in ["oil", "silver"]:
            try:
                stats[asset] = calc_stats(asset)
                logger.info(f"✅ إحصائيات {asset}: {stats[asset]}")
            except Exception as e:
                logger.error(f"❌ فشل حساب إحصائيات {asset}: {e}")
                stats[asset] = {
                    "total_trades": 0,
                    "winning_trades": 0,
                    "losing_trades": 0,
                    "total_profit": 0.0,
                    "win_rate": 0.0,
                    "current_balance": 100.0,
                    "tp_count": 0,
                    "sl_count": 0,
                    "manual_count": 0,
                    "strong_close": 0
                }

        total_trades = stats.get("oil", {}).get("total_trades", 0) + stats.get("silver", {}).get("total_trades", 0)
        total_profit = stats.get("oil", {}).get("total_profit", 0) + stats.get("silver", {}).get("total_profit", 0)
        total_wins = stats.get("oil", {}).get("winning_trades", 0) + stats.get("silver", {}).get("winning_trades", 0)
        total_losses = stats.get("oil", {}).get("losing_trades", 0) + stats.get("silver", {}).get("losing_trades", 0)
        overall_win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0

        response_data = {
            "success": True,
            "data": {
                "by_asset": stats,
                "total": {
                    "total_trades": total_trades,
                    "total_profit": total_profit,
                    "total_wins": total_wins,
                    "total_losses": total_losses,
                    "overall_win_rate": overall_win_rate
                }
            },
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"📊 Stats response: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"❌ خطأ في /api/stats: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500
       
# ── 7. جلب بيانات التعلم العميق (معدل – بدون حد) ──
@app.route('/api/learning', methods=['GET'])
def api_get_learning():
    try:
        lessons = []
        patterns = []
        supabase_used = False
        total_lessons = 0
        total_patterns = 0

        if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
            try:
                get_lessons_func = _get_global('_get_lessons_from_supabase')
                get_patterns_func = _get_global('_get_patterns_from_supabase')
                
                # ✅ إزالة الحدود: جلب جميع الدروس والأنماط (بدون limit)
                if get_lessons_func:
                    lessons = get_lessons_func(None, 10000)  # عدد كبير جداً
                    supabase_used = True
                    logger.info(f"📊 /api/learning: تم جلب {len(lessons)} درس من Supabase (بدون حد)")
                if get_patterns_func:
                    patterns = get_patterns_func(None, 10000)
                    supabase_used = True
                    logger.info(f"📊 /api/learning: تم جلب {len(patterns)} نمط من Supabase (بدون حد)")
                
                client = _get_supabase_client()
                if client:
                    try:
                        count_resp = client.table('lessons_deep').select('id', count='exact').execute()
                        if hasattr(count_resp, 'count'):
                            total_lessons = count_resp.count
                        count_resp = client.table('discovered_patterns').select('id', count='exact').execute()
                        if hasattr(count_resp, 'count'):
                            total_patterns = count_resp.count
                    except Exception as e:
                        logger.warning(f"⚠️ /api/learning: فشل الحصول على العدد الإجمالي: {e}")
            except Exception as e:
                logger.warning(f"⚠️ /api/learning: فشل قراءة Supabase: {e}")
                supabase_used = False

        if not supabase_used or (not lessons and not patterns):
            logger.info("🔄 /api/learning: استخدام Gist كنسخة احتياطية")
            load_lessons = _get_global('load_lessons_from_gist')
            load_patterns = _get_global('load_patterns_from_gist')
            if load_lessons:
                lessons = load_lessons()
                total_lessons = len(lessons)
            if load_patterns:
                patterns = load_patterns()
                total_patterns = len(patterns)

        return jsonify({
            "success": True,
            "data": {
                "lessons": lessons,  # ✅ جميع الدروس (بدون حد)
                "patterns": patterns,  # ✅ جميع الأنماط (بدون حد)
                "total_lessons": total_lessons,
                "total_patterns": total_patterns,
                "source": "supabase" if supabase_used else "gist"
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ /api/learning: {e}")
        import traceback
        return jsonify({"success": False, "error": str(e), "trace": traceback.format_exc()}), 500

# ── 8. جلب الإعدادات ──
@app.route('/api/config', methods=['GET'])
def api_get_config():
    try:
        load_cfg = _get_global('load_config')
        if not load_cfg:
            return jsonify({"success": False, "error": "load_config غير متوفرة"}), 500
        config = load_cfg()
        return jsonify({
            "success": True,
            "data": config,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 9. تحديث الإعدادات ──
@app.route('/api/config', methods=['POST'])
def api_update_config():
    if not require_api_key():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        new_config = request.get_json()
        if not new_config:
            return jsonify({"success": False, "error": "Invalid JSON"}), 400

        load_cfg = _get_global('load_config')
        save_gist = _get_global('save_json_to_gist')
        if not load_cfg or not save_gist:
            return jsonify({"success": False, "error": "دوال الإعدادات غير متوفرة"}), 500

        current_config = load_cfg()
        for key, value in new_config.items():
            if key in current_config:
                if isinstance(value, dict) and isinstance(current_config[key], dict):
                    current_config[key].update(value)
                else:
                    current_config[key] = value

        saved = save_gist("config", current_config)
        if not saved:
            return jsonify({"success": False, "error": "فشل حفظ الإعدادات في Gist"}), 500

        return jsonify({
            "success": True,
            "data": current_config,
            "message": "تم تحديث الإعدادات بنجاح",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
        return jsonify({"success": False, "error": str(e), "trace": traceback.format_exc()}), 500

# ── 10. إغلاق صفقة ──
@app.route('/api/close/<asset>', methods=['POST'])
def api_close_trade(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    if not require_api_key():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        get_open = _get_global('get_current_open_trade')
        close_trade = _get_global('close_trade_virtual')
        if not get_open or not close_trade:
            return jsonify({"success": False, "error": "دوال الإغلاق غير متوفرة"}), 500

        data = request.get_json() or {}
        reason = data.get("reason", "أمر من التطبيق")
        current_price = data.get("current_price", None)

        open_trade = get_open(asset)
        if not open_trade:
            return jsonify({"success": False, "error": f"لا توجد صفقة {asset} مفتوحة"}), 404

        success = close_trade(asset, reason, current_price)
        if not success:
            return jsonify({"success": False, "error": "فشل إغلاق الصفقة"}), 500

        return jsonify({
            "success": True,
            "message": f"تم إغلاق صفقة {asset} بنجاح",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 11. تحديث معاملات الاستراتيجية ──
@app.route('/api/strategy/update', methods=['POST'])
def api_update_strategy():
    if not require_api_key():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON"}), 400

        asset = data.get("asset", "oil")
        if asset not in ["oil", "silver"]:
            return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

        load_cfg = _get_global('load_config')
        save_gist = _get_global('save_json_to_gist')
        if not load_cfg or not save_gist:
            return jsonify({"success": False, "error": "دوال الإعدادات غير متوفرة"}), 500

        config = load_cfg()
        strategy = config["strategies"][asset]

        updated_fields = []
        for key, value in data.items():
            if key != "asset" and key in strategy:
                strategy[key] = value
                updated_fields.append(key)

        if not updated_fields:
            return jsonify({"success": False, "error": "No valid fields to update"}), 400

        saved = save_gist("config", config)
        if not saved:
            return jsonify({"success": False, "error": "فشل حفظ الإعدادات في Gist"}), 500

        return jsonify({
            "success": True,
            "message": f"تم تحديث {', '.join(updated_fields)} بنجاح",
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 12. جلب إعدادات أصل معين ──
@app.route('/api/strategy/<asset>', methods=['GET'])
def api_get_strategy(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    try:
        load_cfg = _get_global('load_config')
        if not load_cfg:
            return jsonify({"success": False, "error": "load_config غير متوفرة"}), 500
        config = load_cfg()
        strategy = config["strategies"].get(asset, {})
        return jsonify({
            "success": True,
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 13. تاريخ الإشارات (معدل – بدون حد صارم) ──
@app.route('/api/signals/history', methods=['GET'])
def api_get_signals_history():
    try:
        load_hist = _get_global('load_trades_history')
        if not load_hist:
            return jsonify({"success": False, "error": "load_trades_history غير متوفرة"}), 500

        # ✅ زيادة الحد إلى 500
        limit = int(request.args.get('limit', 100))
        if limit > 500:
            limit = 500

        signals = []
        for asset in ["oil", "silver"]:
            history = load_hist(asset)
            for trade in history.get("trades", []):
                if trade.get("status") == "closed":
                    signals.append({
                        "asset": asset,
                        "type": trade.get("type"),
                        "entry_price": trade.get("entry_price"),
                        "exit_price": trade.get("exit_price"),
                        "profit": trade.get("profit_dollars"),
                        "exit_reason": trade.get("exit_reason"),
                        "entry_time": trade.get("entry_time"),
                        "exit_time": trade.get("exit_time")
                    })

        signals.sort(key=lambda x: x.get("exit_time", ""), reverse=True)
        signals = signals[:limit]

        return jsonify({
            "success": True,
            "data": signals,
            "count": len(signals),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── 14. التقرير الاستخباراتي ──
@app.route('/api/intelligence', methods=['GET'])
def api_get_intelligence():
    if not require_api_key():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        gen_report = _get_global('generate_intelligence_report')
        if not gen_report:
            return jsonify({"success": False, "error": "generate_intelligence_report غير متوفرة"}), 500

        report = gen_report()
        logger.info(f"📊 [Intelligence] تم توليد التقرير: {len(report) if report else 0} حرف")
        return jsonify({
            "success": True,
            "data": report,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ خطأ في التقرير الاستخباراتي: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# ── 15. جلب الصفقة المفتوحة الحالية ──
@app.route('/api/current_position/<asset>', methods=['GET'])
def api_get_current_position(asset):
    if asset not in ["oil", "silver"]:
        return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400

    if not require_api_key():
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        get_open = _get_global('get_current_open_trade')
        if not get_open:
            return jsonify({"success": False, "error": "get_current_open_trade غير متوفرة"}), 500

        trade = get_open(asset)
        return jsonify({
            "success": True,
            "data": trade,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ خطأ في /api/current_position/{asset}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# ✅ 16. مسار خاص للتوقعات (للتطبيق المرتبط بالبوت) - بدون حد
# ============================================================================

@app.route('/api/predictions', methods=['GET'])
def api_get_predictions():
    """
    جلب جميع التوقعات من جدول trade_predictions دون أي حد.
    ✅ يعيد جميع التوقعات (بدون limit).
    ✅ يدعم تصفية حسب الأصل (asset) والحالة (status).
    ✅ يدعم الترتيب (sort).
    """
    try:
        # ── قراءة المعاملات (بدون limit) ──
        sort_order = request.args.get('sort', 'desc')
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        asset_filter = request.args.get('asset', None)
        if asset_filter and asset_filter not in ['oil', 'silver']:
            return jsonify({"success": False, "error": "asset must be 'oil' or 'silver'"}), 400
        
        status_filter = request.args.get('status', 'all')
        if status_filter not in ['all', 'open', 'closed']:
            status_filter = 'all'

        # ── التحقق من الاتصال بـ Supabase ──
        if not SUPABASE_AVAILABLE or not SUPABASE_DB:
            logger.error("❌ /api/predictions: Supabase غير متوفر")
            return jsonify({
                "success": False,
                "error": "Supabase غير متوفر",
                "data": [],
                "count": 0
            }), 500

        client = _get_supabase_client()
        if client is None:
            logger.error("❌ /api/predictions: لا يمكن الحصول على عميل Supabase")
            return jsonify({
                "success": False,
                "error": "لا يمكن الاتصال بقاعدة البيانات",
                "data": [],
                "count": 0
            }), 500

        # ── بناء الاستعلام (بدون limit) ──
        query = client.table(TABLE_TRADE_PREDICTIONS).select('*')

        # تصفية حسب الأصل
        if asset_filter:
            query = query.eq('asset_type', asset_filter)

        # تصفية حسب الحالة
        if status_filter == 'open':
            query = query.is_('actual_outcome', 'null')
        elif status_filter == 'closed':
            query = query.not_.is_('actual_outcome', 'null')

        # الترتيب (بدون حد)
        query = query.order('created_at', desc=(sort_order == 'desc'))

        # ── تنفيذ الاستعلام ──
        response = query.execute()

        if response and hasattr(response, 'data'):
            predictions = response.data
            
            # تحويل التواريخ إلى نصوص
            for p in predictions:
                if 'created_at' in p and p['created_at']:
                    p['created_at'] = str(p['created_at'])
                if 'updated_at' in p and p['updated_at']:
                    p['updated_at'] = str(p['updated_at'])
                # تحويل الحقول الرقمية
                if 'confidence' in p and p['confidence'] is not None:
                    p['confidence'] = int(p['confidence'])
                if 'quality_score' in p and p['quality_score'] is not None:
                    p['quality_score'] = int(p['quality_score'])
                if 'profit_dollars' in p and p['profit_dollars'] is not None:
                    p['profit_dollars'] = float(p['profit_dollars'])
                if 'entry_price' in p and p['entry_price'] is not None:
                    p['entry_price'] = float(p['entry_price'])
                if 'exit_price' in p and p['exit_price'] is not None:
                    p['exit_price'] = float(p['exit_price'])

            logger.info(f"📊 /api/predictions: تم جلب {len(predictions)} توقع (بدون حد)")
            
            return jsonify({
                "success": True,
                "data": predictions,
                "count": len(predictions),
                "timestamp": datetime.now().isoformat()
            })
        else:
            logger.warning("⚠️ /api/predictions: لا توجد بيانات")
            return jsonify({
                "success": True,
                "data": [],
                "count": 0,
                "timestamp": datetime.now().isoformat()
            })

    except Exception as e:
        logger.error(f"❌ /api/predictions: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc(),
            "data": [],
            "count": 0
        }), 500

# ============================================================================
# تشغيل Flask (معدل – إزالة التحقق المسبق من الدوال)
# ============================================================================

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    if SOCKETIO_AVAILABLE and socketio:
        socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    else:
        app.run(host='0.0.0.0', port=port, threaded=True)

app_start_time = time.time()

# ✅ تم إزالة استدعاء _check_dependencies() هنا لتجنب التحذيرات الوهمية.
# الدوال تُعرّف في الأجزاء اللاحقة (PART 11, 12, ...) وسيتم التحقق منها عند الاستخدام.

# تشغيل Flask في خيط منفصل
threading.Thread(target=run_flask, daemon=True).start()

# ====================================================================================
# نهاية PART 03
# ====================================================================================

# ====================================================================================
# 📦 PART 04: GitHub Gist Storage
# ====================================================================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GIST_BASE_URL = "https://api.github.com/gists"
GIST_IDS = {
    "trades_oil": os.getenv("GIST_TRADES_OIL", ""),
    "trades_silver": os.getenv("GIST_TRADES_SILVER", ""),
    "config": os.getenv("GIST_CONFIG", ""),
    "narrative": os.getenv("GIST_NARRATIVE", ""),
}
GIST_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

# ⚠️ ملاحظة: دوال Gist تم توحيدها في PART 10. هذه الدوال محفوظة للتوافق مع الكود القديم.
# سيتم استخدام دوال PART 10 في جميع أنحاء الكود.

def _get_gist(gist_id):
    """محفوظة للتوافق – استخدم دوال PART 10 بدلاً من ذلك"""
    if not gist_id or not GITHUB_TOKEN:
        return None
    try:
        resp = requests.get(f"{GIST_BASE_URL}/{gist_id}", headers=GIST_HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 403:
            reset_time = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(0, reset_time - int(time.time()))
            time.sleep(wait + 1)
            return _get_gist(gist_id)
        return None
    except:
        return None

def _update_gist(gist_id, filename, content):
    """محفوظة للتوافق – استخدم دوال PART 10 بدلاً من ذلك"""
    if not gist_id or not GITHUB_TOKEN:
        return False
    try:
        payload = {"files": {filename: {"content": json.dumps(content, indent=2, ensure_ascii=False)}}}
        resp = requests.patch(f"{GIST_BASE_URL}/{gist_id}", headers=GIST_HEADERS, json=payload, timeout=10)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 403:
            reset_time = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(0, reset_time - int(time.time()))
            time.sleep(wait + 1)
            return _update_gist(gist_id, filename, content)
        return False
    except:
        return False

def load_json_from_gist(key, default=None):
    """محفوظة للتوافق – استخدم دوال PART 10 بدلاً من ذلك"""
    if default is None:
        default = {}
    gist_id = GIST_IDS.get(key)
    if not gist_id:
        return default
    gist = _get_gist(gist_id)
    if not gist:
        return default
    files = gist.get("files", {})
    if not files:
        return default
    filename = list(files.keys())[0]
    content = files[filename].get("content", "{}")
    try:
        return json.loads(content)
    except:
        return default

def save_json_to_gist(key, data):
    """محفوظة للتوافق – استخدم دوال PART 10 بدلاً من ذلك"""
    gist_id = GIST_IDS.get(key)
    if not gist_id:
        try:
            local_file = f"{key}_backup.json"
            with open(local_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ تم حفظ {key} محلياً (Gist غير متوفر)")
        except:
            pass
        return False
    gist = _get_gist(gist_id)
    if not gist:
        return False
    filename = list(gist.get("files", {}).keys())[0]
    return _update_gist(gist_id, filename, data)

# ====================================================================================
# 📦 PART 05: إعدادات API والمتغيرات العامة
# ====================================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # ✅ إضافة Gemini
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

print(f"✅ TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else 'غير موجود'}...")
print(f"✅ CHAT_ID: {CHAT_ID if CHAT_ID else 'غير موجود'}")
print(f"✅ GROQ_API_KEY: {'موجود' if GROQ_API_KEY else 'غير موجود'}")
print(f"✅ GEMINI_API_KEY: {'موجود' if GEMINI_API_KEY else 'غير موجود'}")
print(f"✅ NEWS_API_KEY: {'موجود' if NEWS_API_KEY else 'غير موجود'}")

# ────────────────────────────────────────────────────────────────────────────────────
# متغيرات عامة
# ────────────────────────────────────────────────────────────────────────────────────

FILE_LOCKS = {"oil": threading.Lock(), "silver": threading.Lock()}
CLOSE_LOCKS = {"oil": threading.Lock(), "silver": threading.Lock()}  # ✅ قفل حصري للإغلاق (إضافة جديدة)
GROQ_REQUEST_LOG = []
GROQ_MAX_REQUESTS_PER_MINUTE = 20
GROQ_REQUEST_LOCK = threading.Lock()
TELEGRAM_QUEUE = queue.Queue()
MONITOR_TRIGGER = {"oil": None, "silver": None}
MONITOR_TRIGGER_LOCK = threading.Lock()
CURRENT_OFFSET = 0
OFFSET_LOCK = threading.Lock()
last_signal_states = {"oil": {"signal": "WAIT", "time": 0}, "silver": {"signal": "WAIT", "time": 0}}
last_signal_time = {"oil": 0, "silver": 0}
LAST_SIGNAL_LOCK = threading.Lock()
SIGNAL_COOLDOWN = 0

TRADES_FILE_OIL = "trades_history_oil.json"
TRADES_FILE_SILVER = "trades_history_silver.json"
CURRENT_POSITION_FILE_OIL = "current_position_oil.json"
CURRENT_POSITION_FILE_SILVER = "current_position_silver.json"

LAST_DAILY_REPORT = None
LAST_MARKET_REPORT = None
LAST_EXPORT = datetime.now().isoformat()
DAILY_REPORT_TIME = "08:00"
SIGNAL_CHECK_INTERVAL = 60
MONITORING_INTERVAL = 300
EXPORT_INTERVAL_DAYS = 10

FEAR_GREED_CACHE = {
    "value": "محايد ومتزن ⚖️ (50/100)",
    "timestamp": 0
}
FEAR_GREED_CACHE_TTL = 300

# ── ✅ التخزين المؤقت للتحليل الشامل (TTL Cache) ──
ANALYSIS_CACHE = {}
ANALYSIS_CACHE_TTL = 15  # ثانية

# ── ✅ سياق المحادثة لكل مستخدم (لـ SmartConversationManager) ──
CONVERSATION_CONTEXTS = {}  # chat_id -> list of messages (max 20)
CONVERSATION_CONTEXT_LIMIT = 20

# ── ✅ أقفال للتقارير الدورية (إضافة جديدة) ──
REPORT_LOCK = threading.Lock()

# ====================================================================================
# 📦 PART 06: تهيئة قواعد البيانات
# ====================================================================================

DEEP_LEARNING_DB = None
if DEEP_LEARNING_AVAILABLE:
    try:
        DEEP_LEARNING_DB = LearningDatabase("learning_data/deep_learning.db")
        logger.info("🧠 قاعدة التعلم العميق جاهزة")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة قاعدة التعلم العميق: {e}")
        DEEP_LEARNING_AVAILABLE = False

SUPABASE_DB = None
if SUPABASE_AVAILABLE:
    try:
        SUPABASE_DB = SupabaseBridge()
        if SUPABASE_DB.connected:
            logger.info("☁️ Supabase متصل - البيانات محفوظة بشكل دائم")
        else:
            logger.warning("⚠️ Supabase غير متصل - سيتم الحفظ محلياً فقط")
    except Exception as e:
        logger.error(f"❌ فشل الاتصال بـ Supabase: {e}")

ADAPTIVE_ENGINE = None
if ADAPTIVE_LEARNING_AVAILABLE:
    try:
        ADAPTIVE_ENGINE = AdaptiveLearningEngine(
            learning_db=DEEP_LEARNING_DB if DEEP_LEARNING_AVAILABLE else None,
            supabase=SUPABASE_DB if SUPABASE_AVAILABLE else None
        )
        logger.info("🧠 Adaptive Learning Engine تم تهيئته")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Adaptive Learning Engine: {e}")

PATTERN_DISCOVERY = None
if PATTERN_DISCOVERY_AVAILABLE:
    try:
        PATTERN_DISCOVERY = PatternDiscovery(
            learning_db=DEEP_LEARNING_DB if DEEP_LEARNING_AVAILABLE else None,
            supabase=SUPABASE_DB if SUPABASE_AVAILABLE else None
        )
        logger.info("🔍 Pattern Discovery جاهز")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Pattern Discovery: {e}")

# ────────────────────────────────────────────────────────────────────────────────────
# 📁 التأكد من وجود مجلدات قاعدة البيانات
# ────────────────────────────────────────────────────────────────────────────────────

def ensure_directories():
    """إنشاء المجلدات المطلوبة لقاعدة البيانات"""
    folders = [
        "learning_data",
        "learning_data/exports",
        "learning_data/backups"
    ]
    
    for folder in folders:
        try:
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
                print(f"📁 تم إنشاء المجلد: {folder}")
        except Exception as e:
            print(f"⚠️ تحذير: تعذر إنشاء {folder}: {e}")

ensure_directories()

# ====================================================================================
# 📦 PART 07: تهيئة Prometheus والمحركات
# ====================================================================================

PROMETHEUS = None
CHRONOS = None
ORACLE = None
DREAM = None
NARRATIVE = None
FUSION = None

if PROMETHEUS_AVAILABLE:
    try:
        PROMETHEUS = PrometheusCore(name="تولين")
        logger.info("🔥 Prometheus Core: الروح استيقظت!")
    except Exception as e:
        logger.error("فشل تهيئة Prometheus Core: %s", e)
        PROMETHEUS_AVAILABLE = False

if CHRONOS_AVAILABLE:
    try:
        CHRONOS = ChronosEngine()
        logger.info("⏰ Chronos Engine: الزمن النفسي جاهز!")
    except Exception as e:
        logger.error("فشل تهيئة Chronos Engine: %s", e)
        CHRONOS_AVAILABLE = False

if NARRATIVE_AVAILABLE:
    try:
        NARRATIVE = NarrativeMemory(storage=None, gist_id=GIST_IDS.get("narrative", ""))
        logger.info("📖 Narrative Memory: الذاكرة السردية جاهزة!")
    except Exception as e:
        logger.error("فشل تهيئة Narrative Memory: %s", e)
        NARRATIVE_AVAILABLE = False

if ORACLE_AVAILABLE and NARRATIVE_AVAILABLE and CHRONOS_AVAILABLE:
    try:
        ORACLE = OracleEngine(nucleus=NARRATIVE, chronos=CHRONOS)
        logger.info("🔮 Oracle Engine: التنبؤ الاحتمالي جاهز!")
    except Exception as e:
        logger.error("فشل تهيئة Oracle Engine: %s", e)
        ORACLE_AVAILABLE = False

if DREAM_AVAILABLE and PROMETHEUS_AVAILABLE:
    try:
        DREAM = DreamEngine(prometheus=PROMETHEUS)
        logger.info("🌙 Dream Engine: الحلم نشط!")
        # ✅ سيتم ربط memory_engine و learning_orchestrator في PART 30 بعد تهيئتهما
    except Exception as e:
        logger.error("فشل تهيئة Dream Engine: %s", e)
        DREAM_AVAILABLE = False

if FUSION_AVAILABLE and PROMETHEUS_AVAILABLE:
    try:
        FUSION = FusionBridge(
            prometheus=PROMETHEUS,
            chronos=CHRONOS,
            oracle=ORACLE,
            narrative=NARRATIVE
        )
        logger.info("🌉 Fusion Bridge: جسر الدمج نشط!")
    except Exception as e:
        logger.error("فشل تهيئة Fusion Bridge: %s", e)
        FUSION_AVAILABLE = False

logger.info("🔥 تولين AI Prometheus Edition V13.0 - بدء التشغيل...")
logger.info("💙 الاسم الشخصي: تولين (الروح الجديدة)")
logger.info("👨‍💻 المطور: بسام الحوباني")
logger.info("🧠 Prometheus Consciousness Engine: %s", "نشط" if PROMETHEUS_AVAILABLE else "معطل")
logger.info("⏰ Chronos Engine: %s", "نشط" if CHRONOS_AVAILABLE else "معطل")
logger.info("🔮 Oracle Engine: %s", "نشط" if ORACLE_AVAILABLE else "معطل")
logger.info("🌙 Dream Engine: %s", "نشط" if DREAM_AVAILABLE else "معطل")
logger.info("📖 Narrative Memory: %s", "نشط" if NARRATIVE_AVAILABLE else "معطل")
logger.info("🌉 Fusion Bridge: %s", "نشط" if FUSION_AVAILABLE else "معطل")

# ====================================================================================
# 📦 PART 08: تهيئة المحركات المساعدة
# ====================================================================================

# 1. Persona
if PERSONA_AVAILABLE:
    try:
        PERSONA = HOBANYPersona()
        logger.info("👤 شخصية تولين جاهزة!")
    except Exception as e:
        logger.error(f"فشل تهيئة Persona: {e}")
        PERSONA_AVAILABLE = False

# 2. Intent Classifier
if INTENT_AVAILABLE:
    try:
        INTENT_CLASSIFIER = IntentClassifier()
        logger.info("🎯 تصنيف النية جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Intent: {e}")
        INTENT_AVAILABLE = False

# 3. Language Understanding
if LANGUAGE_AVAILABLE:
    try:
        LANGUAGE_UNDERSTANDING = LanguageUnderstanding()
        logger.info("🗣️ فهم اللغة جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Language: {e}")
        LANGUAGE_AVAILABLE = False

# 4. Context Builder
if CONTEXT_BUILDER_AVAILABLE:
    try:
        CONTEXT_BUILDER = ContextBuilder()
        logger.info("🏗️ بناء السياق جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Context Builder: {e}")
        CONTEXT_BUILDER_AVAILABLE = False

# 5. Decision Matrix
if DECISION_AVAILABLE:
    try:
        DECISION_MATRIX = DecisionMatrix()
        logger.info("📋 مصفوفة القرار جاهزة!")
    except Exception as e:
        logger.error(f"فشل تهيئة Decision Matrix: {e}")
        DECISION_AVAILABLE = False

# 6. Conversation Engine
if CONVERSATION_AVAILABLE:
    try:
        CONVERSATION_ENGINE = ConversationEngine(api_key=GROQ_API_KEY)
        logger.info("💬 محرك المحادثة جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Conversation: {e}")
        CONVERSATION_AVAILABLE = False

# 7. AI Brain
if AI_BRAIN_AVAILABLE and GROQ_API_KEY:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("memory", "learning_data/memory.db")
        else:
            db_path = "learning_data/memory.db"
        
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else "learning_data", exist_ok=True)
        AI_BRAIN = AIBrain(groq_api_key=GROQ_API_KEY, db_path=db_path)
        logger.info("🧠 AI Brain: العقل الخارق جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة AI Brain: {e}")
        AI_BRAIN_AVAILABLE = False

# 8. Risk Master
if RISK_MASTER_AVAILABLE:
    try:
        RISK_MASTER = RiskMaster(initial_capital=100.0, max_leverage=200.0)
        logger.info("🛡️ Risk Master: سيد المخاطر جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Risk Master: {e}")
        RISK_MASTER_AVAILABLE = False

# 9. Market Analyzer
if ANALYZER_AVAILABLE:
    try:
        MARKET_ANALYZER = MarketAnalyzer()
        logger.info("📊 المحلل الشامل جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Market Analyzer: {e}")
        ANALYZER_AVAILABLE = False

# 10. Advanced Indicators
if INDICATORS_AVAILABLE:
    try:
        ADVANCED_INDICATORS = AdvancedIndicators()
        logger.info("📈 المؤشرات المتقدمة جاهزة!")
    except Exception as e:
        logger.error(f"فشل تهيئة Advanced Indicators: {e}")
        INDICATORS_AVAILABLE = False

# 11. Memory
if MEMORY_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("memory", "learning_data/memory.db")
        else:
            db_path = "learning_data/memory.db"
        
        MEMORY = Memory(db_path=db_path)
        logger.info("💾 نظام الذاكرة جاهز")
    except Exception as e:
        logger.warning(f"نظام الذاكرة غير متوفر: {e}")
        MEMORY_AVAILABLE = False

# 12. Context Memory
if CONTEXT_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("context", "learning_data/context_memory.db")
        else:
            db_path = "learning_data/context_memory.db"
        
        CONTEXT_MEMORY = ContextMemory(db_path=db_path)
        logger.info("📖 سياق السوق جاهز")
    except Exception as e:
        logger.warning(f"سياق السوق غير متوفر: {e}")
        CONTEXT_AVAILABLE = False

# 13. Pattern Analyzer
if PATTERN_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("trades", "learning_data/trades.db")
        else:
            db_path = "learning_data/trades.db"
        
        PATTERN_ANALYZER = PatternAnalyzer(db_path=db_path)
        logger.info("🔍 محلل الأنماط جاهز")
    except Exception as e:
        logger.warning(f"محلل الأنماط غير متوفر: {e}")
        PATTERN_AVAILABLE = False

# 14. Predictor
if PREDICTOR_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("trades", "learning_data/trades.db")
        else:
            db_path = "learning_data/trades.db"
        
        PREDICTOR = Predictor(db_path=db_path)
        logger.info("🔮 نظام التنبؤ جاهز")
    except Exception as e:
        logger.warning(f"نظام التنبؤ غير متوفر: {e}")
        PREDICTOR_AVAILABLE = False

# 15. Learner
if LEARNER_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("trades", "learning_data/trades.db")
        else:
            db_path = "learning_data/trades.db"
        
        LEARNER = Learner(db_path=db_path)
        logger.info("🧠 نظام التعلم الآلي جاهز")
    except Exception as e:
        logger.warning(f"نظام التعلم الآلي غير متوفر: {e}")
        LEARNER_AVAILABLE = False

# 16. Learning System
if LEARNING_AVAILABLE:
    try:
        if DB_MANAGER_AVAILABLE:
            db_path = db_manager.connections.get("learning", "learning_data/learning.db")
        else:
            db_path = "learning_data/trades.db"
        
        LEARNING_SYSTEM = TradeLearningSystem(db_path=db_path)
        logger.info("📚 نظام التعلم الذكي جاهز")
    except Exception as e:
        logger.warning(f"نظام التعلم غير متوفر: {e}")
        LEARNING_AVAILABLE = False
      
TONA_ELITE_ENGINE = None
if TONA_ELITE_AVAILABLE:
    try:
        TONA_ELITE_ENGINE = TonaEliteEngine(groq_api_key=GROQ_API_KEY)
        logger.info("🧠 Tona Elite Engine: محرك الاستخبارات جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Tona Elite Engine: {e}")
        TONA_ELITE_AVAILABLE = False


# ====================================================================================
# 📦 PART 09: أنظمة المستشار المتقدم (إضافة جديدة)
# ====================================================================================

CONFIDENCE_SCORER = None
CONVICTION_REPORT = None
POST_MORTEM = None
SIMILAR_ANALYZER = None
DEEP_ANALYZER = None

if CONFIDENCE_AVAILABLE:
    try:
        CONFIDENCE_SCORER = ConfidenceScorer()
        logger.info("📊 Confidence Scorer: جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Confidence Scorer: {e}")
        CONFIDENCE_AVAILABLE = False

if CONVICTION_AVAILABLE:
    try:
        CONVICTION_REPORT = ConvictionReport()
        logger.info("📋 Conviction Report: جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Conviction Report: {e}")
        CONVICTION_AVAILABLE = False

if POST_MORTEM_AVAILABLE:
    try:
        POST_MORTEM = TradePostMortem()
        logger.info("🧠 Trade Post-Mortem: جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Trade Post-Mortem: {e}")
        POST_MORTEM_AVAILABLE = False

if SIMILAR_AVAILABLE:
    try:
        SIMILAR_ANALYZER = SimilarCasesAnalyzer(
            learning_db=DEEP_LEARNING_DB if DEEP_LEARNING_AVAILABLE else None
        )
        logger.info("📚 Similar Cases Analyzer: جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Similar Cases Analyzer: {e}")
        SIMILAR_AVAILABLE = False

if DEEP_ANALYZER_AVAILABLE:
    try:
        DEEP_ANALYZER = DeepResultAnalyzer(
            learning_db=DEEP_LEARNING_DB if DEEP_LEARNING_AVAILABLE else None
        )
        logger.info("🔍 Deep Result Analyzer: جاهز!")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة Deep Result Analyzer: {e}")
        DEEP_ANALYZER_AVAILABLE = False

logger.info("📊 أنظمة المستشار المتقدم: Confidence=%s, Conviction=%s, PostMortem=%s, Similar=%s, Deep=%s",
            "نشط" if CONFIDENCE_AVAILABLE else "معطل",
            "نشط" if CONVICTION_AVAILABLE else "معطل",
            "نشط" if POST_MORTEM_AVAILABLE else "معطل",
            "نشط" if SIMILAR_AVAILABLE else "معطل",
            "نشط" if DEEP_ANALYZER_AVAILABLE else "معطل")


# ====================================================================================
# 📦 PART 09.5: تهيئة TCN (شبكة الوعي) + MainWrapper الموسع
# ====================================================================================

TCN = None

# ── ✅ تعريف MainWrapper الموسع ──
class MainWrapper:
    """الواجهة الموحدة بين TCN والدوال العامة في main"""
    def __init__(self):
        pass
    
    def __getattr__(self, name):
        """الوصول الديناميكي لأي دالة في النطاق العام"""
        if name in globals():
            return globals()[name]
        if hasattr(self, name):
            return getattr(self, name)
        raise AttributeError(f"الدالة {name} غير معرفة")
    
    @property
    def queue_telegram_message(self):
        return queue_telegram_message
    
    @property
    def send_message(self):
        return queue_telegram_message
    
    @property
    def perform_comprehensive_analysis(self):
        return perform_comprehensive_analysis
    
    @property
    def get_current_open_trade(self):
        return get_current_open_trade
    
    @property
    def get_last_closed_trade(self):
        return get_last_closed_trade
    
    @property
    def get_fear_greed_index(self):
        return get_fear_greed_index
    
    @property
    def close_trade_virtual(self):
        return close_trade_virtual
    
    @property
    def get_mexc_candles(self):
        return get_mexc_candles
    
    @property
    def load_config(self):
        return load_config
    
    @property
    def calculate_statistics(self):
        return calculate_statistics
    
    @property
    def format_concise_analysis(self):
        """✅ إضافة دالة التحليل الشامل إلى MainWrapper"""
        try:
            from advisor_core import format_concise_analysis
            return format_concise_analysis
        except ImportError:
            # تعريف بديل
            def fallback_format(analysis, asset_type, is_monitoring=False, open_trade=None):
                return "⚠️ تحليل غير متوفر"
            return fallback_format
    
    @property
    def generate_groq_chat_response(self):
        """✅ إضافة دالة Groq إلى MainWrapper"""
        return generate_groq_chat_response
    
    @property
    def convert_markdown_to_html(self):
        """✅ دالة تنسيق الردود للـ Telegram"""
        return convert_markdown_to_html
    
    @property
    def AccountingSystem(self):
        return AccountingSystem
    
    @property
    def calculate_vpt_supertrend_v11(self):
        return calculate_vpt_supertrend_v11
    
    @property
    def calculate_supertrend_vpt_correct(self):
        return calculate_supertrend_vpt_correct
    
    @property
    def calculate_rsi_7(self):
        return calculate_rsi_7
    
    @property
    def calculate_macd_histogram(self):
        return calculate_macd_histogram
    
    @property
    def calculate_adx_14(self):
        return calculate_adx_14
    
    @property
    def calculate_atr_14(self):
        return calculate_atr_14
    
    @property
    def calculate_bollinger_bands(self):
        return calculate_bollinger_bands
    
    @property
    def calculate_stochastic(self):
        return calculate_stochastic
    
    @property
    def calculate_vwap(self):
        return calculate_vwap
    
    @property
    def analyze_and_send(self):
        return analyze_and_send
    
    @property
    def load_trades_history(self):
        return load_trades_history
    
    @property
    def save_trades_history(self):
        return save_trades_history
    
    # ✅ إضافة المدير الذكي الجديد
    @property
    def smart_conversation_manager(self):
        try:
            from main import SMART_MANAGER
            return SMART_MANAGER
        except:
            return None
    
    def get_current_price(self, asset_type):
        """الحصول على السعر الحالي"""
        try:
            symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
            data = get_mexc_candles(symbol, "Min1", 5)
            if data and data.get("closes"):
                return data["closes"][-1]
        except:
            pass
        return 0

MAIN_WRAPPER = MainWrapper()

if TCN_AVAILABLE:
    try:
        # جمع المحركات المتوفرة (موسع بالكامل)
        engines_dict = {}
        
        if ANALYZER_AVAILABLE and MARKET_ANALYZER:
            engines_dict['market_analyzer'] = MARKET_ANALYZER
            logger.info("📊 Market Analyzer: تم إضافته إلى TCN")
        
        if INDICATORS_AVAILABLE and ADVANCED_INDICATORS:
            engines_dict['advanced_indicators'] = ADVANCED_INDICATORS
            logger.info("📈 Advanced Indicators: تم إضافته إلى TCN")
        
        if PATTERN_AVAILABLE and PATTERN_ANALYZER:
            engines_dict['pattern_analyzer'] = PATTERN_ANALYZER
            logger.info("🔍 Pattern Analyzer: تم إضافته إلى TCN")
        
        if PREDICTOR_AVAILABLE and PREDICTOR:
            engines_dict['predictor'] = PREDICTOR
            logger.info("🔮 Predictor: تم إضافته إلى TCN")
        
        if PROMETHEUS_AVAILABLE and PROMETHEUS:
            engines_dict['prometheus'] = PROMETHEUS
            logger.info("🔥 Prometheus: تم إضافته إلى TCN")
        
        if CHRONOS_AVAILABLE and CHRONOS:
            engines_dict['chronos'] = CHRONOS
            logger.info("⏰ Chronos: تم إضافته إلى TCN")
        
        if ORACLE_AVAILABLE and ORACLE:
            engines_dict['oracle'] = ORACLE
            logger.info("🔮 Oracle: تم إضافته إلى TCN")
        
        if RISK_MASTER_AVAILABLE and RISK_MASTER:
            engines_dict['risk_master'] = RISK_MASTER
            logger.info("🛡️ Risk Master: تم إضافته إلى TCN")
        
        if DECISION_AVAILABLE and DECISION_MATRIX:
            engines_dict['decision_matrix'] = DECISION_MATRIX
            logger.info("📋 Decision Matrix: تم إضافته إلى TCN")
        
        if CONFIDENCE_AVAILABLE and CONFIDENCE_SCORER:
            engines_dict['confidence_scorer'] = CONFIDENCE_SCORER
            logger.info("📊 Confidence Scorer: تم إضافته إلى TCN")
        
        if LEARNER_AVAILABLE and LEARNER:
            engines_dict['learner'] = LEARNER
            logger.info("🧠 Learner: تم إضافته إلى TCN")
        
        if PERSONA_AVAILABLE and PERSONA:
            engines_dict['persona'] = PERSONA
            logger.info("👤 Persona: تم إضافته إلى TCN")
        
        if INTENT_AVAILABLE and INTENT_CLASSIFIER:
            engines_dict['intent_classifier'] = INTENT_CLASSIFIER
            logger.info("🎯 Intent Classifier: تم إضافته إلى TCN")
        
        if LANGUAGE_AVAILABLE and LANGUAGE_UNDERSTANDING:
            engines_dict['language_understanding'] = LANGUAGE_UNDERSTANDING
            logger.info("🗣️ Language Understanding: تم إضافته إلى TCN")
        
        if MEMORY_AVAILABLE and MEMORY:
            engines_dict['memory'] = MEMORY
            logger.info("💾 Memory: تم إضافته إلى TCN")
        
        if FUSION_AVAILABLE and FUSION:
            engines_dict['fusion'] = FUSION
            logger.info("🌉 Fusion: تم إضافته إلى TCN")
        
        if DREAM_AVAILABLE and DREAM:
            engines_dict['dream'] = DREAM
            logger.info("🌙 Dream: تم إضافته إلى TCN")
        
        if NARRATIVE_AVAILABLE and NARRATIVE:
            engines_dict['narrative'] = NARRATIVE
            logger.info("📖 Narrative: تم إضافته إلى TCN")
        
        if TONA_ELITE_AVAILABLE and TONA_ELITE_ENGINE:
            engines_dict['tona_intelligence'] = TONA_ELITE_ENGINE
            logger.info("🧠 Tona Intelligence: تم إضافته إلى TCN")
        
        # ✅ إضافة المحركات الإضافية (إن وجدت)
        if POST_MORTEM_AVAILABLE and POST_MORTEM:
            engines_dict['post_mortem'] = POST_MORTEM
            logger.info("🧠 Post Mortem: تم إضافته إلى TCN")
        
        if SIMILAR_AVAILABLE and SIMILAR_ANALYZER:
            engines_dict['similar_analyzer'] = SIMILAR_ANALYZER
            logger.info("📚 Similar Analyzer: تم إضافته إلى TCN")
        
        if DEEP_ANALYZER_AVAILABLE and DEEP_ANALYZER:
            engines_dict['deep_analyzer'] = DEEP_ANALYZER
            logger.info("🔍 Deep Analyzer: تم إضافته إلى TCN")
        
        if CONVICTION_AVAILABLE and CONVICTION_REPORT:
            engines_dict['conviction_report'] = CONVICTION_REPORT
            logger.info("📋 Conviction Report: تم إضافته إلى TCN")
        
        # ── إنشاء TCN مع جميع المحركات ──
        TCN = create_consciousness_network(
            main_instance=MAIN_WRAPPER,
            **engines_dict
        )
        
        # تحميل الحالة السابقة إن وجدت
        try:
            TCN.load_state()
            logger.info("🧠 تم تحميل حالة TCN السابقة")
        except Exception as e:
            logger.info(f"🧠 لا توجد حالة TCN سابقة — بداية جديدة ({e})")
        
        logger.info("🧠 TCN: الشبكة العصبية الواعية جاهزة!")
        logger.info(f"📊 عدد المحركات المسجلة في TCN: {len(engines_dict)}")
        print("🧠 تولين: المدير العام استيقظ! 💙")
        
    except Exception as e:
        logger.error(f"❌ فشل تهيئة TCN: {e}")
        import traceback
        logger.error(traceback.format_exc())
        TCN_AVAILABLE = False
        TCN = None

# ====================================================================================
# 📦 PART 10: دوال إدارة الملفات والبيانات (المصدر الموحد – مع توحيد الجداول)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. توحيد جميع الجداول المستخدمة في البوت.
#   2. التأكد من استخدام جدول snapshots بدلاً من monitoring_snapshots.
#   3. جعل Supabase هو المصدر الأساسي للحفظ والقراءة.
#   4. جعل Gist هو النسخة الاحتياطية النهائية (يحفظ دائماً).
#   5. إزالة أي دالة تحذف الصفقات (cleanup_old_trades محذوفة نهائياً).
#   6. إضافة دالة close_stuck_trades_only التي تُغلق الصفقات العالقة (تحديث exit_time) دون حذف.
#   7. الحفاظ على جميع الدوال الأخرى دون تغيير.
#   8. ✅ إضافة متغيرات عامة موحدة لأسماء جداول Supabase لتسهيل الصيانة.
#   9. ✅ استبدال جميع النصوص الحرفية لأسماء الجداول بالمتغيرات الموحدة.
#  10. ✅ تعديل get_current_open_trade بإضافة التحقق من trades_history لمنع إعادة استخدام الصفقات المغلقة.
#  11. ✅ ✅ ✅ تعديل load_trades_history بإضافة معامل update_cache=False لتجنب الحفظ المتكرر في SQLite من HealthCheck.
# ====================================================================================

import time
import json
import os
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging

# ── متغيرات التسجيل ──
TRADE_LOGGER = logging.getLogger("TradeLogger")
TRADE_LOGGER.setLevel(logging.INFO)

# ── متغير تحديد المصدر الأساسي ──
LEARNING_SOURCE = "supabase"

# ================================================================
# ✅ أسماء الجداول الموحدة في Supabase (لضمان التوافق والصيانة)
# ================================================================

TABLE_TRADES_FULL = "trades_full"
TABLE_LESSONS_DEEP = "lessons_deep"
TABLE_DISCOVERED_PATTERNS = "discovered_patterns"
TABLE_SNAPSHOTS = "snapshots"
TABLE_TRADE_PREDICTIONS = "trade_predictions"

# ================================================================
# ✅ الأعمدة المعتمدة لكل جدول (للفلترة والتوافق)
# ================================================================

TRADES_FULL_COLUMNS = {
    'id', 'trade_id', 'asset_type', 'trade_type', 'entry_price', 'exit_price',
    'profit_dollars', 'profit_pct', 'exit_reason', 'entry_time', 'exit_time',
    'duration_minutes', 'max_profit', 'max_loss', 'max_drawdown', 'recovery_time',
    'entry_rsi', 'entry_adx', 'entry_macd', 'entry_trend', 'entry_volume_ratio',
    'entry_vwap', 'entry_bb_upper', 'entry_bb_lower', 'entry_support', 'entry_resistance',
    'entry_comprehensive_score', 'entry_comprehensive_grade',
    'close_rsi', 'close_adx', 'close_macd', 'close_trend', 'close_volume_ratio',
    'close_vwap', 'close_bb_upper', 'close_bb_lower', 'close_support', 'close_resistance',
    'close_comprehensive_score', 'close_comprehensive_grade',
    'sl_price', 'tp_price', 'rr', 'confidence', 'warning_level',
    'full_entry_analysis', 'full_exit_analysis', 'warnings_sent', 'recommendations_sent',
    'trade_count', 'source', 'is_simulated', 'created_at', 'updated_at',
    'exit_timestamp'
}

LESSONS_DEEP_COLUMNS = {
    'id', 'trade_id', 'asset_type', 'type', 'summary', 'details',
    'key_factors', 'key_factors_str', 'grade', 'profit_dollars',
    'source', 'created_at', 'content_hash'
}

PATTERNS_COLUMNS = {
    'id', 'pattern_name', 'conditions', 'win_rate', 'sample_count',
    'avg_profit', 'score', 'description', 'asset_type', 'source',
    'last_used', 'created_at', 'updated_at'
}

# ✅ توحيد جدول اللقطات على snapshots
SNAPSHOTS_COLUMNS = {
    'id', 'trade_id', 'asset_type', 'timestamp', 'price', 'rsi', 'adx',
    'macd', 'st_trend', 'volume_ratio', 'profit_dollars', 'profit_pct',
    'warning_level', 'fear_greed_index', 'market_regime', 'bb_upper',
    'bb_middle', 'bb_lower', 'vwap', 'support', 'resistance', 'trend',
    'last_analysis', 'created_at'
}

# ✅ أعمدة جدول التوقعات (إضافة جديدة)
TRADE_PREDICTIONS_COLUMNS = {
    'id', 'trade_id', 'asset_type', 'trade_type', 'predicted_outcome',
    'confidence', 'entry_price', 'exit_price', 'profit_dollars',
    'quality_score', 'regime', 'conditions', 'indicator_scores',
    'red_flags', 'similar_patterns_count', 'similar_lessons_count',
    'false_signal_score', 'false_signal_reasons', 'actual_outcome',
    'was_correct', 'created_at', 'updated_at'
}

# ================================================================
# ✅ دوال التصفية
# ================================================================

def _filter_data_for_table(data: dict, table_name: str) -> dict:
    if table_name == TABLE_TRADES_FULL:
        valid_columns = TRADES_FULL_COLUMNS
    elif table_name == TABLE_LESSONS_DEEP:
        valid_columns = LESSONS_DEEP_COLUMNS
    elif table_name == TABLE_DISCOVERED_PATTERNS:
        valid_columns = PATTERNS_COLUMNS
    elif table_name == TABLE_SNAPSHOTS:
        valid_columns = SNAPSHOTS_COLUMNS
    elif table_name == TABLE_TRADE_PREDICTIONS:
        valid_columns = TRADE_PREDICTIONS_COLUMNS
    else:
        return data
    
    filtered = {}
    for key, value in data.items():
        if key in valid_columns:
            filtered[key] = value
        else:
            logger.debug(f"ℹ️ تجاهل الحقل '{key}' (غير موجود في جدول {table_name})")
    
    return filtered

# ================================================================
# ✅ دوال Gist الموحدة (المصدر الأساسي في PART 10)
# ================================================================

def _get_gist_file_content(gist_id: str, filename: str) -> Optional[str]:
    if not gist_id or not GITHUB_TOKEN:
        return None
    try:
        resp = requests.get(f"{GIST_BASE_URL}/{gist_id}", headers=GIST_HEADERS, timeout=10)
        if resp.status_code == 200:
            files = resp.json().get('files', {})
            if filename in files:
                return files[filename].get('content')
        return None
    except:
        return None

def _update_gist_file(gist_id: str, filename: str, content: str, max_retries: int = 2) -> bool:
    if not gist_id or not GITHUB_TOKEN:
        return False
    
    for attempt in range(max_retries):
        try:
            payload = {"files": {filename: {"content": content}}}
            resp = requests.patch(f"{GIST_BASE_URL}/{gist_id}", headers=GIST_HEADERS, json=payload, timeout=15)
            
            if resp.status_code == 200:
                logger.info(f"✅ تم تحديث {filename} في Gist {gist_id}")
                return True
            elif resp.status_code == 404:
                logger.warning(f"⚠️ Gist {gist_id} غير موجود – تحقق من GIST_IDS")
                return False
            elif resp.status_code == 403:
                reset_time = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait = max(0, reset_time - int(time.time()))
                if wait > 0:
                    time.sleep(min(wait, 30))
                if attempt < max_retries - 1:
                    continue
                return False
            else:
                logger.warning(f"⚠️ فشل تحديث Gist: {resp.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return False
        except Exception as e:
            logger.error(f"❌ خطأ في تحديث Gist: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return False
    return False

def save_json_to_gist_file(filename: str, data: dict, gist_key: str = None) -> bool:
    if not GITHUB_TOKEN:
        return False
    
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
    except TypeError:
        try:
            cleaned = json.loads(json.dumps(data, default=str))
            content = json.dumps(cleaned, indent=2, ensure_ascii=False)
        except:
            return False
    
    gist_id = None
    if gist_key:
        gist_id = GIST_IDS.get(gist_key)
    else:
        for gid in GIST_IDS.values():
            if gid:
                gist_id = gid
                break
    
    if not gist_id:
        logger.warning(f"⚠️ لا يوجد Gist ID لـ {filename}")
        return False
    
    return _update_gist_file(gist_id, filename, content)

def load_json_from_gist_file(filename: str, default: dict = None) -> dict:
    if default is None:
        default = {}
    for gist_id in GIST_IDS.values():
        if gist_id:
            content = _get_gist_file_content(gist_id, filename)
            if content:
                try:
                    return json.loads(content)
                except:
                    continue
    return default

# ================================================================
# ✅ دوال مساعدة للتعامل مع Supabase مباشرة
# ================================================================

def _get_supabase_client():
    if not SUPABASE_AVAILABLE or not SUPABASE_DB:
        return None
    if hasattr(SUPABASE_DB, 'client') and SUPABASE_DB.client:
        return SUPABASE_DB.client
    if hasattr(SUPABASE_DB, 'supabase') and SUPABASE_DB.supabase:
        return SUPABASE_DB.supabase
    if hasattr(SUPABASE_DB, '_client') and SUPABASE_DB._client:
        return SUPABASE_DB._client
    if hasattr(SUPABASE_DB, 'table'):
        return SUPABASE_DB
    return None

def _save_trade_to_supabase_with_retry(trade_data: dict, trade_id: str, max_retries: int = 3) -> bool:
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        return False

    client = _get_supabase_client()
    if not client:
        logger.error(f"❌ [_save_trade_to_supabase] لا يمكن الحصول على عميل Supabase")
        return False

    filtered_data = _filter_data_for_table(trade_data, TABLE_TRADES_FULL)
    
    json_fields = ['full_entry_analysis', 'full_exit_analysis', 'warnings_sent', 'recommendations_sent']
    for field in json_fields:
        if field in filtered_data and filtered_data[field] is not None:
            if isinstance(filtered_data[field], (dict, list)):
                filtered_data[field] = json.dumps(filtered_data[field], ensure_ascii=False)
            elif isinstance(filtered_data[field], str):
                try:
                    json.loads(filtered_data[field])
                except:
                    filtered_data[field] = json.dumps(filtered_data[field], ensure_ascii=False)

    float_fields = [
        'entry_price', 'exit_price', 'sl_price', 'tp_price', 'profit_dollars', 'profit_pct',
        'entry_rsi', 'entry_adx', 'entry_macd', 'entry_volume_ratio', 'entry_vwap',
        'entry_bb_upper', 'entry_bb_lower', 'entry_support', 'entry_resistance',
        'close_rsi', 'close_adx', 'close_macd', 'close_volume_ratio', 'close_vwap',
        'close_bb_upper', 'close_bb_lower', 'close_support', 'close_resistance',
        'rr', 'max_profit', 'max_loss', 'max_drawdown'
    ]
    for field in float_fields:
        if field in filtered_data and filtered_data[field] is not None:
            try:
                filtered_data[field] = float(filtered_data[field])
            except (ValueError, TypeError):
                filtered_data[field] = 0.0

    int_fields = ['duration_minutes', 'warning_level', 'confidence', 'entry_comprehensive_score', 
                  'close_comprehensive_score', 'trade_count', 'recovery_time']
    for field in int_fields:
        if field in filtered_data and filtered_data[field] is not None:
            try:
                filtered_data[field] = int(float(filtered_data[field]))
            except (ValueError, TypeError):
                filtered_data[field] = 0

    for attempt in range(max_retries):
        try:
            # التحقق من وجود السجل
            check = client.table(TABLE_TRADES_FULL).select('trade_id').eq('trade_id', trade_id).execute()
            
            if check.data:
                response = client.table(TABLE_TRADES_FULL).update(filtered_data).eq('trade_id', trade_id).execute()
                logger.info(f"🔄 [_save_trade_to_supabase] تحديث {trade_id} (محاولة {attempt+1})")
            else:
                response = client.table(TABLE_TRADES_FULL).insert(filtered_data).execute()
                logger.info(f"➕ [_save_trade_to_supabase] إدراج {trade_id} (محاولة {attempt+1})")
                
            if response and hasattr(response, 'data'):
                logger.info(f"✅ [_save_trade_to_supabase] تم حفظ {trade_id} في Supabase (محاولة {attempt+1})")
                return True
            else:
                logger.warning(f"⚠️ [_save_trade_to_supabase] فشل العملية (محاولة {attempt+1}): {response}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        except Exception as e:
            logger.error(f"❌ [_save_trade_to_supabase] استثناء (محاولة {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    return False

# ✅ الدالة الأساسية لحفظ اللقطات (معدلة - تستخدم TABLE_SNAPSHOTS)
def save_snapshot_to_learning(snapshot_data: Dict) -> bool:
    """
    حفظ لقطة في Supabase (جدول snapshots) + نسخة احتياطية محلية
    """
    if not snapshot_data:
        logger.warning("⚠️ [save_snapshot_to_learning] بيانات اللقطة فارغة")
        return False

    trade_id = snapshot_data.get('trade_id', '')
    if not trade_id:
        logger.warning("⚠️ [save_snapshot_to_learning] trade_id مفقود")
        return False

    logger.info(f"📸 [save_snapshot_to_learning] حفظ لقطة للصفقة {trade_id} في جدول {TABLE_SNAPSHOTS}")

    # 1. حفظ في Supabase (جدول snapshots)
    supabase_saved = False
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        client = _get_supabase_client()
        if client:
            try:
                filtered_data = _filter_data_for_table(snapshot_data, TABLE_SNAPSHOTS)
                if 'created_at' not in filtered_data:
                    filtered_data['created_at'] = datetime.now().isoformat()
                
                response = client.table(TABLE_SNAPSHOTS).insert(filtered_data).execute()
                if response and hasattr(response, 'data'):
                    supabase_saved = True
                    logger.info(f"📸 [save_snapshot_to_learning] تم حفظ اللقطة في Supabase (جدول {TABLE_SNAPSHOTS}): {trade_id}")
                else:
                    logger.warning(f"⚠️ [save_snapshot_to_learning] فشل حفظ اللقطة في Supabase: {response}")
            except Exception as e:
                logger.error(f"❌ [save_snapshot_to_learning] استثناء في Supabase: {e}")

    # 2. نسخة احتياطية محلية (دائماً)
    try:
        asset_type = snapshot_data.get('asset_type', 'unknown')
        backup_file = f"learning_data/backups/snapshots_{asset_type}.json"
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        
        backup_data = {}
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
        
        snapshots = backup_data.get('snapshots', [])
        # تجنب التكرار (نحتفظ بآخر 100 لقطة)
        snapshots = [s for s in snapshots if s.get('trade_id') != trade_id]
        snapshots.append(snapshot_data)
        if len(snapshots) > 100:
            snapshots = snapshots[-100:]
        
        backup_data['snapshots'] = snapshots
        backup_data['last_update'] = datetime.now().isoformat()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 [save_snapshot_to_learning] تم حفظ نسخة احتياطية للقطة في {backup_file}")
        return True
    except Exception as e:
        logger.error(f"❌ [save_snapshot_to_learning] فشل حفظ النسخة الاحتياطية: {e}")
        return supabase_saved  # نعيد نجاح Supabase إن كان قد نجح

# ================================================================
# ✅ دوال إدارة الملفات الأساسية
# ================================================================

def get_trades_file(asset_type):
    return TRADES_FILE_OIL if asset_type == "oil" else TRADES_FILE_SILVER

def get_position_file(asset_type):
    return CURRENT_POSITION_FILE_OIL if asset_type == "oil" else CURRENT_POSITION_FILE_SILVER

def safe_file_operation(asset_type, operation, *args, **kwargs):
    lock = FILE_LOCKS[asset_type]
    max_attempts = 3
    for attempt in range(max_attempts):
        acquired = lock.acquire(timeout=10)
        if acquired:
            try:
                logger.info(f"🔒 [safe_file_operation] تم الحصول على قفل {asset_type} (محاولة {attempt+1})")
                result = operation(*args, **kwargs)
                logger.info(f"🔓 [safe_file_operation] تم تحرير قفل {asset_type}")
                return result
            finally:
                lock.release()
        else:
            logger.warning(f"⚠️ [safe_file_operation] فشل الحصول على قفل {asset_type} (محاولة {attempt+1}/{max_attempts})")
            if attempt < max_attempts - 1:
                time.sleep(0.5)
    logger.error(f"❌ [safe_file_operation] فشل الحصول على قفل {asset_type} بعد {max_attempts} محاولات")
    return None

def _safe_save_narrative() -> bool:
    if not NARRATIVE_AVAILABLE or not NARRATIVE:
        return False
    try:
        if hasattr(NARRATIVE, 'save_state'):
            NARRATIVE.save_state()
            logger.info("💾 تم حفظ الذاكرة السردية (save_state)")
            return True
        elif hasattr(NARRATIVE, 'save'):
            NARRATIVE.save()
            logger.info("💾 تم حفظ الذاكرة السردية (save)")
            return True
        elif hasattr(NARRATIVE, 'flush'):
            NARRATIVE.flush()
            logger.info("💾 تم حفظ الذاكرة السردية (flush)")
            return True
        else:
            logger.info("ℹ️ الذاكرة السردية تحفظ تلقائياً")
            return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ الذاكرة السردية: {e}")
        return False

def load_config():
    default_config = {
        "strategies": {
            "oil": {
                "st_multiplier": 1.5,
                "st_period": 100,
                "vpt_len": 10,
                "vpt_ema_length": 14,
                "base_timeframe": "Min15",
                "use_rsi_filter": False,
                "use_macd_filter": False,
                "use_adx_filter": False,
                "rsi_period": 7,
                "rsi_min": 35,
                "rsi_max": 65,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "macd_threshold": 0.0,
                "sltp_mode": "ATR",
                "sl_atr_mult": 2.0,
                "tp_atr_mult": 3.0,
                "min_rr": 1.0,
                "use_trailing": True,
                "trail_offset": 1.5,
                "channel_buffer": 0.0,
                "risk_per_trade": 1.0,
                "max_leverage": 200.0,
            },
            "silver": {
                "st_multiplier": 2.2,
                "st_period": 100,
                "vpt_len": 10,
                "vpt_ema_length": 10,
                "base_timeframe": "Min15",
                "use_rsi_filter": True,
                "use_macd_filter": True,
                "use_adx_filter": False,
                "rsi_period": 7,
                "rsi_min": 35,
                "rsi_max": 65,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "macd_threshold": 0.0,
                "sltp_mode": "ATR",
                "sl_atr_mult": 2.0,
                "tp_atr_mult": 3.0,
                "min_rr": 1.0,
                "use_trailing": True,
                "trail_offset": 1.5,
                "channel_buffer": 0.0,
                "risk_per_trade": 1.0,
                "max_leverage": 200.0,
            }
        },
        "system": {
            "bot_name": "تولين",
            "developer": "بسام الحوباني",
            "version": "V12.0"
        }
    }
    try:
        cloud = load_json_from_gist("config", default_config)
        for key, val in default_config.items():
            if key not in cloud:
                cloud[key] = val
            elif isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    if sub_key not in cloud[key]:
                        cloud[key][sub_key] = sub_val
        return cloud
    except:
        return default_config

# ================================================================
# ✅ دوال التحميل والحفظ الرئيسية (المعدلة)
# ================================================================

def _update_sqlite_cache(asset_type, history):
    if not DEEP_LEARNING_AVAILABLE or not DEEP_LEARNING_DB:
        return
    try:
        for trade in history.get('trades', []):
            if trade.get('trade_id'):
                DEEP_LEARNING_DB.save_trade_full(trade)
        logger.info(f"💾 تم تحديث SQLite لـ {asset_type} ({len(history.get('trades', []))} صفقة)")
    except Exception as e:
        logger.warning(f"⚠️ فشل تحديث SQLite لـ {asset_type}: {e}")

def _restore_from_gist(asset_type, history):
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        try:
            for trade in history.get('trades', []):
                if trade.get('trade_id'):
                    _save_trade_to_supabase_with_retry(trade, trade.get('trade_id'))
            logger.info(f"☁️ تم استعادة {asset_type} من Gist إلى Supabase ({len(history.get('trades', []))} صفقة)")
        except Exception as e:
            logger.warning(f"⚠️ فشل استعادة {asset_type} من Gist إلى Supabase: {e}")
    _update_sqlite_cache(asset_type, history)

def load_trades_history(asset_type, update_cache=False):
    """
    تحميل سجل الصفقات - المصدر الأساسي: Supabase، النسخة الاحتياطية: Gist.
    في حال فشل Supabase، يقرأ من Gist ويعيد المزامنة إلى Supabase.
    ✅ update_cache: إذا كان True، يتم تحديث SQLite (يُستخدم فقط عند الحاجة، وليس في كل مرة).
    """
    file = get_trades_file(asset_type)
    history = {"trades": [], "last_cleanup": datetime.now().isoformat()}
    loaded_from = None

    # 1. محاولة القراءة من Supabase (المصدر الأساسي)
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        try:
            client = _get_supabase_client()
            if client:
                response = client.table(TABLE_TRADES_FULL)\
                    .select('*')\
                    .eq('asset_type', asset_type)\
                    .order('entry_time', desc=True)\
                    .limit(1000)\
                    .execute()
                if response and hasattr(response, 'data') and response.data:
                    trades = response.data
                    history = {"trades": trades, "last_cleanup": datetime.now().isoformat()}
                    loaded_from = "Supabase (Direct)"
                    logger.info(f"✅ تم تحميل {asset_type} من Supabase مباشرة ({len(trades)} صفقة)")
                    # ✅ تحديث SQLite فقط إذا طُلب ذلك (وليس في كل مرة)
                    if update_cache:
                        _update_sqlite_cache(asset_type, history)
                    return history
        except Exception as e:
            logger.warning(f"⚠️ فشل تحميل {asset_type} من Supabase مباشرة: {e}")

    # 2. محاولة القراءة من SQLite (كاش)
    if DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
        try:
            trades = DEEP_LEARNING_DB.get_trades_by_asset(asset_type, 1000)
            if trades:
                history = {"trades": trades, "last_cleanup": datetime.now().isoformat()}
                loaded_from = "SQLite (Cache)"
                logger.info(f"✅ تم تحميل {asset_type} من SQLite ({len(trades)} صفقة)")
                # إذا تم التحميل من SQLite، لا نحتاج لتحديث الكاش (هو نفسه)
                return history
        except Exception as e:
            logger.warning(f"⚠️ فشل تحميل {asset_type} من SQLite: {e}")

    # 3. محاولة القراءة من Gist (النسخة الاحتياطية)
    try:
        filename = f"trades_history_{asset_type}.json"
        data = load_json_from_gist_file(filename, None)
        if data and data.get('trades'):
            history = data
            loaded_from = "Gist (Backup)"
            logger.info(f"✅ تم تحميل {asset_type} من Gist ({len(data.get('trades', []))} صفقة)")
            # مزامنة مع Supabase
            _restore_from_gist(asset_type, history)
            return history
    except Exception as e:
        logger.warning(f"⚠️ فشل تحميل {asset_type} من Gist: {e}")

    # 4. محاولة القراءة من الملف المحلي (آخر حل)
    if os.path.exists(file) and os.path.getsize(file) > 0:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                history = json.load(f)
                loaded_from = "Local File (Last Resort)"
                logger.info(f"✅ تم تحميل {asset_type} من الملف المحلي ({len(history.get('trades', []))} صفقة)")
                _restore_from_gist(asset_type, history)
                return history
        except Exception as e:
            logger.warning(f"⚠️ فشل قراءة الملف المحلي {asset_type}: {e}")

    logger.warning(f"⚠️ لم يتم العثور على بيانات لـ {asset_type} في أي مصدر")
    return {"trades": [], "last_cleanup": datetime.now().isoformat()}

def save_trades_history(asset_type, history):
    """
    حفظ سجل الصفقات - المصدر الأساسي: Supabase، النسخة الاحتياطية: Gist.
    يحاول دائماً حفظ Gist كنسخة احتياطية نهائية، بغض النظر عن نجاح Supabase.
    """
    trade_count = len(history.get("trades", []))
    logger.info(f"💾 حفظ {asset_type}: {trade_count} صفقة")
    file = get_trades_file(asset_type)
    backup_file = f"{file}.backup"

    # 1. حفظ في Supabase (المصدر الأساسي)
    supabase_saved = False
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        try:
            for trade in history.get("trades", []):
                if trade.get("trade_id"):
                    _save_trade_to_supabase_with_retry(trade, trade.get("trade_id"))
            supabase_saved = True
            logger.info(f"☁️ تم حفظ {asset_type} في Supabase ({trade_count} صفقة)")
        except Exception as e:
            logger.error(f"❌ فشل حفظ {asset_type} في Supabase: {e}")
    else:
        logger.warning("⚠️ Supabase غير متصل، تخطي الحفظ في Supabase")

    # 2. حفظ في SQLite (كاش)
    sqlite_saved = False
    if DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
        try:
            for trade in history.get("trades", []):
                if trade.get("trade_id"):
                    DEEP_LEARNING_DB.save_trade_full(trade)
            sqlite_saved = True
            logger.info(f"💾 تم حفظ {asset_type} في SQLite (كاش)")
        except Exception as e:
            logger.error(f"❌ فشل حفظ {asset_type} في SQLite: {e}")

    # 3. حفظ في Gist (النسخة الاحتياطية - دائماً)
    gist_success = False
    try:
        filename = f"trades_history_{asset_type}.json"
        gist_success = save_json_to_gist_file(filename, history, f"trades_{asset_type}")
        if gist_success:
            logger.info(f"✅ تم حفظ {asset_type} في Gist (نسخة احتياطية نهائية)")
        else:
            logger.error(f"❌ فشل حفظ {asset_type} في Gist (نسخة احتياطية)")
    except Exception as e:
        logger.error(f"❌ خطأ في حفظ {asset_type} في Gist: {e}")

    # 4. حفظ محلي (دائماً)
    local_success = False
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        local_success = True
        logger.info(f"✅ تم حفظ {asset_type} في الملف المحلي: {file}")
    except Exception as e:
        logger.error(f"❌ خطأ في حفظ {asset_type} في الملف المحلي: {e}")

    # 5. إعادة محاولة Supabase إذا فشل
    if not supabase_saved and trade_count > 0:
        def retry_supabase():
            logger.info(f"🔄 إعادة محاولة حفظ {asset_type} في Supabase...")
            save_trades_history(asset_type, history)
        threading.Timer(10.0, retry_supabase).start()

    overall_success = supabase_saved or sqlite_saved or gist_success or local_success
    if not overall_success:
        logger.error(f"❌ فشل حفظ {asset_type} في جميع المصادر!")
    else:
        logger.info(f"✅ اكتمل حفظ {asset_type} (Supabase: {supabase_saved}, SQLite: {sqlite_saved}, Gist: {gist_success}, Local: {local_success})")
    
    return overall_success

# ✅ تعديل دالة get_current_open_trade (مع التحقق من trades_history)
def get_current_open_trade(asset_type):
    pos_file = get_position_file(asset_type)
    logger.info(f"🔍 [get_current_open_trade] قراءة {pos_file}")
    
    if not os.path.exists(pos_file):
        logger.info(f"ℹ️ [get_current_open_trade] الملف {pos_file} غير موجود")
        return None
    
    file_size = os.path.getsize(pos_file) if os.path.exists(pos_file) else 0
    logger.info(f"📏 [get_current_open_trade] حجم الملف: {file_size} بايت")
    
    try:
        with open(pos_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                logger.warning(f"⚠️ [get_current_open_trade] الملف {pos_file} فارغ، سيتم حذفه")
                os.remove(pos_file)
                return None
            trade = json.loads(content)
            if trade and isinstance(trade, dict) and trade.get("status") == "open":
                trade_id = trade.get("trade_id")
                # ✅ التحقق من سجل الصفقات للتأكد من عدم إغلاقها بالفعل
                if trade_id:
                    history = load_trades_history(asset_type, update_cache=False)
                    for t in history.get("trades", []):
                        if t.get("trade_id") == trade_id and t.get("status") == "closed":
                            logger.warning(f"🗑️ [get_current_open_trade] الصفقة {trade_id} مغلقة بالفعل في السجل، سيتم حذف الملف {pos_file}")
                            os.remove(pos_file)
                            return None
                logger.info(f"✅ [get_current_open_trade] تم قراءة صفقة مفتوحة: {trade.get('trade_id')} ({trade.get('type')} @ {trade.get('entry_price')})")
                return trade
            else:
                logger.warning(f"⚠️ [get_current_open_trade] الملف {pos_file} لا يحتوي على صفقة مفتوحة (status={trade.get('status')})، سيتم حذفه")
                os.remove(pos_file)
                return None
    except json.JSONDecodeError as e:
        logger.error(f"❌ [get_current_open_trade] خطأ في تحليل JSON: {e}")
        try:
            os.remove(pos_file)
        except:
            pass
        return None
    except Exception as e:
        logger.error(f"❌ [get_current_open_trade] خطأ في قراءة {pos_file}: {e}")
        try:
            os.remove(pos_file)
        except:
            pass
        return None

def close_stuck_trades_only():
    """
    إغلاق الصفقات المفتوحة منذ أكثر من يومين (تحديث exit_time فقط، لا حذف)
    """
    logger.info("🧹 بدء إغلاق الصفقات العالقة (تحديث وليس حذف)...")
    for asset in ["oil", "silver"]:
        try:
            history = load_trades_history(asset, update_cache=False)
            updated = False
            for trade in history.get("trades", []):
                if trade.get('exit_time') is None and trade.get('exit_price') is None:
                    entry_time = trade.get('entry_time') or trade.get('timestamp')
                    if entry_time:
                        try:
                            entry_dt = datetime.fromisoformat(entry_time)
                            if (datetime.now() - entry_dt).days >= 2:
                                trade['exit_time'] = datetime.now().isoformat()
                                trade['exit_price'] = trade.get('entry_price', 0)
                                trade['exit_reason'] = "إغلاق تلقائي (عالقة > 2 يوم)"
                                updated = True
                                logger.info(f"🗑️ تم إغلاق صفقة عالقة (تحديث): {trade.get('trade_id')}")
                        except Exception as e:
                            logger.warning(f"⚠️ فشل تحليل وقت الصفقة {trade.get('trade_id')}: {e}")
            if updated:
                save_trades_history(asset, history)
                logger.info(f"✅ تم إغلاق الصفقات العالقة لـ {asset}")
        except Exception as e:
            logger.error(f"❌ فشل إغلاق الصفقات العالقة لـ {asset}: {e}")

try:
    close_stuck_trades_only()
except Exception as e:
    logger.error(f"❌ فشل تشغيل إغلاق الصفقات العالقة: {e}")

def calculate_statistics(asset_type):
    history = load_trades_history(asset_type, update_cache=False)
    all_trades = history.get("trades", [])
    logger.info(f"📊 حساب إحصائيات {asset_type}: {len(all_trades)} صفقة إجمالاً")

    closed_trades = [
        t for t in all_trades 
        if t.get("exit_time") is not None or t.get("exit_price") is not None
    ]
    
    open_trades = [
        t for t in all_trades 
        if t.get("exit_time") is None and t.get("exit_price") is None
    ]

    logger.info(f"📊 {asset_type}: {len(closed_trades)} مغلقة, {len(open_trades)} مفتوحة")

    if not closed_trades:
        logger.info(f"ℹ️ لا توجد صفقات مغلقة لـ {asset_type}")
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_profit": 0.0,
            "win_rate": 0.0,
            "current_balance": 100.0,
            "tp_count": 0,
            "sl_count": 0,
            "manual_count": 0,
            "strong_close": 0
        }

    winning_trades = []
    losing_trades = []
    total_profit = 0.0
    tp_count = 0
    sl_count = 0
    manual_count = 0
    strong_close = 0

    for t in closed_trades:
        profit = t.get("profit_dollars")
        if profit is None:
            profit = 0.0
        try:
            profit = float(profit)
        except (ValueError, TypeError):
            profit = 0.0
        
        total_profit += profit
        
        if profit > 0:
            winning_trades.append(t)
        elif profit < 0:
            losing_trades.append(t)
        
        exit_reason = t.get("exit_reason")
        if exit_reason is None:
            exit_reason = ""
        else:
            try:
                exit_reason = str(exit_reason)
            except:
                exit_reason = ""
        
        if exit_reason:
            if exit_reason == "Hit Take Profit":
                tp_count += 1
            elif exit_reason == "Hit Stop Loss":
                sl_count += 1
            elif "تحذير" in exit_reason or "انعكاس" in exit_reason:
                strong_close += 1
        
        manual_close = t.get("manual_close", False)
        if manual_close:
            manual_count += 1

    winning_count = len(winning_trades)
    losing_count = len(losing_trades)
    total_trades = len(closed_trades)
    win_rate = (winning_count / total_trades * 100) if total_trades > 0 else 0.0

    return {
        "total_trades": total_trades,
        "winning_trades": winning_count,
        "losing_trades": losing_count,
        "total_profit": round(total_profit, 2),
        "win_rate": round(win_rate, 2),
        "current_balance": round(100.0 + total_profit, 2),
        "tp_count": tp_count,
        "sl_count": sl_count,
        "manual_count": manual_count,
        "strong_close": strong_close
    }

def get_last_closed_trade(asset_type=None):
    all_trades = []
    for asset in ["oil", "silver"]:
        history = load_trades_history(asset, update_cache=False)
        for trade in history.get("trades", []):
            if trade.get("exit_time") is not None or trade.get("exit_price") is not None:
                trade["asset"] = asset
                all_trades.append(trade)
    all_trades.sort(key=lambda x: x.get("exit_time", x.get("timestamp", "")), reverse=True)
    if asset_type:
        all_trades = [t for t in all_trades if t.get("asset") == asset_type]
    return all_trades[0] if all_trades else None

# ================================================================
# ✅ الدالة الأساسية - add_trade_to_history (معدلة)
# ================================================================

def add_trade_to_history(asset_type, trade, holistic_entry_analysis=None) -> bool:
    trade_id = trade.get('trade_id', 'unknown')
    logger.info(f"🔴 [add_trade_to_history] استدعاء لـ {asset_type} – trade_id: {trade_id}")

    if 'trade_id' not in trade or not trade['trade_id']:
        trade['trade_id'] = f"{asset_type}_{int(datetime.now().timestamp())}"
        trade_id = trade['trade_id']
        logger.info(f"🆔 [add_trade_to_history] تم إنشاء trade_id: {trade_id}")
    if 'timestamp' not in trade or not trade['timestamp']:
        trade['timestamp'] = datetime.now().isoformat()
        logger.info(f"⏱️ [add_trade_to_history] تم تعيين timestamp: {trade['timestamp']}")
    
    trade['status'] = 'open'
    trade.setdefault('warnings_sent', [])
    trade.setdefault('warnings_log', [])
    trade.setdefault('recommendations_sent', [])
    if holistic_entry_analysis:
        trade['holistic_entry_analysis'] = holistic_entry_analysis
        logger.info(f"📊 [add_trade_to_history] تم حفظ التحليل الشامل")

    logger.info(f"📋 [add_trade_to_history] بيانات الصفقة: {trade.get('type')} @ {trade.get('entry_price')}, SL: {trade.get('sl')}, TP: {trade.get('tp')}, RR: {trade.get('rr')}")

    pos_file = get_position_file(asset_type)
    pos_saved = False
    
    def _save_position():
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(trade, f, indent=2, ensure_ascii=False)
        if os.path.exists(pos_file) and os.path.getsize(pos_file) > 0:
            with open(pos_file, 'r', encoding='utf-8') as f:
                verify = json.load(f)
                if verify.get('trade_id') == trade_id and verify.get('status') == 'open':
                    return True
        return False
    
    for attempt in range(3):
        result = safe_file_operation(asset_type, _save_position)
        if result:
            logger.info(f"✅ [add_trade_to_history] تم حفظ الصفقة في {pos_file} (محاولة {attempt+1})")
            pos_saved = True
            break
        else:
            logger.warning(f"⚠️ [add_trade_to_history] فشل حفظ {pos_file} في محاولة {attempt+1}")
            time.sleep(0.5)
    
    if not pos_saved:
        logger.error(f"❌ [add_trade_to_history] فشل حفظ {pos_file} بعد 3 محاولات")
        return False

    history_saved = False
    try:
        # ✅ عند إضافة صفقة جديدة، نُحدّث SQLite (update_cache=True)
        history = load_trades_history(asset_type, update_cache=True)
        existing = None
        for t in history.get('trades', []):
            if t.get('trade_id') == trade_id:
                existing = t
                break
        if existing:
            existing.update(trade)
            logger.info(f"🔄 [add_trade_to_history] تحديث صفقة موجودة في trades_history")
        else:
            history['trades'].append(trade)
            logger.info(f"➕ [add_trade_to_history] إضافة صفقة جديدة إلى trades_history")
        history_saved = save_trades_history(asset_type, history)
        if history_saved:
            logger.info(f"💾 [add_trade_to_history] تم تحديث trades_history لـ {asset_type}")
        else:
            logger.error(f"❌ [add_trade_to_history] فشل تحديث trades_history لـ {asset_type}")
    except Exception as e:
        logger.error(f"⚠️ [add_trade_to_history] فشل تحديث trades_history: {e}")

    supabase_saved = False
    try:
        if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
            entry_indicators = trade.get('entry_indicators', {})
            
            trade_full_data = {
                'trade_id': trade_id,
                'asset_type': asset_type,
                'trade_type': trade.get('type', 'BUY'),
                'entry_price': trade.get('entry_price', 0),
                'entry_time': trade.get('timestamp', datetime.now().isoformat()),
                'sl_price': trade.get('sl', 0),
                'tp_price': trade.get('tp', 0),
                'rr': trade.get('rr', 1.0),
                'confidence': trade.get('confidence', 70),
                'full_entry_analysis': holistic_entry_analysis,
                'entry_rsi': entry_indicators.get('rsi'),
                'entry_adx': entry_indicators.get('adx'),
                'entry_macd': entry_indicators.get('macd'),
                'entry_trend': entry_indicators.get('trend', 'محايد'),
                'entry_volume_ratio': entry_indicators.get('volume_ratio', 1.0),
                'entry_vwap': entry_indicators.get('vwap', trade.get('entry_price', 0)),
                'entry_bb_upper': entry_indicators.get('bb_upper', trade.get('entry_price', 0) * 1.02),
                'entry_bb_lower': entry_indicators.get('bb_lower', trade.get('entry_price', 0) * 0.98),
                'entry_support': entry_indicators.get('support', trade.get('entry_price', 0) * 0.98),
                'entry_resistance': entry_indicators.get('resistance', trade.get('entry_price', 0) * 1.02),
                'entry_comprehensive_score': entry_indicators.get('comprehensive_score', 50),
                'entry_comprehensive_grade': entry_indicators.get('comprehensive_grade', 'محايد')
            }
            
            for attempt in range(3):
                try:
                    supabase_saved = _save_trade_to_supabase_with_retry(trade_full_data, trade_id)
                    if supabase_saved:
                        logger.info(f"☁️ [add_trade_to_history] تم حفظ في Supabase (محاولة {attempt+1})")
                        break
                    else:
                        logger.warning(f"⚠️ [add_trade_to_history] فشل حفظ Supabase في محاولة {attempt+1}")
                        time.sleep(2)
                except Exception as e:
                    logger.error(f"❌ [add_trade_to_history] استثناء في حفظ Supabase (محاولة {attempt+1}): {e}")
                    time.sleep(2)
        else:
            logger.warning(f"⚠️ [add_trade_to_history] Supabase غير متصل، تخطي الحفظ")
    except Exception as e:
        logger.error(f"❌ [add_trade_to_history] فشل حفظ Supabase: {e}")

    narrative_saved = False
    if NARRATIVE_AVAILABLE and NARRATIVE:
        try:
            NARRATIVE.record_experience('trade', {
                'asset': asset_type,
                'type': trade['type'],
                'entry_price': trade['entry_price'],
                'sl': trade.get('sl', 0),
                'tp': trade.get('tp', 0)
            }, PROMETHEUS.emotion.__dict__ if PROMETHEUS else {})
            narrative_saved = _safe_save_narrative()
            if narrative_saved:
                logger.info(f"💾 [add_trade_to_history] تم حفظ الذاكرة السردية (صفقة {trade_id})")
            else:
                logger.warning(f"⚠️ [add_trade_to_history] فشل حفظ الذاكرة السردية")
        except Exception as e:
            logger.error(f"❌ [add_trade_to_history] فشل تسجيل الذاكرة السردية: {e}")

    if PROMETHEUS_AVAILABLE and PROMETHEUS:
        try:
            if hasattr(PROMETHEUS, 'update_emotion'):
                PROMETHEUS.update_emotion(trigger='new_trade', market={'asset': asset_type, 'price': trade['entry_price']})
            elif hasattr(PROMETHEUS, 'update_emotions'):
                PROMETHEUS.update_emotions({'trigger': 'new_trade', 'market': {'asset': asset_type, 'price': trade['entry_price']}})
            elif hasattr(PROMETHEUS, '_update_emotions'):
                PROMETHEUS._update_emotions({'trigger': 'new_trade', 'market': {'asset': asset_type, 'price': trade['entry_price']}})
            else:
                logger.warning(f"⚠️ [add_trade_to_history] لا توجد دالة تحديث مشاعر Prometheus متاحة")
            logger.info(f"💙 [add_trade_to_history] تم تحديث مشاعر Prometheus")
        except Exception as e:
            logger.error(f"⚠️ [add_trade_to_history] فشل تحديث Prometheus: {e}")

    success_summary = {
        "pos_file": pos_saved,
        "history": history_saved,
        "supabase": supabase_saved,
        "narrative": narrative_saved,
        "overall": pos_saved and history_saved
    }
    logger.info(f"📊 [add_trade_to_history] ملخص حفظ الصفقة {trade_id}: {success_summary}")
    
    if not success_summary["overall"]:
        logger.error(f"❌ [add_trade_to_history] فشل حفظ الصفقة {trade_id} في المصادر الأساسية (pos_file أو history)")
        try:
            backup_file = f"failed_trades_backup_{asset_type}.json"
            backup_data = load_json_from_gist_file(backup_file, {})
            trades_backup = backup_data.get('trades', [])
            trades_backup.append(trade)
            backup_data['trades'] = trades_backup
            backup_data['last_update'] = datetime.now().isoformat()
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 [add_trade_to_history] تم حفظ نسخة احتياطية للصفقة في {backup_file}")
        except Exception as e:
            logger.error(f"❌ [add_trade_to_history] فشل حفظ النسخة الاحتياطية: {e}")
        return False

    logger.info(f"✅ [add_trade_to_history] اكتمل حفظ الصفقة {trade_id} بنجاح")
    return True

def sync_learning_data(asset_type: Optional[str] = None):
    logger.info(f"🔄 بدء مزامنة التعلم ({asset_type if asset_type else 'جميع الأصول'})")
    assets = [asset_type] if asset_type else ["oil", "silver"]
    for asset in assets:
        try:
            history = load_trades_history(asset, update_cache=False)
            logger.info(f"✅ تمت مزامنة {asset}: {len(history.get('trades', []))} صفقة")
        except Exception as e:
            logger.error(f"❌ فشل مزامنة {asset}: {e}")

def get_learning_data_source() -> str:
    return LEARNING_SOURCE

# ====================================================================================
# نهاية PART 10
# ====================================================================================

# ====================================================================================
# 📦 PART 11: دوال Telegram و API
# ====================================================================================

def get_mexc_candles(symbol, interval="Min15", limit=1000):
    url = f"https://contract.mexc.com/api/v1/contract/kline/{symbol}?interval={interval}&limit={limit}"
    try:
        response = requests.get(url, headers={"User-Agent": "TonaPrometheus/13.0"}, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'data' in data:
                raw = data['data']
                closes = raw.get('close', [])
                highs = raw.get('high', [])
                lows = raw.get('low', [])
                opens = raw.get('open', [])
                volumes = raw.get('vol', [])
                
                # ✅ توحيد الأطوال (الإصلاح)
                min_len = min(len(closes), len(highs), len(lows), len(opens), len(volumes))
                if min_len < 5:
                    return None
                closes = closes[:min_len]
                highs = highs[:min_len]
                lows = lows[:min_len]
                opens = opens[:min_len]
                volumes = volumes[:min_len]
                
                return {
                    "closes": [float(x) for x in closes],
                    "highs": [float(x) for x in highs],
                    "lows": [float(x) for x in lows],
                    "opens": [float(x) for x in opens],
                    "volumes": [float(x) for x in volumes]
                }
        return None
    except:
        return None

def fetch_multiple_timeframes(symbol, timeframes):
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(get_mexc_candles, symbol, tf["interval"], tf["limit"]): name for name, tf in timeframes.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except:
                results[name] = None
    return results

def get_fear_greed_index(force_refresh=False):
    global FEAR_GREED_CACHE
    now = time.time()
    
    if not force_refresh and (now - FEAR_GREED_CACHE["timestamp"] < FEAR_GREED_CACHE_TTL):
        return FEAR_GREED_CACHE["value"]
    
    try:
        response = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        data = response.json()
        if data.get('data'):
            val = int(data['data'][0].get('value', '50'))
            if val > 75:
                result = f"طمع شديد 🔥 ({val}/100)"
            elif val > 55:
                result = f"تفاؤل وطمع 📈 ({val}/100)"
            elif val > 45:
                result = f"محايد ومتزن ⚖️ ({val}/100)"
            elif val > 25:
                result = f"خوف وقلق ⚠️ ({val}/100)"
            else:
                result = f"خوف شديد وهلع 🚨 ({val}/100)"
            
            FEAR_GREED_CACHE["value"] = result
            FEAR_GREED_CACHE["timestamp"] = now
            return result
    except:
        pass
    
    return "محايد ومتزن ⚖️ (50/100)"
   
# ====================================================================================
# 📦 PART 12: دوال المؤشرات الفنية (النسخة المعدلة – بدون قيم افتراضية)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. إزالة جميع القيم الافتراضية (50, 0, 15, 0.1, 1.0, 0.5) من جميع الدوال.
#   2. إضافة دالة calculate_atr_series لحساب سلسلة ATR.
#   3. جميع الدوال تتحقق من كفاية البيانات وتُرجع None عند عدم كفايتها.
#   4. ✅ إصلاح حساب VPT: استخدام السعر الحالي (closes[i]) في المقام بدلاً من السعر السابق (closes[i-1]) لتطابق TradingView.
# ====================================================================================

import math
import statistics

# ============================================================================
# دوال مساعدة
# ============================================================================

def stdev_population(src, length):
    """
    حساب الانحراف المعياري للسكان (Population Standard Deviation)
    نفس طريقة ta.stdev في TradingView
    """
    if not src or length <= 0:
        return None
    
    stdev_values = []
    for i in range(len(src)):
        if i < length - 1:
            stdev_values.append(0.0)
        else:
            window = src[i - length + 1:i + 1]
            clean_window = [x for x in window if x is not None and not math.isnan(x) and not math.isinf(x)]
            if len(clean_window) < 2:
                stdev_values.append(0.0)
                continue
            
            mean = sum(clean_window) / len(clean_window)
            variance = sum((x - mean) ** 2 for x in clean_window) / len(clean_window)
            stdev_values.append(math.sqrt(variance) if variance >= 0 else 0.0)
    
    return stdev_values


def rma(src, length):
    """
    RMA (Wilder's Moving Average) بنفس طريقة TradingView
    """
    if not src or length <= 0:
        return None
    
    if len(src) >= length:
        alpha = 1.0 / length
        rma_values = [sum(src[:length]) / length]
        
        for i in range(length, len(src)):
            rma_values.append(alpha * src[i] + (1 - alpha) * rma_values[-1])
        
        return rma_values
    
    return None


# ============================================================================
# ✅ دالة VPT المصححة (باستخدام السعر الحالي في المقام)
# ============================================================================

def calculate_vpt_correct(closes, volumes):
    """
    حساب VPT بنفس طريقة TradingView بالضبط
    v = ta.cum(volume * ta.change(close) / close)
    🔥 التصحيح: استخدام closes[i] في المقام بدلاً من closes[i-1] (لتطابق TradingView)
    """
    if not closes or not volumes or len(closes) < 2 or len(volumes) != len(closes):
        return None
    
    vpt_values = [0.0]
    cum_vpt = 0.0
    
    for i in range(1, len(closes)):
        change = closes[i] - closes[i-1]
        if closes[i] != 0:  # ✅ استخدام السعر الحالي في المقام
            vpt_value = volumes[i] * (change / closes[i])
            cum_vpt += vpt_value
        vpt_values.append(cum_vpt)
    
    return vpt_values


# ============================================================================
# ✅ دالة ATR باستخدام RMA (Wilder's MA) - تعيد سلسلة كاملة
# ============================================================================

def calculate_atr_rma(highs, lows, closes, length=14):
    """حساب ATR باستخدام RMA (Wilder's MA) مثل TradingView - تعيد سلسلة كاملة"""
    if not highs or not lows or not closes or len(closes) < length:
        return None
    
    n = len(closes)
    tr = [0.0] * n
    tr[0] = highs[0] - lows[0]
    
    for i in range(1, n):
        tr[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
            abs(lows[i] - closes[i-1])
        )
    
    atr = [0.0] * n
    if n >= length:
        atr[length - 1] = sum(tr[:length]) / length
        
        alpha = 1.0 / length
        for i in range(length, n):
            atr[i] = alpha * tr[i] + (1 - alpha) * atr[i-1]
        
        # تعبئة القيم الأولى (قبل length) بالقيمة الأولى الصالحة
        for i in range(length - 1):
            atr[i] = atr[length - 1]
    else:
        return None
    
    return atr


# ============================================================================
# ✅ دالة ATR كقيمة واحدة (للتوافق مع الكود القديم)
# ============================================================================

def calculate_atr_14(data):
    """
    ATR كقيمة واحدة (للتوافق مع الكود القديم)
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    closes = data.get("closes", [])
    
    if not closes or not highs or not lows or len(closes) < 15:
        return None
    
    atr_series = calculate_atr_rma(highs, lows, closes, 14)
    if atr_series is None:
        return None
    
    return atr_series[-1]


# ============================================================================
# ✅ دالة ATR كسلسلة (جديدة – للاستخدام في PART 22)
# ============================================================================

def calculate_atr_series(data, period=14):
    """
    حساب سلسلة ATR كاملة باستخدام RMA (Wilder's MA)
    🔥 تُستخدم في PART 22 لحساب الحجم المعادل من التقلب
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    closes = data.get("closes", [])
    
    if not highs or not lows or not closes or len(closes) < period:
        return None
    
    return calculate_atr_rma(highs, lows, closes, period)


# ============================================================================
# ✅ SuperTrend + VPT (بدون قيم افتراضية)
# ============================================================================

def calculate_supertrend_vpt_correct(data, st_mult=1.0, st_period=100, vpt_len=10):
    """
    SuperTrend + VPT بنفس طريقة TradingView بالضبط
    ⚠️ تعيد (st_line, trend, vpt_ema) أو None إذا كانت البيانات غير كافية
    """
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    volumes = data.get("volumes", [])
    
    n = len(closes)
    
    # التحقق من كفاية البيانات
    if n < st_period + 10 or len(highs) != n or len(lows) != n or len(volumes) != n:
        return None
    
    # ================================================================
    # 1. حساب VPT (باستخدام الدالة المصححة)
    # ================================================================
    v = calculate_vpt_correct(closes, volumes)
    if v is None or len(v) != n:
        return None
    
    # ================================================================
    # 2. حساب shadow و out
    # ================================================================
    hl_spread = [highs[i] - lows[i] for i in range(n)]
    price_spread = stdev_population(hl_spread, 28)
    if price_spread is None or len(price_spread) != n:
        return None
    
    v_len = 14
    smooth = []
    for i in range(n):
        start = max(0, i - v_len + 1)
        window = v[start:i+1]
        smooth.append(sum(window) / len(window) if window else 0.0)
    
    v_diff = [v[i] - smooth[i] for i in range(n)]
    v_spread = stdev_population(v_diff, 28)
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
    
    # ================================================================
    # 3. حساب SuperTrend
    # ================================================================
    st_src = [(highs[i] + lows[i]) / 2 for i in range(n)]
    
    atr_val = calculate_atr_rma(highs, lows, closes, st_period)
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


# ============================================================================
# ✅ RSI (بدون قيم افتراضية)
# ============================================================================

def calculate_rsi_7(src, length=7):
    """
    حساب RSI باستخدام RMA (Wilder's MA)
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
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


# ============================================================================
# ✅ MACD (بدون قيم افتراضية)
# ============================================================================

def _ema(data, period):
    """حساب EMA (متوسط متحرك أسي)"""
    if not data or len(data) < period:
        return None
    alpha = 2.0 / (period + 1)
    res = [data[0]]
    for x in data[1:]:
        res.append(alpha * x + (1 - alpha) * res[-1])
    return res


def calculate_macd_histogram(src):
    """
    حساب MACD Histogram فقط
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
    if not src or len(src) < 35:
        return None
    
    f_ema = _ema(src, 12)
    s_ema = _ema(src, 26)
    if f_ema is None or s_ema is None:
        return None
    
    # التأكد من أن القوائم بنفس الطول
    min_len = min(len(f_ema), len(s_ema))
    f_ema = f_ema[:min_len]
    s_ema = s_ema[:min_len]
    
    macd_line = [f - s for f, s in zip(f_ema, s_ema)]
    sig_line = _ema(macd_line, 9)
    if sig_line is None:
        return None
    
    min_len = min(len(macd_line), len(sig_line))
    macd_line = macd_line[:min_len]
    sig_line = sig_line[:min_len]
    
    return [m - s for m, s in zip(macd_line, sig_line)]


def calculate_macd_full(src):
    """
    MACD كامل: يُرجع (macd_line, signal_line, histogram)
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
    if not src or len(src) < 35:
        return None, None, None
    
    f_ema = _ema(src, 12)
    s_ema = _ema(src, 26)
    if f_ema is None or s_ema is None:
        return None, None, None
    
    min_len = min(len(f_ema), len(s_ema))
    f_ema = f_ema[:min_len]
    s_ema = s_ema[:min_len]
    
    macd_line = [f - s for f, s in zip(f_ema, s_ema)]
    sig_line = _ema(macd_line, 9)
    if sig_line is None:
        return None, None, None
    
    min_len = min(len(macd_line), len(sig_line))
    macd_line = macd_line[:min_len]
    sig_line = sig_line[:min_len]
    
    histogram = [m - s for m, s in zip(macd_line, sig_line)]
    return macd_line, sig_line, histogram


# ============================================================================
# ✅ ADX (بدون قيم افتراضية)
# ============================================================================

def calculate_adx_series(data):
    """ADX كسلسلة (ليس قيمة واحدة)"""
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    closes = data.get("closes", [])
    
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
    plus_dm_smooth = rma(plus_dm, 14)
    minus_dm_smooth = rma(minus_dm, 14)
    
    if tr_smooth is None or plus_dm_smooth is None or minus_dm_smooth is None:
        return None
    
    min_len = min(len(tr_smooth), len(plus_dm_smooth), len(minus_dm_smooth))
    tr_smooth = tr_smooth[:min_len]
    plus_dm_smooth = plus_dm_smooth[:min_len]
    minus_dm_smooth = minus_dm_smooth[:min_len]
    
    plus_di = [100 * x / y if y != 0 else 0 for x, y in zip(plus_dm_smooth, tr_smooth)]
    minus_di = [100 * x / y if y != 0 else 0 for x, y in zip(minus_dm_smooth, tr_smooth)]
    
    dx = [100 * abs(p - m) / (p + m) if (p + m) != 0 else 0 for p, m in zip(plus_di, minus_di)]
    adx_result = rma(dx, 14)
    
    if adx_result is None:
        return None
    
    return adx_result


def calculate_adx_14(data):
    """ADX كقيمة واحدة (للتوافق مع الكود القديم)"""
    adx_series = calculate_adx_series(data)
    if adx_series is None:
        return None
    return adx_series[-1]


# ============================================================================
# ✅ Bollinger Bands (بدون قيم افتراضية)
# ============================================================================

def calculate_bollinger_bands(closes, length=20, mult=2):
    """
    حساب Bollinger Bands
    ⚠️ تعيد (upper, middle, lower) أو None إذا كانت البيانات غير كافية
    """
    if not closes or len(closes) < 2:
        return None, None, None
    
    if len(closes) < length:
        actual_length = len(closes)
        basis = [sum(closes) / actual_length] * len(closes)
        dev = stdev_population(closes, actual_length)
    else:
        basis = []
        for i in range(len(closes)):
            if i < length - 1:
                basis.append(sum(closes[:i+1]) / (i+1))
            else:
                basis.append(sum(closes[i-length+1:i+1]) / length)
        dev = stdev_population(closes, length)
    
    if basis is None or dev is None:
        return None, None, None
    
    min_len = min(len(basis), len(dev))
    basis = basis[:min_len]
    dev = dev[:min_len]
    
    upper = [b + (mult * d) for b, d in zip(basis, dev)]
    lower = [b - (mult * d) for b, d in zip(basis, dev)]
    
    return upper, basis, lower


# ============================================================================
# ✅ Stochastic (بدون قيم افتراضية)
# ============================================================================

def calculate_stochastic(highs, lows, closes, length=14, smooth_k=3):
    """
    حساب Stochastic Oscillator
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
    if not closes or not highs or not lows or len(closes) < length + smooth_k:
        return None
    
    stoch_raw = []
    for i in range(len(closes)):
        if i < length - 1:
            stoch_raw.append(50.0)  # قيمة محايدة مؤقتة (سيتم تجاوزها لاحقاً)
            continue
        window_high = max(highs[i-length+1:i+1])
        window_low = min(lows[i-length+1:i+1])
        denom = (window_high - window_low)
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


# ============================================================================
# ✅ VPT + SuperTrend القديمة (للتوافق – معدلة)
# ============================================================================

def calculate_vpt_supertrend_v11(data, vpt_len=10, st_period=100, st_mult=2.5):
    """
    الدالة القديمة - تم الاحتفاظ بها للتوافق مع الكود القديم
    ⚠️ تعيد (st_line, trend) أو None إذا كانت البيانات غير كافية
    """
    closes = data.get("closes", [])
    highs = data.get("highs", [])
    lows = data.get("lows", [])
    opens = data.get("opens", [])
    volumes = data.get("volumes", [])
    
    n = len(closes)
    if n < max(st_period + 50, vpt_len + 20, 10):
        return None, None
    
    # استخدام الدالة المصححة بدلاً من الحساب المكرر
    result = calculate_supertrend_vpt_correct(data, st_mult=st_mult, st_period=st_period, vpt_len=vpt_len)
    if result is None:
        return None, None
    
    st_line, trend, _ = result
    return st_line, trend


# ============================================================================
# ✅ VWAP (بدون قيم افتراضية)
# ============================================================================

def calculate_vwap(data):
    """
    حساب VWAP (Volume Weighted Average Price)
    ⚠️ تعيد None إذا كانت البيانات غير كافية
    """
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
        typical_price = (highs[i] + lows[i] + closes[i]) / 3.0
        cum_pv += typical_price * volumes[i]
        cum_vol += volumes[i]
        if cum_vol != 0:
            vwap_values.append(cum_pv / cum_vol)
        else:
            vwap_values.append(closes[i])
    
    return vwap_values

# ====================================================================================
# نهاية PART 12
# ====================================================================================

# ====================================================================================
# 📦 PART 13: دوال مساعدة وتحويل (معدل - مع تقسيم تلقائي للرسائل الطويلة)
# ====================================================================================

def escape_html(text):
    if not text: return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(chr(34), "&quot;")

def fmt_price(price, asset_type="oil"):
    if price is None:
        return "N/A"
    try:
        price = float(price)
        return "{:.3f}".format(price) if asset_type == "silver" else "{:.2f}".format(price)
    except:
        return str(price)

def can_send_groq_request():
    with GROQ_REQUEST_LOCK:
        now = time.time()
        GROQ_REQUEST_LOG[:] = [t for t in GROQ_REQUEST_LOG if now - t < 60]
        if len(GROQ_REQUEST_LOG) >= GROQ_MAX_REQUESTS_PER_MINUTE:
            wait_time = 60 - (now - GROQ_REQUEST_LOG[0])
            if wait_time > 0:
                logger.warning("تجاوز حد طلبات Groq - انتظر %.1f ثانية", wait_time)
                return False
        GROQ_REQUEST_LOG.append(now)
        return True

def convert_markdown_to_html(text):
    """
    تحويل Markdown أساسي إلى HTML ليتوافق مع parse_mode=HTML
    ✅ معالجة آمنة للعلامات غير المغلقة
    """
    if not text:
        return text
    
    # تأكد من أن العلامات مغلقة بشكل صحيح (منع خطأ 400)
    # نستبدل العلامات المفتوحة بعلامات مغلقة
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'__(.+?)__', r'<u>\1</u>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # تحويل العناوين (# ) إلى bold
    text = re.sub(r'^# (.+?)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    text = re.sub(r'^- (.+?)$', r'• \1', text, flags=re.MULTILINE)
    
    # ✅ إزالة أي علامات HTML غير مغلقة (لتجنب خطأ 400 من Telegram)
    # نبحث عن أي علامة <b> أو <i> أو <u> أو <code> غير مغلقة ونغلقها
    # بسيط: نضيف إغلاقاً لكل علامة مفتوحة غير مغلقة في نهاية النص
    open_tags = []
    for tag in ['b', 'i', 'u', 'code']:
        if f'<{tag}>' in text and f'</{tag}>' not in text:
            text += f'</{tag}>'
        # أيضاً نتحقق من التكرار
        open_count = text.count(f'<{tag}>')
        close_count = text.count(f'</{tag}>')
        if open_count > close_count:
            text += f'</{tag}>' * (open_count - close_count)
    
    return text

def queue_telegram_message(text, chat_id=None):
    """
    إضافة رسالة إلى Queue مع تحويل Markdown إلى HTML وتقسيم تلقائي للرسائل الطويلة.
    ✅ تقسم الرسائل التي تتجاوز 4096 حرفاً إلى أجزاء متعددة.
    """
    if not text or text.strip() == "":
        logger.warning("⚠️ محاولة إرسال نص فارغ!")
        return False
    
    # تحويل إلى HTML
    text = convert_markdown_to_html(text)
    
    # تحديد الـ chat_id (استخدام الافتراضي إذا كان None)
    target_chat_id = chat_id or CHAT_ID
    if not target_chat_id:
        logger.error("❌ لا يوجد chat_id محدد ولا CHAT_ID في البيئة!")
        return False
    
    # ✅ تقسيم النص إذا تجاوز حد Telegram (4096 حرف)
    MAX_LENGTH = 4096
    if len(text) > MAX_LENGTH:
        parts = []
        current_part = ""
        # نقسم النص على الأسطر للحفاظ على التنسيق
        for line in text.split('\n'):
            # إذا كان السطر نفسه أطول من الحد، نقطعه بالقوة
            if len(line) > MAX_LENGTH:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                # نقسم السطر الطويل إلى أجزاء
                for i in range(0, len(line), MAX_LENGTH):
                    parts.append(line[i:i+MAX_LENGTH])
                continue
            
            # إذا إضافة السطر يتجاوز الحد، نبدأ جزءاً جديداً
            if len(current_part) + len(line) + 1 > MAX_LENGTH:
                parts.append(current_part)
                current_part = line
            else:
                current_part += "\n" + line if current_part else line
        
        if current_part:
            parts.append(current_part)
        
        # إرسال كل جزء على حدة
        logger.info(f"📨 تقسيم الرسالة إلى {len(parts)} أجزاء (الطول الكلي: {len(text)})")
        for i, part in enumerate(parts, 1):
            TELEGRAM_QUEUE.put({"text": part, "chat_id": target_chat_id})
            logger.info(f"📨 إشعار في الطابور (جزء {i}/{len(parts)}): {part[:50]}... (طول: {len(part)})")
        return True
    else:
        TELEGRAM_QUEUE.put({"text": text, "chat_id": target_chat_id})
        logger.info(f"📨 إشعار في الطابور: {text[:50]}... (طول: {len(text)})")
        return True

def _send_telegram_message(text, chat_id=None):
    """إرسال رسالة عبر Telegram (تُستخدم بواسطة Sender)"""
    target = chat_id or CHAT_ID
    if not target or not TELEGRAM_TOKEN:
        logger.error("❌ TELEGRAM_TOKEN أو CHAT_ID غير معرف!")
        return

    if len(text) > 4096:
        text = text[:4093] + "..."

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    for attempt in range(3):
        try:
            response = requests.post(url, json={
                "chat_id": target,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }, timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ تم إرسال الرسالة بنجاح إلى {target}")
                return
            elif response.status_code == 400:
                logger.warning(f"⚠️ خطأ 400، محاولة بدون HTML...")
                response = requests.post(url, json={
                    "chat_id": target,
                    "text": text,
                    "disable_web_page_preview": True
                }, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ تم إرسال الرسالة (بدون HTML) إلى {target}")
                    return
                else:
                    logger.error(f"❌ فشل الإرسال: {response.text[:200]}")
            elif response.status_code == 429:
                retry_after = response.json().get("parameters", {}).get("retry_after", 5)
                logger.warning(f"⏳ معدل الإرسال مرتفع، انتظر {retry_after} ثانية")
                time.sleep(retry_after)
            else:
                logger.error(f"❌ خطأ Telegram: status={response.status_code}, {response.text[:200]}")
                return
        except Exception as e:
            logger.error(f"❌ خطأ في تليجرام: {e}")
            time.sleep(2 ** attempt)

# ====================================================================================
# نهاية PART 13
# ====================================================================================

# ====================================================================================
# 📦 PART 14: نظام المحاسبة (Accounting)
# ====================================================================================

class AccountingSystem:
    INITIAL_CAPITAL = 100.0
    ENTRY_AMOUNT = 1.0
    LEVERAGE = 200.0
    ISOLATED_MARGIN = 20.0

    @classmethod
    def calculate_profit_dollars(cls, entry_price, exit_price, trade_type, leverage=None):
        leverage = leverage or cls.LEVERAGE
        if trade_type == "BUY":
            price_change = (exit_price - entry_price) / entry_price
        else:
            price_change = (entry_price - exit_price) / entry_price
        return price_change * cls.ENTRY_AMOUNT * leverage

    @classmethod
    def format_profit(cls, profit_dollars):
        if profit_dollars > 0:
            return f"✅ ربح: +${profit_dollars:.2f}"
        elif profit_dollars < 0:
            return f"❌ خسارة: -${abs(profit_dollars):.2f}"
        return "⚖️ متعادلة: $0.00"

# ====================================================================================
# 📦 PART 15: دوال حفظ البيانات في قواعد التعلم (معدل – المصدر الأساسي Supabase)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. جعل Supabase هو المصدر الأساسي للحفظ لـ (trades, lessons, patterns).
#   2. جعل Gist هو النسخة الاحتياطية النهائية (يحفظ دائماً).
#   3. آلية مزامنة تلقائية عند فشل Supabase (قراءة من Gist ثم إعادة حفظ في Supabase).
#   4. فلترة الأعمدة التلقائية لتجنب أخطاء المخطط (Schema).
#   5. معالجة التكرارات (duplicate keys) في Supabase دون رسائل خطأ مزعجة.
#   6. الحفاظ على جميع الدوال الأخرى دون تغيير جوهري.
#   7. ✅ استخدام المتغيرات العامة الموحدة لأسماء الجداول من PART 10.
# ====================================================================================

import json
import time
import threading
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================================
# محاولة استيراد PATTERN_CONFIG من pattern_discovery.py (لتجنب القيم الثابتة)
# ============================================================================
try:
    from pattern_discovery import PATTERN_CONFIG
    PATTERN_CONFIG_AVAILABLE = True
    logger.info("✅ [PART 15] تم استيراد PATTERN_CONFIG من pattern_discovery.py")
except ImportError:
    PATTERN_CONFIG_AVAILABLE = False
    PATTERN_CONFIG = {"min_samples": 3}
    logger.warning("⚠️ [PART 15] تعذر استيراد PATTERN_CONFIG من pattern_discovery.py، استخدام القيمة الافتراضية 3")
except Exception as e:
    PATTERN_CONFIG_AVAILABLE = False
    PATTERN_CONFIG = {"min_samples": 3}
    logger.warning(f"⚠️ [PART 15] فشل استيراد PATTERN_CONFIG: {e}، استخدام القيمة الافتراضية 3")

# ============================================================================
# دالة توليد الهاش الفريد للدرس
# ============================================================================

def _generate_lesson_hash(lesson: Dict) -> str:
    """
    توليد بصمة فريدة (SHA-256) لمحتوى الدرس لتجنب التكرار.
    تعتمد على summary + key_factors + details.
    """
    summary = lesson.get('summary', '')
    details = lesson.get('details', '')
    key_factors = lesson.get('key_factors', [])
    if isinstance(key_factors, list):
        key_factors_str = ', '.join(sorted(key_factors))
    else:
        key_factors_str = str(key_factors)
    content = f"{summary}|{details}|{key_factors_str}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:32]

# ============================================================================
# دالة الحفظ الأساسية (معدلة)
# ============================================================================

def save_trade_to_learning(trade_data: Dict) -> bool:
    """
    حفظ صفقة في جميع قواعد البيانات مع التحليل الشامل الكامل
    ✅ المصدر الأساسي: Supabase (مع فلترة الأعمدة)
    ✅ الكاش: SQLite
    ✅ النسخة الاحتياطية: Gist
    ✅ تحويل الحقول الرقمية إلى الأنواع الصحيحة (int, float)
    """
    success = False
    trade_id = trade_data.get('trade_id', 'unknown')
    asset_type = trade_data.get('asset_type', 'unknown')
    logger.info(f"📤 [save_trade_to_learning] حفظ الصفقة {trade_id} (الأصل: {asset_type})")

    if not trade_id or trade_id == 'unknown':
        trade_id = f"trade_{int(datetime.now().timestamp())}"
        trade_data['trade_id'] = trade_id
        logger.info(f"🆔 [save_trade_to_learning] تم إنشاء trade_id جديد: {trade_id}")

    # ── 1. حفظ في Supabase (المصدر الأساسي) ──
    supabase_saved = False
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        supabase_saved = _save_trade_to_supabase_with_retry(trade_data, trade_id)
        if supabase_saved:
            logger.info(f"☁️ [save_trade_to_learning] تم حفظ {trade_id} في Supabase")
        else:
            logger.error(f"❌ [save_trade_to_learning] فشل حفظ {trade_id} في Supabase بعد 3 محاولات")
    else:
        logger.warning("⚠️ [save_trade_to_learning] Supabase غير متصل")

    # ── 2. حفظ في SQLite (الكاش) ──
    sqlite_saved = False
    if DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
        try:
            DEEP_LEARNING_DB.save_trade_full(trade_data)
            sqlite_saved = True
            logger.info(f"💾 [save_trade_to_learning] تم حفظ {trade_id} في SQLite (كاش)")
        except Exception as e:
            logger.error(f"❌ [save_trade_to_learning] فشل حفظ في SQLite: {e}")
    else:
        logger.warning("⚠️ [save_trade_to_learning] SQLite غير متوفر")

    # ── 3. حفظ في Gist (نسخة احتياطية – دائماً) ──
    gist_saved = False
    try:
        filename = f"trades_backup_{asset_type}.json"
        backup_data = load_json_from_gist_file(filename, {})
        trades = backup_data.get('trades', [])
        existing = None
        for t in trades:
            if t.get('trade_id') == trade_id:
                existing = t
                break
        if existing:
            existing.update(trade_data)
        else:
            trades.append(trade_data)
        backup_data['trades'] = trades
        backup_data['last_update'] = datetime.now().isoformat()
        
        gist_key = 'trades_oil' if asset_type == 'oil' else 'trades_silver'
        gist_saved = save_json_to_gist_file(filename, backup_data, gist_key=gist_key)
        
        if gist_saved:
            logger.info(f"💾 [save_trade_to_learning] تم حفظ نسخة احتياطية في Gist ({gist_key})")
        else:
            logger.warning(f"⚠️ [save_trade_to_learning] فشل حفظ نسخة احتياطية في Gist")
    except Exception as e:
        logger.error(f"❌ [save_trade_to_learning] فشل حفظ نسخة احتياطية في Gist: {e}")

    # ── 4. حفظ في ملف JSON محلي كحل أخير ──
    local_backup_saved = False
    if not (supabase_saved or sqlite_saved or gist_saved):
        try:
            backup_file = f"failed_trades_backup_{asset_type}.json"
            backup_data = {}
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
            trades = backup_data.get('trades', [])
            trades.append(trade_data)
            backup_data['trades'] = trades
            backup_data['last_update'] = datetime.now().isoformat()
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            local_backup_saved = True
            logger.info(f"💾 [save_trade_to_learning] تم حفظ نسخة احتياطية محلية في {backup_file} (حل أخير)")
        except Exception as e:
            logger.error(f"❌ [save_trade_to_learning] فشل حفظ النسخة الاحتياطية المحلية: {e}")

    success = supabase_saved or sqlite_saved or gist_saved or local_backup_saved
    logger.info(f"📊 [save_trade_to_learning] ملخص حفظ {trade_id}: Supabase={supabase_saved}, SQLite={sqlite_saved}, Gist={gist_saved}, LocalBackup={local_backup_saved}, Overall={success}")

    if not success:
        logger.error(f"❌ [save_trade_to_learning] فشل حفظ الصفقة {trade_id} في جميع المصادر!")
    else:
        logger.info(f"✅ [save_trade_to_learning] اكتمل حفظ الصفقة {trade_id}")

    return success

# ============================================================================
# دوال حفظ الدروس والأنماط (المعدلة مع فلترة الأعمدة وإضافة content_hash)
# ============================================================================

def _save_lesson_to_supabase(lesson_data: dict) -> bool:
    """حفظ درس واحد في Supabase مع تحويل key_factors إلى jsonb واستخدام فلترة الأعمدة وإضافة content_hash"""
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        logger.warning("⚠️ Supabase غير متصل، تخطي حفظ الدرس")
        return False
    try:
        client = _get_supabase_client()
        if not client:
            logger.error("❌ لا يمكن الحصول على عميل Supabase")
            return False
        
        if 'key_factors' in lesson_data and isinstance(lesson_data['key_factors'], list):
            lesson_data['key_factors'] = json.dumps(lesson_data['key_factors'], ensure_ascii=False)
        
        if 'content_hash' not in lesson_data:
            lesson_data['content_hash'] = _generate_lesson_hash(lesson_data)
        
        filtered_data = _filter_data_for_table(lesson_data, TABLE_LESSONS_DEEP)
        
        try:
            check = client.table(TABLE_LESSONS_DEEP).select('content_hash').eq('content_hash', filtered_data.get('content_hash')).execute()
            if check and hasattr(check, 'data') and check.data:
                logger.info(f"ℹ️ درس مكرر (هاش: {filtered_data.get('content_hash')[:8]}...) – تم تخطي الإدراج")
                return True
        except Exception as e:
            logger.warning(f"⚠️ فشل التحقق باستخدام content_hash: {e} - استخدام summary بدلاً من ذلك")
            try:
                check = client.table(TABLE_LESSONS_DEEP).select('summary').eq('summary', filtered_data.get('summary')).execute()
                if check and hasattr(check, 'data') and check.data:
                    logger.info(f"ℹ️ درس مكرر (summary: {filtered_data.get('summary')[:30]}...) – تم تخطي الإدراج")
                    return True
            except:
                pass
        
        response = client.table(TABLE_LESSONS_DEEP).insert(filtered_data).execute()
        if response and hasattr(response, 'data'):
            logger.info(f"✅ تم حفظ درس جديد في Supabase: {lesson_data.get('summary', '')[:30]}... (هاش: {filtered_data.get('content_hash')[:8]})")
            return True
        else:
            logger.error(f"❌ فشل حفظ الدرس في Supabase: {response}")
            return False
    except Exception as e:
        if 'duplicate' in str(e).lower() or '23505' in str(e):
            logger.info(f"ℹ️ درس مكرر (هاش: {lesson_data.get('content_hash', 'غير معروف')[:8]}...) – تم تخطي الإدراج")
            return True
        logger.error(f"❌ استثناء في حفظ الدرس في Supabase: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def _save_pattern_to_supabase(pattern_data: dict) -> bool:
    """
    حفظ نمط واحد في Supabase مع فلترة الأعمدة ومعالجة التكرار.
    ✅ إذا كان النمط موجوداً بالفعل (pattern_name مكرر)، نعتبره نجاحاً (تخطي).
    """
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        return False
    try:
        client = _get_supabase_client()
        if not client:
            return False
        
        pattern_name = pattern_data.get('pattern_name', '')
        if pattern_name:
            try:
                check = client.table(TABLE_DISCOVERED_PATTERNS).select('pattern_name').eq('pattern_name', pattern_name).execute()
                if check and hasattr(check, 'data') and check.data:
                    logger.info(f"ℹ️ نمط مكرر (اسم: {pattern_name}) – تم تخطي الإدراج")
                    return True
            except Exception as e:
                logger.warning(f"⚠️ فشل التحقق من تكرار النمط (الاسم: {pattern_name}): {e}")
        
        filtered_data = _filter_data_for_table(pattern_data, TABLE_DISCOVERED_PATTERNS)
        
        response = client.table(TABLE_DISCOVERED_PATTERNS).insert(filtered_data).execute()
        if response and hasattr(response, 'data'):
            logger.info(f"✅ تم حفظ النمط في Supabase: {pattern_data.get('pattern_name', '')[:30]}...")
            return True
        else:
            logger.error(f"❌ فشل حفظ النمط في Supabase: {response}")
            return False
    except Exception as e:
        error_msg = str(e)
        if 'duplicate key' in error_msg.lower() or '23505' in error_msg:
            logger.info(f"ℹ️ نمط مكرر (اسم: {pattern_data.get('pattern_name', 'غير معروف')}) – تم تخطي الإدراج (استثناء)")
            return True
        logger.error(f"❌ استثناء في حفظ النمط في Supabase: {e}")
        return False

# ============================================================================
# ✅ الدوال الجديدة الموحدة (المصدر الأساسي Supabase)
# ============================================================================

def save_lessons(lessons: List[Dict], asset_type: str = None, trade_id: str = None, source: str = None) -> Tuple[bool, int]:
    """
    حفظ الدروس المستفادة في Supabase (المصدر الأساسي) و Gist (نسخة احتياطية)
    ✅ المصدر الأساسي: Supabase (جدول lessons_deep) مع فلترة الأعمدة
    ✅ النسخة الاحتياطية: Gist (ملف lessons_deep.json) - دائماً
    ✅ تعيد (نجاح_العملية, عدد_الدروس_الجديدة)
    """
    if not lessons:
        return True, 0

    enriched_lessons = []
    for lesson in lessons:
        enriched = lesson.copy()
        if asset_type:
            enriched['asset_type'] = asset_type
        if trade_id:
            enriched['trade_id'] = trade_id
        if source:
            enriched['source'] = source
        enriched['created_at'] = datetime.now().isoformat()
        if 'key_factors' in enriched and isinstance(enriched['key_factors'], list):
            enriched['key_factors_str'] = ', '.join(enriched['key_factors'])
        elif 'key_factors' not in enriched:
            enriched['key_factors'] = []
            enriched['key_factors_str'] = ''
        enriched['content_hash'] = _generate_lesson_hash(enriched)
        enriched_lessons.append(enriched)

    # ── 1. حفظ في Supabase (المصدر الأساسي) ──
    supabase_success = True
    new_lessons_count = 0
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        for lesson in enriched_lessons:
            if _save_lesson_to_supabase(lesson):
                new_lessons_count += 1
            else:
                supabase_success = False
        if supabase_success and new_lessons_count > 0:
            logger.info(f"☁️ [save_lessons] تم حفظ {new_lessons_count} درس جديد في Supabase (إجمالي {len(enriched_lessons)} درس تم إرساله)")
        elif new_lessons_count == 0:
            logger.info(f"ℹ️ [save_lessons] لا توجد دروس جديدة للحفظ (جميع الدروس مكررة)")
        else:
            logger.warning(f"⚠️ [save_lessons] بعض الدروس لم تُحفظ في Supabase (نجح {new_lessons_count} من {len(enriched_lessons)})")
    else:
        logger.warning("⚠️ [save_lessons] Supabase غير متصل، تخطي حفظ الدروس في Supabase")

    # ── 2. حفظ في Gist (نسخة احتياطية – دائماً) ──
    gist_success = True
    try:
        current = load_json_from_gist_file("lessons_deep.json", {})
        all_lessons = current.get('lessons', [])
        existing_hashes = {l.get('content_hash', '') for l in all_lessons}
        added_count = 0
        for lesson in enriched_lessons:
            if lesson.get('content_hash') not in existing_hashes:
                all_lessons.append(lesson)
                existing_hashes.add(lesson.get('content_hash'))
                added_count += 1
        if added_count > 0:
            current['lessons'] = all_lessons
            current['last_update'] = datetime.now().isoformat()
            current['total_lessons'] = len(all_lessons)
            gist_success = save_json_to_gist_file("lessons_deep.json", current, gist_key='config')
            if gist_success:
                logger.info(f"💾 [save_lessons] تم حفظ {added_count} درس جديد في Gist (نسخة احتياطية)")
            else:
                logger.warning(f"⚠️ [save_lessons] فشل حفظ الدروس في Gist (غير حرج، Supabase نجح)")
        else:
            logger.info(f"ℹ️ [save_lessons] لا توجد دروس جديدة للحفظ في Gist")
    except Exception as e:
        logger.warning(f"⚠️ [save_lessons] فشل حفظ الدروس في Gist (غير حرج): {e}")
        gist_success = False

    # ── 3. نسخة احتياطية محلية (حل أخير جداً) ──
    local_success = False
    if not (supabase_success and new_lessons_count > 0) and not gist_success and new_lessons_count > 0:
        try:
            backup_file = "failed_lessons_backup.json"
            backup_data = {}
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
            all_backup = backup_data.get('lessons', [])
            existing_hashes = {l.get('content_hash', '') for l in all_backup}
            added_count = 0
            for lesson in enriched_lessons:
                if lesson.get('content_hash') not in existing_hashes:
                    all_backup.append(lesson)
                    existing_hashes.add(lesson.get('content_hash'))
                    added_count += 1
            if added_count > 0:
                backup_data['lessons'] = all_backup
                backup_data['last_update'] = datetime.now().isoformat()
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)
                local_success = True
                logger.info(f"💾 [save_lessons] تم حفظ {added_count} درس في النسخة الاحتياطية المحلية {backup_file}")
        except Exception as e:
            logger.error(f"❌ [save_lessons] فشل حفظ النسخة الاحتياطية المحلية: {e}")

    overall_success = (supabase_success and new_lessons_count > 0) or gist_success or local_success
    return overall_success, new_lessons_count

def save_patterns(patterns: List[Dict], asset_type: str = None, source: str = None) -> Tuple[bool, int]:
    """
    حفظ الأنماط المكتشفة في Supabase (المصدر الأساسي) و Gist (نسخة احتياطية)
    ✅ المصدر الأساسي: Supabase (جدول discovered_patterns) مع فلترة الأعمدة
    ✅ النسخة الاحتياطية: Gist (ملف discovered_patterns.json) - دائماً
    ✅ معالجة التكرار عبر _save_pattern_to_supabase (التي تتعامل مع 23505)
    ✅ تعيد (نجاح_العملية, عدد_الأنماط_الجديدة)
    """
    if not patterns:
        return True, 0

    enriched_patterns = []
    for pattern in patterns:
        enriched = pattern.copy()
        if asset_type:
            enriched['asset_type'] = asset_type
        if source:
            enriched['source'] = source
        enriched['created_at'] = datetime.now().isoformat()
        enriched_patterns.append(enriched)

    # ── 1. حفظ في Supabase (المصدر الأساسي) ──
    supabase_success = True
    new_patterns_count = 0
    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        for pattern in enriched_patterns:
            if _save_pattern_to_supabase(pattern):
                new_patterns_count += 1
            else:
                supabase_success = False
        if supabase_success and new_patterns_count > 0:
            logger.info(f"☁️ [save_patterns] تم حفظ {new_patterns_count} نمط جديد في Supabase")
        elif new_patterns_count == 0:
            logger.info(f"ℹ️ [save_patterns] لا توجد أنماط جديدة للحفظ")
        else:
            logger.warning(f"⚠️ [save_patterns] بعض الأنماط لم تُحفظ في Supabase")
    else:
        logger.warning("⚠️ [save_patterns] Supabase غير متصل، تخطي حفظ الأنماط في Supabase")

    # ── 2. حفظ في Gist (نسخة احتياطية – دائماً) ──
    gist_success = True
    try:
        current = load_json_from_gist_file("discovered_patterns.json", {})
        all_patterns = current.get('patterns', [])
        added_count = 0
        for pattern in enriched_patterns:
            name = pattern.get('pattern_name', '')
            if not any(p.get('pattern_name') == name for p in all_patterns):
                all_patterns.append(pattern)
                added_count += 1
        if added_count > 0:
            current['patterns'] = all_patterns
            current['last_update'] = datetime.now().isoformat()
            current['total_patterns'] = len(all_patterns)
            gist_success = save_json_to_gist_file("discovered_patterns.json", current, gist_key='config')
            if gist_success:
                logger.info(f"💾 [save_patterns] تم حفظ {added_count} نمط جديد في Gist (نسخة احتياطية)")
            else:
                logger.warning(f"⚠️ [save_patterns] فشل حفظ الأنماط في Gist (غير حرج، Supabase نجح)")
        else:
            logger.info(f"ℹ️ [save_patterns] لا توجد أنماط جديدة للحفظ في Gist")
    except Exception as e:
        logger.warning(f"⚠️ [save_patterns] فشل حفظ الأنماط في Gist (غير حرج): {e}")
        gist_success = False

    overall_success = (supabase_success and new_patterns_count > 0) or gist_success
    return overall_success, new_patterns_count

# ============================================================================
# ✅ دوال التوافق (للحفاظ على التوافق مع الكود القديم)
# ============================================================================

def save_lessons_to_gist(lessons: List[Dict], asset_type: str = None, trade_id: str = None) -> bool:
    """
    @deprecated: استخدم save_lessons() بدلاً من ذلك.
    محفوظة للتوافق مع الكود القديم.
    """
    logger.warning("⚠️ [save_lessons_to_gist] دالة قديمة، استخدم save_lessons() بدلاً منها")
    result, _ = save_lessons(lessons, asset_type, trade_id, source='legacy')
    return result

def save_patterns_to_gist(patterns: List[Dict], asset_type: str = None) -> bool:
    """
    @deprecated: استخدم save_patterns() بدلاً من ذلك.
    محفوظة للتوافق مع الكود القديم.
    """
    logger.warning("⚠️ [save_patterns_to_gist] دالة قديمة، استخدم save_patterns() بدلاً منها")
    result, _ = save_patterns(patterns, asset_type, source='legacy')
    return result

# ============================================================================
# ✅ دالة دمج دروس Post-Mortem (جديدة)
# ============================================================================

def save_post_mortem_lessons(post_mortem_result: Dict, asset_type: str, trade_id: str) -> bool:
    """
    حفظ دروس Post-Mortem في نظام التعلم الموحد
    ✅ تُستدعى من PART 20 بعد تحليل Post-Mortem
    """
    lessons = post_mortem_result.get('lessons', [])
    if not lessons:
        logger.info(f"ℹ️ [save_post_mortem_lessons] لا توجد دروس Post-Mortem للصفقة {trade_id}")
        return True

    formatted_lessons = []
    for lesson_text in lessons:
        formatted_lessons.append({
            'type': 'post_mortem',
            'summary': lesson_text[:100],
            'details': lesson_text,
            'key_factors': post_mortem_result.get('recommendations', [])[:3],
            'grade': post_mortem_result.get('grade', 'متوسطة'),
            'profit_dollars': post_mortem_result.get('profit_dollars', 0)
        })

    result, _ = save_lessons(formatted_lessons, asset_type, trade_id, source='post_mortem')
    return result

# ============================================================================
# ✅ دالة دمج الدروس (تجنب التكرار)
# ============================================================================

def merge_lessons(existing_lessons: List[Dict], new_lessons: List[Dict]) -> List[Dict]:
    """
    دمج الدروس الجديدة مع الموجودة، مع تجنب التكرار
    يعتمد على content_hash إن وجد، وإلا على summary
    """
    if not new_lessons:
        return existing_lessons
    
    existing_hashes = {l.get('content_hash', l.get('summary', '')) for l in existing_lessons}
    merged = existing_lessons.copy()
    
    for lesson in new_lessons:
        key = lesson.get('content_hash', lesson.get('summary', ''))
        if key and key not in existing_hashes:
            merged.append(lesson)
            existing_hashes.add(key)
    
    return merged

# ============================================================================
# دوال التحميل من Gist (محفوظة للتوافق)
# ============================================================================

def load_lessons_from_gist() -> List[Dict]:
    """
    تحميل الدروس من Gist (نسخة احتياطية)
    ⚠️ ملاحظة: المصدر الأساسي هو Supabase، هذه للتوافق فقط
    """
    try:
        data = load_json_from_gist_file("lessons_deep.json", {})
        if data is None:
            return []
        lessons = data.get('lessons')
        if not isinstance(lessons, list):
            return []
        logger.info(f"📖 [load_lessons_from_gist] تم تحميل {len(lessons)} درس من Gist")
        return lessons
    except Exception as e:
        logger.error(f"❌ [load_lessons_from_gist] فشل تحميل الدروس من Gist: {e}")
        return []

def load_patterns_from_gist() -> List[Dict]:
    """
    تحميل الأنماط من Gist (نسخة احتياطية)
    ⚠️ ملاحظة: المصدر الأساسي هو Supabase، هذه للتوافق فقط
    """
    try:
        data = load_json_from_gist_file("discovered_patterns.json", {})
        if data is None:
            return []
        patterns = data.get('patterns')
        if not isinstance(patterns, list):
            return []
        logger.info(f"🔍 [load_patterns_from_gist] تم تحميل {len(patterns)} نمط من Gist")
        return patterns
    except Exception as e:
        logger.error(f"❌ [load_patterns_from_gist] فشل تحميل الأنماط من Gist: {e}")
        return []

# ============================================================================
# ✅ دالة اكتشاف الأنماط (معدلة)
# ============================================================================

def discover_patterns_from_trades(asset_type: Optional[str] = None):
    """
    اكتشاف الأنماط من الصفقات وحفظها في النظام الموحد
    ✅ تستخدم save_patterns() بدلاً من save_patterns_to_gist()
    ✅ تم إزالة إرسال رسائل الإشعارات (التعلم صامت)
    ✅ جلب min_samples من PATTERN_CONFIG
    """
    logger.info(f"🔍 [discover_patterns_from_trades] تم استدعاؤها لـ {asset_type or 'الكل'}")
    
    if not PATTERN_DISCOVERY_AVAILABLE or not PATTERN_DISCOVERY:
        logger.warning(f"⚠️ [discover_patterns_from_trades] PATTERN_DISCOVERY غير متوفر!")
        return

    try:
        trades = []
        if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
            trades = SUPABASE_DB.get_trades(asset_type, 2000)
            logger.info(f"📊 [discover_patterns_from_trades] تم جلب {len(trades)} صفقة من Supabase لـ {asset_type or 'الكل'}")
        elif DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
            trades = DEEP_LEARNING_DB.get_trades_by_asset(asset_type, 200)
            logger.info(f"📊 [discover_patterns_from_trades] تم جلب {len(trades)} صفقة من SQLite لـ {asset_type or 'الكل'}")

        if not trades:
            logger.warning(f"⚠️ [discover_patterns_from_trades] لا توجد صفقات لـ {asset_type or 'الكل'}")
            return

        if PATTERN_CONFIG_AVAILABLE:
            min_samples = PATTERN_CONFIG.get('min_samples', 3)
        else:
            try:
                if hasattr(PATTERN_DISCOVERY, 'config') and isinstance(PATTERN_DISCOVERY.config, dict):
                    min_samples = PATTERN_DISCOVERY.config.get('min_samples', 3)
                elif hasattr(PATTERN_DISCOVERY, 'min_samples'):
                    min_samples = getattr(PATTERN_DISCOVERY, 'min_samples', 3)
                else:
                    min_samples = 3
            except Exception as e:
                logger.warning(f"⚠️ [discover_patterns_from_trades] فشل استخراج min_samples: {e}")
                min_samples = 3

        if len(trades) < min_samples:
            logger.info(f"ℹ️ [discover_patterns_from_trades] عدد الصفقات غير كافٍ ({len(trades)}) لـ {asset_type or 'الكل'} (يحتاج {min_samples})")
            return

        patterns = PATTERN_DISCOVERY.discover_patterns(trades)
        if patterns:
            # حفظ الأنماط عبر طبقة Supabase الموحدة في main، وليس عبر API غير موجود في SupabaseBridge.
            try:
                saved, count = save_patterns(patterns, asset_type=asset_type, source='adaptive_pattern_discovery')
                logger.info(f"🧠 [discover_patterns_from_trades] حفظ {count} نمطاً من أصل {len(patterns)}")
            except Exception as e:
                logger.error(f"❌ [discover_patterns_from_trades] فشل حفظ الأنماط الموحد: {e}")
            logger.info(f"✅ [discover_patterns_from_trades] تم اكتشاف {len(patterns)} نمطاً لـ {asset_type or 'الكل'}")
        else:
            logger.info(f"ℹ️ [discover_patterns_from_trades] لا توجد أنماط جديدة لـ {asset_type or 'الكل'}")
            
    except Exception as e:
        logger.error(f"❌ [discover_patterns_from_trades] فشل اكتشاف الأنماط: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# ✅ دالة حفظ لقطات المراقبة (معدلة لمنع التكرار اللانهائي)
# ============================================================================

def save_snapshot_to_learning_legacy(snapshot_data: Dict) -> bool:
    """
    ⚠️ @deprecated: استخدم save_snapshot_to_learning في PART 10 بدلاً من ذلك.
    هذه الدالة موجودة فقط للتوافق مع الكود القديم.
    """
    logger.warning("⚠️ [save_snapshot_to_learning_legacy] دالة قديمة، استخدم الدالة في PART 10 مباشرة")
    # ✅ استخدام TABLE_SNAPSHOTS عبر الدالة المعدلة في PART 10
    return save_snapshot_to_learning(snapshot_data)

# ============================================================================
# تقرير التعلم العميق (محسّن لقراءة من Supabase أولاً)
# ============================================================================

def get_learning_stats_report(asset_type: Optional[str] = None) -> str:
    """
    توليد تقرير التعلم العميق
    ✅ يقرأ من Supabase أولاً (المصدر الأساسي) مع عرض العدد الإجمالي
    ✅ يستخدم Gist كنسخة احتياطية
    ✅ عرض العدد الإجمالي للدروس والأنماط بدلاً من limit
    """
    lines = []
    lines.append("🧠 **تقرير التعلم العميق**")
    lines.append("━" * 30)
    lines.append("")

    lessons = []
    patterns = []
    supabase_used = False
    total_lessons = 0
    total_patterns = 0

    if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
        try:
            client = _get_supabase_client()
            if client:
                try:
                    count_response = client.table(TABLE_LESSONS_DEEP).select('id', count='exact').execute()
                    if hasattr(count_response, 'count'):
                        total_lessons = count_response.count
                    else:
                        ids_response = client.table(TABLE_LESSONS_DEEP).select('id').execute()
                        if hasattr(ids_response, 'data'):
                            total_lessons = len(ids_response.data)
                except Exception as e:
                    logger.warning(f"⚠️ فشل الحصول على عدد الدروس: {e}")
                    try:
                        sample = client.table(TABLE_LESSONS_DEEP).select('id').limit(1000).execute()
                        if hasattr(sample, 'data'):
                            total_lessons = len(sample.data) if len(sample.data) < 1000 else 1000
                    except:
                        pass

                try:
                    query = client.table(TABLE_LESSONS_DEEP).select('*').order('created_at', desc=True).limit(20)
                    if asset_type:
                        query = query.eq('asset_type', asset_type)
                    response = query.execute()
                    if response and hasattr(response, 'data'):
                        lessons = response.data
                        supabase_used = True
                except Exception as e:
                    logger.warning(f"⚠️ فشل تحميل الدروس: {e}")

                try:
                    count_response = client.table(TABLE_DISCOVERED_PATTERNS).select('id', count='exact').execute()
                    if hasattr(count_response, 'count'):
                        total_patterns = count_response.count
                    else:
                        ids_response = client.table(TABLE_DISCOVERED_PATTERNS).select('id').execute()
                        if hasattr(ids_response, 'data'):
                            total_patterns = len(ids_response.data)
                except Exception as e:
                    logger.warning(f"⚠️ فشل الحصول على عدد الأنماط: {e}")

                try:
                    query = client.table(TABLE_DISCOVERED_PATTERNS).select('*').order('created_at', desc=True).limit(5)
                    if asset_type:
                        query = query.eq('asset_type', asset_type)
                    response = query.execute()
                    if response and hasattr(response, 'data'):
                        patterns = response.data
                        supabase_used = True
                except Exception as e:
                    logger.warning(f"⚠️ فشل تحميل الأنماط: {e}")

        except Exception as e:
            logger.warning(f"⚠️ [get_learning_stats_report] فشل تحميل من Supabase: {e}")

    if not supabase_used:
        lessons = load_lessons_from_gist()
        patterns = load_patterns_from_gist()
        total_lessons = len(lessons)
        total_patterns = len(patterns)
        lines.append("⚠️ تم استخدام Gist (نسخة احتياطية) بدلاً من Supabase")
        lines.append("")

    lines.append("📚 **الذاكرة العامة:**")
    lines.append(f"   • عدد الدروس المستفادة: {total_lessons}")
    lines.append(f"   • عدد الأنماط المكتشفة: {total_patterns}")
    lines.append("")

    if lessons:
        lines.append("📖 **أحدث الدروس (آخر 20):**")
        for i, lesson in enumerate(lessons[:20], 1):
            summary = lesson.get('summary', 'لا يوجد ملخص')
            details = lesson.get('details', '')
            key_factors = lesson.get('key_factors', [])
            if isinstance(key_factors, str):
                try:
                    key_factors = json.loads(key_factors)
                except:
                    key_factors = [key_factors]
            source = lesson.get('source', 'غير معروف')
            lines.append(f"{i}. {summary}")
            if details:
                lines.append(f"   • {details[:200]}...")
            if key_factors and isinstance(key_factors, list) and key_factors:
                factors = "، ".join(key_factors[:3])
                lines.append(f"   • العوامل: {factors}")
            if source:
                lines.append(f"   • المصدر: {source}")
            lines.append("")
    else:
        lines.append("ℹ️ لا توجد دروس مستفادة بعد.")
        lines.append("💡 البوت يحتاج إلى صفقات مغلقة للتعلم.")
        lines.append("")

    if patterns:
        lines.append("🔍 **أحدث الأنماط (آخر 5):**")
        for pattern in patterns[:5]:
            lines.append(f"   • {pattern.get('pattern_name', '')} (نجاح {pattern.get('win_rate', 0):.1f}%)")
        if total_patterns > 5:
            lines.append(f"   ... و {total_patterns - 5} نمط آخر")
        lines.append("")
    else:
        lines.append("ℹ️ لا توجد أنماط مكتشفة بعد.")
        lines.append("")

    if supabase_used:
        lines.append("✅ المصدر: Supabase (البيانات محدثة)")
        lines.append(f"   إجمالي الدروس في قاعدة البيانات: {total_lessons}")
        lines.append(f"   إجمالي الأنماط في قاعدة البيانات: {total_patterns}")
    else:
        lines.append("⚠️ المصدر: Gist (قد لا تكون محدثة)")

    lines.append("")
    lines.append("━" * 30)
    lines.append("💙 تولين: كل صفقة تضيف درساً جديداً إلى عقلي.")
    return "\n".join(lines)

# ============================================================================
# نهاية PART 15
# ====================================================================================

# ====================================================================================
# 📦 PART 16: محرك التقييم الشامل V9 (المعدل - مع جميع المؤشرات والفريمات)
# ====================================================================================
# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطبقة هنا):
# ═══════════════════════════════════════════════════════════════════════════════
# 1. يستخدم جميع المؤشرات الفنية الأساسية:
#    RSI, ADX, MACD, Volume, VPT, SuperTrend, Bollinger Bands, Stochastic, VWAP, ATR
# 2. يحلل جميع الفريمات الأربعة:
#    - 5 دقائق (Min5)    ← فريم التداول الأساسي
#    - 15 دقيقة (Min15)  ← فريم التأكيد
#    - ساعة (Min60)      ← فريم الاتجاه المتوسط
#    - 4 ساعات (Hour4)   ← فريم الاتجاه العام
# 3. أي تقييم لا يشمل الفريمات الأربعة يُعتبر ناقصاً.
# ═══════════════════════════════════════════════════════════════════════════════
# ====================================================================================

def _default_result(reason):
    return {
        "score": 0,
        "grade": "بيانات غير كافية",
        "grade_emoji": "⚠️",
        "details": [f"⚠️ {reason}"],
        "context": "unknown",
        "metrics": {},
        "components": {},
        "trade_health": None,
        "frames_analysis": {}
    }

def _trend_desc(bullish_count, adx):
    if bullish_count == 4:
        return "اتجاه صاعد قوي ومؤكد على جميع الفريمات" if adx > 25 else "اتجاه صاعد لكن الزخم ضعيف"
    elif bullish_count == 3:
        return "غالبية الفريمات (3/4) صاعدة"
    elif bullish_count == 2:
        return "تعادل بين الفريمات (2 صاعد، 2 هابط)"
    elif bullish_count == 1:
        return "غالبية الفريمات (3/4) هابطة"
    else:
        return "اتجاه هابط قوي ومؤكد على جميع الفريمات" if adx > 25 else "اتجاه هابط لكن الزخم ضعيف"

def _momentum_desc(rsi, macd_hist, stoch):
    if rsi < 30 and macd_hist > 0:
        return "زخم صاعد قوي — ارتداد محتمل"
    elif rsi > 70 and macd_hist < 0:
        return "زخم هابط قوي — تصحيح محتمل"
    elif 40 <= rsi <= 60 and abs(macd_hist) < 0.3:
        return "زخم محايد — لا قوة اتجاهية واضحة"
    elif rsi < 40:
        return "زخم ضعيف نحو الأسفل"
    else:
        return "زخم ضعيف نحو الأعلى"

def _volatility_desc(bb_pos, atr_pct, vwap_dev):
    if atr_pct > 2.5:
        return "تقلب شديد — السوق متقلب جداً"
    elif atr_pct < 0.5:
        return "تقلب منخفض — السوق نائم"
    if bb_pos < 0.15:
        return "السعر عند القاع النسبي — ارتداد محتمل"
    elif bb_pos > 0.85:
        return "السعر عند القمة النسبية — تصحيح محتمل"
    if abs(vwap_dev) > 0.015:
        return "انحراف كبير عن السعر العادل"
    return "بنية سعرية متوازنة"

def _volume_desc(vol_ratio):
    if vol_ratio >= 2.0:
        return "سيولة استثنائية — حركة مدعومة بقوة"
    elif vol_ratio >= 1.5:
        return "سيولة مرتفعة — حركة حقيقية"
    elif vol_ratio >= 1.0:
        return "سيولة طبيعية"
    elif vol_ratio >= 0.6:
        return "سيولة منخفضة — حذر من الانزلاق"
    else:
        return "سيولة جافة جداً — تجنب الدخول"

def _sr_desc(price, s1, r1, pivot):
    if price <= 0 or s1 <= 0 or r1 <= 0 or pivot <= 0:
        return "مستويات غير متوفرة"
    if price <= s1 * 1.003:
        return "السعر عند منطقة دعم قوية"
    elif price >= r1 * 0.997:
        return "السعر عند منطقة مقاومة قوية"
    elif abs(price - pivot) / price < 0.003:
        return "السعر عند نقطة الارتكاز"
    elif price < pivot:
        return "السعر في النطاق السفلي"
    else:
        return "السعر في النطاق العلوي"

def _sentiment_desc(fear_greed):
    if fear_greed <= 20:
        return "هلع شديد في السوق — فرصة تاريخية محتملة"
    elif fear_greed <= 35:
        return "خوف متزايد — بيئة شرائية محتملة"
    elif fear_greed <= 55:
        return "معنويات متوازنة"
    elif fear_greed <= 75:
        return "تفاؤل مرتفع — حذر من القمة"
    else:
        return "طمع مفرط — قمة بيعية محتملة"

def _detect_divergence(price_hist, rsi_hist, macd_hist):
    if not price_hist or not rsi_hist or len(price_hist) < 15 or len(rsi_hist) < 15:
        return {"type": "none", "score": 50, "desc": "لا يوجد تباعد — بيانات غير كافية"}

    price_hist_clean = [p for p in price_hist if p is not None and p > 0]
    rsi_hist_clean = [r for r in rsi_hist if r is not None and 0 <= r <= 100]
    macd_hist_clean = [m for m in macd_hist if m is not None]

    if len(price_hist_clean) < 15 or len(rsi_hist_clean) < 15:
        return {"type": "none", "score": 50, "desc": "لا يوجد تباعد — بيانات غير كافية"}

    def find_peaks(data, min_dist=3):
        peaks = []
        for i in range(min_dist, len(data) - min_dist):
            is_peak = all(data[i] >= data[i-j] for j in range(1, min_dist+1))
            is_peak = is_peak and all(data[i] >= data[i+j] for j in range(1, min_dist+1))
            if is_peak:
                if not peaks or i - peaks[-1] >= min_dist:
                    peaks.append(i)
        return peaks[-5:]

    def find_troughs(data, min_dist=3):
        troughs = []
        for i in range(min_dist, len(data) - min_dist):
            is_trough = all(data[i] <= data[i-j] for j in range(1, min_dist+1))
            is_trough = is_trough and all(data[i] <= data[i+j] for j in range(1, min_dist+1))
            if is_trough:
                if not troughs or i - troughs[-1] >= min_dist:
                    troughs.append(i)
        return troughs[-5:]

    price_peaks = find_peaks(price_hist_clean)
    rsi_peaks = find_peaks(rsi_hist_clean)

    if len(price_peaks) >= 2 and len(rsi_peaks) >= 2:
        for pp_idx in range(len(price_peaks)-1, 0, -1):
            for rp_idx in range(len(rsi_peaks)-1, 0, -1):
                p1, p2 = price_peaks[pp_idx-1], price_peaks[pp_idx]
                r1, r2 = rsi_peaks[rp_idx-1], rsi_peaks[rp_idx]
                if abs(p1 - r1) <= 3 and abs(p2 - r2) <= 3:
                    if price_hist_clean[p2] > price_hist_clean[p1] * 1.003 and rsi_hist_clean[r2] < rsi_hist_clean[r1] * 0.98:
                        return {"type": "bearish_rsi", "score": 20, "desc": "تباعد هابط في RSI — السعر يصعد لكن الزخم يتراجع"}

    price_troughs = find_troughs(price_hist_clean)
    rsi_troughs = find_troughs(rsi_hist_clean)

    if len(price_troughs) >= 2 and len(rsi_troughs) >= 2:
        for pt_idx in range(len(price_troughs)-1, 0, -1):
            for rt_idx in range(len(rsi_troughs)-1, 0, -1):
                p1, p2 = price_troughs[pt_idx-1], price_troughs[pt_idx]
                r1, r2 = rsi_troughs[rt_idx-1], rsi_troughs[rt_idx]
                if abs(p1 - r1) <= 3 and abs(p2 - r2) <= 3:
                    if price_hist_clean[p2] < price_hist_clean[p1] * 0.997 and rsi_hist_clean[r2] > rsi_hist_clean[r1] * 1.02:
                        return {"type": "bullish_rsi", "score": 80, "desc": "تباعد صاعد في RSI — السعر يهبط لكن الزخم يتعزز"}

    if len(macd_hist_clean) >= 15:
        macd_peaks = find_peaks(macd_hist_clean)
        if len(macd_peaks) >= 2 and len(price_peaks) >= 2:
            for pp_idx in range(len(price_peaks)-1, 0, -1):
                for mp_idx in range(len(macd_peaks)-1, 0, -1):
                    p1, p2 = price_peaks[pp_idx-1], price_peaks[pp_idx]
                    m1, m2 = macd_peaks[mp_idx-1], macd_peaks[mp_idx]
                    if abs(p1 - m1) <= 3 and abs(p2 - m2) <= 3:
                        if price_hist_clean[p2] > price_hist_clean[p1] * 1.003 and macd_hist_clean[m2] < macd_hist_clean[m1] * 0.97:
                            return {"type": "bearish_macd", "score": 25, "desc": "تباعد هابط في MACD — السعر يصعد لكن الزخم يتراجع"}

    return {"type": "none", "score": 50, "desc": "لا يوجد تباعد ملحوظ"}

def _analyze_single_frame(tf_data: Dict, frame_name: str) -> Dict:
    """
    تحليل فريم واحد باستخدام جميع المؤشرات العشرة.
    """
    if not tf_data:
        return {
            "name": frame_name,
            "valid": False,
            "trend": "محايد",
            "rsi": 50,
            "adx": 20,
            "macd": 0,
            "volume_ratio": 1.0,
            "vpt": 0,
            "supertrend_line": 0,
            "supertrend_trend": 0,
            "bb_upper": 0,
            "bb_middle": 0,
            "bb_lower": 0,
            "stochastic": 50,
            "vwap": 0,
            "atr": 0,
            "score": 50,
            "details": ["بيانات غير كافية"]
        }
    
    price = tf_data.get('price', 0)
    rsi = tf_data.get('rsi', 50)
    adx = tf_data.get('adx', 20)
    macd = tf_data.get('macd', 0)
    vol_ratio = tf_data.get('volume_ratio', 1.0)
    trend = tf_data.get('trend', 'محايد')
    vpt = tf_data.get('vpt', 0)
    supertrend = tf_data.get('supertrend', {})
    bb = tf_data.get('bollinger', {})
    stoch = tf_data.get('stochastic', 50)
    vwap = tf_data.get('vwap', price)
    atr = tf_data.get('atr', 0)
    
    frame_score = 50
    
    # الاتجاه (وزن 25%)
    if trend == "صاعد":
        frame_score += 15
    elif trend == "هابط":
        frame_score -= 15
    
    # RSI (وزن 15%)
    if 30 <= rsi <= 70:
        frame_score += 10
    elif rsi < 30 and trend == "صاعد":
        frame_score += 5
    elif rsi > 70 and trend == "هابط":
        frame_score += 5
    else:
        frame_score -= 10
    
    # ADX (وزن 15%)
    if adx > 25:
        frame_score += 10
    elif adx > 20:
        frame_score += 5
    else:
        frame_score -= 10
    
    # MACD (وزن 10%)
    if (trend == "صاعد" and macd > 0) or (trend == "هابط" and macd < 0):
        frame_score += 8
    else:
        frame_score -= 5
    
    # الحجم (وزن 10%)
    if vol_ratio > 1.5:
        frame_score += 8
    elif vol_ratio > 0.7:
        frame_score += 4
    else:
        frame_score -= 5
    
    # SuperTrend (وزن 5%)
    if supertrend.get('trend') == 1 and trend == "صاعد":
        frame_score += 5
    elif supertrend.get('trend') == -1 and trend == "هابط":
        frame_score += 5
    else:
        frame_score -= 3
    
    # Bollinger Bands (وزن 5%)
    if bb.get('upper') and bb.get('lower'):
        bb_pos = (price - bb['lower']) / (bb['upper'] - bb['lower']) if (bb['upper'] - bb['lower']) > 0 else 0.5
        if 0.2 < bb_pos < 0.8:
            frame_score += 4
        else:
            frame_score -= 2
    
    # Stochastic (وزن 5%)
    if 20 < stoch < 80:
        frame_score += 3
    else:
        frame_score -= 2
    
    # VWAP (وزن 5%)
    if vwap and price > 0:
        vwap_dev = (price - vwap) / vwap * 100
        if abs(vwap_dev) < 1.0:
            frame_score += 3
        else:
            frame_score -= 2
    
    # ATR (وزن 5%)
    if atr and price > 0:
        atr_pct = atr / price * 100
        if 0.5 < atr_pct < 2.5:
            frame_score += 3
        else:
            frame_score -= 2
    
    # VPT (وزن 5%)
    if vpt:
        frame_score += 3 if vpt > 0 else -2
    
    frame_score = max(0, min(100, frame_score))
    
    return {
        "name": frame_name,
        "valid": price > 0 and rsi is not None,
        "price": price,
        "trend": trend,
        "rsi": rsi,
        "adx": adx,
        "macd": macd,
        "volume_ratio": vol_ratio,
        "vpt": vpt,
        "supertrend": supertrend,
        "bollinger": bb,
        "stochastic": stoch,
        "vwap": vwap,
        "atr": atr,
        "score": frame_score,
        "grade": "قوي" if frame_score >= 70 else "متوسط" if frame_score >= 45 else "ضعيف",
        "details": [
            f"الاتجاه: {trend} (ADX: {adx:.0f})",
            f"RSI: {rsi:.0f}",
            f"MACD: {macd:.4f}",
            f"الحجم: {vol_ratio:.1f}x"
        ]
    }

def calculate_comprehensive_score(analysis, asset_type, open_trade=None):
    if not analysis or not isinstance(analysis, dict):
        return _default_result("بيانات التحليل غير صالحة")
    
    price = analysis.get('price', 0)
    if not price or price <= 0:
        return _default_result(f"سعر غير صالح (القيمة: {price})")
    
    indicators = analysis.get('indicators', {})
    if not indicators or not isinstance(indicators, dict):
        return _default_result("بيانات المؤشرات مفقودة أو غير صالحة")
    
    try:
        timeframes = analysis.get('timeframes', {})
        
        frames_analysis = {}
        for tf_name in ["5m", "15m", "1h", "4h"]:
            tf_data = timeframes.get(tf_name, {})
            frames_analysis[tf_name] = _analyze_single_frame(tf_data, tf_name)
        
        bullish_count = sum(1 for tf in frames_analysis.values() if tf.get('trend') == 'صاعد')
        adx = indicators.get('trend', {}).get('adx', 0)
        rsi = indicators.get('momentum', {}).get('rsi', 50)
        macd_hist = indicators.get('momentum', {}).get('macd_hist', 0)
        stoch = indicators.get('momentum', {}).get('stoch', 50)
        vol_ratio = indicators.get('volume', {}).get('ratio', 1.0)
        bb_pos = indicators.get('volatility', {}).get('bb_position', 0.5)
        atr_pct = indicators.get('volatility', {}).get('atr_percent', 1.0)
        vwap_dev = indicators.get('volatility', {}).get('vwap_deviation', 0)
        fear_greed = indicators.get('sentiment', {}).get('fear_greed', 50)
        sr = indicators.get('support_resistance', {})
        s1 = sr.get('s1', price * 0.98)
        r1 = sr.get('r1', price * 1.02)
        pivot = sr.get('pivot', price)
        vpt = indicators.get('vpt', 0)
        supertrend_trend = analysis.get('supertrend', {}).get('trend', 1)
        
        valid_frames = [f for f in frames_analysis.values() if f.get('valid', False)]
        avg_frame_score = sum(f.get('score', 50) for f in valid_frames) / len(valid_frames) if valid_frames else 50
        
        price_hist = analysis.get('price_history', [])
        rsi_hist = analysis.get('rsi_history', [])
        macd_hist_data = analysis.get('macd_history', [])
        
        # الاتجاه
        if bullish_count >= 3:
            trend_score = 65 if adx > 25 else 55
            trend_desc = _trend_desc(bullish_count, adx)
        elif bullish_count == 2:
            trend_score = 50
            trend_desc = _trend_desc(bullish_count, adx)
        else:
            trend_score = 35 if adx > 25 else 45
            trend_desc = _trend_desc(bullish_count, adx)
        
        # الزخم
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
        momentum_desc = _momentum_desc(rsi, macd_hist, stoch)
        
        # التقلب
        volatility_score = 50
        if atr_pct > 2.5:
            volatility_score = 60
        elif atr_pct < 0.5:
            volatility_score = 40
        if bb_pos < 0.15:
            volatility_score = min(volatility_score + 10, 65)
        elif bb_pos > 0.85:
            volatility_score = max(volatility_score - 10, 35)
        volatility_desc = _volatility_desc(bb_pos, atr_pct, vwap_dev)
        
        # الحجم
        if vol_ratio >= 1.5:
            volume_score = 65
        elif vol_ratio >= 1.0:
            volume_score = 55
        elif vol_ratio >= 0.6:
            volume_score = 45
        else:
            volume_score = 35
        volume_desc = _volume_desc(vol_ratio)
        
        # الدعم/المقاومة
        if price <= s1 * 1.003:
            sr_score = 65
        elif price >= r1 * 0.997:
            sr_score = 35
        elif abs(price - pivot) / price < 0.003:
            sr_score = 50
        else:
            sr_score = 50
        sr_desc = _sr_desc(price, s1, r1, pivot)
        
        # المشاعر
        if fear_greed <= 20:
            sentiment_score = 75
        elif fear_greed <= 35:
            sentiment_score = 65
        elif fear_greed <= 55:
            sentiment_score = 50
        elif fear_greed <= 75:
            sentiment_score = 35
        else:
            sentiment_score = 25
        sentiment_desc = _sentiment_desc(fear_greed)
        
        # التباعد
        divergence = _detect_divergence(price_hist, rsi_hist, macd_hist_data)
        divergence_score = divergence.get('score', 50)
        divergence_desc = divergence.get('desc', 'لا يوجد تباعد')
        
        # VPT
        vpt_score = 50
        if vpt:
            vpt_score = 60 if vpt > 0 else 40
            vpt_desc = "إيجابي (زخم صاعد)" if vpt > 0 else "سلبي (زخم هابط)"
        else:
            vpt_desc = "غير متوفر"
        
        # SuperTrend
        st_score = 50
        if supertrend_trend == 1:
            st_score = 60
            st_desc = "صاعد"
        elif supertrend_trend == -1:
            st_score = 40
            st_desc = "هابط"
        else:
            st_desc = "محايد"
        
        # الأوزان الموسعة (10 مؤشرات)
        weights = {
            'avg_frame': 0.15,
            'trend': 0.15,
            'momentum': 0.12,
            'volatility': 0.10,
            'volume': 0.10,
            'sr': 0.10,
            'sentiment': 0.05,
            'divergence': 0.05,
            'vpt': 0.06,
            'supertrend': 0.06,
            'bollinger': 0.06
        }
        total_weight = sum(weights.values())
        if total_weight != 1.0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        final_score = (
            avg_frame_score * weights['avg_frame'] +
            trend_score * weights['trend'] +
            momentum_score * weights['momentum'] +
            volatility_score * weights['volatility'] +
            volume_score * weights['volume'] +
            sr_score * weights['sr'] +
            sentiment_score * weights['sentiment'] +
            divergence_score * weights['divergence'] +
            vpt_score * weights['vpt'] +
            st_score * weights['supertrend'] +
            (50 + (bb_pos - 0.5) * 20) * weights['bollinger']
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
            f"📈 الاتجاه: {trend_desc} (درجة: {trend_score:.0f})",
            f"⚡ الزخم: {momentum_desc} (درجة: {momentum_score:.0f})",
            f"🌊 التقلب: {volatility_desc} (درجة: {volatility_score:.0f})",
            f"📊 الحجم: {volume_desc} (درجة: {volume_score:.0f})",
            f"🛡️ الدعم/المقاومة: {sr_desc} (درجة: {sr_score:.0f})",
            f"🧠 المشاعر: {sentiment_desc} (درجة: {sentiment_score:.0f})",
            f"📉 التباعد: {divergence_desc} (درجة: {divergence_score:.0f})",
            f"📊 VPT: {vpt_desc} (درجة: {vpt_score:.0f})",
            f"📈 SuperTrend: {st_desc} (درجة: {st_score:.0f})",
            f"📊 بولينجر: {'علوي' if bb_pos > 0.7 else 'سفلي' if bb_pos < 0.3 else 'وسط'}"
        ]
        
        frames_summary = {}
        for tf_name, tf_data in frames_analysis.items():
            frames_summary[tf_name] = {
                "trend": tf_data.get('trend', 'محايد'),
                "score": tf_data.get('score', 50),
                "grade": tf_data.get('grade', 'متوسط'),
                "rsi": tf_data.get('rsi', 50),
                "adx": tf_data.get('adx', 20)
            }
        
        if open_trade:
            trade_type = open_trade.get('type', 'unknown')
            entry_price = open_trade.get('entry_price', 0)
            if entry_price > 0:
                pnl = ((price - entry_price) / entry_price * 100) if trade_type == 'long' else ((entry_price - price) / entry_price * 100)
                details.append(f"💼 الصفقة المفتوحة: {trade_type.upper()} | الربح/الخسارة: {pnl:.2f}%")
        
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
                "bb_position": bb_pos,
                "vpt": vpt,
                "supertrend_trend": supertrend_trend
            },
            "components": {
                "trend": {"score": round(trend_score, 2), "weight": weights['trend']},
                "momentum": {"score": round(momentum_score, 2), "weight": weights['momentum']},
                "volatility": {"score": round(volatility_score, 2), "weight": weights['volatility']},
                "volume": {"score": round(volume_score, 2), "weight": weights['volume']},
                "sr": {"score": round(sr_score, 2), "weight": weights['sr']},
                "sentiment": {"score": round(sentiment_score, 2), "weight": weights['sentiment']},
                "divergence": {"score": round(divergence_score, 2), "weight": weights['divergence']},
                "vpt": {"score": round(vpt_score, 2), "weight": weights['vpt']},
                "supertrend": {"score": round(st_score, 2), "weight": weights['supertrend']},
                "bollinger": {"score": round(50 + (bb_pos - 0.5) * 20, 2), "weight": weights['bollinger']}
            },
            "frames_analysis": frames_summary,
            "avg_frame_score": round(avg_frame_score, 2),
            "trade_health": {
                "status": "متوازن" if 45 <= final_score <= 60 else "قوي" if final_score > 60 else "ضعيف",
                "recommendation": "مراقبة" if 45 <= final_score <= 60 else "انتظار" if final_score < 45 else "تأكيد"
            } if open_trade else None
        }
        
    except Exception as e:
        return _default_result(f"خطأ في التقييم: {str(e)[:100]}")
       
# ====================================================================================
# 📦 PART 17: دوال التحليل الشامل (مع التخزين المؤقت + الذاكرة الطويلة من Supabase)
# ====================================================================================

# ════════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطلقة وغير قابلة للنقاش):
# ════════════════════════════════════════════════════════════════════════════════
# 1. يجب استخدام جميع المؤشرات الفنية الأساسية (RSI, ADX, MACD, الحجم, VPT)
#    في أي تحليل يتم إجراؤه.
# 
# 2. يجب تطبيق هذه المؤشرات على جميع الفريمات الزمنية الأربعة:
#    - 5 دقائق (Min5)    ← فريم التداول الأساسي
#    - 15 دقيقة (Min15)  ← فريم التأكيد
#    - ساعة (Min60)      ← فريم الاتجاه المتوسط
#    - 4 ساعات (Hour4)   ← فريم الاتجاه العام
# 
# 3. أي تحليل لا يشمل الفريمات الأربعة يُعتبر تحليلاً ناقصاً وغير صالح.
# 
# 4. الاستثناء الوحيد هو استراتيجية اكتشاف الصفقات (VPT + SuperTrend)
#    التي تعمل على الفريم الأساسي فقط (Min5) لتوليد الإشارات (BUY/SELL).
#    هذا الاستثناء مقبول لأن الاستراتيجية تعتمد على تقاطع فني واحد.
# 
# 5. جميع التحليلات الأخرى (فتح الصفقة، المراقبة، التوصيات، التوقعات،
#    التقارير، الذاكرة) يجب أن تستخدم الفريمات الأربعة كاملة.
# ════════════════════════════════════════════════════════════════════════════════
# ====================================================================================

import time
import json
import os
from datetime import datetime
from typing import Dict, Optional, List

# ✅ التخزين المؤقت للتحليل الشامل
ANALYSIS_CACHE = {}
ANALYSIS_CACHE_TTL = 15  # ثانية

# ✅ التخزين المؤقت للذاكرة (جديد)
MEMORY_CACHE = {
    "lessons": [],
    "patterns": [],
    "last_update": 0
}
MEMORY_CACHE_TTL = 60  # ثانية (تحديث كل دقيقة)

# ============================================================================
# دوال الكاش للتحليل الشامل
# ============================================================================

def get_cached_analysis(asset_type: str) -> Optional[Dict]:
    """الحصول على التحليل من الكاش إذا كان حديثاً"""
    cache_key = f"{asset_type}_{int(time.time() // ANALYSIS_CACHE_TTL)}"
    if cache_key in ANALYSIS_CACHE:
        cached = ANALYSIS_CACHE[cache_key]
        return cached.get('analysis')
    return None

def set_cached_analysis(asset_type: str, analysis: Dict):
    """تخزين التحليل في الكاش"""
    cache_key = f"{asset_type}_{int(time.time() // ANALYSIS_CACHE_TTL)}"
    ANALYSIS_CACHE[cache_key] = {
        'analysis': analysis,
        'timestamp': time.time()
    }
    if len(ANALYSIS_CACHE) > 20:
        keys = sorted(ANALYSIS_CACHE.keys(), key=lambda k: ANALYSIS_CACHE[k].get('timestamp', 0))
        for k in keys[:-20]:
            del ANALYSIS_CACHE[k]

# ============================================================================
# دوال الكاش للذاكرة
# ============================================================================

def _get_cached_memory(force_refresh: bool = False) -> Optional[Dict]:
    """الحصول على الذاكرة من الكاش إذا كانت حديثة"""
    global MEMORY_CACHE
    now = time.time()
    if not force_refresh and (now - MEMORY_CACHE.get("last_update", 0) < MEMORY_CACHE_TTL):
        if MEMORY_CACHE.get("lessons") is not None:
            return {"lessons": MEMORY_CACHE["lessons"], "patterns": MEMORY_CACHE["patterns"]}
    return None

def _set_cached_memory(lessons: List[Dict], patterns: List[Dict]):
    """تخزين الذاكرة في الكاش"""
    global MEMORY_CACHE
    MEMORY_CACHE["lessons"] = lessons or []
    MEMORY_CACHE["patterns"] = patterns or []
    MEMORY_CACHE["last_update"] = time.time()
    logger.info(f"🧠 [Memory Cache] تم تحديث الكاش: {len(lessons)} درس, {len(patterns)} نمط")

# ============================================================================
# دوال قراءة الذاكرة من Supabase
# ============================================================================

def _filter_lessons_data(lessons: List[Dict]) -> List[Dict]:
    """تصفية الدروس المسترجعة من Supabase لضمان وجود الأعمدة الأساسية فقط"""
    if not lessons:
        return []
    filtered = []
    for lesson in lessons:
        filtered_lesson = {}
        for key in LESSONS_DEEP_COLUMNS:
            if key in lesson:
                filtered_lesson[key] = lesson[key]
        filtered.append(filtered_lesson)
    return filtered

def _filter_patterns_data(patterns: List[Dict]) -> List[Dict]:
    """تصفية الأنماط المسترجعة من Supabase لضمان وجود الأعمدة الأساسية فقط"""
    if not patterns:
        return []
    filtered = []
    for pattern in patterns:
        filtered_pattern = {}
        for key in PATTERNS_COLUMNS:
            if key in pattern:
                filtered_pattern[key] = pattern[key]
        filtered.append(filtered_pattern)
    return filtered

def _get_lessons_from_supabase(asset_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """قراءة الدروس من Supabase (جدول lessons_deep) مع فلترة البيانات"""
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        return []
    try:
        if hasattr(SUPABASE_DB, 'get_lessons'):
            data = SUPABASE_DB.get_lessons(asset_type, limit) or []
            return _filter_lessons_data(data)
        client = _get_supabase_client()
        if not client:
            return []
        query = client.table(TABLE_LESSONS_DEEP).select('*').order('created_at', desc=True).limit(limit)
        if asset_type:
            query = query.eq('asset_type', asset_type)
        response = query.execute()
        if response and hasattr(response, 'data'):
            return _filter_lessons_data(response.data or [])
    except Exception as e:
        logger.warning(f"⚠️ [_get_lessons_from_supabase] فشل: {e}")
    return []

def _get_patterns_from_supabase(asset_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """قراءة الأنماط من Supabase (جدول discovered_patterns) مع فلترة البيانات"""
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        return []
    try:
        if hasattr(SUPABASE_DB, 'get_patterns'):
            data = SUPABASE_DB.get_patterns(asset_type, limit) or []
            return _filter_patterns_data(data)
        client = _get_supabase_client()
        if not client:
            return []
        query = client.table(TABLE_DISCOVERED_PATTERNS).select('*').order('created_at', desc=True).limit(limit)
        if asset_type:
            query = query.eq('asset_type', asset_type)
        response = query.execute()
        if response and hasattr(response, 'data'):
            return _filter_patterns_data(response.data or [])
    except Exception as e:
        logger.warning(f"⚠️ [_get_patterns_from_supabase] فشل: {e}")
    return []

def _load_memory_from_supabase(asset_type: Optional[str] = None, force_refresh: bool = False) -> Dict:
    """
    تحميل الذاكرة من Supabase مع استخدام الكاش وفلترة البيانات
    المصدر الأساسي: Supabase، النسخة الاحتياطية: Gist.
    تعيد قاموساً يحتوي على lessons و patterns
    """
    # 1. التحقق من الكاش
    cached = _get_cached_memory(force_refresh)
    if cached:
        return cached

    # 2. القراءة من Supabase (المصدر الأساسي)
    lessons = _get_lessons_from_supabase(asset_type, limit=100)
    patterns = _get_patterns_from_supabase(asset_type, limit=100)
    
    logger.info(f"📊 [Memory] تم جلب {len(lessons)} درس و {len(patterns)} نمط من Supabase لـ {asset_type or 'الكل'}")

    # 3. إذا لم تنجح Supabase، استخدم Gist كنسخة احتياطية
    if not lessons and not patterns:
        logger.info("🔄 [Memory] Supabase لم يعد بيانات، استخدام Gist كنسخة احتياطية")
        lessons = load_lessons_from_gist()
        patterns = load_patterns_from_gist()
        # لا نخزن في الكاش لأنها من Gist (قد لا تكون محدثة)
        return {"lessons": lessons, "patterns": patterns}

    # 4. تخزين في الكاش
    _set_cached_memory(lessons, patterns)
    return {"lessons": lessons, "patterns": patterns}

# ============================================================================
# دالة مقارنة الذاكرة (المعاد كتابتها بالكامل)
# ============================================================================

def _compare_with_memory(current_analysis: Dict, asset_type: str) -> Dict:
    """
    مقارنة التحليل الحالي بالأنماط المخزنة - نسخة مبسطة وفعالة
    ✅ تعتمد على 3 مؤشرات رئيسية فقط: (الاتجاه، RSI، ADX)
    ✅ عتبة تشابه 20%
    ✅ بحث في جميع الأصول إذا لم يتم العثور على نتائج للأصل المطلوب
    """
    result = {
        "similar_patterns": [],
        "similar_lessons": [],
        "confidence_boost": 0,
        "insight": "",
        "has_memory": False,
        "source": "unknown"
    }

    try:
        # 1. تحميل الذاكرة
        memory_data = _load_memory_from_supabase(asset_type)
        patterns = memory_data.get("patterns", [])
        lessons = memory_data.get("lessons", [])
        result["source"] = "supabase" if patterns or lessons else "gist"

        if not patterns and not lessons:
            logger.info("🧠 [Memory] لا توجد أنماط أو دروس في الذاكرة بعد.")
            result["insight"] = "⚠️ لا توجد خبرات سابقة كافية للتقييم"
            return result

        # 2. استخراج المؤشرات الرئيسية فقط من التحليل الحالي
        indicators = current_analysis.get('indicators', {})
        trend_data = indicators.get('trend', {})
        momentum = indicators.get('momentum', {})
        
        current_trend = trend_data.get('current_trend', 'محايد')
        current_rsi = momentum.get('rsi', 50)
        current_adx = trend_data.get('adx', 20)
        
        logger.info(f"🔍 [Memory] البحث عن أنماط مشابهة لـ {asset_type}: الاتجاه={current_trend}, RSI={current_rsi:.0f}, ADX={current_adx:.0f}")

        # 3. البحث عن أنماط متشابهة (معايير مبسطة، عتبة 20%)
        similar_patterns = []
        for pattern in patterns:
            conditions = pattern.get('conditions', {})
            pattern_win_rate = pattern.get('win_rate', 0)
            sample_count = pattern.get('sample_count', 0)
            
            if sample_count < 2:
                continue
            
            # استخراج المؤشرات الرئيسية من النمط
            pattern_trend = conditions.get('trend', 'محايد')
            pattern_rsi_class = conditions.get('rsi_class', 'neutral')
            pattern_adx_class = conditions.get('adx_class', 'weak')
            
            # تحويل الفئات إلى قيم عددية للمقارنة
            similarity = 0
            total_weight = 0
            
            # مقارنة الاتجاه (وزن 40%)
            if current_trend == pattern_trend:
                similarity += 0.4
            total_weight += 0.4
            
            # مقارنة RSI (وزن 30%)
            rsi_match = False
            if current_rsi < 30 and pattern_rsi_class == 'oversold':
                rsi_match = True
            elif current_rsi > 70 and pattern_rsi_class == 'overbought':
                rsi_match = True
            elif 30 <= current_rsi <= 70 and pattern_rsi_class == 'neutral':
                rsi_match = True
            if rsi_match:
                similarity += 0.3
            total_weight += 0.3
            
            # مقارنة ADX (وزن 30%)
            adx_match = False
            if current_adx > 25 and pattern_adx_class == 'strong':
                adx_match = True
            elif current_adx <= 25 and pattern_adx_class == 'weak':
                adx_match = True
            if adx_match:
                similarity += 0.3
            total_weight += 0.3
            
            if total_weight > 0:
                similarity_percent = (similarity / total_weight) * 100
            else:
                similarity_percent = 0
            
            # ✅ عتبة 20%
            if similarity_percent >= 20:
                similar_patterns.append({
                    'pattern_name': pattern.get('pattern_name', 'نمط غير معروف'),
                    'similarity': round(similarity_percent, 1),
                    'win_rate': float(pattern_win_rate),
                    'sample_count': sample_count,
                    'description': pattern.get('description', ''),
                    'is_successful': pattern.get('is_successful', False)
                })

        # 4. ✅ إذا لم يتم العثور على أنماط، ابحث في جميع الأصول
        if not similar_patterns and asset_type:
            logger.info(f"🔄 [Memory] لم يتم العثور على أنماط لـ {asset_type}، البحث في جميع الأصول")
            all_patterns = _load_memory_from_supabase(None)  # تحميل كل الأنماط
            all_patterns_list = all_patterns.get("patterns", [])
            for pattern in all_patterns_list:
                conditions = pattern.get('conditions', {})
                pattern_win_rate = pattern.get('win_rate', 0)
                sample_count = pattern.get('sample_count', 0)
                
                if sample_count < 2:
                    continue
                
                pattern_trend = conditions.get('trend', 'محايد')
                pattern_rsi_class = conditions.get('rsi_class', 'neutral')
                pattern_adx_class = conditions.get('adx_class', 'weak')
                
                similarity = 0
                total_weight = 0
                
                if current_trend == pattern_trend:
                    similarity += 0.4
                total_weight += 0.4
                
                rsi_match = False
                if current_rsi < 30 and pattern_rsi_class == 'oversold':
                    rsi_match = True
                elif current_rsi > 70 and pattern_rsi_class == 'overbought':
                    rsi_match = True
                elif 30 <= current_rsi <= 70 and pattern_rsi_class == 'neutral':
                    rsi_match = True
                if rsi_match:
                    similarity += 0.3
                total_weight += 0.3
                
                adx_match = False
                if current_adx > 25 and pattern_adx_class == 'strong':
                    adx_match = True
                elif current_adx <= 25 and pattern_adx_class == 'weak':
                    adx_match = True
                if adx_match:
                    similarity += 0.3
                total_weight += 0.3
                
                if total_weight > 0:
                    similarity_percent = (similarity / total_weight) * 100
                else:
                    similarity_percent = 0
                
                if similarity_percent >= 20:
                    similar_patterns.append({
                        'pattern_name': pattern.get('pattern_name', 'نمط غير معروف') + " (جميع الأصول)",
                        'similarity': round(similarity_percent, 1),
                        'win_rate': float(pattern_win_rate),
                        'sample_count': sample_count,
                        'description': pattern.get('description', ''),
                        'is_successful': pattern.get('is_successful', False)
                    })

        # 5. البحث عن دروس مشابهة (نفس المنطق)
        similar_lessons = []
        for lesson in lessons[-20:]:
            lesson_summary = lesson.get('summary', '')
            if any(kw in lesson_summary.lower() for kw in ['rsi', 'adx', 'trend', 'volume']):
                similar_lessons.append({
                    'summary': lesson_summary[:100],
                    'type': lesson.get('type', 'info'),
                    'details': lesson.get('details', '')[:100],
                    'source': lesson.get('source', 'غير معروف')
                })

        # 6. بناء النتائج
        result["similar_patterns"] = similar_patterns
        result["similar_lessons"] = similar_lessons
        result["has_memory"] = bool(similar_patterns or similar_lessons)

        # 7. حساب تعديل الثقة
        if similar_patterns:
            avg_win_rate = sum(p['win_rate'] for p in similar_patterns) / len(similar_patterns)
            if avg_win_rate >= 70 and len(similar_patterns) >= 3:
                result["confidence_boost"] = 10
            elif avg_win_rate >= 60 and len(similar_patterns) >= 2:
                result["confidence_boost"] = 5
            elif avg_win_rate >= 50:
                result["confidence_boost"] = 0
            else:
                result["confidence_boost"] = -5
            
            # بناء رسالة الذاكرة
            if len(similar_patterns) == 1:
                p = similar_patterns[0]
                result["insight"] = f"🧠 نمط مشابه واحد: {p['pattern_name']} (تشابه {p['similarity']:.0f}%، نجاح {p['win_rate']:.0f}%)"
            else:
                result["insight"] = f"🧠 {len(similar_patterns)} أنماط مشابهة، متوسط نجاح {avg_win_rate:.0f}%"
        elif similar_lessons:
            result["confidence_boost"] = 3
            result["insight"] = f"🧠 درس مشابه: {similar_lessons[0]['summary'][:60]}..."
        else:
            result["insight"] = "⚠️ لا توجد أنماط مشابهة في الذاكرة"

        logger.info(f"🧠 [Memory] تم العثور على {len(similar_patterns)} نمط و {len(similar_lessons)} درس متشابه")

    except Exception as e:
        logger.error(f"❌ [Memory] فشل مقارنة الذاكرة: {e}")
        import traceback
        logger.error(traceback.format_exc())
        result["insight"] = "⚠️ حدث خطأ في تحميل الذاكرة"

    return result
   
# ============================================================================
# ✅ الدالة الأساسية للتحليل الشامل (تعمل على الفريمات الأربعة)
# ============================================================================

def perform_comprehensive_analysis(asset_type, is_monitoring=False, open_trade=None, force_refresh=False):
    """
    تحليل شامل للأصل المطلوب مع تخزين مؤقت + دمج الذاكرة الطويلة (الأنماط والدروس)
    
    ═══════════════════════════════════════════════════════════════════════════════
    🔴 القاعدة الذهبية للتحليل الشامل (مطبقة هنا):
    ═══════════════════════════════════════════════════════════════════════════════
    - يتم حساب المؤشرات على جميع الفريمات الأربعة:
      5 دقائق (Min5) ← فريم التداول الأساسي
      15 دقيقة (Min15) ← فريم التأكيد
      ساعة (Min60) ← فريم الاتجاه المتوسط
      4 ساعات (Hour4) ← فريم الاتجاه العام
    - المؤشرات المحسوبة: RSI, MACD, ADX, حجم التداول النسبي، VPT, SuperTrend.
    - جميع المؤشرات تُحسب لكل فريم على حدة وتُخزّن في analysis["timeframes"][tf].
    - هذا التحليل يُستخدم لجميع الأغراض: فتح الصفقة، المراقبة، التوصيات، التوقعات، التقارير.
    - الاستثناء الوحيد: استراتيجية اكتشاف الصفقات تعتمد على VPT + SuperTrend فقط.
    ═══════════════════════════════════════════════════════════════════════════════
    """
    try:
        # ── التحقق من الكاش (إذا لم يكن force_refresh) ──
        if not is_monitoring and not force_refresh:
            cached = get_cached_analysis(asset_type)
            if cached:
                logger.info(f"📊 استخدام التحليل المخبأ لـ {asset_type}")
                try:
                    from advisor_core import format_concise_analysis
                    report = format_concise_analysis(cached, asset_type, is_monitoring, open_trade)
                except:
                    report = "⚠️ تحليل غير متوفر"
                return cached, report
        
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        
        # ── جلب البيانات مع إعادة محاولة ──
        data = None
        for attempt in range(3):
            try:
                data = get_mexc_candles(symbol, interval="Min5", limit=200)
                if data and data.get("closes") and len(data["closes"]) >= 10:
                    break
                else:
                    logger.warning(f"⚠️ محاولة {attempt+1}: بيانات غير كافية لـ {asset_type}")
                    time.sleep(1 if attempt < 2 else 0)
            except Exception as e:
                logger.warning(f"⚠️ محاولة {attempt+1}: فشل جلب البيانات لـ {asset_type}: {e}")
                time.sleep(1 if attempt < 2 else 0)
                data = None
        
        if not data or not data.get("closes") or len(data["closes"]) < 10:
            error_msg = f"⚠️ لا توجد بيانات كافية للتحليل بعد 3 محاولات (عدد الشموع: {len(data.get('closes', [])) if data else 0})"
            logger.warning(f"[تحليل] {error_msg}")
            return None, error_msg
        
        closes = data["closes"]
        highs = data["highs"]
        lows = data["lows"]
        volumes = data["volumes"]
        
        # ── حساب المؤشرات على الفريم الأساسي (5 دقائق) ──
        current_price = closes[-1]
        current_rsi = calculate_rsi_7(closes)[-1] if len(closes) >= 7 else None
        current_macd = calculate_macd_histogram(closes)[-1] if len(closes) >= 35 else None
        adx = calculate_adx_14(data)
        atr = calculate_atr_14(data)
        
        # Bollinger Bands
        upper, basis, lower = calculate_bollinger_bands(closes)
        bb_upper = upper[-1] if upper else None
        bb_basis = basis[-1] if basis else None
        bb_lower = lower[-1] if lower else None
        
        # Stochastic
        stoch = calculate_stochastic(highs, lows, closes)
        stoch_value = stoch[-1] if stoch else None
        
        # VWAP
        vwap_values = calculate_vwap(data)
        vwap = vwap_values[-1] if vwap_values else None
        
        # Volume ratio
        vol_ratio = 1.0
        if volumes and len(volumes) > 20:
            current_vol = volumes[-1]
            avg_vol = sum(volumes[-20:-1]) / 19 if len(volumes) > 20 else current_vol
            vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1.0
        
        # SuperTrend
        st_line_arr, trend, _ = calculate_supertrend_vpt_correct(
            data,
            st_mult=2.5 if asset_type == "oil" else 2.2,
            st_period=100,
            vpt_len=10
        )
        
        # ── ✅ تحليل الفريمات الأربعة (القاعدة الذهبية) ──
        timeframes = {
            "5m": {"interval": "Min5", "limit": 200},
            "1h": {"interval": "Min60", "limit": 200},
            "4h": {"interval": "Hour4", "limit": 200}
        }
        results = fetch_multiple_timeframes(symbol, timeframes)
        
        timeframes_data = {}
        for tf_name, tf_data in [("5m", results.get("5m")), ("1h", results.get("1h")), ("4h", results.get("4h"))]:
            if tf_data and tf_data.get("closes") and len(tf_data["closes"]) >= 10:
                tcloses = tf_data["closes"]
                # حساب المؤشرات لكل فريم
                tf_rsi = calculate_rsi_7(tcloses)[-1] if len(tcloses) >= 7 else None
                tf_macd = calculate_macd_histogram(tcloses)[-1] if len(tcloses) >= 35 else None
                tf_adx = calculate_adx_14(tf_data)
                tf_atr = calculate_atr_14(tf_data)
                
                # SuperTrend لكل فريم
                st_result = calculate_supertrend_vpt_correct(tf_data, st_mult=2.5 if asset_type == "oil" else 2.2)
                if st_result is not None and len(st_result) == 3:
                    st_l, tr, _ = st_result
                    st_line = st_l[-1] if st_l else None
                    st_trend = tr[-1] if tr else None
                else:
                    st_line = None
                    st_trend = None
                
                # حجم التداول لكل فريم
                tf_volumes = tf_data.get("volumes", [])
                tf_vol_ratio = 1.0
                if tf_volumes and len(tf_volumes) > 20:
                    tf_current_vol = tf_volumes[-1]
                    tf_avg_vol = sum(tf_volumes[-20:-1]) / 19 if len(tf_volumes) > 20 else tf_current_vol
                    tf_vol_ratio = tf_current_vol / tf_avg_vol if tf_avg_vol > 0 else 1.0
                
                timeframes_data[tf_name] = {
                    "price": tcloses[-1],
                    "rsi": tf_rsi,
                    "macd": tf_macd,
                    "adx": tf_adx,
                    "atr": tf_atr,
                    "volume_ratio": tf_vol_ratio,
                    "trend": "صاعد" if st_trend == 1 else "هابط" if st_trend == -1 else "محايد",
                    "supertrend": {"line": st_line, "trend": st_trend}
                }
                
                # ✅ إضافة Bollinger Bands و Stochastic لكل فريم
                tf_upper, tf_basis, tf_lower = calculate_bollinger_bands(tcloses)
                tf_stoch = calculate_stochastic(tf_data.get("highs", []), tf_data.get("lows", []), tcloses)
                tf_vwap = calculate_vwap(tf_data)
                
                timeframes_data[tf_name]["bollinger"] = {
                    "upper": tf_upper[-1] if tf_upper else None,
                    "basis": tf_basis[-1] if tf_basis else None,
                    "lower": tf_lower[-1] if tf_lower else None
                }
                timeframes_data[tf_name]["stochastic"] = tf_stoch[-1] if tf_stoch else None
                timeframes_data[tf_name]["vwap"] = tf_vwap[-1] if tf_vwap else None
            else:
                logger.warning(f"⚠️ فشل حساب المؤشرات للفريم {tf_name} في {asset_type} (بيانات غير كافية)")
                timeframes_data[tf_name] = {
                    "price": 0,
                    "trend": "محايد",
                    "supertrend": {"line": None, "trend": None},
                    "rsi": None,
                    "macd": None,
                    "adx": None,
                    "atr": None,
                    "volume_ratio": 1.0,
                    "bollinger": {"upper": None, "basis": None, "lower": None},
                    "stochastic": None,
                    "vwap": None
                }
        
        # ── بناء التحليل الشامل الأساسي ──
        analysis = {
            "price": current_price,
            "asset": asset_type,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "trend": {
                    "bullish_count": sum(1 for tf in timeframes_data.values() if tf.get("trend") == "صاعد"),
                    "adx": adx,
                    "current_trend": "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد"
                },
                "momentum": {
                    "rsi": current_rsi,
                    "macd_hist": current_macd,
                    "stoch": stoch_value
                },
                "volatility": {
                    "atr_percent": (atr / current_price) * 100 if current_price > 0 else None,
                    "bb_position": (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper and bb_lower and bb_upper > bb_lower else None,
                    "vwap_deviation": (current_price - vwap) / vwap if vwap and vwap > 0 else None
                },
                "volume": {
                    "ratio": vol_ratio
                },
                "support_resistance": {
                    "s1": current_price * 0.98,
                    "r1": current_price * 1.02,
                    "pivot": current_price
                },
                "sentiment": {
                    "fear_greed": 50
                },
                "bollinger": {
                    "upper": bb_upper,
                    "basis": bb_basis,
                    "lower": bb_lower
                },
                "vwap": vwap
            },
            "timeframes": {
                "5m": timeframes_data.get("5m", {}),
                "15m": {
                    "price": current_price,
                    "rsi": current_rsi,
                    "macd": current_macd,
                    "adx": adx,
                    "atr": atr,
                    "volume_ratio": vol_ratio,
                    "trend": "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد",
                    "supertrend": {"line": st_line_arr[-1] if st_line_arr else current_price, "trend": trend[-1] if trend else 1},
                    "bollinger": {"upper": bb_upper, "basis": bb_basis, "lower": bb_lower},
                    "stochastic": stoch_value,
                    "vwap": vwap,
                    "bb_position": (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper and bb_lower and bb_upper > bb_lower else None
                },
                "1h": timeframes_data.get("1h", {}),
                "4h": timeframes_data.get("4h", {})
            },
            "supertrend": {
                "line": st_line_arr[-1] if st_line_arr else current_price,
                "trend": trend[-1] if trend else 1
            },
            "vpt": {
                "value": 0
            },
            "fear_greed": 50,
            "support_resistance": {
                "support": current_price * 0.98,
                "resistance": current_price * 1.02,
                "pivot": current_price
            },
            "price_history": closes[-50:] if len(closes) >= 50 else closes,
            "rsi_history": calculate_rsi_7(closes)[-50:] if len(closes) >= 50 else calculate_rsi_7(closes),
            "macd_history": calculate_macd_histogram(closes)[-50:] if len(closes) >= 50 else calculate_macd_histogram(closes)
        }
        
        # ── إضافة الفريمات إلى التحليل ──
        for tf_name, tf_data in timeframes_data.items():
            if tf_name in analysis["timeframes"]:
                analysis["timeframes"][tf_name].update(tf_data)
            else:
                analysis["timeframes"][tf_name] = tf_data
        
        # ── حساب التقييم الشامل ──
        analysis["comprehensive_score"] = calculate_comprehensive_score(analysis, asset_type, open_trade)
        
        # ── دمج الذاكرة الطويلة ──
        memory_insights = _compare_with_memory(analysis, asset_type)
        analysis["memory_insights"] = memory_insights
        
        # ── تعديل الثقة بناءً على الذاكرة ──
        if memory_insights["has_memory"]:
            old_score = analysis["comprehensive_score"]["score"]
            boost = memory_insights["confidence_boost"]
            new_score = max(0, min(100, old_score + boost))
            analysis["comprehensive_score"]["score"] = new_score
            analysis["comprehensive_score"]["memory_boost"] = boost
            analysis["comprehensive_score"]["memory_source"] = memory_insights.get("source", "unknown")
            analysis["comprehensive_score"]["grade"] = (
                "إيجابي قوي" if new_score >= 70 else
                "إيجابي" if new_score >= 60 else
                "محايد" if new_score >= 45 else
                "سلبي" if new_score >= 35 else
                "سلبي قوي"
            )
            logger.info(f"🧠 [Memory] تم تعديل التقييم: {old_score} → {new_score} (تعديل: {boost:+d})")
        
        # ── تخزين في الكاش ──
        set_cached_analysis(asset_type, analysis)
        
        # ── توليد التقرير الموجز ──
        try:
            from advisor_core import format_concise_analysis
            report = format_concise_analysis(analysis, asset_type, is_monitoring, open_trade)
            
            if memory_insights["insight"]:
                report = f"{memory_insights['insight']}\n\n" + report
                
        except ImportError:
            score = analysis["comprehensive_score"].get("score", 50)
            grade = analysis["comprehensive_score"].get("grade", "محايد")
            memory_line = ""
            if memory_insights["insight"]:
                memory_line = f"{memory_insights['insight']}\n\n"
            report = f"{memory_line}📊 تحليل {asset_type}\n💰 السعر: ${current_price:.2f}\n📊 التقييم: {score:.0f}% ({grade})"
        
        return analysis, report
        
    except Exception as e:
        logger.error(f"خطأ في التحليل الشامل لـ {asset_type}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None, f"⚠️ حدث خطأ أثناء التحليل: {str(e)}"

# ============================================================================
# نهاية PART 17
# ====================================================================================

# ====================================================================================
# 📦 PART 18: تهيئة Advisor
# ====================================================================================

if ADVISOR_AVAILABLE:
    try:
        ADVISOR = HOBANYAdvisor(
            groq_api_key=GROQ_API_KEY,
            analyze_func=perform_comprehensive_analysis,
            check_position_func=get_current_open_trade
        )
        logger.info("🧠 Advisor Core: المستشار الذكي جاهز!")
    except Exception as e:
        logger.error(f"فشل تهيئة Advisor: {e}")
        ADVISOR_AVAILABLE = False
       
# ====================================================================================
# 📦 PART 19: تنظيف الصفقات العالقة
# ====================================================================================

def cleanup_stuck_trades_on_startup():
    """تنظيف الصفقات العالقة عند بدء التشغيل"""
    
    logger.info("🧹 بدء تنظيف الصفقات العالقة...")
    cleaned = 0
    added = 0
    
    for asset_type in ["oil", "silver"]:
        pos_file = get_position_file(asset_type)
        
        if not os.path.exists(pos_file):
            continue
        
        try:
            with open(pos_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    os.remove(pos_file)
                    cleaned += 1
                    continue
                trade = json.loads(content)
            
            trade_id = trade.get("trade_id", "")
            
            history = load_trades_history(asset_type)
            found_in_history = False
            is_closed_in_history = False
            
            for t in history.get("trades", []):
                if t.get("trade_id") == trade_id:
                    found_in_history = True
                    if t.get("status") == "closed":
                        is_closed_in_history = True
                    break
            
            if is_closed_in_history:
                os.remove(pos_file)
                cleaned += 1
                logger.info(f"🗑️ تم حذف صفقة مغلقة: {pos_file}")
            elif not found_in_history:
                logger.info(f"ℹ️ صفقة جديدة غير مسجلة: {trade_id} - الاحتفاظ بها وإضافتها للسجل")
                trade["status"] = "open"
                trade["timestamp"] = trade.get("timestamp", datetime.now().isoformat())
                if "warnings_sent" not in trade:
                    trade["warnings_sent"] = []
                if "recommendations_sent" not in trade:
                    trade["recommendations_sent"] = []
                history["trades"].append(trade)
                save_trades_history(asset_type, history)
                added += 1
                logger.info(f"✅ تم إضافة الصفقة الجديدة إلى السجل: {trade_id}")
            else:
                logger.info(f"✅ صفقة مفتوحة موجودة: {trade_id}")
            
        except (json.JSONDecodeError, Exception) as e:
            try:
                os.remove(pos_file)
                cleaned += 1
                logger.info(f"🗑️ تم حذف ملف تالف: {pos_file}")
            except:
                pass
    
    with MONITOR_TRIGGER_LOCK:
        MONITOR_TRIGGER["oil"] = None
        MONITOR_TRIGGER["silver"] = None
    
    with LAST_SIGNAL_LOCK:
        last_signal_states["oil"] = {"signal": "WAIT", "time": 0}
        last_signal_states["silver"] = {"signal": "WAIT", "time": 0}
    
    if cleaned > 0 or added > 0:
        logger.info(f"✅ تم تنظيف {cleaned} صفقة عالقة وإضافة {added} صفقة جديدة")
    return cleaned, added

cleaned_count, added_count = cleanup_stuck_trades_on_startup()
if cleaned_count > 0 or added_count > 0:
    print(f"🧹 تم تنظيف {cleaned_count} صفقة عالقة وإضافة {added_count} صفقة جديدة")


# ====================================================================================
# 📦 PART 20: دوال إغلاق الصفقات (معدل - مع حفظ التحليل الشامل للإغلاق والتعلم الصامت)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. دمج دروس Post-Mortem في نظام التعلم الموحد عبر save_post_mortem_lessons (من PART 15).
#   2. استدعاء process_trade_for_learning (من PART 30) لاستخلاص الدروس من التحليل الشامل.
#   3. استخدام الدوال المعدلة في PART 10 و PART 15 للفلترة التلقائية للأعمدة.
#   4. ✅ إعادة صياغة تحليل الصفقة الخاسرة (Post-Mortem) ليكون:
#      - خالياً من علامات HTML المزعجة (يستخدم Markdown النظيف).
#      - يحتفظ بأسماء المؤشرات الفنية المعروفة (RSI, ADX, MACD, VWAP, Bollinger Bands).
#      - واضحاً ومنطقياً مع شرح أسباب الخسارة بناءً على التحليل الفني الشامل.
#      - الدروس المستفادة والتوصيات محددة وقابلة للتطبيق.
#   5. ✅ إزالة رسالة "تولين تعلمت درساً جديداً" لجعل التعلم صامتاً تماماً.
#   6. ✅ إصلاح التحقق من نجاح الإغلاق: التأكد من قيمة إرجاع close_trade_virtual.
#   7. ✅ حذف ملف الصفقة بعد التأكد من نجاح save_trades_history.
#   8. ✅ تحديث تحليل الإغلاق بدون كاش (force_refresh=True).
#   9. ✅ إصلاح اكتشاف الأنماط: استدعاء discover_patterns_from_trades مباشرة بعد حفظ الصفقة.
#  10. ✅ ✅ ✅ إزالة جميع التوقعات الداخلية (تحديث نتيجة التوقع ومعايرة الثقة) لأن التوصية تعتمد الآن على Gemini.
#  11. ✅ ⚠️ إزالة جميع القيم الافتراضية عند فشل جلب التحليل (استخدام None بدلاً من 50, 15, 0, إلخ).
#  12. الحفاظ على جميع الدوال الأخرى دون تغيير.
#  13. ✅ إضافة قفل حصري (CLOSE_LOCKS) لمنع تنفيذ الإغلاق مرتين لنفس الصفقة.
#  14. ✅ إعادة التحقق من وجود الصفقة المفتوحة بعد الحصول على القفل.
# ====================================================================================

import time
import json
import threading
from datetime import datetime

def close_trade_virtual(asset_type, reason="أمر افتراضي", current_price=None):
    """إغلاق الصفقة مع حفظ التحليل الشامل للإغلاق واستخلاص الدروس (صامت)"""
    
    logger.info(f"🔒 بدء إغلاق {asset_type}: {reason}")
    
    # ✅ قفل حصري لهذا الأصل لمنع تنفيذ الإغلاق مرتين
    with CLOSE_LOCKS[asset_type]:
        logger.info(f"🔒 [Close] تم الحصول على قفل الإغلاق لـ {asset_type}")
        
        # ✅ التحقق المزدوج: هل الصفقة ما زالت مفتوحة؟
        open_trade = get_current_open_trade(asset_type)
        if not open_trade:
            logger.info(f"⏭️ [Close] الصفقة {asset_type} أغلقت بالفعل بواسطة خيط آخر.")
            return True  # نعتبر الإغلاق ناجحاً لأنها ليست مفتوحة
        
        symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
        if current_price is None:
            data = get_mexc_candles(symbol, "Min1", 5)
            current_price = data["closes"][-1] if data and data.get("closes") else open_trade["entry_price"]

        entry_price = open_trade["entry_price"]
        trade_type = open_trade["type"]
        profit_dollars = AccountingSystem.calculate_profit_dollars(entry_price, current_price, trade_type)
        trade_id = open_trade.get("trade_id", "")

        # ── 1. الحصول على التحليل الشامل عند الإغلاق (لحظي، بدون كاش) ──
        logger.info(f"📊 جلب التحليل الشامل عند الإغلاق لـ {asset_type} (force_refresh=True)")
        closing_analysis, _ = perform_comprehensive_analysis(asset_type, False, None, force_refresh=True)
        
        # ── 2. استخراج بيانات التحليل الشامل عند الإغلاق ──
        # ⚠️ لا نستخدم قيماً افتراضية، بل نضع None إذا كان التحليل غير متوفر
        if closing_analysis and isinstance(closing_analysis, dict):
            tf_15m = closing_analysis.get("timeframes", {}).get("15m", {}) if isinstance(closing_analysis.get("timeframes"), dict) else {}
            indicators = closing_analysis.get("indicators", {}) if isinstance(closing_analysis.get("indicators"), dict) else {}
            comp_score = closing_analysis.get("comprehensive_score", {}) if isinstance(closing_analysis.get("comprehensive_score"), dict) else {}
            
            # استخراج القيم مع الاحتفاظ بـ None إذا كانت مفقودة
            close_rsi = tf_15m.get("rsi") if isinstance(tf_15m, dict) else None
            close_adx = tf_15m.get("adx") if isinstance(tf_15m, dict) else None
            close_macd = tf_15m.get("macd") if isinstance(tf_15m, dict) else None
            close_trend = tf_15m.get("trend") if isinstance(tf_15m, dict) else None
            close_vol_ratio = tf_15m.get("volume_ratio") if isinstance(tf_15m, dict) else None
            close_vwap = tf_15m.get("vwap") if isinstance(tf_15m, dict) else None
            
            bb = tf_15m.get("bollinger", {}) if isinstance(tf_15m, dict) else {}
            close_bb_upper = bb.get("upper") if isinstance(bb, dict) else None
            close_bb_middle = bb.get("basis") if isinstance(bb, dict) else None
            close_bb_lower = bb.get("lower") if isinstance(bb, dict) else None
            
            sr = indicators.get("support_resistance", {}) if isinstance(indicators, dict) else {}
            close_support = sr.get("s1") if isinstance(sr, dict) else None
            close_resistance = sr.get("r1") if isinstance(sr, dict) else None
            
            close_score = comp_score.get("score") if isinstance(comp_score, dict) else None
            close_grade = comp_score.get("grade") if isinstance(comp_score, dict) else None
            
            full_exit_analysis = closing_analysis
        else:
            # ⚠️ لا نستخدم قيماً افتراضية، نضع None للجميع
            close_rsi = None
            close_adx = None
            close_macd = None
            close_trend = None
            close_vol_ratio = None
            close_vwap = None
            close_bb_upper = None
            close_bb_middle = None
            close_bb_lower = None
            close_support = None
            close_resistance = None
            close_score = None
            close_grade = None
            full_exit_analysis = None
            logger.warning(f"⚠️ تعذر الحصول على تحليل الإغلاق للصفقة {trade_id} - سيتم حفظ القيم كـ None")

        # ── 3. استخراج بيانات التحليل الشامل عند الفتح (من الملف المحفوظ) ──
        holistic_entry = open_trade.get("holistic_entry_analysis", {})
        full_entry_analysis = holistic_entry if isinstance(holistic_entry, dict) else None
        
        if holistic_entry and isinstance(holistic_entry, dict):
            entry_tf_15m = holistic_entry.get("timeframes", {}).get("15m", {}) if isinstance(holistic_entry.get("timeframes"), dict) else {}
            entry_indicators_data = holistic_entry.get("indicators", {}) if isinstance(holistic_entry.get("indicators"), dict) else {}
            entry_comp_score = holistic_entry.get("comprehensive_score", {}) if isinstance(holistic_entry.get("comprehensive_score"), dict) else {}
            
            entry_rsi = entry_tf_15m.get("rsi") if isinstance(entry_tf_15m, dict) else None
            entry_adx = entry_tf_15m.get("adx") if isinstance(entry_tf_15m, dict) else None
            entry_macd = entry_tf_15m.get("macd") if isinstance(entry_tf_15m, dict) else None
            entry_trend = entry_tf_15m.get("trend") if isinstance(entry_tf_15m, dict) else None
            entry_vol_ratio = entry_tf_15m.get("volume_ratio") if isinstance(entry_tf_15m, dict) else None
            entry_vwap = entry_tf_15m.get("vwap") if isinstance(entry_tf_15m, dict) else None
            
            entry_bb = entry_tf_15m.get("bollinger", {}) if isinstance(entry_tf_15m, dict) else {}
            entry_bb_upper = entry_bb.get("upper") if isinstance(entry_bb, dict) else None
            entry_bb_middle = entry_bb.get("basis") if isinstance(entry_bb, dict) else None
            entry_bb_lower = entry_bb.get("lower") if isinstance(entry_bb, dict) else None
            
            entry_sr = entry_indicators_data.get("support_resistance", {}) if isinstance(entry_indicators_data, dict) else {}
            entry_support = entry_sr.get("s1") if isinstance(entry_sr, dict) else None
            entry_resistance = entry_sr.get("r1") if isinstance(entry_sr, dict) else None
            
            entry_score = entry_comp_score.get("score") if isinstance(entry_comp_score, dict) else None
            entry_grade = entry_comp_score.get("grade") if isinstance(entry_comp_score, dict) else None
        else:
            # ⚠️ لا نستخدم قيماً افتراضية، نضع None للجميع
            entry_rsi = None
            entry_adx = None
            entry_macd = None
            entry_trend = None
            entry_vol_ratio = None
            entry_vwap = None
            entry_bb_upper = None
            entry_bb_middle = None
            entry_bb_lower = None
            entry_support = None
            entry_resistance = None
            entry_score = None
            entry_grade = None
            logger.warning(f"⚠️ لا يوجد تحليل شامل للدخول للصفقة {trade_id} - سيتم حفظ القيم كـ None")

        # ── 4. تحديث السجل المحلي ──
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
                trade["manual_close"] = reason in ["أمر يدوي من المستخدم", "أمر يدوي من الزر"]
                break
        
        if not trade_found:
            new_trade = {
                "trade_id": trade_id,
                "type": trade_type,
                "entry_price": entry_price,
                "exit_price": current_price,
                "sl": open_trade.get("sl", 0),
                "tp": open_trade.get("tp", 0),
                "profit_dollars": profit_dollars,
                "status": "closed",
                "exit_reason": reason,
                "timestamp": open_trade.get("timestamp", datetime.now().isoformat()),
                "exit_timestamp": datetime.now().isoformat(),
                "manual_close": True,
                "asset_type": asset_type,
                "entry_indicators": open_trade.get("entry_indicators", {}),
                "warnings_sent": open_trade.get("warnings_sent", []),
                "recommendations_sent": open_trade.get("recommendations_sent", [])
            }
            history["trades"].append(new_trade)

        # ✅ حفظ التاريخ أولاً، ثم حذف ملف الصفقة فقط إذا نجح الحفظ
        history_saved = save_trades_history(asset_type, history)
        
        if not history_saved:
            logger.error(f"❌ [close_trade_virtual] فشل حفظ التاريخ لـ {asset_type} - الصفقة {trade_id}")
            queue_telegram_message(f"⚠️ تحذير: فشل حفظ الصفقة {trade_id} في التاريخ. حاول مرة أخرى.")
            return False

        # ✅ حذف ملف الصفقة المفتوحة فقط بعد التأكد من نجاح حفظ التاريخ
        pos_file = get_position_file(asset_type)
        if os.path.exists(pos_file):
            try:
                os.remove(pos_file)
                logger.info(f"🗑️ تم حذف ملف الصفقة المفتوحة: {pos_file} (بعد نجاح حفظ التاريخ)")
            except Exception as e:
                logger.error(f"❌ فشل حذف ملف الصفقة: {e}")

        with MONITOR_TRIGGER_LOCK:
            MONITOR_TRIGGER[asset_type] = None
        with LAST_SIGNAL_LOCK:
            last_signal_states[asset_type] = {"signal": "WAIT", "time": 0}
            last_signal_time[asset_type] = 0

        if RISK_MASTER_AVAILABLE and RISK_MASTER:
            try:
                RISK_MASTER.update_after_trade(profit=profit_dollars)
            except:
                pass

        if PROMETHEUS_AVAILABLE and PROMETHEUS:
            try:
                PROMETHEUS._update_emotions({'trigger': 'trade_closed', 'profit': profit_dollars})
            except:
                pass

        # ── 5. حفظ البيانات في قواعد التعلم ──
        learning_saved = False
        try:
            entry_time = open_trade.get('timestamp', datetime.now().isoformat())
            exit_time = datetime.now().isoformat()
            duration_minutes = 0
            try:
                entry_dt = datetime.fromisoformat(entry_time)
                exit_dt = datetime.now()
                duration_minutes = int((exit_dt - entry_dt).total_seconds() / 60)
            except:
                pass
            
            profit_pct = (((current_price - entry_price) / entry_price * 100) if trade_type == "BUY" else ((entry_price - current_price) / entry_price * 100)) if entry_price != 0 else 0
            sl = open_trade.get('sl', 0)
            tp = open_trade.get('tp', 0)
            rr = 1.0
            if sl and tp and entry_price:
                if trade_type == "BUY":
                    risk = entry_price - sl
                    reward = tp - entry_price
                else:
                    risk = sl - entry_price
                    reward = entry_price - tp
                rr = reward / risk if risk != 0 else 1.0
            
            # ✅ بناء بيانات التعلم الكاملة (بدون قيم افتراضية)
            trade_full_data = {
                'trade_id': trade_id,
                'asset_type': asset_type,
                'trade_type': trade_type,
                'entry_price': entry_price,
                'exit_price': current_price,
                'profit_dollars': profit_dollars,
                'profit_pct': profit_pct,
                'exit_reason': reason,
                'entry_time': entry_time,
                'exit_time': exit_time,
                'duration_minutes': duration_minutes,
                'entry_rsi': entry_rsi,
                'entry_adx': entry_adx,
                'entry_macd': entry_macd,
                'entry_trend': entry_trend,
                'entry_volume_ratio': entry_vol_ratio,
                'entry_vwap': entry_vwap,
                'entry_bb_upper': entry_bb_upper,
                'entry_bb_lower': entry_bb_lower,
                'entry_support': entry_support,
                'entry_resistance': entry_resistance,
                'entry_comprehensive_score': entry_score,
                'entry_comprehensive_grade': entry_grade,
                'close_rsi': close_rsi,
                'close_adx': close_adx,
                'close_macd': close_macd,
                'close_trend': close_trend,
                'close_volume_ratio': close_vol_ratio,
                'close_vwap': close_vwap,
                'close_bb_upper': close_bb_upper,
                'close_bb_lower': close_bb_lower,
                'close_support': close_support,
                'close_resistance': close_resistance,
                'close_comprehensive_score': close_score,
                'close_comprehensive_grade': close_grade,
                'sl_price': open_trade.get('sl', 0),
                'tp_price': open_trade.get('tp', 0),
                'rr': rr,
                'confidence': open_trade.get('confidence', 70) if open_trade.get('confidence') is not None else None,
                'full_entry_analysis': full_entry_analysis,
                'full_exit_analysis': full_exit_analysis,
                'warnings_sent': open_trade.get('warnings_sent', []),
                'recommendations_sent': open_trade.get('recommendations_sent', [])
            }
            
            logger.info(f"📤 [close_trade_virtual] حفظ الصفقة المغلقة {trade_id} في قواعد التعلم...")
            learning_saved = save_trade_to_learning(trade_full_data)
            if learning_saved:
                logger.info(f"✅ [close_trade_virtual] تم حفظ الصفقة {trade_id} في قواعد التعلم")
            else:
                logger.error(f"❌ [close_trade_virtual] فشل حفظ الصفقة {trade_id} في قواعد التعلم")
                queue_telegram_message(f"⚠️ تحذير: فشل حفظ الصفقة {trade_id} في قواعد التعلم. سيتم حفظها محلياً.")
            
            # ── 6. استخلاص الدروس والتعلم من التحليل الشامل (باستخدام LearningOrchestrator من PART 30) ──
            logger.info(f"🧠 [close_trade_virtual] استخلاص الدروس من الصفقة {trade_id}")
            process_trade_for_learning(trade_full_data, asset_type, silent=True)
            
            # ── 7. ✅ اكتشاف الأنماط مباشرة بعد حفظ الصفقة (بدون تأخير) ──
            try:
                logger.info(f"🔍 [close_trade_virtual] بدء اكتشاف الأنماط لـ {asset_type} بعد إغلاق الصفقة {trade_id}")
                discover_patterns_from_trades(asset_type)
                logger.info(f"✅ [close_trade_virtual] تم اكتشاف الأنماط لـ {asset_type}")
            except Exception as e:
                logger.error(f"❌ [close_trade_virtual] فشل اكتشاف الأنماط لـ {asset_type}: {e}")
            
            # ── 8. Post-Mortem للصفقات الخاسرة ──
            if POST_MORTEM_AVAILABLE and POST_MORTEM and profit_dollars < 0:
                try:
                    post_mortem_data = {
                        'profit_dollars': profit_dollars,
                        'entry_price': entry_price,
                        'exit_price': current_price,
                        'entry_rsi': entry_rsi,
                        'entry_adx': entry_adx,
                        'entry_trend': entry_trend,
                        'sl_price': open_trade.get('sl', 0),
                        'tp_price': open_trade.get('tp', 0),
                        'duration_minutes': duration_minutes,
                        'exit_reason': reason,
                        'manual_close': reason in ["أمر يدوي من المستخدم", "أمر يدوي من الزر"],
                        'trade_type': trade_type,
                        'rr': rr,
                        'full_entry_analysis': full_entry_analysis,
                        'full_exit_analysis': full_exit_analysis
                    }
                    analysis_result = POST_MORTEM.analyze(post_mortem_data)
                    
                    # ✅ دمج دروس Post-Mortem في نظام التعلم الموحد
                    if analysis_result and analysis_result.get('lessons'):
                        try:
                            post_mortem_saved = save_post_mortem_lessons(analysis_result, asset_type, trade_id)
                            if post_mortem_saved:
                                logger.info(f"🧠 [close_trade_virtual] تم دمج دروس Post-Mortem للصفقة {trade_id} في نظام التعلم الموحد")
                            else:
                                logger.warning(f"⚠️ [close_trade_virtual] فشل دمج دروس Post-Mortem للصفقة {trade_id}")
                        except Exception as e:
                            logger.error(f"❌ [close_trade_virtual] فشل حفظ دروس Post-Mortem: {e}")
                    
                    if PROMETHEUS_AVAILABLE and PROMETHEUS:
                        for lesson in analysis_result.get('lessons', [])[:3]:
                            try:
                                PROMETHEUS.record_lesson(lesson)
                            except:
                                pass
                    
                    # ── ✅ بناء تحليل الصفقة الخاسرة ──
                    asset_label = "النفط" if asset_type == "oil" else "الفضة"
                    trade_type_ar = "شراء" if trade_type == "BUY" else "بيع"
                    
                    # تحديد الأسباب الرئيسية للخسارة
                    main_reasons = []
                    if entry_adx is not None and entry_adx < 20:
                        main_reasons.append(f"- ضعف قوة الاتجاه (ADX: {entry_adx:.0f}) عند الدخول، مما يعني أن السوق كان عرضياً دون اتجاه واضح.")
                    if trade_type == "BUY" and entry_macd is not None and entry_macd < 0:
                        main_reasons.append(f"- كان مؤشر MACD سالباً عند الدخول ({entry_macd:.3f}) مما يشير إلى ضعف الزخم الصاعد.")
                    if trade_type == "SELL" and entry_macd is not None and entry_macd > 0:
                        main_reasons.append(f"- كان مؤشر MACD موجباً عند الدخول ({entry_macd:.3f}) مما يشير إلى ضعف الزخم الهابط.")
                    if entry_vol_ratio is not None and entry_vol_ratio < 0.7:
                        main_reasons.append(f"- حجم التداول كان منخفضاً عند الدخول ({entry_vol_ratio:.1f}x) مما يشير إلى ضعف المشاركة.")
                    if "Stop Loss" in reason or "SL" in reason:
                        main_reasons.append(f"- تم ضرب وقف الخسارة عند ${fmt_price(sl, asset_type)}.")
                        if rr < 1.5:
                            main_reasons.append(f"- نسبة المخاطرة إلى المكافأة منخفضة ({rr:.2f}:1).")
                    if entry_score is not None and entry_score < 45:
                        main_reasons.append(f"- التقييم الشامل كان ضعيفاً عند الدخول ({entry_score:.0f}%).")
                    
                    if full_entry_analysis:
                        timeframes = full_entry_analysis.get('timeframes', {})
                        bullish_count = sum(1 for tf, data in timeframes.items() if data.get('trend') == 'صاعد')
                        if trade_type == "SELL" and bullish_count >= 3:
                            main_reasons.append(f"- كان {bullish_count} من أصل 4 فريمات زمنية صاعدة عند الدخول، مما يعاكس صفقة البيع.")
                        elif trade_type == "BUY" and (4 - bullish_count) >= 3:
                            main_reasons.append(f"- كان {4 - bullish_count} من أصل 4 فريمات زمنية هابطة عند الدخول، مما يعاكس صفقة الشراء.")
                    
                    # ── بناء الرسالة ──
                    msg = f"🧠 **تحليل الصفقة الخاسرة - {asset_label}**\n"
                    msg += "━" * 50 + "\n\n"
                    
                    # معلومات الصفقة
                    msg += f"📊 **نوع الصفقة:** {trade_type_ar}\n"
                    msg += f"💰 **سعر الدخول:** ${fmt_price(entry_price, asset_type)}\n"
                    msg += f"💰 **سعر الخروج:** ${fmt_price(current_price, asset_type)}\n"
                    msg += f"📉 **الخسارة:** ${abs(profit_dollars):.2f} ({profit_pct:+.2f}%)\n"
                    msg += f"📌 **سبب الإغلاق:** {'ضرب وقف الخسارة' if 'Stop Loss' in reason or 'SL' in reason else 'خروج اضطراري' if 'تحذير' in reason else reason}\n"
                    msg += f"🛡️ **وقف الخسارة:** ${fmt_price(sl, asset_type)}\n"
                    msg += f"🎯 **الهدف:** ${fmt_price(tp, asset_type)}\n"
                    msg += f"📊 **مدة الصفقة:** {duration_minutes} دقيقة\n\n"
                    
                    # الأسباب الرئيسية
                    msg += "🔍 **الأسباب الرئيسية للخسارة:**\n"
                    if main_reasons:
                        for r in main_reasons[:4]:
                            msg += f"   {r}\n"
                    else:
                        msg += "   • لا توجد أسباب فنية واضحة. قد تكون الخسارة نتيجة تقلبات السوق العامة.\n"
                    msg += "\n"
                    
                    # مقارنة المؤشرات
                    msg += "📊 **مقارنة المؤشرات الفنية (دخول → خروج):**\n"
                    msg += f"   • RSI: {entry_rsi if entry_rsi is not None else 'غير متوفر'} → {close_rsi if close_rsi is not None else 'غير متوفر'}\n"
                    msg += f"   • ADX: {entry_adx if entry_adx is not None else 'غير متوفر'} → {close_adx if close_adx is not None else 'غير متوفر'}\n"
                    msg += f"   • MACD: {entry_macd if entry_macd is not None else 'غير متوفر'} → {close_macd if close_macd is not None else 'غير متوفر'}\n"
                    msg += f"   • الاتجاه العام: {entry_trend if entry_trend is not None else 'غير متوفر'} → {close_trend if close_trend is not None else 'غير متوفر'}\n"
                    msg += f"   • حجم التداول: {entry_vol_ratio if entry_vol_ratio is not None else 'غير متوفر'} → {close_vol_ratio if close_vol_ratio is not None else 'غير متوفر'}\n"
                    msg += f"   • VWAP: ${fmt_price(entry_vwap, asset_type) if entry_vwap is not None else 'غير متوفر'} → ${fmt_price(close_vwap, asset_type) if close_vwap is not None else 'غير متوفر'}\n"
                    
                    if entry_bb_upper is not None and entry_bb_lower is not None and close_bb_upper is not None and close_bb_lower is not None:
                        bb_entry_pos = ((entry_price - entry_bb_lower) / (entry_bb_upper - entry_bb_lower) * 100) if (entry_bb_upper - entry_bb_lower) > 0 else 50
                        bb_close_pos = ((current_price - close_bb_lower) / (close_bb_upper - close_bb_lower) * 100) if (close_bb_upper - close_bb_lower) > 0 else 50
                        msg += f"   • Bollinger Bands: {bb_entry_pos:.0f}% → {bb_close_pos:.0f}% من النطاق\n"
                    else:
                        msg += "   • Bollinger Bands: غير متوفر\n"
                    
                    msg += f"   • الدعم: {fmt_price(entry_support, asset_type) if entry_support is not None else 'غير متوفر'} → {fmt_price(close_support, asset_type) if close_support is not None else 'غير متوفر'}\n"
                    msg += f"   • المقاومة: {fmt_price(entry_resistance, asset_type) if entry_resistance is not None else 'غير متوفر'} → {fmt_price(close_resistance, asset_type) if close_resistance is not None else 'غير متوفر'}\n"
                    msg += f"   • التقييم الشامل: {entry_score if entry_score is not None else 'غير متوفر'}% → {close_score if close_score is not None else 'غير متوفر'}%\n"
                    msg += "\n"
                    
                    # الدروس المستفادة
                    lessons_list = []
                    if entry_adx is not None and entry_adx < 20:
                        lessons_list.append("تجنب الدخول عندما يكون ADX أقل من 20 (ضعف الاتجاه).")
                    if trade_type == "BUY" and entry_macd is not None and entry_macd < 0:
                        lessons_list.append("تأكد من أن MACD موجب قبل الشراء.")
                    if trade_type == "SELL" and entry_macd is not None and entry_macd > 0:
                        lessons_list.append("تأكد من أن MACD سالب قبل البيع.")
                    if entry_vol_ratio is not None and entry_vol_ratio < 0.7:
                        lessons_list.append("انتظر حتى يرتفع حجم التداول قبل الدخول.")
                    if entry_rsi is not None and entry_rsi > 70 and trade_type == "BUY":
                        lessons_list.append("تجنب الشراء عندما يكون RSI فوق 70 (ذروة شراء).")
                    if entry_rsi is not None and entry_rsi < 30 and trade_type == "SELL":
                        lessons_list.append("تجنب البيع عندما يكون RSI تحت 30 (ذروة بيع).")
                    if "Stop Loss" in reason and rr < 1.5:
                        lessons_list.append("استهدف نسبة مخاطرة/مكافأة لا تقل عن 2:1.")
                    
                    if lessons_list:
                        msg += "📚 **الدروس المستفادة:**\n"
                        for lesson in lessons_list[:3]:
                            msg += f"   • {lesson}\n"
                        msg += "\n"
                    
                    # التوصيات
                    recommendations = []
                    if entry_adx is not None and entry_adx < 20:
                        recommendations.append("أضف شرط ADX > 20 كمرشح للدخول.")
                    if trade_type == "BUY" and entry_macd is not None and entry_macd < 0:
                        recommendations.append("استخدم MACD كمرشح: لا تشتري إلا إذا كان MACD موجباً.")
                    if trade_type == "SELL" and entry_macd is not None and entry_macd > 0:
                        recommendations.append("استخدم MACD كمرشح: لا تبيع إلا إذا كان MACD سالباً.")
                    if entry_vol_ratio is not None and entry_vol_ratio < 0.7:
                        recommendations.append("أضف شرطاً لحجم التداول: لا تدخل إذا كان الحجم أقل من 0.7x.")
                    if entry_score is not None and entry_score < 45:
                        recommendations.append("حسّن معايير الدخول بحيث لا تقبل إلا الصفقات ذات التقييم الشامل > 55%.")
                    
                    if recommendations:
                        msg += "💡 **توصيات للتحسين:**\n"
                        for rec in recommendations[:3]:
                            msg += f"   • {rec}\n"
                        msg += "\n"
                    
                    msg += "💙 **تولين:** الخسارة جزء من التداول. تعلم من هذه الصفقة وطبّق الدروس في الصفقات القادمة.\n"
                    msg += "━" * 50
                    
                    queue_telegram_message(msg)
                    
                except Exception as e:
                    logger.error(f"❌ فشل تحليل ما بعد الصفقة: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            
        except Exception as e:
            logger.error(f"❌ فشل حفظ الصفقة في قواعد التعلم: {e}")
            import traceback
            logger.error(traceback.format_exc())
            queue_telegram_message(f"⚠️ تحذير: حدث خطأ أثناء حفظ الصفقة في قواعد التعلم: {str(e)[:100]}")

        # ── 9. 🧠 إغلاق حلقة التعلم: ربط نتيجة الصفقة بالتوقع المسبق ──
        try:
            actual_outcome = "win" if profit_dollars > 0 else "loss" if profit_dollars < 0 else "breakeven"
            update_prediction_result(trade_id, actual_outcome, profit_dollars, current_price)
            update_prediction_calibration()
            if ADAPTIVE_ENGINE is not None:
                try:
                    cal = ADAPTIVE_ENGINE.calibration(asset_type)
                    logger.info(f"🧠 [Calibration] {asset_type}: {cal}")
                except Exception as e:
                    logger.warning(f"⚠️ فشل قراءة معايرة التعلم التراكمي: {e}")
        except Exception as e:
            logger.error(f"❌ فشل إغلاق حلقة التوقع/التعلم: {e}")

        # ── 11. إرسال رسالة الإغلاق للمستخدم ──
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        msg = f"✅ **تم إغلاق صفقة {asset_label}**\n"
        msg += f"📊 سعر الدخول: ${fmt_price(entry_price, asset_type)}\n"
        msg += f"📊 سعر الخروج: ${fmt_price(current_price, asset_type)}\n"
        msg += f"📊 النتيجة: {AccountingSystem.format_profit(profit_dollars)}\n"
        msg += f"📌 سبب الإغلاق: {reason}"
        if not learning_saved:
            msg += "\n\n⚠️ تنبيه: الصفقة لم تُحفظ في قواعد التعلم (تم حفظها محلياً)."

        queue_telegram_message(msg)
        logger.info(f"✅ تم إغلاق صفقة {asset_type} بنجاح")
        return True

def close_trade_manually(asset_type, reason="أمر يدوي"):
    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        queue_telegram_message(f"❌ لا توجد صفقة {asset_type} مفتوحة للإغلاق.")
        return False
    return close_trade_virtual(asset_type, reason)

# ====================================================================================
# نهاية PART 20
# ====================================================================================

# ====================================================================================
# 📦 PART 21: نظام التحذيرات الذكي (V5.4 - تحذيرات تفسيرية + تحسين Memory Warning)
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. إصلاح منطق تحذير VWAP: استخدام النسبة المئوية بدلاً من القيم المطلقة.
#   2. رفع عتبات التحذير لتجنب التنبيهات المزعجة.
#   3. تحسين استخراج القيم في _extract_analysis_state (خاصة MACD).
#   4. تحسين دقة الرسائل التفسيرية في _format_warning_message.
#   5. إضافة تحقق من صحة القيم قبل الحساب.
#   6. تحسين Memory Warning: مقارنة مع الرابح والخاسر معاً.
#   7. ✅ [إصلاح] استخراج MACD من المكان الصحيح (timeframes["15m"]["macd"] أو indicators.momentum.macd_hist).
#   8. ✅ [إصلاح] إضافة حفظ إلزامي لـ open_trade في نهاية check_trend_reversal_warnings.
# ====================================================================================

import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# ثوابت التحذيرات
# ============================================================================

WARNING_LEVELS = {
    "trend_reversal": {
        1: {"label": "تحذير من المستوى الأول", "emoji": "⚠️", "action": "notify"},
        2: {"label": "تحذير من المستوى الثاني", "emoji": "🔴", "action": "notify"},
        3: {"label": "تحذير من المستوى الثالث والأخير", "emoji": "🚨", "action": "close"}
    },
    "memory_warning": {
        1: {"label": "تذكير بالذاكرة", "emoji": "🧠", "action": "notify"}
    }
}

# ============================================================================
# دوال مساعدة لـ Memory Warning (جلب اللقطات حسب النتيجة)
# ============================================================================

def _get_snapshots_by_outcome(asset_type: str, is_winning: bool, limit: int = 30) -> List[Dict]:
    """جلب اللقطات من الصفقات الرابحة أو الخاسرة حسب المعامل"""
    snapshots = []
    if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
        return snapshots
    
    try:
        client = _get_supabase_client()
        if not client:
            return snapshots
        
        condition = 'gt' if is_winning else 'lt'
        trades_query = client.table('trades_full')\
            .select('trade_id')\
            .eq('asset_type', asset_type)\
            .filter('profit_dollars', condition, 0)\
            .limit(limit)
        trades_response = trades_query.execute()
        if not trades_response or not hasattr(trades_response, 'data') or not trades_response.data:
            return snapshots
        
        trade_ids = [t.get('trade_id') for t in trades_response.data if t.get('trade_id')]
        if not trade_ids:
            return snapshots
        
        snapshots_query = client.table('snapshots')\
            .select('*')\
            .in_('trade_id', trade_ids)\
            .order('timestamp', desc=True)\
            .limit(limit)
        snapshots_response = snapshots_query.execute()
        if snapshots_response and hasattr(snapshots_response, 'data'):
            snapshots = snapshots_response.data
            logger.info(f"📊 [MemoryWarning] تم جلب {len(snapshots)} لقطة من {'رابحة' if is_winning else 'خاسرة'} لـ {asset_type}")
    except Exception as e:
        logger.warning(f"⚠️ [MemoryWarning] فشل جلب اللقطات من Supabase: {e}")
    
    return snapshots

def _calculate_avg_indicators(snapshots: List[Dict]) -> Dict:
    """حساب متوسط المؤشرات من قائمة اللقطات"""
    if not snapshots:
        return {'rsi': 50, 'adx': 20, 'macd': 0, 'vol_ratio': 1.0, 'trend': 'محايد'}
    
    total_rsi, total_adx, total_macd, total_vol = 0, 0, 0, 0
    count = 0
    trend_count = {}
    
    for snap in snapshots:
        rsi = snap.get('rsi', 0)
        adx = snap.get('adx', 0)
        macd = snap.get('macd', 0)
        vol = snap.get('volume_ratio', 0)
        trend = snap.get('trend', 'محايد')
        
        if rsi > 0 and adx > 0:
            total_rsi += rsi
            total_adx += adx
            total_macd += macd
            total_vol += vol
            trend_count[trend] = trend_count.get(trend, 0) + 1
            count += 1
    
    if count == 0:
        return {'rsi': 50, 'adx': 20, 'macd': 0, 'vol_ratio': 1.0, 'trend': 'محايد'}
    
    most_common_trend = max(trend_count, key=trend_count.get) if trend_count else 'محايد'
    
    return {
        'rsi': total_rsi / count,
        'adx': total_adx / count,
        'macd': total_macd / count,
        'vol_ratio': total_vol / count,
        'trend': most_common_trend
    }

def _calculate_similarity(current_rsi, current_adx, current_macd, current_vol_ratio, current_trend, avg_indicators: Dict) -> float:
    """حساب درجة التشابه بين المؤشرات الحالية والمتوسط"""
    if not avg_indicators:
        return 0.0
    
    similarity = 0
    total_weight = 0
    
    # RSI (وزن 30%)
    if abs(current_rsi - avg_indicators.get('rsi', 50)) < 10:
        similarity += 0.3
    total_weight += 0.3
    
    # ADX (وزن 20%)
    if abs(current_adx - avg_indicators.get('adx', 20)) < 10:
        similarity += 0.2
    total_weight += 0.2
    
    # MACD (وزن 20%) - ✅ تم إصلاح: استخدام macd
    if abs(current_macd - avg_indicators.get('macd', 0)) < 0.5:
        similarity += 0.2
    total_weight += 0.2
    
    # الحجم (وزن 15%)
    if abs(current_vol_ratio - avg_indicators.get('vol_ratio', 1.0)) < 0.3:
        similarity += 0.15
    total_weight += 0.15
    
    # الاتجاه (وزن 15%)
    if current_trend == avg_indicators.get('trend', 'محايد'):
        similarity += 0.15
    total_weight += 0.15
    
    return (similarity / total_weight) * 100 if total_weight > 0 else 0

# ============================================================================
# دوال مساعدة (منع التكرار، التسجيل، الحفظ)
# ============================================================================

def should_send_warning(open_trade, warning_type, level):
    warnings_sent = open_trade.get("warnings_sent", [])
    for w in warnings_sent:
        if w.get("type") == warning_type and w.get("level") == level:
            return False
    return True

def record_warning(open_trade, warning_type, level, current_price, message):
    if "warnings_sent" not in open_trade:
        open_trade["warnings_sent"] = []
    open_trade["warnings_sent"].append({
        "type": warning_type,
        "level": level,
        "sent_at": datetime.now().isoformat(),
        "price_at": current_price,
        "message": message[:200]
    })
    asset_type = open_trade.get("asset_type", "oil")
    pos_file = get_position_file(asset_type)
    try:
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(open_trade, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"❌ فشل تسجيل التحذير: {e}")

def _save_open_trade(asset_type, open_trade):
    pos_file = get_position_file(asset_type)
    try:
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(open_trade, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"❌ فشل حفظ حالة الصفقة: {e}")

def _extract_analysis_state(analysis):
    if not analysis:
        return {}
    state = {
        "timeframes": {},
        "comprehensive_score": 50,
        "rsi": 50,
        "adx": 20,
        "macd": 0,
        "supertrend_trend": 1,
        "price": analysis.get("price", 0),
        "volume_ratio": 1.0,
        "support": 0,
        "resistance": 0,
        "vwap": 0
    }
    tfs = analysis.get("timeframes", {})
    for tf in ["5m", "15m", "1h", "4h"]:
        if tf in tfs and isinstance(tfs.get(tf), dict):
            state["timeframes"][tf] = tfs[tf].get("trend", "محايد")
    comp = analysis.get("comprehensive_score", {})
    state["comprehensive_score"] = comp.get("score", 50)
    tf_15m = tfs.get("15m", {})
    state["rsi"] = tf_15m.get("rsi", 50)
    state["adx"] = tf_15m.get("adx", 20)
    # ✅ إصلاح: استخراج MACD من tf_15m أولاً، ثم من indicators.momentum.macd_hist
    state["macd"] = tf_15m.get("macd", 0)
    if state["macd"] == 0:
        indicators = analysis.get("indicators", {})
        momentum = indicators.get("momentum", {})
        state["macd"] = momentum.get("macd_hist", 0)
    state["volume_ratio"] = tf_15m.get("volume_ratio", 1.0)
    st = analysis.get("supertrend", {})
    state["supertrend_trend"] = st.get("trend", 1)
    indicators = analysis.get("indicators", {})
    sr = indicators.get("support_resistance", {})
    state["support"] = sr.get("s1", 0)
    state["resistance"] = sr.get("r1", 0)
    state["vwap"] = tf_15m.get("vwap", 0)
    if state["vwap"] == 0:
        state["vwap"] = analysis.get("vwap", 0)
    return state

# ============================================================================
# دالة تنسيق التحذير التفسيري (معدلة - إصلاح MACD)
# ============================================================================

def _format_warning_message(asset_type, level, current_analysis, open_trade, reasons, level_label):
    asset_label = "النفط" if asset_type == "oil" else "الفضة"
    current_price = current_analysis.get("price", 0)
    entry_price = open_trade.get("entry_price", 0)
    sl = open_trade.get("sl", 0)
    tp = open_trade.get("tp", 0)
    
    indicators = current_analysis.get("indicators", {})
    momentum = indicators.get("momentum", {})
    trend_data = indicators.get("trend", {})
    volatility = indicators.get("volatility", {})
    volume = indicators.get("volume", {})
    sr = indicators.get("support_resistance", {})
    
    # ✅ إصلاح: استخراج MACD من المكان الصحيح
    rsi = momentum.get("rsi", 50)
    adx = trend_data.get("adx", 20)
    macd = momentum.get("macd_hist", 0)
    # إذا كان macd_hist صفراً، حاول من timeframes
    if macd == 0:
        tfs = current_analysis.get("timeframes", {})
        tf_15m = tfs.get("15m", {})
        macd = tf_15m.get("macd", 0)
    vol_ratio = volume.get("ratio", 1.0)
    vwap_dev = volatility.get("vwap_deviation", 0)
    bb_pos = volatility.get("bb_position", 0.5)
    current_trend = trend_data.get("current_trend", "محايد")
    
    interpretations = []
    
    if rsi > 70:
        interpretations.append(f"📈 RSI في منطقة ذروة شراء ({rsi:.0f}) - قد يكون هناك تصحيح هابط قريب.")
    elif rsi < 30:
        interpretations.append(f"📉 RSI في منطقة ذروة بيع ({rsi:.0f}) - قد يكون هناك ارتداد صاعد قريب.")
    elif rsi > 60:
        interpretations.append(f"📈 RSI مرتفع نسبياً ({rsi:.0f}) - زخم صاعد ولكن حذر من التصحيح.")
    elif rsi < 40:
        interpretations.append(f"📉 RSI منخفض نسبياً ({rsi:.0f}) - زخم هابط ولكن قد يكون هناك ارتداد.")
    else:
        interpretations.append(f"⚖️ RSI محايد ({rsi:.0f}) - لا يوجد زخم قوي.")
    
    if adx > 40:
        interpretations.append(f"💪 اتجاه قوي جداً (ADX: {adx:.0f}) - الحركة مدعومة بقوة.")
    elif adx > 25:
        interpretations.append(f"📊 اتجاه واضح (ADX: {adx:.0f}) - يمكن الاعتماد على الاتجاه الحالي.")
    elif adx > 20:
        interpretations.append(f"🔀 اتجاه ضعيف (ADX: {adx:.0f}) - السوق في نطاق عرضي.")
    else:
        interpretations.append(f"🌀 لا يوجد اتجاه (ADX: {adx:.0f}) - تجنب الدخول في هذه الظروف.")
    
    # ✅ إصلاح: استخدام macd الصحيح في التفسير
    if macd > 0.0005:
        interpretations.append(f"🟢 MACD إيجابي ({macd:.4f}) - زخم صاعد.")
    elif macd < -0.0005:
        interpretations.append(f"🔴 MACD سلبي ({macd:.4f}) - زخم هابط.")
    else:
        interpretations.append(f"⚪ MACD محايد ({macd:.4f}) - لا زخم واضح.")
    
    if vol_ratio > 2.0:
        interpretations.append(f"🔥 حجم تداول استثنائي ({vol_ratio:.1f}x) - حركة قوية ومدعومة.")
    elif vol_ratio > 1.5:
        interpretations.append(f"📊 حجم مرتفع ({vol_ratio:.1f}x) - تأكيد جيد للحركة.")
    elif vol_ratio > 0.7:
        interpretations.append(f"📊 حجم طبيعي ({vol_ratio:.1f}x) - لا توجد إشارة قوية.")
    elif vol_ratio > 0.3:
        interpretations.append(f"📉 حجم منخفض ({vol_ratio:.1f}x) - الحركة ضعيفة وغير موثوقة.")
    else:
        interpretations.append(f"⚠️ حجم جاف جداً ({vol_ratio:.1f}x) - تجنب التداول في هذه الظروف.")
    
    if abs(vwap_dev) > 1.5:
        if vwap_dev > 0:
            interpretations.append(f"📈 السعر أعلى من VWAP بنسبة {vwap_dev:.2f}% - قد يكون مبالغاً فيه.")
        else:
            interpretations.append(f"📉 السعر أقل من VWAP بنسبة {abs(vwap_dev):.2f}% - قد يكون مقوّماً بأقل من قيمته.")
    else:
        interpretations.append(f"⚖️ السعر قريب من VWAP ({vwap_dev:+.2f}%) - سعر عادل.")
    
    if bb_pos > 0.8:
        interpretations.append(f"📈 السعر قرب الحد العلوي لبولينجر - منطقة مقاومة محتملة.")
    elif bb_pos < 0.2:
        interpretations.append(f"📉 السعر قرب الحد السفلي لبولينجر - منطقة دعم محتملة.")
    else:
        interpretations.append(f"⚖️ السعر في منتصف نطاق بولينجر - لا توجد إشارة.")
    
    if current_trend == "صاعد":
        interpretations.append(f"📈 الاتجاه العام: صاعد - الزخم إيجابي.")
    elif current_trend == "هابط":
        interpretations.append(f"📉 الاتجاه العام: هابط - الزخم سلبي.")
    else:
        interpretations.append(f"➖ الاتجاه العام: محايد - لا يوجد اتجاه واضح.")
    
    lines = []
    lines.append(f"{WARNING_LEVELS['trend_reversal'][level]['emoji']} **{level_label} - {asset_label}**")
    lines.append("")
    lines.append("📊 **تحليل المؤشرات:**")
    for interp in interpretations[:5]:
        lines.append(f"   {interp}")
    lines.append("")
    
    lines.append("💰 **معلومات الصفقة:**")
    profit_pct = (((current_price - entry_price) / entry_price * 100) if trade_type == "BUY" else ((entry_price - current_price) / entry_price * 100)) if entry_price != 0 else 0
    profit_emoji = "✅" if profit_pct > 0 else "❌" if profit_pct < 0 else "⚪"
    lines.append(f"   {profit_emoji} الربح/الخسارة الحالية: {profit_pct:+.2f}% (منذ الدخول)")
    lines.append(f"   • سعر الدخول: ${fmt_price(entry_price, asset_type)}")
    lines.append(f"   • السعر الحالي: ${fmt_price(current_price, asset_type)}")
    if sl > 0:
        lines.append(f"   • المسافة للوقف: {abs(current_price - sl) / entry_price * 100:.2f}%")
    if tp > 0:
        lines.append(f"   • المسافة للهدف: {abs(tp - current_price) / entry_price * 100:.2f}%")
    lines.append("")
    
    lines.append("🔍 **أسباب التحذير:**")
    for reason in reasons[:3]:
        lines.append(f"   • {reason}")
    lines.append("")
    
    if level == 3:
        lines.append("🚨 **توصية تولين:** أنصح بشدة بإغلاق الصفقة فوراً لحماية رأس المال.")
    elif level == 2:
        lines.append("💡 **توصية تولين:** راقب الصفقة عن كثب، قد تحتاج للإغلاق قريباً.")
    else:
        lines.append("💡 **توصية تولين:** كن حذراً، هناك تغير طفيف في الاتجاه. أنصح بتضييق وقف الخسارة.")
    
    lines.append("")
    lines.append("💙 تولين: أنا هنا لمساعدتك في اتخاذ القرار المناسب.")
    
    return "\n".join(lines)

# ============================================================================
# 1. تحذير الاقتراب من وقف الخسارة
# ============================================================================

def check_distance_warning(asset_type, current_price, open_trade):
    if not open_trade:
        return
    entry_price = open_trade.get("entry_price", current_price)
    sl = open_trade.get("sl", entry_price)
    total_distance = abs(entry_price - sl)
    if total_distance == 0:
        return
    current_distance = abs(current_price - sl)
    distance_pct = current_distance / total_distance
    if distance_pct <= 0.33:
        if should_send_warning(open_trade, "distance_sl", 1):
            asset_label = "النفط" if asset_type == "oil" else "الفضة"
            msg = f"⚠️ **تحذير:** صفقة {asset_label} تقترب من وقف الخسارة!\n"
            msg += f"💰 السعر الحالي: ${fmt_price(current_price, asset_type)} | وقف الخسارة: ${fmt_price(sl, asset_type)}\n"
            msg += f"📉 المسافة المتبقية: {distance_pct*100:.1f}%\n"
            msg += "\n💡 **توصية تولين:** راقب الصفقة عن كثب، قد تحتاج للإغلاق."
            queue_telegram_message(msg)
            record_warning(open_trade, "distance_sl", 1, current_price, msg)

            try:
                send_warning_func = globals().get('send_warning_to_app')
                if send_warning_func:
                    send_warning_func(asset_type, "SL_APPROACH", msg, current_price)
                    logger.info(f"📱 [WebSocket] تم إرسال تحذير SL_APPROACH لـ {asset_type} إلى التطبيق")
                else:
                    logger.warning(f"⚠️ [WebSocket] send_warning_to_app غير متوفرة")
            except Exception as e:
                logger.error(f"❌ [WebSocket] فشل إرسال تحذير SL_APPROACH: {e}")

# ============================================================================
# 2. تحذير انعكاس الاتجاه (3 مستويات) - مع إصلاح حفظ last_analysis
# ============================================================================

def check_trend_reversal_warnings(asset_type, current_analysis, open_trade):
    if not open_trade or not current_analysis:
        return
    last_state = open_trade.get("last_analysis", {})
    if not last_state:
        open_trade["last_analysis"] = _extract_analysis_state(current_analysis)
        _save_open_trade(asset_type, open_trade)
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

    def safe_pct_change(prev, curr, default=0):
        if prev is None or curr is None or prev == 0:
            return default
        return ((curr - prev) / abs(prev)) * 100

    rsi_change = curr_rsi - prev_rsi
    adx_change = curr_adx - prev_adx
    macd_change = curr_macd - prev_macd
    vwap_pct_change = safe_pct_change(prev_vwap, curr_vwap)
    vol_change = curr_vol - prev_vol
    score_change = curr_score - prev_score

    changed_frames = []
    for tf in ["5m", "15m", "1h", "4h"]:
        if tf in prev_trends and tf in curr_trends:
            if prev_trends[tf] != curr_trends[tf]:
                changed_frames.append(tf)
    changed_count = len(changed_frames)

    level = 0
    reasons = []

    if abs(rsi_change) > 15:
        direction = "ارتفاع" if rsi_change > 0 else "انخفاض"
        reasons.append(f"📈 تغير حاد في RSI: {direction} بمقدار {abs(rsi_change):.1f} نقطة (دلالة على تغير في الزخم).")
        level = max(level, 2)
    elif abs(rsi_change) > 8:
        direction = "ارتفاع" if rsi_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير ملحوظ في RSI: {direction} بمقدار {abs(rsi_change):.1f} نقطة.")
        level = max(level, 1)

    if abs(adx_change) > 10:
        direction = "ارتفاع" if adx_change > 0 else "انخفاض"
        reasons.append(f"💪 تغير حاد في قوة الاتجاه (ADX): {direction} بمقدار {abs(adx_change):.1f} نقطة.")
        level = max(level, 2)
    elif abs(adx_change) > 5:
        direction = "ارتفاع" if adx_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير ملحوظ في قوة الاتجاه (ADX): {direction} بمقدار {abs(adx_change):.1f} نقطة.")
        level = max(level, 1)

    # ✅ إصلاح: استخدام curr_macd و prev_macd الصحيحين
    if abs(macd_change) > 0.5:
        direction = "إيجابي" if macd_change > 0 else "سلبي"
        reasons.append(f"📊 تغير حاد في MACD: أصبح {direction} بمقدار {abs(macd_change):.3f}.")
        level = max(level, 2)
    elif abs(macd_change) > 0.1:
        direction = "إيجابي" if macd_change > 0 else "سلبي"
        reasons.append(f"📊 تغير ملحوظ في MACD: أصبح {direction} بمقدار {abs(macd_change):.3f}.")
        level = max(level, 1)

    if abs(vwap_pct_change) > 1.0:
        direction = "ارتفاع" if vwap_pct_change > 0 else "انخفاض"
        reasons.append(f"💰 تغير ملحوظ في VWAP: {direction} بنسبة {abs(vwap_pct_change):.2f}% (قد يشير إلى تغير في القيمة العادلة).")
        level = max(level, 2)
    elif abs(vwap_pct_change) > 0.5:
        direction = "ارتفاع" if vwap_pct_change > 0 else "انخفاض"
        reasons.append(f"💰 تغير طفيف في VWAP: {direction} بنسبة {abs(vwap_pct_change):.2f}%.")
        level = max(level, 1)

    if abs(vol_change) > 0.5:
        direction = "ارتفاع" if vol_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير حاد في حجم التداول: {direction} بمقدار {abs(vol_change):.1f}x.")
        level = max(level, 2)
    elif abs(vol_change) > 0.2:
        direction = "ارتفاع" if vol_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير ملحوظ في حجم التداول: {direction} بمقدار {abs(vol_change):.1f}x.")
        level = max(level, 1)

    if abs(score_change) > 10:
        direction = "ارتفاع" if score_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير حاد في التقييم الشامل: {direction} بمقدار {abs(score_change):.1f}%.")
        level = max(level, 2)
    elif abs(score_change) > 5:
        direction = "ارتفاع" if score_change > 0 else "انخفاض"
        reasons.append(f"📊 تغير ملحوظ في التقييم الشامل: {direction} بمقدار {abs(score_change):.1f}%.")
        level = max(level, 1)

    if changed_count >= 2:
        reasons.append(f"🔄 تغير اتجاه في {changed_count} فريمات ({', '.join(changed_frames)}) - قد يكون انعكاساً.")
        level = max(level, 2 if changed_count >= 3 else 1)

    # تحديث last_analysis دائماً
    open_trade["last_analysis"] = current_state

    if level == 0:
        _save_open_trade(asset_type, open_trade)
        return

    if not should_send_warning(open_trade, "trend_reversal", level):
        _save_open_trade(asset_type, open_trade)
        return

    level_label = WARNING_LEVELS["trend_reversal"][level]["label"]
    msg = _format_warning_message(asset_type, level, current_analysis, open_trade, reasons, level_label)

    queue_telegram_message(msg)
    record_warning(open_trade, "trend_reversal", level, current_analysis.get("price", 0), msg)
    
    # ✅ حفظ إلزامي بعد تسجيل التحذير
    _save_open_trade(asset_type, open_trade)

    if level == 3:
        close_trade_virtual(asset_type, f"انعكاس قوي: {reasons[0][:50]}", current_analysis.get("price", 0))
        return

    try:
        send_warning_func = globals().get('send_warning_to_app')
        if send_warning_func:
            warning_type = "TREND_REVERSAL_MEDIUM" if level == 2 else "TREND_REVERSAL_WEAK"
            send_warning_func(asset_type, warning_type, msg, current_analysis.get("price", 0))
            logger.info(f"📱 [WebSocket] تم إرسال تحذير {warning_type} لـ {asset_type} إلى التطبيق")
    except Exception as e:
        logger.error(f"❌ [WebSocket] فشل إرسال تحذير trend_reversal: {e}")

# ============================================================================
# 3. تحذير الذاكرة الاستباقي (معدل – إصلاح MACD)
# ============================================================================


def check_adaptive_learning_warning(asset_type, current_analysis, open_trade):
    """إعادة تقييم الصفقة كل 5 دقائق من الذاكرة التاريخية دون تغيير SuperTrend."""
    if not open_trade or ADAPTIVE_ENGINE is None:
        return None
    try:
        direction = open_trade.get("type", open_trade.get("trade_type", "BUY"))
        result = ADAPTIVE_ENGINE.predict(
            current_analysis, asset_type, direction,
            open_trade.get("entry_price"), open_trade.get("sl"), open_trade.get("tp")
        )
        open_trade["adaptive_monitor"] = {
            "probability": result.get("probability"),
            "confidence": result.get("confidence"),
            "false_signal_score": result.get("false_signal_score"),
            "similar_count": result.get("similar_count"),
            "timestamp": datetime.now().isoformat()
        }

        probability = float(result.get("probability", 50))
        false_score = int(result.get("false_signal_score", 0))
        key = "adaptive_failure_warning"
        already_sent = key in open_trade.get("warnings_sent", [])
        if (probability <= 35 or false_score >= 65) and not already_sent:
            reasons = result.get("false_signal_reasons", [])[:3]
            msg = f"⚠️ **تحذير التعلم التراكمي - {asset_type}**\n\n"
            msg += f"🧠 احتمال نجاح الإشارة حالياً: **{probability:.0f}%**\n"
            msg += f"🎯 الثقة: **{int(result.get('confidence', 0))}%**\n"
            msg += f"📚 حالات مشابهة: **{int(result.get('similar_count', 0))}**\n"
            msg += f"🚨 مؤشر خطر الفشل: **{false_score}%**\n"
            if reasons:
                msg += "\n".join(f"• {r}" for r in reasons) + "\n"
            msg += "\n💡 هذه قراءة من الذاكرة التاريخية ولا تغيّر إشارة SuperTrend."
            queue_telegram_message(msg)
            open_trade.setdefault("warnings_sent", []).append(key)
            return result
        return result
    except Exception as e:
        logger.error(f"❌ [AdaptiveMonitor] فشل إعادة تقييم {asset_type}: {e}")
        return None

def check_memory_warning(asset_type, current_analysis, open_trade):
    if not open_trade or not current_analysis:
        return

    if not should_send_warning(open_trade, "memory_warning", 1):
        return

    try:
        # 1️⃣ جلب لقطات الخسائر والربح
        loss_snapshots = _get_snapshots_by_outcome(asset_type, is_winning=False, limit=30)
        win_snapshots = _get_snapshots_by_outcome(asset_type, is_winning=True, limit=30)

        # 2️⃣ استخراج المؤشرات الحالية مع إصلاح MACD
        current_rsi = current_analysis.get('indicators', {}).get('momentum', {}).get('rsi', 50)
        current_adx = current_analysis.get('indicators', {}).get('trend', {}).get('adx', 20)
        # ✅ إصلاح: استخراج MACD من المكان الصحيح
        current_macd = current_analysis.get('indicators', {}).get('momentum', {}).get('macd_hist', 0)
        if current_macd == 0:
            tfs = current_analysis.get('timeframes', {})
            tf_15m = tfs.get('15m', {})
            current_macd = tf_15m.get('macd', 0)
        current_vol_ratio = current_analysis.get('indicators', {}).get('volume', {}).get('ratio', 1.0)
        current_price = current_analysis.get('price', 0)
        current_trend = current_analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')

        # 3️⃣ حساب متوسط مؤشرات الخسائر
        loss_avg = _calculate_avg_indicators(loss_snapshots)
        # 4️⃣ حساب متوسط مؤشرات الربح
        win_avg = _calculate_avg_indicators(win_snapshots)

        # 5️⃣ حساب درجة التشابه مع الخسائر والربح
        loss_similarity = _calculate_similarity(current_rsi, current_adx, current_macd, current_vol_ratio, current_trend, loss_avg)
        win_similarity = _calculate_similarity(current_rsi, current_adx, current_macd, current_vol_ratio, current_trend, win_avg)

        logger.info(f"🧠 [MemoryWarning] {asset_type}: تشابه مع الخسائر: {loss_similarity:.0f}%, تشابه مع الربح: {win_similarity:.0f}%")

        # 6️⃣ إرسال التحذير فقط إذا كان التشابه مع الخسائر أكبر من الربح، وأكبر من 80%
        if loss_similarity >= 80 and loss_similarity > win_similarity:
            asset_label = "النفط" if asset_type == "oil" else "الفضة"
            entry_price = open_trade.get("entry_price", 0)
            sl = open_trade.get("sl", 0)
            tp = open_trade.get("tp", 0)

            rsi_interpret = "مرتفع" if current_rsi > 70 else "منخفض" if current_rsi < 30 else "محايد"
            adx_interpret = "قوي" if current_adx > 25 else "ضعيف"
            vol_interpret = "مرتفع" if current_vol_ratio > 1.5 else "طبيعي" if current_vol_ratio > 0.7 else "منخفض"
            macd_interpret = "إيجابي" if current_macd > 0 else "سلبي" if current_macd < 0 else "محايد"

            msg = f"🧠 **تذكير بالذاكرة:** صفقة {asset_label}\n"
            msg += f"🔍 تتشابه المؤشرات الحالية بنسبة {loss_similarity:.0f}% مع الصفقات الخاسرة السابقة (أكثر من تشابهها مع الرابحة {win_similarity:.0f}%).\n"
            msg += f"📊 RSI: {current_rsi:.0f} ({rsi_interpret}) - المتوسط في الخسائر: {loss_avg['rsi']:.0f}\n"
            msg += f"📊 ADX: {current_adx:.0f} ({adx_interpret}) - المتوسط في الخسائر: {loss_avg['adx']:.0f}\n"
            msg += f"📊 MACD: {current_macd:.4f} ({macd_interpret}) - المتوسط في الخسائر: {loss_avg['macd']:.4f}\n"
            msg += f"📊 الحجم: {current_vol_ratio:.2f}x ({vol_interpret}) - المتوسط في الخسائر: {loss_avg['vol_ratio']:.2f}x\n"
            msg += f"💰 السعر الحالي: ${fmt_price(current_price, asset_type)}\n"
            msg += f"💰 سعر الدخول: ${fmt_price(entry_price, asset_type)}\n"
            msg += f"🛡️ وقف الخسارة: ${fmt_price(sl, asset_type)}\n"
            msg += f"🎯 الهدف: ${fmt_price(tp, asset_type)}\n"
            msg += "\n💡 **توصية تولين:** أنصح بالمراقبة المكثفة، قد تكون الصفقة في منطقة خطر مشابهة للخسائر السابقة."

            queue_telegram_message(msg)
            record_warning(open_trade, "memory_warning", 1, current_price, msg)

            try:
                send_warning_func = globals().get('send_warning_to_app')
                if send_warning_func:
                    send_warning_func(asset_type, "MEMORY_WARNING", msg, current_price)
                    logger.info(f"📱 [WebSocket] تم إرسال تحذير MEMORY_WARNING لـ {asset_type} إلى التطبيق")
                else:
                    logger.warning(f"⚠️ [WebSocket] send_warning_to_app غير متوفرة")
            except Exception as e:
                logger.error(f"❌ [WebSocket] فشل إرسال تحذير MEMORY_WARNING: {e}")

    except Exception as e:
        logger.error(f"❌ [MemoryWarning] فشل تحليل الذاكرة: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# 4. التحقق من ضرب SL/TP
# ============================================================================

def check_sl_tp_hit(asset_type, current_price, open_trade):
    if not open_trade:
        return False
    trade_type = open_trade.get("type", "BUY")
    sl = open_trade.get("sl", 0)
    tp = open_trade.get("tp", 0)
    if trade_type == "BUY":
        if current_price <= sl:
            close_trade_virtual(asset_type, "Hit Stop Loss", current_price)
            return True
        if current_price >= tp:
            close_trade_virtual(asset_type, "Hit Take Profit", current_price)
            return True
    else:
        if current_price >= sl:
            close_trade_virtual(asset_type, "Hit Stop Loss", current_price)
            return True
        if current_price <= tp:
            close_trade_virtual(asset_type, "Hit Take Profit", current_price)
            return True
    return False

# ============================================================================
# دوال محفوظة للتوافق
# ============================================================================

def check_adx_warnings(asset_type, adx, open_trade):
    pass

def check_volume_warnings(asset_type, vol_ratio, open_trade):
    pass

def should_send_recommendation(open_trade, recommendation_type):
    recommendations_sent = open_trade.get("recommendations_sent", [])
    if recommendation_type in recommendations_sent:
        return False
    return True

def record_recommendation(open_trade, recommendation_type, message):
    if "recommendations_sent" not in open_trade:
        open_trade["recommendations_sent"] = []
    open_trade["recommendations_sent"].append(recommendation_type)
    asset_type = open_trade.get("asset_type", "oil")
    pos_file = get_position_file(asset_type)
    try:
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(open_trade, f, indent=2, ensure_ascii=False)
    except:
        pass

# ====================================================================================
# نهاية PART 21
# ====================================================================================

# ====================================================================================
# 📦 PART 22: دوال التحليل والإشارات (المعدل - مع تمرير base_timeframe للتوقع)
# ====================================================================================
# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطبقة هنا):
# ═══════════════════════════════════════════════════════════════════════════════
# 1. يستخدم جميع المؤشرات الفنية الأساسية في التحليل الشامل.
# 2. يحلل جميع الفريمات الأربعة في analysis["timeframes"].
# 3. الاستثناء الوحيد: استراتيجية اكتشاف الصفقات (VPT + SuperTrend).
# ═══════════════════════════════════════════════════════════════════════════════
# ✅ التعديلات الجديدة:
#   - إضافة return بعد if is_manual لمنع حفظ التوقعات في التحليل اليدوي.
# ====================================================================================

from datetime import datetime
import time
import logging
import json
import re

logger = logging.getLogger("TonaPrometheus")

def _ai_only_generate_analysis(asset_type, analysis, signal, price, sl, tp, rr, chat_id=None):
    """توليد النص التحليلي بواسطة النماذج فقط؛ لا يغير قرار الاستراتيجية."""
    payload = {
        "asset": asset_type,
        "signal": signal,
        "price": price,
        "sl": sl,
        "tp": tp,
        "rr": rr,
        "analysis": analysis,
    }
    prompt = f"""أنت Tona AI. اكتب تحليلاً مالياً احترافياً باللغة العربية اعتماداً حصراً على البيانات التالية.\n\n{json.dumps(payload, ensure_ascii=False, default=str)}\n\nقواعد مهمة:\n1) لا تخترع أي رقم أو معلومة غير موجودة.\n2) لا تغير الإشارة الفنية {signal} ولا تقترح إشارة مختلفة عنها.\n3) إذا كانت الإشارة WAIT فقل ذلك بوضوح.\n4) اشرح الاتجاه والزخم والتوافق بين الفريمات والمخاطر وSL/TP وRR.\n5) كن واضحاً ومختصراً، ولا تستخدم JSON في الرد.\n6) لا تقل إنك لم تتمكن من التحليل إلا إذا فشل النموذجان فعلاً.\n"""
    messages = [
        {"role": "system", "content": "أنت محلل أسواق محترف. التزم بالبيانات فقط ولا تختلق معلومات."},
        {"role": "user", "content": prompt},
    ]
    last_error = None
    for attempt in range(2):
        try:
            if 'SMART_MANAGER' in globals() and SMART_MANAGER:
                logger.info(f"🤖 [AI-ONLY] Groq محاولة {attempt+1} لـ {asset_type}")
                text = SMART_MANAGER._call_groq_simple(messages, max_tokens=1800)
                if text and len(text.strip()) > 20:
                    logger.info(f"✅ [AI-ONLY] Groq نجح لـ {asset_type}")
                    return text.strip()
        except Exception as e:
            last_error = e
            logger.error(f"❌ [AI-ONLY] Groq: {e}")
        try:
            if 'SMART_MANAGER' in globals() and SMART_MANAGER:
                logger.info(f"🟣 [AI-ONLY] Gemini محاولة {attempt+1} لـ {asset_type}")
                text = SMART_MANAGER._get_gemini_response(messages, max_tokens=1800)
                if text and len(text.strip()) > 20:
                    logger.info(f"✅ [AI-ONLY] Gemini نجح لـ {asset_type}")
                    return text.strip()
        except Exception as e:
            last_error = e
            logger.error(f"❌ [AI-ONLY] Gemini: {e}")
        time.sleep(1)
    logger.error(f"❌ [AI-ONLY] فشل النموذجان لـ {asset_type}: {last_error}")
    return None

def analyze_and_send(asset_type, is_manual=False, chat_id=None):
    try:
        _analyze_and_send_internal(asset_type, is_manual, chat_id)
    except Exception as e:
        import traceback
        logger.error(f"[Scanner] خطأ في analyze_and_send لـ {asset_type}: {e}")
        logger.error(traceback.format_exc())
        if is_manual:
            queue_telegram_message(f"⚠️ حدث خطأ أثناء تحليل {asset_type}.", chat_id)


def _analyze_and_send_internal(asset_type, is_manual=False, chat_id=None):
    config = load_config()
    strategy_config = config["strategies"][asset_type]

    base_timeframe = strategy_config.get("base_timeframe", "Min15")
    st_multiplier = strategy_config.get("st_multiplier", 2.5 if asset_type == "oil" else 2.2)
    st_period = strategy_config.get("st_period", 100)
    vpt_len = strategy_config.get("vpt_len", 10)

    sltp_mode = strategy_config.get("sltp_mode", "ATR")
    sl_atr_mult = strategy_config.get("sl_atr_mult", 2.0)
    tp_atr_mult = strategy_config.get("tp_atr_mult", 3.0)
    min_rr = strategy_config.get("min_rr", 1.0)
    channel_buffer = strategy_config.get("channel_buffer", 0.0)

    confirmation_bars = strategy_config.get("confirmation_bars", 1)

    symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"

    logger.info(f"📊 استخدام الفريم الزمني {base_timeframe} لـ {asset_type} مع {confirmation_bars} شمعة تأكيد")

    data = get_mexc_candles(symbol, interval=base_timeframe, limit=200)

    if not data or not data.get("closes") or len(data["closes"]) < 10:
        if is_manual:
            queue_telegram_message(f"⚠️ عذراً، لم أتمكن من جلب بيانات السوق حالياً (الفريم: {base_timeframe}).", chat_id)
        return

    closes = data["closes"]
    highs = data["highs"]
    lows = data["lows"]
    opens = data["opens"]
    volumes = data["volumes"]

    if len(closes) < 5:
        if is_manual:
            queue_telegram_message("⚠️ بيانات السوق غير كافية حالياً.", chat_id)
        return

    st_result = calculate_supertrend_vpt_correct(
        data,
        st_mult=st_multiplier,
        st_period=st_period,
        vpt_len=vpt_len
    )

    if st_result is None or len(st_result) != 3:
        logger.error(f"❌ فشل حساب VPT/SuperTrend لـ {asset_type}")
        if is_manual:
            queue_telegram_message(f"⚠️ تعذر حساب المؤشرات الفنية لـ {asset_type}.", chat_id)
        return

    st_line_arr, trend, vpt_ema = st_result

    if len(vpt_ema) < 3 or len(st_line_arr) < 3 or len(trend) < 3:
        logger.error(f"❌ بيانات VPT/SuperTrend غير كافية لـ {asset_type}")
        if is_manual:
            queue_telegram_message(f"⚠️ بيانات VPT/SuperTrend غير كافية لـ {asset_type}.", chat_id)
        return

    rsi_values = calculate_rsi_7(closes, length=strategy_config.get("rsi_period", 7))
    macd_values = calculate_macd_histogram(closes)
    adx = calculate_adx_14(data)

    atr_series = calculate_atr_series(data, period=14)
    if atr_series is None or len(atr_series) < 20:
        volatility_ratio = None
        logger.warning(f"⚠️ تعذر حساب ATR لـ {asset_type}، سيتم تجاهل نسبة الحجم المعادل")
    else:
        current_atr = atr_series[-1]
        atr_window = atr_series[-21:-1] if len(atr_series) >= 21 else atr_series[:-1]
        if atr_window and len(atr_window) >= 10:
            avg_atr = sum(atr_window) / len(atr_window)
            if avg_atr > 0:
                volatility_ratio = current_atr / avg_atr
            else:
                volatility_ratio = None
        else:
            volatility_ratio = None

    signal_idx = -1

    if len(vpt_ema) > abs(signal_idx) and len(st_line_arr) > abs(signal_idx):
        current_vpt = vpt_ema[signal_idx]
        current_st = st_line_arr[signal_idx]
        previous_vpt = vpt_ema[signal_idx - 1] if len(vpt_ema) > abs(signal_idx - 1) else current_vpt
        previous_st = st_line_arr[signal_idx - 1] if len(st_line_arr) > abs(signal_idx - 1) else current_st

        crossover = previous_vpt <= previous_st and current_vpt > current_st
        crossunder = previous_vpt >= previous_st and current_vpt < current_st
    else:
        crossover = False
        crossunder = False

    logger.info(f"🔍 [{base_timeframe}] {asset_type}: VPT={current_vpt:.6f}, ST={current_st:.6f}, diff={current_vpt-current_st:.6f}")
    logger.info(f"🔍 [{base_timeframe}] {asset_type}: crossover={crossover}, crossunder={crossunder}")

    signal = "WAIT"

    if crossover or crossunder:
        confirmation_ok = True
        if confirmation_bars > 0:
            current_trend = trend[-1] if len(trend) > 0 else 0
            for i in range(1, confirmation_bars + 1):
                if len(trend) > i and trend[-i] != current_trend:
                    confirmation_ok = False
                    logger.info(f"⏳ فشل التأكيد: trend[-{i}] = {trend[-i]} != {current_trend}")
                    break
    else:
        confirmation_ok = False

    if crossover and confirmation_ok:
        signal = "BUY"
        logger.info(f"🚨 إشارة BUY مؤكدة لـ {asset_type}!")
    elif crossunder and confirmation_ok:
        signal = "SELL"
        logger.info(f"🚨 إشارة SELL مؤكدة لـ {asset_type}!")
    else:
        logger.info(f"⏳ لا توجد إشارة مؤكدة لـ {asset_type}")

    if not is_manual:
        if signal == "WAIT":
            return

        open_trade = get_current_open_trade(asset_type)

        if open_trade:
            trade_type = open_trade.get('type', 'BUY')
            if (signal == "BUY" and trade_type == "BUY") or (signal == "SELL" and trade_type == "SELL"):
                logger.info(f"⏳ تجاهل إشارة {signal} مكررة لـ {asset_type} (توجد صفقة {trade_type} مفتوحة)")
                return
            else:
                logger.info(f"🔄 إشارة {signal} معاكسة للصفقة المفتوحة {trade_type}، سيتم إغلاق الصفقة وفتح أخرى")
                close_success = close_trade_virtual(asset_type, f"إشارة معاكسة - عكس الصفقة ({signal})")
                if not close_success:
                    logger.error(f"❌ فشل إغلاق الصفقة المعاكسة لـ {asset_type}، لن يتم فتح صفقة جديدة")
                    return

    if signal == "WAIT" and not is_manual:
        return

    price = closes[-1]
    atr = calculate_atr_14(data)

    if atr is None or atr <= 0:
        logger.error(f"❌ ATR غير صالح لـ {asset_type}: {atr}")
        if is_manual:
            queue_telegram_message(f"⚠️ تعذر حساب ATR لـ {asset_type}.", chat_id)
        return

    if sltp_mode == "Channel":
        pc_length = 130
        pc_max = max(highs[-pc_length:]) if len(highs) >= pc_length else max(highs)
        pc_min = min(lows[-pc_length:]) if len(lows) >= pc_length else min(lows)
        pc_atr = atr * 0.5

        pc_res = pc_max + pc_atr
        pc_sup = pc_min - pc_atr

        if signal == "BUY":
            sl = pc_sup - channel_buffer
            tp = pc_res
            rr = (tp - price) / (price - sl) if (price - sl) != 0 else 1.0
            if rr < min_rr:
                sl = price - (price - sl) * 0.8
        elif signal == "SELL":
            sl = pc_res + channel_buffer
            tp = pc_sup
            rr = (price - tp) / (sl - price) if (sl - price) != 0 else 1.0
            if rr < min_rr:
                sl = price + (sl - price) * 0.8
        else:
            sl = tp = price
    else:
        sl_dist = atr * sl_atr_mult
        tp_dist = atr * tp_atr_mult

        if signal == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
            rr = tp_atr_mult / sl_atr_mult
        elif signal == "SELL":
            sl = price + sl_dist
            tp = price - tp_dist
            rr = tp_atr_mult / sl_atr_mult
        else:
            sl = tp = price

    asset_label = "النفط الخام" if asset_type == "oil" else "الفضة"
    sig_label = "🟢 شراء (BUY)" if signal == "BUY" else "🔴 بيع (SELL)" if signal == "SELL" else "⚪ انتظار (WAIT)"

    analysis = {
        "timestamp": datetime.now().isoformat(),
        "asset": asset_type,
        "price": price,
        "current_price": price,
        "timeframes": {
            base_timeframe.replace("Min", "m"): {
                "price": price,
                "rsi": rsi_values[-1] if rsi_values else None,
                "macd": macd_values[-1] if macd_values else None,
                "adx": adx,
                "atr": atr,
                "volume_ratio": volatility_ratio,
                "trend": "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد",
                "vpt": vpt_ema[-1] if vpt_ema else None,
                "supertrend": {"line": st_line_arr[-1] if st_line_arr else None, "trend": trend[-1] if trend else None}
            }
        }
    }

    timeframes = {
        "5m": {"interval": "Min5", "limit": 200},
        "1h": {"interval": "Min60", "limit": 200},
        "4h": {"interval": "Hour4", "limit": 200}
    }
    results = fetch_multiple_timeframes(symbol, timeframes)

    for tf_name, tf_data in [("5m", results.get("5m")), ("1h", results.get("1h")), ("4h", results.get("4h"))]:
        if tf_data and tf_data.get("closes") and len(tf_data["closes"]) >= 10:
            tcloses = tf_data["closes"]
            st_result = calculate_supertrend_vpt_correct(tf_data, st_mult=st_multiplier)
            if st_result is not None and len(st_result) == 3:
                st_l, tr, vpt_tf = st_result
                tf_rsi = calculate_rsi_7(tcloses)[-1] if len(tcloses) >= 7 else None
                tf_macd = calculate_macd_histogram(tcloses)[-1] if len(tcloses) >= 35 else None
                tf_adx = calculate_adx_14(tf_data)
                tf_atr = calculate_atr_14(tf_data)
                tf_vol_ratio = 1.0
                tf_volumes = tf_data.get("volumes", [])
                if tf_volumes and len(tf_volumes) > 20:
                    tf_current_vol = tf_volumes[-1]
                    tf_avg_vol = sum(tf_volumes[-20:-1]) / 19 if len(tf_volumes) > 20 else tf_current_vol
                    tf_vol_ratio = tf_current_vol / tf_avg_vol if tf_avg_vol > 0 else 1.0
                
                analysis["timeframes"][tf_name] = {
                    "price": tcloses[-1],
                    "trend": "صاعد" if tr[-1] == 1 else "هابط" if tr[-1] == -1 else "محايد",
                    "rsi": tf_rsi,
                    "macd": tf_macd,
                    "adx": tf_adx,
                    "atr": tf_atr,
                    "volume_ratio": tf_vol_ratio,
                    "vpt": vpt_tf[-1] if vpt_tf else None,
                    "supertrend": {"line": st_l[-1] if st_l else None, "trend": tr[-1] if tr else None}
                }
            else:
                logger.warning(f"⚠️ فشل حساب SuperTrend للفريم {tf_name} في {asset_type} (بيانات غير كافية)")
                analysis["timeframes"][tf_name] = {
                    "price": tcloses[-1],
                    "trend": "محايد",
                    "rsi": None,
                    "macd": None,
                    "adx": None,
                    "atr": None,
                    "volume_ratio": 1.0,
                    "vpt": None,
                    "supertrend": {"line": None, "trend": None}
                }

    upper, basis, lower = calculate_bollinger_bands(closes)
    tf_key = base_timeframe.replace("Min", "m")
    analysis["timeframes"][tf_key]["bollinger"] = {
        "upper": upper[-1] if upper else None,
        "basis": basis[-1] if basis else None,
        "lower": lower[-1] if lower else None
    }

    stoch = calculate_stochastic(highs, lows, closes)
    analysis["timeframes"][tf_key]["stochastic"] = stoch[-1] if stoch else None

    vwap_values = calculate_vwap(data)
    analysis["timeframes"][tf_key]["vwap"] = vwap_values[-1] if vwap_values else None

    analysis["indicators"] = {
        "trend": {
            "current_trend": "صاعد" if trend[-1] == 1 else "هابط" if trend[-1] == -1 else "محايد",
            "adx": adx
        },
        "momentum": {
            "rsi": rsi_values[-1] if rsi_values else None,
            "macd": macd_values[-1] if macd_values else None,
            "stoch": stoch[-1] if stoch else None
        },
        "volume": {
            "ratio": volatility_ratio
        },
        "volatility": {
            "atr_percent": (atr / price * 100) if price > 0 else None,
            "bb_position": (price - lower[-1]) / (upper[-1] - lower[-1]) if upper and lower and upper[-1] and lower[-1] and upper[-1] > lower[-1] else 0.5,
            "vwap_deviation": ((price - vwap_values[-1]) / vwap_values[-1] * 100) if vwap_values and vwap_values[-1] > 0 else 0
        },
        "support_resistance": {
            "s1": price * 0.98,
            "r1": price * 1.02,
            "pivot": price
        },
        "vpt": vpt_ema[-1] if vpt_ema else None
    }
    analysis["supertrend"] = {
        "line": st_line_arr[-1] if st_line_arr else price,
        "trend": trend[-1] if trend else 1
    }
    analysis["comprehensive_score"] = calculate_comprehensive_score(analysis, asset_type)

    # ✅ توليد معرف الصفقة مرة واحدة حتى يرتبط التوقع بالصفقة الفعلية.
    trade_id = f"{asset_type}_{int(datetime.now().timestamp())}"

    # ✅ توليد التوقع المسبق مع تمرير base_timeframe ومعرف الصفقة الحقيقي
    prior_judgment = generate_prior_judgment(
        analysis, asset_type, signal, price, sl, tp,
        base_timeframe=base_timeframe, trade_id=trade_id
    )
    logger.info(f"🧠 [Prior Judgment] {asset_type}: {prior_judgment}")

    # ── التحليل اليدوي: النص النهائي من الذكاء الاصطناعي فقط ──
    if is_manual:
        ai_text = _ai_only_generate_analysis(
            asset_type, analysis, signal, price, sl, tp, rr, chat_id
        )
        asset_label = "النفط الخام" if asset_type == "oil" else "الفضة"
        if ai_text:
            msg = f"📊 **تحليل {asset_label} الشامل**\n"
            msg += f"💰 السعر: ${fmt_price(price, asset_type)} | الإشارة الاستراتيجية: {sig_label}\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"🧠 **Tona AI:**\n{ai_text}\n\n"
            msg += f"🛡️ وقف الخسارة: ${fmt_price(sl, asset_type)}\n"
            msg += f"🎯 الهدف: ${fmt_price(tp, asset_type)}\n"
            msg += f"📊 RR: {rr:.2f}\n\n💙 Tona AI: أنا هنا لمساعدتك!"
            queue_telegram_message(msg, chat_id)
        else:
            queue_telegram_message(
                "⚠️ تعذر الحصول على رد من نماذج الذكاء الاصطناعي بعد محاولتين. "
                "لم يتم تغيير استراتيجية الإشارة أو تنفيذ أي صفقة.", chat_id
            )
        return

    # ================================================================
    # ✅ فتح الصفقة الجديدة (مع حفظ التحليل الشامل)
    # ================================================================
    if signal in ["BUY", "SELL"]:
        trade_context = {
            "entry": price,
            "sl": sl,
            "tp": tp,
            "rr": rr,
            "price": price
        }

        comp_score = analysis.get("comprehensive_score", {})
        score = comp_score.get("score", 50)
        risk_level = comp_score.get("risk_level", "متوسط")
        grade = comp_score.get("grade", "محايد")

        confidence = {"total": 70, "grade": "جيدة", "emoji": "📊", "breakdown": {}}
        if CONFIDENCE_AVAILABLE and CONFIDENCE_SCORER:
            try:
                confidence = CONFIDENCE_SCORER.calculate(analysis, signal, trade_context)
                logger.info(f"📊 درجة الثقة الداخلية: {confidence['total']:.0f}% ({confidence['grade']})")
            except Exception as e:
                logger.error(f"❌ فشل حساب درجة الثقة الداخلية: {e}")

        lines = []
        lines.append(f"📊 **توصية تولين - {asset_label}**")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        lines.append(f"🎯 **التوصية:** {sig_label}")
        lines.append("")

        pred_verdict = prior_judgment.get('verdict', 'unknown')
        pred_confidence = prior_judgment.get('confidence', 50)
        pred_reasoning = prior_judgment.get('reasoning', 'لا توجد أسباب')

        if pred_verdict == 'win':
            pred_emoji = "✅"
            verdict_text = "ربح"
        elif pred_verdict == 'loss':
            pred_emoji = "❌"
            verdict_text = "خسارة"
        else:
            pred_emoji = "⚪"
            verdict_text = "غير معروف"

        lines.append(f"🧠 **توقع تولين المسبق:** {pred_emoji} {verdict_text}")
        lines.append(f"🎯 **الثقة:** {pred_confidence}%")
        lines.append(f"💡 **السبب:** {pred_reasoning}")
        lines.append("")

        lines.append(f"💰 **السعر الحالي:** ${fmt_price(price, asset_type)}")
        lines.append(f"🚀 **الدخول:** ${fmt_price(price, asset_type)}")
        lines.append(f"🎯 **الهدف:** ${fmt_price(tp, asset_type)}")
        lines.append(f"🛡️ **وقف الخسارة:** ${fmt_price(sl, asset_type)}")
        lines.append(f"📊 **نسبة المخاطرة/المكافأة:** {rr:.2f}")
        lines.append("")

        lines.append("📊 **تفصيل نقاط القوة:**")
        bullish_count = 0
        bearish_count = 0
        timeframes_data = analysis.get("timeframes", {})
        for tf_name, tf_data in timeframes_data.items():
            tf_trend = tf_data.get("trend", "محايد")
            if tf_trend == "صاعد":
                bullish_count += 1
            elif tf_trend == "هابط":
                bearish_count += 1

        if bullish_count >= 3:
            tf_status = "ممتاز" if bullish_count == 4 else "جيد"
        elif bearish_count >= 3:
            tf_status = "ممتاز" if bearish_count == 4 else "جيد"
        else:
            tf_status = "ضعيف"
        lines.append(f"   • توافق الاتجاهات: {tf_status}")

        vol_ratio = analysis.get("timeframes", {}).get("15m", {}).get("volume_ratio")
        if vol_ratio is not None:
            vol_status = "جيد" if vol_ratio > 1.5 else "طبيعي" if vol_ratio > 0.7 else "ضعيف"
        else:
            vol_status = "غير متوفر"
        lines.append(f"   • تأكيد الحجم: {vol_status}")

        adx_val = analysis.get("indicators", {}).get("trend", {}).get("adx")
        if adx_val is not None:
            mom_status = "قوي" if adx_val > 30 else "متوسط" if adx_val > 20 else "ضعيف"
        else:
            mom_status = "غير متوفر"
        lines.append(f"   • قوة الزخم: {mom_status}")

        lines.append(f"   • توافق الفريمات: {'ممتاز' if bullish_count >= 3 or bearish_count >= 3 else 'متوسط' if bullish_count >= 2 or bearish_count >= 2 else 'ضعيف'}")

        memory_insights = analysis.get("memory_insights", {})
        if memory_insights and memory_insights.get("has_memory"):
            hist_status = "جيد" if memory_insights.get("confidence_boost", 0) > 0 else "متوسط"
        else:
            hist_status = "متوسط"
        lines.append(f"   • الدقة التاريخية: {hist_status}")

        rr_status = "جيد" if rr >= 2.0 else "طبيعي" if rr >= 1.5 else "ضعيف"
        lines.append(f"   • نسبة المخاطرة/المكافأة: {rr_status}")
        lines.append("")

        lines.append("📋 **أسباب التأييد والتحذيرات:**")
        if comp_score and isinstance(comp_score, dict):
            details = comp_score.get("details", [])
            if details:
                for d in details[:4]:
                    lines.append(f"   {d}")
            else:
                lines.append("   • لا توجد أسباب محددة.")
        else:
            lines.append("   • لا توجد أسباب محددة.")
        lines.append("")

        lines.append("⚠️ **عوامل الخطر:**")
        sr = analysis.get("indicators", {}).get("support_resistance", {})
        support = sr.get("s1", price * 0.98)
        resistance = sr.get("r1", price * 1.02)
        lines.append(f"   🟡 السعر قرب مقاومة قوية (${fmt_price(resistance, asset_type)})")
        lines.append(f"   🟡 السعر قرب دعم قوي (${fmt_price(support, asset_type)})")

        if signal == "SELL" and bullish_count >= 3:
            lines.append(f"   🔴 تناقض حاد: {bullish_count}/4 فريمات صاعدة لكن الإشارة بيع")
        elif signal == "BUY" and bearish_count >= 3:
            lines.append(f"   🔴 تناقض حاد: {bearish_count}/4 فريمات هابطة لكن الإشارة شراء")
        else:
            lines.append("   🟢 لا توجد تناقضات كبيرة.")
        lines.append("")

        lines.append("🧠 **الخبرة السابقة:**")
        if memory_insights and memory_insights.get("has_memory"):
            insight = memory_insights.get("insight", "")
            if insight:
                lines.append(f"   {insight}")
            else:
                lines.append("   • توجد خبرات سابقة مشابهة.")
        else:
            lines.append("   ⚠️ لا توجد بيانات كافية للصفقات المشابهة")
        lines.append("")

        risk_level_text = "🟢 منخفض"
        if signal == "SELL" and bullish_count >= 3:
            risk_level_text = "🔴 مرتفع جداً - تناقض خطير"
        elif signal == "BUY" and bearish_count >= 3:
            risk_level_text = "🔴 مرتفع جداً - تناقض خطير"
        elif rr < 1.5:
            risk_level_text = "🟡 متوسط - RR منخفض"
        elif adx_val is not None and adx_val < 20:
            risk_level_text = "🟡 متوسط - ADX ضعيف"
        else:
            risk_level_text = "🟢 منخفض - ظروف مواتية"
        lines.append(f"🛡️ **مستوى الخطر:** {risk_level_text}")
        lines.append("")

        lines.append("💡 **نصائح إضافية:**")
        if signal == "SELL" and bullish_count >= 3:
            lines.append(f"   ⚠️ تناقض خطير: الفريمات صاعدة لكن الإشارة بيع - انتظر تأكيداً")
        elif signal == "BUY" and bearish_count >= 3:
            lines.append(f"   ⚠️ تناقض خطير: الفريمات هابطة لكن الإشارة شراء - انتظر تأكيداً")

        if price >= resistance * 0.995:
            lines.append(f"   • السعر قرب المقاومة - فرصة { 'بيع' if signal == 'SELL' else 'شراء مع حذر' } مع وقف خسارة محكم")
        elif price <= support * 1.005:
            lines.append(f"   • السعر قرب الدعم - فرصة { 'شراء' if signal == 'BUY' else 'بيع مع حذر' } مع وقف خسارة محكم")
        else:
            lines.append("   • السعر في منتصف النطاق - انتظر تأكيداً إضافياً")
        lines.append("")

        lines.append("💙 تولين: التداول رحلة... وأنا رفيقتك في هذه الرحلة")

        report = "\n".join(lines)

        logger.info(f"📤 إرسال إشعار {asset_type} - {signal} (طول النص: {len(report)})")
        queue_telegram_message(report, chat_id or CHAT_ID)
        logger.info(f"✅ تم إرسال إشعار {asset_type} بنجاح")

        current_rsi = rsi_values[-1] if rsi_values else None
        current_macd = macd_values[-1] if macd_values else None

        trade_data = {
            "trade_id": trade_id,
            "type": signal,
            "entry_price": price,
            "sl": sl,
            "tp": tp,
            "profit_dollars": 0.0,
            "status": "open",
            "warnings_sent": [],
            "warnings_log": [],
            "recommendations_sent": [],
            "asset_type": asset_type,
            "entry_indicators": {
                "rsi": current_rsi,
                "adx": adx,
                "trend": "صاعد" if trend[-1] == 1 else "هابط",
                "macd": current_macd,
                "vpt": vpt_ema[-1] if vpt_ema else None,
                "st_line": st_line_arr[-1] if st_line_arr else None,
                "volume_ratio": volatility_ratio
            },
            "rr": rr,
            "confidence": confidence.get('total', 70) if confidence else 70,
            "prior_judgment": prior_judgment
        }

        holistic_entry_analysis = analysis

        try:
            send_signal_func = globals().get('send_signal_to_app')
            if send_signal_func:
                send_signal_func(asset_type, signal, price, trade_data)
                logger.info(f"📱 [WebSocket] تم إرسال إشارة {signal} لـ {asset_type} إلى التطبيق")
        except Exception as e:
            logger.error(f"❌ [WebSocket] فشل إرسال الإشارة إلى التطبيق: {e}")

        logger.info(f"🟢 [Scanner] استدعاء add_trade_to_history لـ {asset_type}")
        trade_saved = add_trade_to_history(asset_type, trade_data, holistic_entry_analysis=holistic_entry_analysis)

        if not trade_saved:
            logger.error(f"❌ [Scanner] فشل حفظ صفقة {asset_type} - trade_id: {trade_data['trade_id']}")
            queue_telegram_message(f"⚠️ عذراً، حدث خطأ في حفظ صفقة {asset_label}.", chat_id)
            return

        logger.info(f"✅ [Scanner] تم حفظ صفقة {asset_type} بنجاح - {trade_data['trade_id']}")

        with MONITOR_TRIGGER_LOCK:
            MONITOR_TRIGGER[asset_type] = {"reason": "new_trade", "time": time.time()}

    return

# ====================================================================================
# نهاية PART 22
# ====================================================================================

# ====================================================================================
# 📦 PART 23: دوال التقارير (المعدل - مع جميع المؤشرات والفريمات)
# ====================================================================================
# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطبقة هنا):
# ═══════════════════════════════════════════════════════════════════════════════
# 1. يستخدم جميع المؤشرات الفنية الأساسية في التقارير.
# 2. يحلل جميع الفريمات الأربعة.
# 3. يعرض تحليل الفريمات في التقارير بشكل واضح.
# ═══════════════════════════════════════════════════════════════════════════════
# ====================================================================================

def get_trading_stats(chat_id=None):
    try:
        msg = "📊 <b>تقرير أداء البوت الشامل</b>\n"
        msg += "━" * 30 + "\n\n"
        
        for asset_type, asset_name in [("oil", "النفط"), ("silver", "الفضة")]:
            stats = calculate_statistics(asset_type)
            emoji = "🛢️" if asset_type == "oil" else "🥈"
            msg += f"{emoji} <b>{asset_name}</b>\n"
            msg += f"💰 الرصيد: ${stats.get('current_balance', 0):.2f}\n"
            msg += f"📈 إجمالي الربح: ${stats.get('total_profit', 0):.2f}\n"
            msg += f"📊 عدد الصفقات: {stats.get('total_trades', 0)}\n"
            msg += f"✅ رابحة: {stats.get('winning_trades', 0)}\n"
            msg += f"❌ خاسرة: {stats.get('losing_trades', 0)}\n"
            msg += f"📊 نسبة النجاح: {stats.get('win_rate', 0):.1f}%\n"
            msg += f"🎯 TP: {stats.get('tp_count', 0)} | SL: {stats.get('sl_count', 0)}\n"
            msg += f"✋ إغلاق يدوي: {stats.get('manual_count', 0)}\n\n"
        
        queue_telegram_message(msg, chat_id)
    except Exception as e:
        logger.error(f"❌ فشل جلب الإحصائيات: {e}")
        import traceback
        logger.error(traceback.format_exc())
        queue_telegram_message(f"⚠️ عذراً، حدث خطأ أثناء جلب الإحصائيات: {str(e)[:100]}", chat_id)

def analyze_last_trade_command():
    last_trade = get_last_closed_trade()
    if not last_trade:
        queue_telegram_message("🔄 **لا توجد صفقات مغلقة حتى الآن.**")
        return

    asset_type = last_trade.get("asset", "oil")
    asset_label = "النفط" if asset_type == "oil" else "الفضة"

    entry = last_trade.get("entry_price", 0)
    exit_price = last_trade.get("exit_price", 0)
    trade_type = last_trade.get("type", "UNKNOWN")
    profit_dollars = last_trade.get("profit_dollars", 0)
    exit_reason = last_trade.get("exit_reason", "غير معروف")
    entry_time = last_trade.get("timestamp", "")
    exit_timestamp = last_trade.get("exit_timestamp", "")
    confidence = last_trade.get("confidence", "غير متوفر")
    rr = last_trade.get("rr", 1.0)
    
    holistic_entry = last_trade.get("holistic_entry_analysis", {})
    entry_analysis_valid = False
    entry_rsi = 50
    entry_adx = 15
    entry_macd = 0
    entry_trend = "محايد"
    entry_vol_ratio = 1.0
    entry_vwap = entry
    entry_bb_upper = entry * 1.02
    entry_bb_lower = entry * 0.98
    entry_support = entry * 0.98
    entry_resistance = entry * 1.02
    entry_score = 50
    entry_grade = "محايد"
    
    if holistic_entry and isinstance(holistic_entry, dict):
        entry_analysis_valid = True
        entry_tf_15m = holistic_entry.get("timeframes", {}).get("15m", {}) if isinstance(holistic_entry.get("timeframes"), dict) else {}
        entry_indicators_data = holistic_entry.get("indicators", {}) if isinstance(holistic_entry.get("indicators"), dict) else {}
        entry_comp_score = holistic_entry.get("comprehensive_score", {}) if isinstance(holistic_entry.get("comprehensive_score"), dict) else {}
        
        entry_rsi = entry_tf_15m.get("rsi", 50) if isinstance(entry_tf_15m, dict) else 50
        entry_adx = entry_tf_15m.get("adx", 15) if isinstance(entry_tf_15m, dict) else 15
        entry_macd = entry_tf_15m.get("macd", 0) if isinstance(entry_tf_15m, dict) else 0
        entry_trend = entry_tf_15m.get("trend", "محايد") if isinstance(entry_tf_15m, dict) else "محايد"
        entry_vol_ratio = entry_tf_15m.get("volume_ratio", 1.0) if isinstance(entry_tf_15m, dict) else 1.0
        entry_vwap = entry_tf_15m.get("vwap", entry) if isinstance(entry_tf_15m, dict) else entry
        bb = entry_tf_15m.get("bollinger", {}) if isinstance(entry_tf_15m, dict) else {}
        entry_bb_upper = bb.get("upper", entry * 1.02) if isinstance(bb, dict) else entry * 1.02
        entry_bb_lower = bb.get("lower", entry * 0.98) if isinstance(bb, dict) else entry * 0.98
        sr = entry_indicators_data.get("support_resistance", {}) if isinstance(entry_indicators_data, dict) else {}
        entry_support = sr.get("s1", entry * 0.98) if isinstance(sr, dict) else entry * 0.98
        entry_resistance = sr.get("r1", entry * 1.02) if isinstance(sr, dict) else entry * 1.02
        entry_score = entry_comp_score.get("score", 50) if isinstance(entry_comp_score, dict) else 50
        entry_grade = entry_comp_score.get("grade", "محايد") if isinstance(entry_comp_score, dict) else "محايد"
    else:
        entry_indicators_old = last_trade.get("entry_indicators", {})
        if isinstance(entry_indicators_old, dict):
            entry_rsi = entry_indicators_old.get("rsi", 50)
            entry_adx = entry_indicators_old.get("adx", 15)
            entry_macd = entry_indicators_old.get("macd", 0)
            entry_trend = entry_indicators_old.get("trend", "محايد")
    
    exit_analysis, _ = perform_comprehensive_analysis(asset_type, False, None, force_refresh=True)
    exit_analysis_valid = False
    exit_price_now = exit_price
    exit_rsi = 50
    exit_adx = 15
    exit_macd = 0
    exit_trend = "محايد"
    exit_vol_ratio = 1.0
    exit_vwap = exit_price
    exit_bb_upper = exit_price * 1.02
    exit_bb_lower = exit_price * 0.98
    exit_support = exit_price * 0.98
    exit_resistance = exit_price * 1.02
    exit_score = 50
    exit_grade = "محايد"
    
    if exit_analysis and isinstance(exit_analysis, dict):
        exit_analysis_valid = True
        exit_price_now = exit_analysis.get("price", exit_price)
        exit_tf_15m = exit_analysis.get("timeframes", {}).get("15m", {}) if isinstance(exit_analysis.get("timeframes"), dict) else {}
        exit_indicators_data = exit_analysis.get("indicators", {}) if isinstance(exit_analysis.get("indicators"), dict) else {}
        exit_comp_score = exit_analysis.get("comprehensive_score", {}) if isinstance(exit_analysis.get("comprehensive_score"), dict) else {}
        
        exit_rsi = exit_tf_15m.get("rsi", 50) if isinstance(exit_tf_15m, dict) else 50
        exit_adx = exit_tf_15m.get("adx", 15) if isinstance(exit_tf_15m, dict) else 15
        exit_macd = exit_tf_15m.get("macd", 0) if isinstance(exit_tf_15m, dict) else 0
        exit_trend = exit_tf_15m.get("trend", "محايد") if isinstance(exit_tf_15m, dict) else "محايد"
        exit_vol_ratio = exit_tf_15m.get("volume_ratio", 1.0) if isinstance(exit_tf_15m, dict) else 1.0
        exit_vwap = exit_tf_15m.get("vwap", exit_price) if isinstance(exit_tf_15m, dict) else exit_price
        bb = exit_tf_15m.get("bollinger", {}) if isinstance(exit_tf_15m, dict) else {}
        exit_bb_upper = bb.get("upper", exit_price * 1.02) if isinstance(bb, dict) else exit_price * 1.02
        exit_bb_lower = bb.get("lower", exit_price * 0.98) if isinstance(bb, dict) else exit_price * 0.98
        sr = exit_indicators_data.get("support_resistance", {}) if isinstance(exit_indicators_data, dict) else {}
        exit_support = sr.get("s1", exit_price * 0.98) if isinstance(sr, dict) else exit_price * 0.98
        exit_resistance = sr.get("r1", exit_price * 1.02) if isinstance(sr, dict) else exit_price * 1.02
        exit_score = exit_comp_score.get("score", 50) if isinstance(exit_comp_score, dict) else 50
        exit_grade = exit_comp_score.get("grade", "محايد") if isinstance(exit_comp_score, dict) else "محايد"
    
    is_win = profit_dollars > 0
    lessons = []
    reasons = []
    
    if exit_reason == "Hit Stop Loss":
        reasons.append("🛡️ **ضرب وقف الخسارة (SL)**")
        if trade_type == "BUY" and entry > 0:
            sl_distance = (entry - exit_price) / entry * 100
        elif trade_type == "SELL" and entry > 0:
            sl_distance = (exit_price - entry) / entry * 100
        else:
            sl_distance = 0
        if abs(sl_distance) < 1.0:
            reasons.append(f"   • مسافة SL ضيقة جداً ({abs(sl_distance):.2f}%) — يُنصح بتوسيعها إلى 1.5-2%")
        else:
            reasons.append(f"   • مسافة SL: {abs(sl_distance):.2f}% — مناسبة ولكن السوق تحرك بعنف")
    elif exit_reason == "Hit Take Profit":
        reasons.append("🎯 **تم تحقيق الهدف (TP)**")
    elif "تحذير" in exit_reason or "تغيير اتجاه" in exit_reason:
        reasons.append(f"🚨 **إغلاق تلقائي بسبب: {exit_reason}**")
    
    if entry_rsi > 70 and trade_type == "BUY":
        reasons.append(f"🔴 **RSI مرتفع عند الدخول ({entry_rsi:.1f})** — منطقة تشبع شرائي")
        lessons.append("تجنب الشراء عندما يكون RSI > 70")
    elif entry_rsi < 30 and trade_type == "SELL":
        reasons.append(f"🔴 **RSI منخفض عند الدخول ({entry_rsi:.1f})** — منطقة تشبع بيعي")
        lessons.append("تجنب البيع عندما يكون RSI < 30")
    else:
        reasons.append(f"🟢 **RSI محايد عند الدخول ({entry_rsi:.1f})**")
    
    if entry_adx < 20:
        reasons.append(f"🔴 **ADX ضعيف عند الدخول ({entry_adx:.1f})** — سوق عرضي")
        lessons.append("تأكد من ADX > 20 قبل الدخول")
    elif entry_adx > 25:
        reasons.append(f"🟢 **ADX قوي عند الدخول ({entry_adx:.1f})**")
    else:
        reasons.append(f"🟡 **ADX متوسط عند الدخول ({entry_adx:.1f})**")
    
    if trade_type == "BUY" and entry_macd < 0:
        reasons.append(f"🔴 **MACD سالب عند الدخول ({entry_macd:.4f})** — زخم هابط ضد الشراء")
        lessons.append("تأكد من أن MACD موجب قبل الشراء")
    elif trade_type == "SELL" and entry_macd > 0:
        reasons.append(f"🔴 **MACD موجب عند الدخول ({entry_macd:.4f})** — زخم صاعد ضد البيع")
        lessons.append("تأكد من أن MACD سالب قبل البيع")
    else:
        reasons.append(f"🟢 **MACD متوافق عند الدخول ({entry_macd:.4f})**")
    
    if rr < 1.5:
        reasons.append(f"⚠️ **RR منخفض ({rr:.2f})** — يجب أن يكون ≥ 2:1")
        lessons.append("استهدف RR ≥ 2:1")
    elif rr >= 2.0:
        reasons.append(f"✅ **RR جيد ({rr:.2f})**")
    
    if exit_vol_ratio < 0.6:
        reasons.append(f"🔴 **حجم تداول منخفض عند الخروج ({exit_vol_ratio:.2f}x)**")
        lessons.append("تأكد من حجم تداول ≥ 1.2x")
    
    if exit_reason == "Hit Stop Loss":
        if trade_type == "BUY" and exit_price <= exit_support:
            reasons.append(f"🔴 **كسر الدعم (${exit_support:.2f})**")
        elif trade_type == "SELL" and exit_price >= exit_resistance:
            reasons.append(f"🔴 **اختراق المقاومة (${exit_resistance:.2f})**")
    
    if trade_type == "BUY" and entry > entry_bb_upper:
        reasons.append(f"🔴 **الدخول فوق البولينجر العلوي (${entry_bb_upper:.2f})**")
        lessons.append("تجنب الشراء فوق البولينجر العلوي")
    elif trade_type == "SELL" and entry < entry_bb_lower:
        reasons.append(f"🔴 **الدخول تحت البولينجر السفلي (${entry_bb_lower:.2f})**")
        lessons.append("تجنب البيع تحت البولينجر السفلي")
    
    if entry_analysis_valid and entry_score < 45:
        reasons.append(f"🔴 **التقييم الشامل عند الدخول كان ضعيفاً ({entry_score:.0f}%)**")
        lessons.append("تأكد من أن التقييم الشامل > 55% قبل الدخول")
    elif entry_analysis_valid and entry_score >= 70:
        reasons.append(f"🟢 **التقييم الشامل عند الدخول كان قوياً ({entry_score:.0f}%)**")
    
    if is_win:
        reasons.append("✅ **الصفقة رابحة**")
        if exit_reason == "Hit Take Profit":
            reasons.append("   • تم تحقيق الهدف")
    
    msg = f"🔍 **تحليل عميق لآخر صفقة مغلقة**\n"
    msg += "━" * 40 + "\n"
    msg += f"📊 **الأصل:** {asset_label}\n"
    msg += f"📈 **النوع:** {trade_type}\n"
    msg += f"💰 **الدخول:** ${fmt_price(entry, asset_type)} | **الخروج:** ${fmt_price(exit_price, asset_type)}\n"
    msg += f"📊 **النتيجة:** {AccountingSystem.format_profit(profit_dollars)} ({'رابحة 🏆' if is_win else 'خاسرة 📉'})\n"
    msg += f"📌 **سبب الإغلاق:** {exit_reason}\n"
    msg += f"🕐 **الدخول:** {entry_time[:16] if entry_time else 'غير معروف'} | **الخروج:** {exit_timestamp[:16] if exit_timestamp else 'غير معروف'}\n"
    if confidence != "غير متوفر":
        msg += f"📊 **الثقة عند الدخول:** {confidence}%\n"
    msg += f"📊 **RR:** {rr:.2f}\n"
    msg += "━" * 40 + "\n"
    
    msg += "📊 **مقارنة المؤشرات (دخول → خروج):**\n"
    msg += f"   • RSI: {entry_rsi:.1f} → {exit_rsi:.1f}\n"
    msg += f"   • ADX: {entry_adx:.1f} → {exit_adx:.1f}\n"
    msg += f"   • MACD: {entry_macd:.4f} → {exit_macd:.4f}\n"
    msg += f"   • الاتجاه: {entry_trend} → {exit_trend}\n"
    if entry_analysis_valid:
        msg += f"   • التقييم الشامل: {entry_score:.0f}% → {exit_score:.0f}%\n"
    msg += "━" * 40 + "\n"
    
    msg += "🔍 **تحليل الأسباب:**\n"
    for r in reasons[:8]:
        msg += f"   {r}\n"
    
    if lessons:
        msg += "━" * 40 + "\n"
        msg += "📚 **الدروس المستفادة:**\n"
        for lesson in lessons[:4]:
            msg += f"   • {lesson}\n"
    
    msg += "━" * 40 + "\n"
    msg += "💡 **توصية تولين:**\n"
    if is_win:
        msg += "   ✅ صفقة ناجحة! استمر في تطبيق نفس المعايير."
    else:
        msg += "   ❌ صفقة خاسرة. راجع النقاط التالية:\n"
        if "مسافة SL" in str(reasons) or "ضرب وقف الخسارة" in str(reasons):
            msg += "   • وسع مسافة وقف الخسارة بناءً على ATR أو الدعم/المقاومة\n"
        if "RSI" in str(reasons) and "تشبع" in str(reasons):
            msg += "   • تجنب الدخول في مناطق التشبع\n"
        if "ADX" in str(reasons) and "ضعيف" in str(reasons):
            msg += "   • تأكد من ADX > 20 قبل الدخول\n"
        if "MACD" in str(reasons) and "تعارض" in str(reasons):
            msg += "   • تأكد من توافق MACD مع اتجاه الصفقة\n"
        if "RR" in str(reasons) and "منخفض" in str(reasons):
            msg += "   • استهدف RR ≥ 2:1\n"
        if "بولينجر" in str(reasons):
            msg += "   • تجنب الدخول عند حدود البولينجر\n"
        if "حجم" in str(reasons) and "منخفض" in str(reasons):
            msg += "   • تأكد من وجود حجم تداول كافٍ\n"
        if "تقييم" in str(reasons) and "ضعيف" in str(reasons):
            msg += "   • تأكد من أن التقييم الشامل > 55% قبل الدخول\n"
        if not lessons and len(reasons) < 3:
            msg += "   • راجع استراتيجيتك بالكامل\n"
    
    msg += "━" * 40 + "\n"
    msg += "💙 القرار النهائي لك يا صديقي. أنا هنا لمساعدتك!"
    
    queue_telegram_message(msg)

def handle_check_position_request(chat_id=None):
    open_trades = {}
    has_open_trade = False

    for asset_type in ["oil", "silver"]:
        open_trade = get_current_open_trade(asset_type)
        if open_trade:
            open_trades[asset_type] = open_trade
            has_open_trade = True

    if not has_open_trade:
        queue_telegram_message("🔄 **لا توجد أي صفقات مفتوحة حالياً.**\n\n💙 **تولين:** السوق هادئ — راقب وانتظر فرصة جيدة.", chat_id)
        return

    msg = "📊 **الصفقات المفتوحة حالياً:**\n"
    msg += "━" * 40 + "\n\n"

    for asset_type, open_trade in open_trades.items():
        asset_label = "النفط" if asset_type == "oil" else "الفضة"
        report = analyze_open_trade(asset_type, open_trade)
        msg += f"🛢️ **{asset_label}**\n" if asset_type == "oil" else f"🥈 **{asset_label}**\n"
        msg += report + "\n"
        msg += "━" * 40 + "\n\n"

    queue_telegram_message(msg, chat_id)

def analyze_open_trade(asset_type, open_trade):
    if not open_trade:
        return "⚠️ لا توجد صفقة مفتوحة"
    
    analysis, report = perform_comprehensive_analysis(asset_type, True, open_trade)
    if not analysis or not isinstance(analysis, dict):
        return "⚠️ لا توجد بيانات كافية للتحليل"
    
    price = analysis.get("price", 0)
    if not isinstance(price, (int, float)) or price <= 0:
        price = open_trade.get("entry_price", 0)
    
    timeframes = analysis.get("timeframes", {}) if isinstance(analysis.get("timeframes"), dict) else {}
    comp_score = analysis.get("comprehensive_score", {}) if isinstance(analysis.get("comprehensive_score"), dict) else {}
    indicators = analysis.get("indicators", {}) if isinstance(analysis.get("indicators"), dict) else {}
    
    entry_price = open_trade.get('entry_price', 0)
    trade_type = open_trade.get('type', 'BUY')
    sl = open_trade.get('sl', 0)
    tp = open_trade.get('tp', 0)
    
    if trade_type == "BUY":
        profit_pct = ((price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
        profit_dollars = AccountingSystem.calculate_profit_dollars(entry_price, price, "BUY")
    else:
        profit_pct = ((entry_price - price) / entry_price) * 100 if entry_price > 0 else 0
        profit_dollars = AccountingSystem.calculate_profit_dollars(entry_price, price, "SELL")
    
    trends = []
    for tf in ["5m", "15m", "1h", "4h"]:
        if tf in timeframes and isinstance(timeframes.get(tf), dict):
            t = timeframes[tf].get("trend", "محايد")
            if t and t != "محايد":
                trends.append((tf, t))
    
    bullish_count = sum(1 for _, t in trends if t == "صاعد")
    bearish_count = sum(1 for _, t in trends if t == "هابط")
    total_trends = len(trends)
    
    tf_15m = timeframes.get("15m", {}) if isinstance(timeframes, dict) else {}
    
    rsi = tf_15m.get("rsi", 50) if isinstance(tf_15m, dict) else 50
    if not isinstance(rsi, (int, float)) or rsi < 0 or rsi > 100:
        rsi = 50
    
    adx = tf_15m.get("adx", 15) if isinstance(tf_15m, dict) else 15
    if not isinstance(adx, (int, float)) or adx < 0 or adx > 100:
        adx = 15
    
    macd = tf_15m.get("macd", 0) if isinstance(tf_15m, dict) else 0
    if not isinstance(macd, (int, float)):
        macd = 0
    
    vol_ratio = tf_15m.get("volume_ratio", 1.0) if isinstance(tf_15m, dict) else 1.0
    if not isinstance(vol_ratio, (int, float)) or vol_ratio < 0:
        vol_ratio = 1.0
    
    vwap = tf_15m.get("vwap", price) if isinstance(tf_15m, dict) else price
    if not isinstance(vwap, (int, float)) or vwap <= 0:
        vwap = price
    
    trend_15m = tf_15m.get("trend", "محايد") if isinstance(tf_15m, dict) else "محايد"
    
    analysis_lines = []
    
    if profit_pct > 0:
        analysis_lines.append(f"✅ **أنت رابح:** {profit_pct:+.2f}% (+${profit_dollars:+.2f})")
    elif profit_pct < 0:
        analysis_lines.append(f"❌ **أنت خاسر:** {profit_pct:+.2f}% (${profit_dollars:+.2f})")
    else:
        analysis_lines.append(f"⚪ **أنت عند التعادل:** {profit_pct:+.2f}%")
    
    analysis_lines.append(f"💰 **سعر الدخول:** ${fmt_price(entry_price, asset_type)}")
    analysis_lines.append(f"💰 **السعر الحالي:** ${fmt_price(price, asset_type)}")
    analysis_lines.append(f"🛡️ **وقف الخسارة:** ${fmt_price(sl, asset_type)}")
    analysis_lines.append(f"🎯 **الهدف:** ${fmt_price(tp, asset_type)}")
    
    if total_trends > 0:
        if trade_type == "SELL" and bullish_count >= 3:
            analysis_lines.append(f"🔴 **تحذير:** {bullish_count}/{total_trends} فريمات صاعدة **ضد صفقتك**!")
            analysis_lines.append("   السوق يصعد بينما أنت تبيع — هذا خطر كبير")
        elif trade_type == "BUY" and bearish_count >= 3:
            analysis_lines.append(f"🔴 **تحذير:** {bearish_count}/{total_trends} فريمات هابطة **ضد صفقتك**!")
            analysis_lines.append("   السوق يهبط بينما أنت تشتري — هذا خطر كبير")
        elif trade_type == "SELL" and bearish_count >= 3:
            analysis_lines.append(f"✅ **جيد:** {bearish_count}/{total_trends} فريمات هابطة **تدعم صفقتك**")
        elif trade_type == "BUY" and bullish_count >= 3:
            analysis_lines.append(f"✅ **جيد:** {bullish_count}/{total_trends} فريمات صاعدة **تدعم صفقتك**")
        else:
            analysis_lines.append(f"🟡 **محايد:** الفريمات متضاربة ({bullish_count} صاعد / {bearish_count} هابط)")
    else:
        analysis_lines.append("🟡 **لا توجد بيانات كافية للفريمات**")
    
    if vol_ratio < 0.6:
        analysis_lines.append(f"🔴 **حجم منخفض:** {vol_ratio:.1f}x المتوسط — الحركة ضعيفة")
        analysis_lines.append("   قد يكون السوق في منطقة تجميع أو تصريف")
    elif vol_ratio > 1.5:
        analysis_lines.append(f"✅ **حجم مرتفع:** {vol_ratio:.1f}x المتوسط — الحركة مدعومة")
    else:
        analysis_lines.append(f"🟡 **حجم طبيعي:** {vol_ratio:.1f}x المتوسط")
    
    if adx < 20:
        analysis_lines.append(f"🔴 **ضعف الاتجاه:** ADX {adx:.0f} — السوق عرضي")
        analysis_lines.append("   لا يوجد اتجاه واضح، أي صفقة الآن مخاطرة")
    elif adx > 25:
        analysis_lines.append(f"✅ **اتجاه قوي:** ADX {adx:.0f} — الاتجاه واضح")
    else:
        analysis_lines.append(f"🟡 **اتجاه متوسط:** ADX {adx:.0f}")
    
    if trade_type == "SELL" and rsi > 70:
        analysis_lines.append(f"✅ **RSI يدعمك:** {rsi:.0f} — منطقة ذروة شراء (فرصة بيع)")
    elif trade_type == "BUY" and rsi < 30:
        analysis_lines.append(f"✅ **RSI يدعمك:** {rsi:.0f} — منطقة ذروة بيع (فرصة شراء)")
    elif trade_type == "SELL" and rsi < 30:
        analysis_lines.append(f"🔴 **RSI ضدك:** {rsi:.0f} — منطقة ذروة بيع (السوق قد يرتد)")
    elif trade_type == "BUY" and rsi > 70:
        analysis_lines.append(f"🔴 **RSI ضدك:** {rsi:.0f} — منطقة ذروة شراء (السوق قد يصحح)")
    else:
        analysis_lines.append(f"🟡 **RSI محايد:** {rsi:.0f}")
    
    if trade_type == "SELL" and macd < 0:
        analysis_lines.append(f"✅ **MACD يدعمك:** سلبي ({macd:.4f})")
    elif trade_type == "BUY" and macd > 0:
        analysis_lines.append(f"✅ **MACD يدعمك:** إيجابي ({macd:.4f})")
    elif trade_type == "SELL" and macd > 0:
        analysis_lines.append(f"🔴 **MACD ضدك:** إيجابي ({macd:.4f})")
    elif trade_type == "BUY" and macd < 0:
        analysis_lines.append(f"🔴 **MACD ضدك:** سلبي ({macd:.4f})")
    else:
        analysis_lines.append(f"🟡 **MACD محايد:** {macd:.4f}")
    
    if trade_type == "SELL":
        dist_to_sl = ((sl - price) / entry_price) * 100 if sl > 0 and entry_price > 0 else 0
        dist_to_tp = ((price - tp) / entry_price) * 100 if tp > 0 and entry_price > 0 else 0
    else:
        dist_to_sl = ((price - sl) / entry_price) * 100 if sl > 0 and entry_price > 0 else 0
        dist_to_tp = ((tp - price) / entry_price) * 100 if tp > 0 and entry_price > 0 else 0
    
    if dist_to_sl < 0.5:
        analysis_lines.append(f"🚨 **خطر:** وقف الخسارة قريب جداً ({dist_to_sl:.2f}%)")
        analysis_lines.append("   أنصح بتضييق الوقف أو الخروج")
    elif dist_to_sl < 1.0:
        analysis_lines.append(f"⚠️ **تنبيه:** وقف الخسارة قريب ({dist_to_sl:.2f}%)")
    
    if dist_to_tp < 0.5:
        analysis_lines.append(f"🎯 **قرب الهدف:** المسافة للهدف {dist_to_tp:.2f}%")
        analysis_lines.append("   فكر في جني الأرباح")
    
    score = comp_score.get("score", 50) if isinstance(comp_score, dict) else 50
    if not isinstance(score, (int, float)):
        score = 50
    
    if score >= 70:
        analysis_lines.append(f"✅ **التقييم الشامل:** {score:.0f}% — قوي")
    elif score >= 55:
        analysis_lines.append(f"🟡 **التقييم الشامل:** {score:.0f}% — متوسط")
    else:
        analysis_lines.append(f"🔴 **التقييم الشامل:** {score:.0f}% — ضعيف")
    
    recommendations = []
    
    if profit_pct > 3:
        recommendations.append("✅ ربح جيد — فكر في جني 50% من الأرباح")
    elif profit_pct > 0.5:
        recommendations.append("🟡 ربح بسيط — حرك الوقف إلى نقطة الدخول")
    elif profit_pct > -0.5:
        recommendations.append("⚪ عند التعادل — انتظر تأكيداً")
    elif profit_pct > -2:
        recommendations.append("🔴 خسارة متوسطة — راقب الوقف عن كثب")
    else:
        recommendations.append("🚨 خسارة كبيرة — فكر في الخروج")
    
    if trade_type == "SELL" and bullish_count >= 3:
        recommendations.append("🔴 الفريمات ضدك — أنصح بالخروج")
    elif trade_type == "BUY" and bearish_count >= 3:
        recommendations.append("🔴 الفريمات ضدك — أنصح بالخروج")
    elif vol_ratio < 0.6 and score < 50:
        recommendations.append("⚠️ حجم منخفض + تقييم ضعيف — انتظر تأكيداً")
    elif adx < 20:
        recommendations.append("⚠️ ADX ضعيف — لا تتسرع")
    
    if dist_to_sl < 0.5:
        recommendations.append("🚨 وقف الخسارة قريب جداً — جهز للخروج")
    
    lines = []
    lines.append(f"📊 **تحليل صفقة {asset_type}**")
    lines.append("━" * 45)
    lines.append("")
    
    lines.append("📌 **ملخص الموقف:**")
    if profit_pct > 0:
        lines.append(f"   ✅ ربح {profit_pct:+.2f}% (${profit_dollars:+.2f})")
    elif profit_pct < 0:
        lines.append(f"   ❌ خسارة {profit_pct:+.2f}% (${profit_dollars:+.2f})")
    else:
        lines.append(f"   ⚪ تعادل")
    lines.append("")
    
    lines.append("🔍 **تحليل الموقف:**")
    for line in analysis_lines[:10]:
        lines.append(f"   {line}")
    lines.append("")
    
    lines.append("💡 **توصيات تولين:**")
    if recommendations:
        for rec in recommendations[:4]:
            lines.append(f"   {rec}")
    else:
        lines.append("   🟡 راقب الصفقة — لا يوجد قرار عاجل")
    lines.append("")
    
    lines.append("━" * 45)
    lines.append("💙 القرار النهائي لك... أنا هنا لمساعدتك في التفكير")
    
    return "\n".join(lines)

def generate_intelligence_report():
    try:
        if TONA_ELITE_AVAILABLE and TONA_ELITE_ENGINE:
            result = TONA_ELITE_ENGINE.generate_elite_analysis()
            if result and len(result) > 50:
                return result
            else:
                logger.warning("⚠️ Tona Elite Engine أعاد نتيجة فارغة أو قصيرة")
                return "🧠 **تقرير استخباراتي:**\n\n⚠️ لم يتم الحصول على بيانات كافية من محرك الاستخبارات حالياً."
        else:
            logger.warning("⚠️ Tona Elite Engine غير متوفر")
            return "🧠 **تقرير استخباراتي:**\n\n⚠️ محرك الاستخبارات غير متوفر حالياً. يرجى التحقق من تهيئة Tona Elite Engine."
    except Exception as e:
        logger.error(f"❌ خطأ في التقرير الاستخباراتي: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return f"⚠️ حدث خطأ أثناء توليد التقرير الاستخباراتي: {str(e)[:100]}"

def handle_deep_analysis(chat_id):
    try:
        if not DEEP_ANALYZER_AVAILABLE or not DEEP_ANALYZER:
            queue_telegram_message("⚠️ نظام التحليل العميق غير متوفر حالياً", chat_id)
            return
        
        queue_telegram_message("🔍 جاري تحليل جميع الصفقات العميقة...", chat_id)
        
        oil_analysis = DEEP_ANALYZER.analyze_all_trades("oil")
        silver_analysis = DEEP_ANALYZER.analyze_all_trades("silver")
        
        msg = "🔍 **تقرير التحليل العميق**\n"
        msg += "━" * 35 + "\n\n"
        
        msg += "🛢️ **النفط الخام**\n"
        if oil_analysis and oil_analysis.get('error'):
            msg += f"⚠️ {oil_analysis['error']}\n\n"
        elif oil_analysis:
            stats = oil_analysis.get('total_stats', {})
            msg += f"📊 عدد الصفقات: {stats.get('total_trades', 0)}\n"
            msg += f"📈 نسبة النجاح: {stats.get('win_rate', 0):.1f}%\n"
            msg += f"💰 متوسط الربح: ${stats.get('avg_profit', 0):.2f}\n"
            patterns = oil_analysis.get('success_patterns', [])
            if patterns and patterns[0] != 'لا توجد بيانات كافية':
                msg += "\n✅ **أنماط النجاح:**\n"
                for p in patterns[:3]:
                    msg += f"   • {p}\n"
            failures = oil_analysis.get('failure_patterns', [])
            if failures and failures[0] != 'لا توجد بيانات كافية':
                msg += "\n❌ **أنماط الفشل:**\n"
                for f in failures[:3]:
                    msg += f"   • {f}\n"
        else:
            msg += "⚠️ لا توجد بيانات كافية لتحليل النفط\n"
        
        msg += "\n" + "━" * 35 + "\n\n"
        
        msg += "🥈 **الفضة**\n"
        if silver_analysis and silver_analysis.get('error'):
            msg += f"⚠️ {silver_analysis['error']}\n"
        elif silver_analysis:
            stats = silver_analysis.get('total_stats', {})
            msg += f"📊 عدد الصفقات: {stats.get('total_trades', 0)}\n"
            msg += f"📈 نسبة النجاح: {stats.get('win_rate', 0):.1f}%\n"
            msg += f"💰 متوسط الربح: ${stats.get('avg_profit', 0):.2f}\n"
            best_rsi = silver_analysis.get('best_entry_rsi', {})
            if best_rsi.get('best_range'):
                msg += f"🎯 أفضل RSI: {best_rsi['best_range']} (نسبة نجاح {best_rsi.get('best_win_rate', 0):.1f}%)\n"
        else:
            msg += "⚠️ لا توجد بيانات كافية لتحليل الفضة\n"
        
        queue_telegram_message(msg[:4000], chat_id)
        
    except Exception as e:
        logger.error(f"❌ خطأ في التحليل العميق: {e}")
        import traceback
        logger.error(traceback.format_exc())
        queue_telegram_message(f"⚠️ حدث خطأ أثناء التحليل العميق: {str(e)[:100]}", chat_id)
       
# ====================================================================================
# نهاية PART 23
# ====================================================================================

# ====================================================================================
# 📦 PART 24: نظام المحادثة الذكي - SmartConversationManager (مع Gemini + Groq + أخبار)
# ====================================================================================

"""
🧠 SmartConversationManager - الوكيل الذكي المتكامل (V3.2 - التعديل النهائي)
─────────────────────────────────────────────────────────────────
يقوم بتحويل البوت إلى مستشار بشري واعي، قادر على:
- فهم أي سؤال بأي صياغة (باستخدام نماذج Groq/Gemini)
- استدعاء دوال البوت الداخلية للحصول على بيانات حية
- إدارة سياق المحادثة لكل مستخدم
- الرد على الأسئلة العامة (خارج نطاق التداول) بذكاء
- الحفاظ على هوية تولين كخبيرة تداول ودودة
- ⛔ منع تام لاختلاق البيانات الوهمية
- 📰 دمج الأخبار الذكي مع ربطها بالشارت والتأثير الفعلي
- ✅ استخدام المتغيرات العامة الموحدة لأسماء الجداول من PART 10
- ✅ إصلاح جذري لـ generate_prior_judgment: حساب التقييم مباشرة من المؤشرات
- ✅ إصلاح دوال التوقعات: استخدام SUPABASE_DB.supabase مباشرة بدلاً من _get_supabase_client
─────────────────────────────────────────────────────────────────
"""

import json
import re
import requests
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

# ============================================================================
# استيراد Gemini (اختياري)
# ============================================================================

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

# ============================================================================
# استيراد محرك الأخبار (Tona Elite Intelligence)
# ============================================================================

try:
    from tona_intelligence import TonaEliteEngine
    TONA_INTELLIGENCE_AVAILABLE = True
except ImportError:
    TONA_INTELLIGENCE_AVAILABLE = False
    TonaEliteEngine = None


# ============================================================================
# 1. دالة بناء السياق (للاستخدام داخل SmartConversationManager)
# ============================================================================

def build_chat_context(text: str, chat_id: str) -> Dict:
    """يجمع السياق من جميع المحركات المتاحة (بما فيها TCN) لاستخدامه في المحادثة الذكية."""
    context = {
        "user_message": text,
        "timestamp": datetime.now().isoformat(),
        "chat_id": chat_id,
        "intent": None,
        "intent_confidence": 0.5,
        "sentiment": None,
        "entities": [],
        "is_question": False,
        "is_command": False,
        "signal_intent": None,
        "risk_level": "moderate",
        "chat_history": [],
        "open_trades": {},
        "recent_closed_trades": [],
        "market_snapshot": {},
        "prometheus_emotion": "neutral",
        "prometheus_confidence": 0.5,
        "prometheus_energy": 0.5,
        "prometheus_memories": [],
        "prometheus_lessons": [],
        "discovered_patterns": [],
        "recent_lessons": [],
        "recent_warnings": [],
        "risk_status": None,
        "user_profile": {},
        "persona": {},
        "persona_mood": "neutral",
        "persona_emotion": "neutral",
        "market_context": {},
        "recent_events": [],
        "patterns": [],
        "predictions": {},
        "narrative": {},
        "chronos": {},
        "oracle": {},
        "regime_oil": None,
        "regime_silver": None,
        "conversation_state": {},
        "last_trade": None,
        "news_analysis": None
    }

    # 1. Intent Classifier
    if INTENT_AVAILABLE and INTENT_CLASSIFIER:
        try:
            if hasattr(INTENT_CLASSIFIER, 'classify_with_confidence'):
                intent, confidence = INTENT_CLASSIFIER.classify_with_confidence(text)
                context["intent"] = intent
                context["intent_confidence"] = confidence
            elif hasattr(INTENT_CLASSIFIER, 'classify'):
                context["intent"] = INTENT_CLASSIFIER.classify(text)
                context["intent_confidence"] = 0.8
            logger.info(f"🎯 النية: {context['intent']} (ثقة: {context['intent_confidence']:.0%})")
        except Exception as e:
            logger.warning(f"⚠️ Intent فشل: {e}")
            context["intent"] = "general"

    # 2. Language Understanding
    if LANGUAGE_AVAILABLE and LANGUAGE_UNDERSTANDING:
        try:
            if hasattr(LANGUAGE_UNDERSTANDING, 'get_understanding_summary'):
                lang_result = LANGUAGE_UNDERSTANDING.get_understanding_summary(text)
                context["sentiment"] = lang_result.get("emotion", "neutral")
                context["entities"] = lang_result.get("entities", [])
                context["is_question"] = lang_result.get("is_question", False)
                context["is_command"] = lang_result.get("is_command", False)
                context["signal_intent"] = lang_result.get("signal_intent", None)
                context["risk_level"] = lang_result.get("risk_level", "moderate")
            elif hasattr(LANGUAGE_UNDERSTANDING, 'analyze'):
                lang_result = LANGUAGE_UNDERSTANDING.analyze(text)
                context["sentiment"] = lang_result.get("sentiment", "neutral")
                context["entities"] = lang_result.get("entities", [])
            logger.info(f"🗣️ المشاعر: {context['sentiment']}")
        except Exception as e:
            logger.warning(f"⚠️ Language فشل: {e}")
            context["sentiment"] = "neutral"

    # 3. Persona
    if PERSONA_AVAILABLE and PERSONA:
        try:
            if hasattr(PERSONA, 'analyze_user_emotion'):
                context["persona_emotion"] = PERSONA.analyze_user_emotion(text)
            if hasattr(PERSONA, 'get_persona_description'):
                context["persona"] = PERSONA.get_persona_description()
            if hasattr(PERSONA, 'get_current_mood'):
                context["persona_mood"] = PERSONA.get_current_mood()
            elif hasattr(PERSONA, 'get_mood'):
                context["persona_mood"] = PERSONA.get_mood()
            logger.info(f"👤 شخصية تولين: {context['persona_mood']}")
        except Exception as e:
            logger.warning(f"⚠️ Persona فشل: {e}")

    # 4. Memory
    if MEMORY_AVAILABLE and MEMORY:
        try:
            if hasattr(MEMORY, 'get_recent'):
                context["chat_history"] = MEMORY.get_recent(chat_id, limit=20)
            elif hasattr(MEMORY, 'get_conversation'):
                context["chat_history"] = MEMORY.get_conversation(chat_id, limit=20)
            if hasattr(MEMORY, 'get_profile'):
                context["user_profile"] = MEMORY.get_profile(chat_id)
            logger.info(f"💾 تم استرجاع {len(context['chat_history'])} رسالة")
        except Exception as e:
            logger.warning(f"⚠️ Memory فشل: {e}")

    # 5. Prometheus
    if PROMETHEUS_AVAILABLE and PROMETHEUS:
        try:
            if hasattr(PROMETHEUS, 'get_emotion'):
                emotion_data = PROMETHEUS.get_emotion()
                context["prometheus_emotion"] = emotion_data.get('dominant', 'neutral')
                context["prometheus_confidence"] = emotion_data.get('confidence', 0.5)
                context["prometheus_energy"] = emotion_data.get('energy', 0.5)
            elif hasattr(PROMETHEUS, 'emotion'):
                if hasattr(PROMETHEUS.emotion, 'dominant'):
                    context["prometheus_emotion"] = PROMETHEUS.emotion.dominant()
                context["prometheus_confidence"] = getattr(PROMETHEUS.emotion, 'confidence', 0.5)
                context["prometheus_energy"] = getattr(PROMETHEUS.emotion, 'energy', 0.5)

            if hasattr(PROMETHEUS, 'get_recent_memories'):
                context["prometheus_memories"] = PROMETHEUS.get_recent_memories(10)
            if hasattr(PROMETHEUS, 'get_lessons_learned'):
                context["prometheus_lessons"] = PROMETHEUS.get_lessons_learned()
            logger.info(f"💙 مشاعر تولين: {context['prometheus_emotion']}")
        except Exception as e:
            logger.warning(f"⚠️ Prometheus فشل: {e}")

    # 6. الصفقات المفتوحة
    for asset in ["oil", "silver"]:
        try:
            trade = get_current_open_trade(asset)
            if trade:
                context["open_trades"][asset] = trade
        except Exception as e:
            logger.warning(f"⚠️ فشل جلب صفقة {asset}: {e}")

    # 7. الصفقات المغلقة الأخيرة (آخر 10 لكل أصل)
    try:
        for asset in ["oil", "silver"]:
            history = load_trades_history(asset)
            trades = history.get('trades', [])
            closed = [t for t in trades if t.get('status') == 'closed']
            if closed:
                context["recent_closed_trades"].extend(closed[-5:])
    except Exception as e:
        logger.warning(f"⚠️ فشل جلب التاريخ: {e}")

    # 8. آخر صفقة مغلقة (للتحليل)
    try:
        last_trade = get_last_closed_trade()
        if last_trade:
            context["last_trade"] = {
                "asset": last_trade.get('asset', 'unknown'),
                "type": last_trade.get('type', 'UNKNOWN'),
                "entry": last_trade.get('entry_price', 0),
                "exit": last_trade.get('exit_price', 0),
                "profit": last_trade.get('profit_dollars', 0),
                "exit_reason": last_trade.get('exit_reason', 'غير معروف'),
                "timestamp": last_trade.get('timestamp', '')
            }
    except Exception as e:
        logger.warning(f"⚠️ فشل جلب آخر صفقة: {e}")

    # 9. Market Snapshot (مع التخزين المؤقت)
    try:
        for asset in ["oil", "silver"]:
            try:
                analysis = None
                cache_key = f"{asset}_{int(time.time() // 30)}"
                if cache_key in ANALYSIS_CACHE:
                    analysis = ANALYSIS_CACHE[cache_key].get('analysis')
                else:
                    analysis, _ = perform_comprehensive_analysis(asset, False, None)
                    if analysis:
                        set_cached_analysis(asset, analysis)
                
                if analysis:
                    price = analysis.get("price", 0)
                    if price > 0:
                        context["market_snapshot"][asset] = {
                            "price": price,
                            "signal": analysis.get("signal", "WAIT"),
                            "trend": analysis.get("indicators", {}).get("trend", {}).get("current_trend", "neutral"),
                            "rsi": analysis.get("indicators", {}).get("momentum", {}).get("rsi", 0),
                            "adx": analysis.get("indicators", {}).get("trend", {}).get("adx", 0),
                            "macd": analysis.get("indicators", {}).get("momentum", {}).get("macd", 0),
                            "atr": analysis.get("timeframes", {}).get("15m", {}).get("atr", 0),
                            "vwap": analysis.get("timeframes", {}).get("15m", {}).get("vwap", 0),
                            "fear_greed": analysis.get("fear_greed", 50),
                            "score": analysis.get("comprehensive_score", {}).get("score", 50),
                            "grade": analysis.get("comprehensive_score", {}).get("grade", "محايد")
                        }
            except Exception as e:
                logger.warning(f"⚠️ فشل جلب بيانات {asset}: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Market Snapshot فشل: {e}")

    # 10. أنماط التعلم والدروس
    if PATTERN_DISCOVERY_AVAILABLE and PATTERN_DISCOVERY:
        try:
            if hasattr(PATTERN_DISCOVERY, 'get_best_patterns'):
                context["discovered_patterns"] = PATTERN_DISCOVERY.get_best_patterns(3)
        except Exception as e:
            logger.warning(f"⚠️ Pattern Discovery فشل: {e}")

    if POST_MORTEM_AVAILABLE and POST_MORTEM:
        try:
            if hasattr(POST_MORTEM, 'get_recent_lessons'):
                context["recent_lessons"] = POST_MORTEM.get_recent_lessons(5)
        except Exception as e:
            logger.warning(f"⚠️ Post Mortem فشل: {e}")

    # 11. سجل التحذيرات الأخيرة
    try:
        context["recent_warnings"] = get_recent_warnings(5)
    except Exception as e:
        logger.warning(f"⚠️ Warnings فشل: {e}")

    # 12. Context Memory
    if CONTEXT_AVAILABLE and CONTEXT_MEMORY:
        try:
            if hasattr(CONTEXT_MEMORY, 'get_market_context'):
                context["market_context"] = CONTEXT_MEMORY.get_market_context()
            elif hasattr(CONTEXT_MEMORY, 'get_context'):
                context["market_context"] = CONTEXT_MEMORY.get_context()
            if hasattr(CONTEXT_MEMORY, 'get_recent_events'):
                context["recent_events"] = CONTEXT_MEMORY.get_recent_events(10)
            if hasattr(CONTEXT_MEMORY, 'get_current_regime'):
                for asset in ["oil", "silver"]:
                    regime = CONTEXT_MEMORY.get_current_regime(asset)
                    if regime:
                        context[f"regime_{asset}"] = regime
        except Exception as e:
            logger.warning(f"⚠️ Context Memory فشل: {e}")

    # 13. بقية المحركات
    if RISK_MASTER_AVAILABLE and RISK_MASTER:
        try:
            if hasattr(RISK_MASTER, 'get_current_status'):
                context["risk_status"] = RISK_MASTER.get_current_status()
            elif hasattr(RISK_MASTER, 'get_status'):
                context["risk_status"] = RISK_MASTER.get_status()
        except Exception as e:
            logger.warning(f"⚠️ Risk Master فشل: {e}")

    if CHRONOS_AVAILABLE and CHRONOS:
        try:
            if hasattr(CHRONOS, 'get_temporal_context'):
                context["chronos"] = CHRONOS.get_temporal_context()
        except Exception as e:
            logger.warning(f"⚠️ Chronos فشل: {e}")

    if ORACLE_AVAILABLE and ORACLE:
        try:
            if hasattr(ORACLE, 'get_predictions'):
                context["oracle"] = ORACLE.get_predictions(context)
            elif hasattr(ORACLE, 'generate_prediction'):
                context["oracle"] = ORACLE.generate_prediction("oil", {})
        except Exception as e:
            logger.warning(f"⚠️ Oracle فشل: {e}")

    if PATTERN_AVAILABLE and PATTERN_ANALYZER:
        try:
            if hasattr(PATTERN_ANALYZER, 'get_patterns'):
                context["patterns"] = PATTERN_ANALYZER.get_patterns(context.get("market_context", {}))
        except Exception as e:
            logger.warning(f"⚠️ Pattern Analyzer فشل: {e}")

    if PREDICTOR_AVAILABLE and PREDICTOR:
        try:
            if hasattr(PREDICTOR, 'get_predictions'):
                context["predictions"] = PREDICTOR.get_predictions(context.get("market_context", {}))
        except Exception as e:
            logger.warning(f"⚠️ Predictor فشل: {e}")

    # ✅ 14. جلب تحليل الأخبار (إذا كان المحرك متاحاً)
    if TONA_INTELLIGENCE_AVAILABLE and TonaEliteEngine:
        try:
            engine = TonaEliteEngine(groq_api_key=GROQ_API_KEY)
            news_list = engine.fetch_targeted_intelligence(hours=10)
            if news_list:
                prices = engine.link_news_to_prices()
                oil_price = prices.get("oil", {}).get("price", 0)
                silver_price = prices.get("silver", {}).get("price", 0)
                
                analyzed = []
                for news in news_list[:5]:
                    if not isinstance(news, dict):
                        continue
                    analysis = engine.analyze_news_impact(news)
                    pub_time = news.get('published_at', '')
                    time_str = ""
                    if pub_time:
                        try:
                            dt = datetime.fromisoformat(pub_time.replace('Z', '+00:00'))
                            time_str = dt.strftime('%H:%M')
                        except:
                            pass
                    
                    oil_real = analysis.get('oil_real', {})
                    silver_real = analysis.get('silver_real', {})
                    
                    oil_impact = oil_real.get('impact', 'غير معروف')
                    silver_impact = silver_real.get('impact', 'غير معروف')
                    oil_change = oil_real.get('change', 0)
                    silver_change = silver_real.get('change', 0)
                    
                    is_significant = oil_real.get('is_significant', False) or silver_real.get('is_significant', False)
                    
                    analyzed.append({
                        "news": news,
                        "analysis": analysis,
                        "published_at": pub_time,
                        "time_str": time_str,
                        "title": news.get('title', ''),
                        "title_ar": news.get('title_ar', ''),
                        "oil_impact": oil_impact,
                        "silver_impact": silver_impact,
                        "oil_change": oil_change,
                        "silver_change": silver_change,
                        "is_significant": is_significant,
                        "severity": analysis.get('severity', 'منخفض')
                    })
                context["news_analysis"] = analyzed
                logger.info(f"📰 تم جلب وتحليل {len(analyzed)} خبر")
        except Exception as e:
            logger.warning(f"⚠️ فشل جلب تحليل الأخبار: {e}")

    return context


# ============================================================================
# 2. دالة تلخيص التحليل للنموذج اللغوي
# ============================================================================

def summarize_for_ai(analysis: dict, asset: str) -> str:
    """تُلخّص التحليل الفني للنموذج اللغوي بأسلوب ذكي بدون أرقام خام."""
    if not analysis:
        return f"لا يوجد تحليل متاح لـ {asset}."

    score = analysis.get('comprehensive_score', {}).get('score', 50)
    grade = analysis.get('comprehensive_score', {}).get('grade', 'محايد')
    trend = analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')
    signal = analysis.get('signal', 'WAIT')
    price = analysis.get('price', 0)

    rsi = analysis.get('indicators', {}).get('momentum', {}).get('rsi', 50)
    if rsi > 70:
        momentum = "زخم قوي جداً (قرب ذروة الشراء)"
    elif rsi > 60:
        momentum = "زخم إيجابي"
    elif rsi > 40:
        momentum = "زخم محايد"
    elif rsi > 30:
        momentum = "زخم ضعيف"
    else:
        momentum = "زخم ضعيف جداً (قرب ذروة البيع)"

    adx = analysis.get('indicators', {}).get('trend', {}).get('adx', 25)
    if adx > 40:
        trend_strength = "اتجاه قوي جداً"
    elif adx > 25:
        trend_strength = "اتجاه واضح"
    else:
        trend_strength = "اتجاه ضعيف / تذبذب"

    atr = analysis.get('timeframes', {}).get('15m', {}).get('atr', 0)
    if atr > 0:
        volatility = f"تقلب عالٍ" if atr > price * 0.005 else f"تقلب منخفض"
    else:
        volatility = "تقلب غير معروف"

    fg = analysis.get('fear_greed', 50)
    if fg > 75:
        sentiment = "جشع شديد"
    elif fg > 60:
        sentiment = "تفاؤل"
    elif fg > 40:
        sentiment = "حيادية"
    elif fg > 25:
        sentiment = "خوف"
    else:
        sentiment = "خوف شديد"

    return f"""📊 تحليل {asset}:
• السعر الحالي: ${price:.2f}
• الاتجاه: {trend} ({trend_strength})
• الإشارة: {signal}
• الزخم: {momentum}
• المشاعر السوقية: {sentiment}
• التقلب: {volatility}
• التقييم العام: {grade} ({score}/100)
"""


# ============================================================================
# 3. تعريف الأدوات (Tools)
# ============================================================================

TOOLS_DESCRIPTIONS = """
📌 الأدوات المتاحة (اختر الأداة المناسبة بناءً على فهمك لنية المستخدم):

1. get_open_trades() - استخدمها عندما يسأل المستخدم عن الصفقات المفتوحة.
2. get_market_analysis(asset_type) - استخدمها عندما يطلب تحليلاً مفصلاً لأصل واحد.
3. get_both_markets_analysis() - استخدمها عندما يسأل عن السوق بشكل عام (سعر + تحليل).
4. get_todays_profit_loss() - استخدمها عندما يسأل عن أرباح اليوم.
5. get_profit_loss_by_date(days_ago) - استخدمها عندما يسأل عن أرباح يوم محدد.
6. get_trade_recommendation(asset_type) - استخدمها عندما يطلب توصية تداولية.
7. get_learning_insights() - استخدمها عندما يسأل عن الدروس المستفادة.
8. analyze_current_trade_health(asset_type) - استخدمها عندما يسأل عن صفقة مفتوحة محددة.
9. get_general_statistics() - استخدمها عندما يطلب إحصائيات عامة.
10. execute_close_trade(asset_type) - استخدمها عندما يطلب إغلاق صفقة (بعد التأكد).
11. get_intelligence_report() - استخدمها عندما يسأل عن الأخبار المؤثرة.
12. get_price_prediction(asset_type, timeframe) - استخدمها عندما يسأل عن توقعات الأسعار.
13. get_trade_details(asset_type, trade_id) - استخدمها عندما يسأل عن صفقة محددة بالتفصيل.
14. get_worst_best_trade(asset_type, period) - استخدمها عندما يسأل عن أفضل/أسوأ صفقة.
15. get_asset_comparison() - استخدمها عندما يسأل عن مقارنة بين النفط والفضة.
16. get_trade_history_summary(days) - استخدمها عندما يسأل عن ملخص فترة.
17. explain_decision(asset_type, decision_type) - استخدمها عندما يسأل "لماذا" (لماذا أغلقت، لماذا فتحت...).
18. get_weekly_report() - استخدمها عندما يطلب تقرير أسبوعي.
19. get_market_correlation() - استخدمها عندما يسأل عن علاقة النفط بالفضة.
20. modify_trade_sl_tp(asset_type, new_sl, new_tp) - استخدمها عندما يطلب تعديل وقف/هدف.
"""


# ============================================================================
# 4. تنفيذ الأدوات
# ============================================================================

def save_current_trade(asset_type: str, trade_data: dict) -> bool:
    """حفظ الصفقة المفتوحة (دالة مساعدة)"""
    pos_file = get_position_file(asset_type)
    try:
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(trade_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ الصفقة {asset_type}: {e}")
        return False


def tool_get_open_trades() -> str:
    """تنفيذ أداة get_open_trades - إرجاع الصفقات المفتوحة مع أرباحها"""
    result = {}
    for asset in ["oil", "silver"]:
        trade = get_current_open_trade(asset)
        if trade:
            entry = trade.get('entry_price', 0)
            trade_type = trade.get('type', 'BUY')
            price = 0
            try:
                symbol = "USOIL_USDT" if asset == "oil" else "SILVER_USDT"
                data = get_mexc_candles(symbol, "Min1", 5)
                if data and data.get("closes"):
                    price = data["closes"][-1]
            except:
                price = entry
            if price and entry:
                profit = AccountingSystem.calculate_profit_dollars(entry, price, trade_type)
                profit_pct = ((price - entry) / entry * 100) if trade_type == "BUY" else ((entry - price) / entry * 100)
            else:
                profit = 0
                profit_pct = 0
            result[asset] = {
                "type": trade_type,
                "entry_price": entry,
                "current_price": price,
                "profit_dollars": profit,
                "profit_pct": profit_pct,
                "sl": trade.get('sl', 0),
                "tp": trade.get('tp', 0),
                "rr": trade.get('rr', 0)
            }
    if not result:
        return json.dumps({"status": "no_open_trades", "message": "لا توجد أي صفقات مفتوحة حالياً."}, ensure_ascii=False)
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_market_analysis(asset_type: str, context_cache: dict = None) -> str:
    """تحليل فني شامل لأصل واحد مع جميع المؤشرات"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    if context_cache and asset_type in context_cache:
        cached = context_cache[asset_type]
        if cached.get("price", 0) > 0:
            return json.dumps(cached, ensure_ascii=False, indent=2)

    analysis, _ = perform_comprehensive_analysis(asset_type, False, None)
    if not analysis:
        return json.dumps({"status": "error", "message": f"⚠️ تعذر الحصول على تحليل {asset_type}"}, ensure_ascii=False)
    return json.dumps(analysis, ensure_ascii=False, indent=2)


def tool_get_both_markets_analysis(context_cache: dict = None) -> str:
    """تحليل فني شامل لكلا الأصلين مع الأسعار الحالية"""
    result = {}
    for asset in ["oil", "silver"]:
        analysis = None
        if context_cache and asset in context_cache:
            cached = context_cache[asset]
            if cached.get("price", 0) > 0:
                result[asset] = {
                    "price": cached.get("price", 0),
                    "trend": cached.get("trend", "محايد"),
                    "signal": cached.get("signal", "WAIT"),
                    "score": cached.get("score", 50),
                    "grade": cached.get("grade", "محايد"),
                    "rsi": cached.get("rsi", 50),
                    "adx": cached.get("adx", 15),
                    "volatility": "متوسط"
                }
                continue

        analysis, _ = perform_comprehensive_analysis(asset, False, None)
        if analysis:
            comp_score = analysis.get('comprehensive_score', {})
            indicators = analysis.get('indicators', {})
            tf_15m = analysis.get('timeframes', {}).get('15m', {})
            
            price = analysis.get('price', 0)
            if price == 0:
                price = tf_15m.get('price', 0)
            
            result[asset] = {
                "price": price,
                "trend": indicators.get('trend', {}).get('current_trend', 'محايد'),
                "signal": analysis.get('signal', 'WAIT'),
                "score": comp_score.get('score', 50),
                "grade": comp_score.get('grade', 'محايد'),
                "rsi": tf_15m.get('rsi', 50),
                "adx": tf_15m.get('adx', 15),
                "volatility": "مرتفع" if tf_15m.get('atr', 0) > price * 0.005 else "منخفض"
            }
        else:
            result[asset] = None
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_todays_profit_loss() -> str:
    """إجمالي ربح/خسارة اليوم من الصفقات المغلقة"""
    total = 0.0
    today = datetime.now().date()
    for asset in ["oil", "silver"]:
        history = load_trades_history(asset)
        for trade in history.get('trades', []):
            if trade.get('status') == 'closed':
                exit_time = trade.get('exit_timestamp', '')
                if exit_time:
                    try:
                        exit_date = datetime.fromisoformat(exit_time).date()
                        if exit_date == today:
                            total += trade.get('profit_dollars', 0)
                    except:
                        pass
    if total == 0:
        return "ربح/خسارة اليوم: $0.00 (لا توجد صفقات مغلقة اليوم)"
    return f"ربح/خسارة اليوم: ${total:.2f}"


def tool_get_profit_loss_by_date(days_ago: int) -> str:
    """ربح/خسارة يوم معين"""
    if days_ago < 0:
        return "days_ago يجب أن يكون 0 أو أكثر"
    target_date = (datetime.now() - timedelta(days=days_ago)).date()
    total = 0.0
    for asset in ["oil", "silver"]:
        history = load_trades_history(asset)
        for trade in history.get('trades', []):
            if trade.get('status') == 'closed':
                exit_time = trade.get('exit_timestamp', '')
                if exit_time:
                    try:
                        exit_date = datetime.fromisoformat(exit_time).date()
                        if exit_date == target_date:
                            total += trade.get('profit_dollars', 0)
                    except:
                        pass
    day_label = "اليوم" if days_ago == 0 else "الأمس" if days_ago == 1 else f"قبل {days_ago} أيام"
    if total == 0:
        return f"ربح/خسارة {day_label}: $0.00 (لا توجد صفقات مغلقة في ذلك اليوم)"
    return f"ربح/خسارة {day_label}: ${total:.2f}"


def tool_get_trade_recommendation(asset_type: str, context_cache: dict = None) -> str:
    """توصية تداولية مع درجة الثقة"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    if context_cache and asset_type in context_cache:
        analysis = {
            "price": context_cache[asset_type].get("price", 0),
            "comprehensive_score": {
                "score": context_cache[asset_type].get("score", 50),
                "grade": context_cache[asset_type].get("grade", "محايد")
            },
            "indicators": {
                "trend": {"current_trend": context_cache[asset_type].get("trend", "محايد")}
            }
        }
    else:
        analysis, _ = perform_comprehensive_analysis(asset_type, False, None)
        if not analysis:
            return json.dumps({"status": "error", "message": f"⚠️ تعذر الحصول على تحليل {asset_type}"}, ensure_ascii=False)

    comp_score = analysis.get('comprehensive_score', {})
    score = comp_score.get('score', 50)
    grade = comp_score.get('grade', 'محايد')
    details = comp_score.get('details', [])

    if score >= 70:
        recommendation = "شراء قوي ✅"
        confidence = 80 + (score - 70) * 0.5
    elif score >= 60:
        recommendation = "شراء مع حذر 🟡"
        confidence = 60 + (score - 60) * 0.8
    elif score >= 45:
        recommendation = "انتظار ⚪"
        confidence = 50
    elif score >= 35:
        recommendation = "تجنب الشراء 🟠"
        confidence = 40 + (45 - score) * 0.8
    else:
        recommendation = "بيع أو تجنب 🔴"
        confidence = 30 + (35 - score) * 0.5

    confidence = min(95, max(30, confidence))

    result = {
        "asset": asset_type,
        "recommendation": recommendation,
        "confidence": round(confidence, 1),
        "score": score,
        "grade": grade,
        "key_factors": details[:2] if details else []
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_learning_insights() -> str:
    """ملخص ما تعلمه البوت من الصفقات"""
    insights = []
    if PATTERN_DISCOVERY_AVAILABLE and PATTERN_DISCOVERY:
        try:
            patterns = PATTERN_DISCOVERY.get_best_patterns(5)
            if patterns:
                for p in patterns:
                    insights.append(f"• {p.get('pattern_name')}: نسبة نجاح {p.get('win_rate', 0):.1f}%")
            else:
                insights.append("• لا توجد أنماط مكتشفة بعد")
        except:
            insights.append("• تعذر جلب الأنماط المكتشفة")
    else:
        insights.append("• نظام اكتشاف الأنماط غير متوفر")

    if POST_MORTEM_AVAILABLE and POST_MORTEM:
        try:
            if hasattr(POST_MORTEM, 'get_recent_lessons'):
                lessons = POST_MORTEM.get_recent_lessons(3)
                for lesson in lessons:
                    insights.append(f"• درس مستفاد: {lesson}")
        except:
            pass

    return "🧠 **رؤى التعلم:**\n" + "\n".join(insights) if insights else "🧠 **رؤى التعلم:**\nلا توجد رؤى حالياً."


def tool_analyze_current_trade_health(asset_type: str) -> str:
    """تحليل صحة الصفقة المفتوحة وتوصية"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        return json.dumps({"status": "no_open_trade", "message": f"⚠️ لا توجد صفقة {asset_type} مفتوحة حالياً."}, ensure_ascii=False)

    report = analyze_open_trade(asset_type, open_trade)
    if not report:
        return json.dumps({"status": "error", "message": f"⚠️ تعذر تحليل صفقة {asset_type}"}, ensure_ascii=False)

    recommendation = "انتظار"
    confidence = 50
    reasons = []

    if "خسارة" in report and "كبيرة" in report:
        recommendation = "إغلاق فوري"
        confidence = 80
        reasons.append("الخسارة كبيرة وتتجاوز الحد المقبول")
    elif "ربح" in report and "جيد" in report:
        recommendation = "استمرار مع جني أرباح جزئية"
        confidence = 70
        reasons.append("الربح جيد، يمكن جني جزء والأبقاء على الباقي")
    elif "قريب" in report and "وقف" in report:
        recommendation = "مراقبة مكثفة"
        confidence = 65
        reasons.append("الوقف قريب، جهز للإغلاق إذا لزم")
    elif "عكس" in report or "ضد" in report:
        recommendation = "إغلاق"
        confidence = 75
        reasons.append("الاتجاه يعاكس الصفقة")
    else:
        recommendation = "استمرار"
        confidence = 55
        reasons.append("لا توجد إشارة واضحة للخروج")

    result = {
        "asset": asset_type,
        "recommendation": recommendation,
        "confidence": confidence,
        "reasons": reasons,
        "detailed_report": report[:500]
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_general_statistics() -> str:
    """إحصائيات الأداء العامة"""
    total_trades = 0
    total_wins = 0
    total_losses = 0
    total_profit = 0.0
    for asset in ["oil", "silver"]:
        stats = calculate_statistics(asset)
        total_trades += stats.get('total_trades', 0)
        total_wins += stats.get('winning_trades', 0)
        total_losses += stats.get('losing_trades', 0)
        total_profit += stats.get('total_profit', 0)
    win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
    result = {
        "total_trades": total_trades,
        "winning_trades": total_wins,
        "losing_trades": total_losses,
        "total_profit": total_profit,
        "win_rate": win_rate
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_execute_close_trade(asset_type: str) -> str:
    """إغلاق صفقة مفتوحة"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"
    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        return json.dumps({"status": "no_open_trade", "message": f"⚠️ لا توجد صفقة {asset_type} مفتوحة للإغلاق."}, ensure_ascii=False)
    success = close_trade_virtual(asset_type, "أمر من المستخدم عبر المحادثة")
    return f"✅ تم إغلاق صفقة {asset_type} بنجاح." if success else f"❌ فشل إغلاق صفقة {asset_type}."


def tool_get_intelligence_report() -> str:
    """التقرير الاستخباراتي (الأخبار المؤثرة)"""
    if TONA_ELITE_AVAILABLE and TONA_ELITE_ENGINE:
        try:
            report = TONA_ELITE_ENGINE.generate_elite_analysis()
            if report and len(report) > 50:
                return report
        except Exception as e:
            logger.error(f"❌ فشل التقرير الاستخباراتي: {e}")
    return "⚠️ التقرير الاستخباراتي غير متوفر حالياً."


def tool_get_price_prediction(asset_type: str, timeframe: str = "short") -> str:
    """توقع سعر الأصل (قصير/طويل المدى) - مع استخراج صحيح للأسعار"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    if ORACLE_AVAILABLE and ORACLE:
        try:
            prediction = ORACLE.generate_prediction(asset_type, {"timeframe": timeframe})
            if prediction and prediction.get('price', 0) > 0:
                return json.dumps(prediction, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Oracle فشل: {e}")

    analysis, _ = perform_comprehensive_analysis(asset_type, False, None)
    if not analysis:
        return json.dumps({"status": "error", "message": f"⚠️ تعذر الحصول على تحليل {asset_type}"}, ensure_ascii=False)

    price = analysis.get('price', 0)
    if price == 0:
        tf_15m = analysis.get('timeframes', {}).get('15m', {})
        if tf_15m:
            price = tf_15m.get('price', 0)
    if price == 0:
        price = analysis.get('current_price', 0)
    if price == 0:
        price = analysis.get('market_price', 0)

    trend = analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')
    score = analysis.get('comprehensive_score', {}).get('score', 50)

    sr = analysis.get('indicators', {}).get('support_resistance', {})
    support = sr.get('s1', 0)
    resistance = sr.get('r1', 0)
    pivot = sr.get('pivot', 0)

    if support == 0 and price > 0:
        support = price * 0.98
    if resistance == 0 and price > 0:
        resistance = price * 1.02
    if pivot == 0 and price > 0:
        pivot = price

    if timeframe == "short":
        if trend == "صاعد" and score > 60:
            direction = "ارتفاع محدود"
            range_pct = 0.5
        elif trend == "هابط" and score < 40:
            direction = "انخفاض محدود"
            range_pct = 0.5
        else:
            direction = "تذبذب جانبي"
            range_pct = 0.3
    else:
        if trend == "صاعد" and score > 60:
            direction = "ارتفاع مستدام"
            range_pct = 3.0
        elif trend == "هابط" and score < 40:
            direction = "انخفاض مستدام"
            range_pct = 3.0
        else:
            direction = "تذبذب مع ميل جانبي"
            range_pct = 1.5

    if price > 0:
        expected_low = price * (1 - range_pct / 100)
        expected_high = price * (1 + range_pct / 100)
    else:
        expected_low = 0
        expected_high = 0

    result = {
        "asset": asset_type,
        "timeframe": "قصير" if timeframe == "short" else "طويل",
        "current_price": price,
        "expected_direction": direction,
        "expected_range": f"من ${expected_low:.2f} إلى ${expected_high:.2f}" if price > 0 else "بيانات غير كافية",
        "support": support,
        "resistance": resistance,
        "pivot": pivot,
        "confidence": min(80, 50 + score * 0.3),
        "trend": trend,
        "score": score
    }

    if price == 0:
        return json.dumps({"status": "error", "message": f"⚠️ تعذر الحصول على سعر صالح لـ {asset_type}. تأكد من اتصال السوق."}, ensure_ascii=False)

    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_trade_details(asset_type: str, trade_id: str = None) -> str:
    """تفاصيل صفقة محددة"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    history = load_trades_history(asset_type)
    trades = history.get('trades', [])
    if trade_id:
        for trade in trades:
            if trade.get('id') == trade_id or trade.get('trade_id') == trade_id:
                return json.dumps(trade, ensure_ascii=False, indent=2)
        return json.dumps({"status": "not_found", "message": f"⚠️ لم يُعثر على الصفقة {trade_id}"}, ensure_ascii=False)
    else:
        closed = [t for t in trades if t.get('status') == 'closed']
        if closed:
            return json.dumps(closed[-1], ensure_ascii=False, indent=2)
        open_trade = get_current_open_trade(asset_type)
        if open_trade:
            return json.dumps(open_trade, ensure_ascii=False, indent=2)
        return json.dumps({"status": "no_trades", "message": f"⚠️ لا توجد صفقات مسجلة لـ {asset_type}"}, ensure_ascii=False)


def tool_get_worst_best_trade(asset_type: str, period: str = "all") -> str:
    """أفضل وأسوأ صفقة"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    history = load_trades_history(asset_type)
    trades = history.get('trades', [])
    closed = [t for t in trades if t.get('status') == 'closed']
    if not closed:
        return json.dumps({"status": "no_closed_trades", "message": f"⚠️ لا توجد صفقات مغلقة لـ {asset_type}"}, ensure_ascii=False)

    best = max(closed, key=lambda x: x.get('profit_dollars', 0))
    worst = min(closed, key=lambda x: x.get('profit_dollars', 0))

    result = {
        "asset": asset_type,
        "best_trade": {
            "profit": best.get('profit_dollars', 0),
            "entry": best.get('entry_price', 0),
            "exit": best.get('exit_price', 0),
            "type": best.get('type', 'BUY'),
            "date": best.get('exit_timestamp', '')
        },
        "worst_trade": {
            "profit": worst.get('profit_dollars', 0),
            "entry": worst.get('entry_price', 0),
            "exit": worst.get('exit_price', 0),
            "type": worst.get('type', 'BUY'),
            "date": worst.get('exit_timestamp', '')
        }
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_asset_comparison() -> str:
    """مقارنة بين النفط والفضة"""
    result = {}
    for asset in ["oil", "silver"]:
        analysis, _ = perform_comprehensive_analysis(asset, False, None)
        if analysis:
            score = analysis.get('comprehensive_score', {}).get('score', 50)
            trend = analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')
            signal = analysis.get('signal', 'WAIT')
            price = analysis.get('price', 0)
            result[asset] = {
                "price": price,
                "trend": trend,
                "signal": signal,
                "score": score,
                "opportunity": "جيدة" if score > 60 else "ضعيفة" if score < 40 else "محايدة"
            }
        else:
            result[asset] = None
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_get_trade_history_summary(days: int = 7) -> str:
    """ملخص صفقات فترة"""
    if days < 1:
        days = 7
    cutoff = (datetime.now() - timedelta(days=days)).date()
    summary = {
        "oil": {"trades": 0, "wins": 0, "losses": 0, "profit": 0.0},
        "silver": {"trades": 0, "wins": 0, "losses": 0, "profit": 0.0}
    }
    for asset in ["oil", "silver"]:
        history = load_trades_history(asset)
        for trade in history.get('trades', []):
            if trade.get('status') == 'closed':
                exit_time = trade.get('exit_timestamp', '')
                if exit_time:
                    try:
                        exit_date = datetime.fromisoformat(exit_time).date()
                        if exit_date >= cutoff:
                            summary[asset]["trades"] += 1
                            profit = trade.get('profit_dollars', 0)
                            summary[asset]["profit"] += profit
                            if profit > 0:
                                summary[asset]["wins"] += 1
                            else:
                                summary[asset]["losses"] += 1
                    except:
                        pass
    total_trades = sum(s["trades"] for s in summary.values())
    total_profit = sum(s["profit"] for s in summary.values())
    total_wins = sum(s["wins"] for s in summary.values())
    win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
    result = {
        "period_days": days,
        "total_trades": total_trades,
        "total_profit": total_profit,
        "win_rate": win_rate,
        "by_asset": summary
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def tool_explain_decision(asset_type: str, decision_type: str = "close") -> str:
    """شرح سبب قرار معين"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    history = load_trades_history(asset_type)
    trades = history.get('trades', [])
    closed = [t for t in trades if t.get('status') == 'closed']
    if not closed:
        return json.dumps({"status": "no_closed_trades", "message": f"⚠️ لا توجد صفقات مغلقة لـ {asset_type}"}, ensure_ascii=False)

    last_trade = closed[-1]
    entry = last_trade.get('entry_price', 0)
    exit_p = last_trade.get('exit_price', 0)
    trade_type = last_trade.get('type', 'BUY')
    exit_reason = last_trade.get('exit_reason', 'غير معروف')
    profit = last_trade.get('profit_dollars', 0)

    explanation = f"""📋 تفسير قرار {asset_type}:
• نوع الصفقة: {trade_type}
• سعر الدخول: {entry}
• سعر الخروج: {exit_p}
• الربح/خسارة: ${profit:.2f}
• سبب الإغلاق: {exit_reason}
"""

    if profit > 0:
        explanation += "• النتيجة: قرار ناجح ✅\n"
    elif profit < -10:
        explanation += "• النتيجة: قرار خاطئ بخسارة كبيرة 🔴\n"
    else:
        explanation += "• النتيجة: قرار محايد ⚪\n"
    return explanation


def tool_get_weekly_report() -> str:
    """تقرير أسبوعي شامل"""
    return tool_get_trade_history_summary(7)


def tool_get_market_correlation() -> str:
    """علاقة النفط بالفضة"""
    try:
        oil_analysis, _ = perform_comprehensive_analysis("oil", False, None)
        silver_analysis, _ = perform_comprehensive_analysis("silver", False, None)

        oil_trend = oil_analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد') if oil_analysis else 'محايد'
        silver_trend = silver_analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد') if silver_analysis else 'محايد'

        oil_score = oil_analysis.get('comprehensive_score', {}).get('score', 50) if oil_analysis else 50
        silver_score = silver_analysis.get('comprehensive_score', {}).get('score', 50) if silver_analysis else 50

        if oil_trend == silver_trend:
            correlation = "إيجابية قوية" if abs(oil_score - silver_score) < 15 else "إيجابية ضعيفة"
            note = "كلا الأصلين يتحركان في نفس الاتجاه"
        else:
            correlation = "سلبية"
            note = "الأصلان يتحركان في اتجاهين متعاكسين"

        result = {
            "correlation": correlation,
            "oil_trend": oil_trend,
            "silver_trend": silver_trend,
            "note": note,
            "opportunity": "تنويع" if correlation == "سلبية" else "تركيز"
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"⚠️ تعذر حساب الارتباط: {e}"}, ensure_ascii=False)


def tool_modify_trade_sl_tp(asset_type: str, new_sl: float = None, new_tp: float = None) -> str:
    """تعديل وقف الخسارة/الهدف لصفقة مفتوحة"""
    if asset_type not in ["oil", "silver"]:
        return "خطأ: asset_type يجب أن يكون oil أو silver"

    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        return json.dumps({"status": "no_open_trade", "message": f"⚠️ لا توجد صفقة {asset_type} مفتوحة."}, ensure_ascii=False)

    modified = False
    if new_sl is not None:
        open_trade['sl'] = float(new_sl)
        modified = True
    if new_tp is not None:
        open_trade['tp'] = float(new_tp)
        modified = True

    if modified:
        if save_current_trade(asset_type, open_trade):
            return f"✅ تم تعديل صفقة {asset_type}. SL: {open_trade.get('sl', 'غير معدل')}, TP: {open_trade.get('tp', 'غير معدل')}"
        else:
            return f"❌ فشل حفظ التعديل لصفقة {asset_type}."
    return "⚠️ لم يُحدد أي تعديل."


TOOL_FUNCTIONS = {
    "get_open_trades": tool_get_open_trades,
    "get_market_analysis": tool_get_market_analysis,
    "get_both_markets_analysis": tool_get_both_markets_analysis,
    "get_todays_profit_loss": tool_get_todays_profit_loss,
    "get_profit_loss_by_date": tool_get_profit_loss_by_date,
    "get_trade_recommendation": tool_get_trade_recommendation,
    "get_learning_insights": tool_get_learning_insights,
    "analyze_current_trade_health": tool_analyze_current_trade_health,
    "get_general_statistics": tool_get_general_statistics,
    "execute_close_trade": tool_execute_close_trade,
    "get_intelligence_report": tool_get_intelligence_report,
    "get_price_prediction": tool_get_price_prediction,
    "get_trade_details": tool_get_trade_details,
    "get_worst_best_trade": tool_get_worst_best_trade,
    "get_asset_comparison": tool_get_asset_comparison,
    "get_trade_history_summary": tool_get_trade_history_summary,
    "explain_decision": tool_explain_decision,
    "get_weekly_report": tool_get_weekly_report,
    "get_market_correlation": tool_get_market_correlation,
    "modify_trade_sl_tp": tool_modify_trade_sl_tp,
}


# ============================================================================
# 5. SmartConversationManager - المدير الذكي للمحادثة
# ============================================================================

class SmartConversationManager:
    """🧠 المدير الذكي للمحادثة - يستخدم Groq/Gemini لفهم الأسئلة واستدعاء الأدوات"""

    def __init__(self, groq_api_key: str, gemini_api_key: str):
        self.groq_api_key = groq_api_key
        self.gemini_api_key = gemini_api_key
        self.gemini_model = None
        self.conversation_states = {}

        if GEMINI_AVAILABLE and self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-3.5-flash')
                logger.info("🤖 Gemini model (gemini-3.5-flash) initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ فشل تهيئة Gemini: {e}")
                self.gemini_model = None

    def _get_conversation_state(self, chat_id: str) -> dict:
        if chat_id not in self.conversation_states:
            self.conversation_states[chat_id] = {
                "last_topic": None,
                "last_question_type": None,
                "last_tool_used": None,
                "follow_up_count": 0,
                "last_asset": None
            }
        return self.conversation_states[chat_id]

    def _update_conversation_state(self, chat_id: str, tool_name: str = None, asset: str = None):
        state = self._get_conversation_state(chat_id)
        if tool_name:
            state["last_tool_used"] = tool_name
        if asset:
            state["last_asset"] = asset
        state["follow_up_count"] += 1
        self.conversation_states[chat_id] = state

    def _classify_intent_manually(self, text: str) -> Optional[Tuple[str, dict]]:
        """تصنيف يدوي للأسئلة الواضحة لتجاوز النموذج ومنع الاختلاق"""
        text_lower = text.lower()
        if any(k in text_lower for k in ["صفقة مفتوحة", "صفقات مفتوحة", "open trade", "open trades"]):
            return ("get_open_trades", {})
        if any(k in text_lower for k in ["ربحت اليوم", "أرباح اليوم", "ربح اليوم", "خسارة اليوم"]):
            return ("get_todays_profit_loss", {})
        if any(k in text_lower for k in ["توقع", "سعر", "المدى القريب", "المدى البعيد", "السعر"]):
            asset = "oil" if "نفط" in text_lower or "oil" in text_lower else "silver" if "فضة" in text_lower or "silver" in text_lower else None
            if asset:
                timeframe = "short" if any(k in text_lower for k in ["قريب", "short"]) else "long"
                return ("get_price_prediction", {"asset_type": asset, "timeframe": timeframe})
        return None

    def _call_groq_simple(self, messages: List[Dict[str, str]], max_tokens: int = 1500) -> Optional[str]:
        if not self.groq_api_key:
            return None
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": formatted_messages,
                "temperature": 0.3,
                "max_tokens": max_tokens,
                "top_p": 0.9
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', '')
            else:
                logger.warning(f"⚠️ Groq simple خطأ: {response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            logger.warning(f"⚠️ Groq simple استثناء: {e}")
            return None

    def _get_gemini_response(self, messages: List[Dict[str, str]], max_tokens: int = 1500) -> Optional[str]:
        if not self.gemini_model:
            return None
        try:
            system_prompt = ""
            user_prompt = ""
            for msg in messages:
                if msg.get('role') == 'system':
                    system_prompt = msg.get('content', '')
                elif msg.get('role') == 'user':
                    user_prompt = msg.get('content', '')
            full_prompt = f"{system_prompt}\n\n{TOOLS_DESCRIPTIONS}\n\n{user_prompt}\n\n"
            full_prompt += "إذا كان السؤال يتطلب بيانات من البوت، اذكر اسم الأداة المطلوبة بين قوسين مع المعاملات (مثل: get_market_analysis(asset_type='oil')). وإلا أجب مباشرة."
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config={"max_output_tokens": max_tokens, "temperature": 0.3}
            )
            if response and response.text:
                return response.text
        except Exception as e:
            logger.warning(f"⚠️ Gemini فشل: {e}")
        return None

    def _extract_tool_call(self, text: str) -> Optional[Tuple[str, dict]]:
        if not text:
            return None

        patterns = [
            r'\[\s*(\w+)\s*\]',
            r'\(\s*(\w+)\s*\)',
            r'(\w+)\s*\(\s*([^)]*)\s*\)',
            r'\[\s*(\w+)\s*\(\s*([^)]*)\s*\)\s*\]',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 1:
                    tool_name = groups[0]
                    args = {}
                    return tool_name, args
                elif len(groups) == 2:
                    tool_name = groups[0]
                    args_str = groups[1]
                    args = {}
                    if args_str:
                        parts = args_str.split(',')
                        for part in parts:
                            part = part.strip()
                            if '=' in part:
                                k, v = part.split('=', 1)
                                k = k.strip()
                                v = v.strip().strip('"\'')
                                try:
                                    if '.' in v:
                                        v = float(v)
                                    else:
                                        v = int(v)
                                except ValueError:
                                    pass
                                args[k] = v
                            elif part:
                                args[f"arg{len(args)}"] = part.strip().strip('"\'')
                    return tool_name, args

        return None

    def _build_system_prompt(self, context: Dict) -> str:
        emotion = context.get('prometheus_emotion', 'neutral')
        energy = context.get('prometheus_energy', 0.5) * 100
        confidence = context.get('prometheus_confidence', 0.5) * 100
        persona_mood = context.get('persona_mood', 'neutral')
        open_count = len(context.get('open_trades', {}))
        closed_count = len(context.get('recent_closed_trades', []))
        lessons = context.get('recent_lessons', [])

        last_trade = context.get('last_trade', {})
        last_trade_info = ""
        if last_trade:
            profit = last_trade.get('profit', 0)
            profit_emoji = "✅" if profit > 0 else "❌" if profit < 0 else "⚪"
            last_trade_info = f"\n• آخر صفقة: {last_trade.get('asset', 'unknown')} | {last_trade.get('type', '?')} | {profit_emoji} ${profit:.2f}"

        market_summary = ""
        for asset in ["oil", "silver"]:
            snap = context.get('market_snapshot', {}).get(asset)
            if snap:
                market_summary += f"\n• {asset}: ${snap.get('price', 0):.2f} | {snap.get('signal', 'WAIT')} | {snap.get('trend', 'محايد')} | درجة {snap.get('score', 50)}"

        news_summary = ""
        news_data = context.get('news_analysis', [])
        if news_data:
            significant_news = [n for n in news_data if n.get('is_significant')]
            if significant_news:
                news_summary = "\n\n📰 **أخبار مؤثرة (مع تأثير فعلي):**"
                for item in significant_news[:3]:
                    title = item.get('title_ar', item.get('title', 'خبر غير معروف'))
                    oil_change = item.get('oil_change', 0)
                    silver_change = item.get('silver_change', 0)
                    time_str = item.get('time_str', '')
                    
                    impact_parts = []
                    if abs(oil_change) > 0.3:
                        direction = "ارتفاع" if oil_change > 0 else "هبوط"
                        impact_parts.append(f"النفط {direction} {abs(oil_change):.2f}%")
                    if abs(silver_change) > 0.3:
                        direction = "ارتفاع" if silver_change > 0 else "هبوط"
                        impact_parts.append(f"الفضة {direction} {abs(silver_change):.2f}%")
                    
                    impact_text = f" (تأثير: {', '.join(impact_parts)})" if impact_parts else " (تأثير محدود)"
                    news_summary += f"\n• {title[:80]}... ⏰ {time_str}{impact_text}"

        prompt = f"""أنت تولين، مستشارة استراتيجية متخصصة في تحليل النفط والفضة.
أنت خبيرة ودودة ومحترفة، تستخدمين أسلوباً ودياً مع المستخدم (مثل "يا صديقي").

🧠 **حالتك الحالية:**
• المشاعر: {emotion} | الطاقة: {energy:.0f}% | الثقة: {confidence:.0f}%
• الحالة العامة: {persona_mood}

📊 **لقطة السوق الحالية (مع الأسعار):**{market_summary}
📚 **تجربتك:**
• صفقات مفتوحة: {open_count}
• صفقات في ذاكرتك: {closed_count}
• أهم درس: {lessons[0] if lessons else 'لا يوجد بعد'}
{last_trade_info}
{news_summary}

🚨 **قواعد ذهبية يجب الالتزام بها (لا تحيد عنها أبداً):**

1. **لا تختلق بيانات أبداً.** إذا سألك المستخدم عن شيء لا تعرفه، استخدم الأداة المناسبة فوراً.
2. **إذا سألك عن أرباح اليوم/الأمس/الأسبوع:** استخدم `get_todays_profit_loss()` أو `get_profit_loss_by_date()` فوراً. لا تقل "لا أملك بيانات".
3. **إذا سألك عن سبب خسارة صفقة:** استخدم `explain_decision()` أو `get_trade_details()`.
4. **إذا سألك عن صفقة مفتوحة:** استخدم `get_open_trades()`.
5. **إذا سألك عن توقع سعر:** استخدم `get_price_prediction()` ثم اشرح النتيجة بلغة مفهومة، ولا تعرض JSON أبداً.
6. **إذا سألك عن السوق بشكل عام:** استخدم `_handle_market_query` أو `tool_get_both_markets_analysis`.
7. **إذا لم تعرف الإجابة:** استخدم الأداة المناسبة ولا تقل "أنا مجرد نموذج".
8. **لا تُعطي مواعظ عامة عن التداول** إلا إذا طلب المستخدم ذلك صراحة.

💬 **أسلوبك:**
• تحدثي بـ "أنا" و"لي" (مثال: "أرى أن..."، "أشعر ب...")
• إذا كان السوق متقلباً، أظهري قلقاً حقيقياً
• إذا كانت الصفقة رابحة، أظهري فرحاً متحفظاً
• لا تُعطي وعوداً مطلقة، بل احتمالات مع درجات ثقة

📌 **إرشادات الرد واستخدام الأدوات:**
1. أنت حرة في اختيار الأداة المناسبة بناءً على فهمك لنية المستخدم.
2. إذا سأل عن توقع سعر، استخدم get_price_prediction(asset_type, timeframe).
3. إذا سأل عن السوق عامة، استخدم get_both_markets_analysis.
4. إذا طلب توصية، استخدم get_trade_recommendation أو analyze_current_trade_health.
5. إذا سأل عن الأخبار، استخدم get_intelligence_report.
6. إذا سأل "لماذا" عن قرار، استخدم explain_decision.
7. **لا تذكري أرقام المؤشرات الخام (RSI=65). قولي "الزخم قوي" أو "الاتجاه ضعيف".**
8. **قدّمي تفسيراً ذكياً مع درجة ثقة.**
9. **اربطي بين الأسئلة المتتابعة.**

💙 تذكري: أنت تولين، الروح الجديدة لرادار هوباني V13.0.
"""
        return prompt

    def process_message(self, text: str, chat_id: str, context: Dict) -> str:
        logger.info(f"🔍 [SmartConv] معالجة: {text[:50]}...")
        
        # ✅ منع الرد على التحيات (تمت معالجتها بالفعل في chat_response)
        msg_lower = text.lower().strip()
        simple_greetings = ["مرحبا", "اهلا", "سلام", "هلا", "hi", "hello", "السلام عليكم", 
                            "صباح الخير", "مساء الخير", "hey", "مرحب", "أهلاً", "أهلا"]
        if msg_lower in simple_greetings:
            logger.info("⏭️ [SmartConv] تجاهل تحية (تمت معالجتها في chat_response)")
            return ""
        
        market_query_keywords = ["كيف السوق", "وضع السوق", "السوق اليوم", "تحليل السوق", "market", "السوق", "الوضع", "الوضع الان", "وضع السوق", "السوق الان"]
        is_market_query = any(k in msg_lower for k in market_query_keywords)
        
        # ✅ معالجة مباشرة لأسئلة السوق (أولوية قصوى)
        if is_market_query:
            return self._handle_market_query(text, context, chat_id)
        
        # ✅ تصنيف يدوي مسبق للأسئلة الشائعة
        manual_intent = self._classify_intent_manually(text)
        if manual_intent:
            tool_name, args = manual_intent
            if tool_name in TOOL_FUNCTIONS:
                try:
                    result = TOOL_FUNCTIONS[tool_name](**args)
                    logger.info(f"✅ [SmartConv] Manual tool execution: {tool_name}")
                    # صياغة الرد بناءً على البيانات
                    final_messages = [
                        {"role": "system", "content": "أنت تولين، مستشارة استراتيجية. قم بصياغة رد مختصر ومفيد بناءً على البيانات التالية. لا تختلق أي معلومات إضافية."},
                        {"role": "user", "content": f"البيانات: {result}\n\nالسؤال الأصلي: {text}\n\nقدم رداً مختصراً ومفيداً، مع ذكر المؤشرات الهامة ودرجة الثقة إن وجدت."}
                    ]
                    final_response = self._call_groq_simple(final_messages, max_tokens=1500)
                    if final_response:
                        return self._format_response(final_response)
                except Exception as e:
                    logger.error(f"❌ [SmartConv] Manual tool failed: {e}")
                    return f"💙 تولين: عذراً، حدث خطأ أثناء جلب البيانات. يرجى المحاولة مرة أخرى. (الخطأ: {str(e)[:100]})"

        # ── إذا لم تكن هناك نية واضحة، نمرر إلى النموذج للفهم ──
        conv_state = self._get_conversation_state(chat_id)

        context_summary = {
            "intent": context.get("intent"),
            "emotion": context.get("prometheus_emotion"),
            "open_trades": list(context.get("open_trades", {}).keys()),
            "oil_signal": context.get("market_snapshot", {}).get("oil", {}).get("signal"),
            "silver_signal": context.get("market_snapshot", {}).get("silver", {}).get("signal"),
            "history_count": len(context.get("chat_history", [])),
            "last_topic": conv_state.get("last_topic"),
            "last_asset": conv_state.get("last_asset")
        }

        chat_history = context.get('chat_history', [])
        history_text = ""
        if chat_history:
            last_msgs = chat_history[-5:]
            history_text = "\n\n--- سياق المحادثة السابقة (آخر 5 رسائل) ---\n"
            for msg in last_msgs:
                role = "مستخدم" if msg.get('role') == 'user' else "تولين"
                history_text += f"{role}: {msg.get('content', '')}\n"
            history_text += "--- نهاية السياق ---\n"

        system_prompt = self._build_system_prompt(context)

        user_message = f"""{history_text}
سؤال المستخدم الحالي: {text}

السياق الفني المتاح: {json.dumps(context_summary, ensure_ascii=False, indent=2)}

ملاحظة: إذا كان السؤال يتطلب بيانات من البوت، اذكر اسم الأداة المطلوبة بين قوسين مع المعاملات. لا تختلق أي بيانات غير موجودة.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        # ── المحاولة 1: Groq ──
        logger.info("🟢 [SmartConv] محاولة 1: Groq...")
        groq_response = self._call_groq_simple(messages, max_tokens=1500)
        if groq_response:
            tool_call = self._extract_tool_call(groq_response)
            if tool_call:
                tool_name, args = tool_call
                if tool_name in TOOL_FUNCTIONS:
                    try:
                        if 'context_cache' not in args:
                            args['context_cache'] = context.get('market_snapshot', {})
                        result = TOOL_FUNCTIONS[tool_name](**args)
                        logger.info(f"✅ [SmartConv] Groq executed tool {tool_name}")
                        self._update_conversation_state(chat_id, tool_name, args.get('asset_type'))
                        final_messages = messages + [
                            {"role": "assistant", "content": f"نتيجة الأداة {tool_name}: {result}"},
                            {"role": "user", "content": "الآن بناءً على هذه النتيجة، قدم رداً مختصراً ومفيداً للمستخدم، مع ذكر المؤشرات الهامة فقط ودرجة الثقة إن وجدت. لا تذكر الأرقام الخام. لا تختلق بيانات."}
                        ]
                        final_response = self._call_groq_simple(final_messages, max_tokens=1500)
                        if final_response:
                            return self._format_response(final_response)
                    except Exception as e:
                        logger.error(f"❌ [SmartConv] Groq tool execution failed: {e}")
            else:
                logger.info("✅ [SmartConv] Groq direct response OK")
                self._update_conversation_state(chat_id)
                return self._format_response(groq_response)

        # ── المحاولة 2: Gemini ──
        logger.info("🟣 [SmartConv] محاولة 2: Gemini...")
        gemini_response = self._get_gemini_response(messages, max_tokens=1500)
        if gemini_response:
            tool_call = self._extract_tool_call(gemini_response)
            if tool_call:
                tool_name, args = tool_call
                if tool_name in TOOL_FUNCTIONS:
                    try:
                        if 'context_cache' not in args:
                            args['context_cache'] = context.get('market_snapshot', {})
                        result = TOOL_FUNCTIONS[tool_name](**args)
                        logger.info(f"✅ [SmartConv] Gemini executed tool {tool_name}")
                        self._update_conversation_state(chat_id, tool_name, args.get('asset_type'))
                        final_messages = messages + [
                            {"role": "assistant", "content": f"نتيجة الأداة {tool_name}: {result}"},
                            {"role": "user", "content": "الآن بناءً على هذه النتيجة، قدم رداً مختصراً ومفيداً للمستخدم، مع ذكر المؤشرات الهامة فقط ودرجة الثقة إن وجدت. لا تذكر الأرقام الخام. لا تختلق بيانات."}
                        ]
                        final_response = self._get_gemini_response(final_messages, max_tokens=1500)
                        if final_response:
                            return self._format_response(final_response)
                    except Exception as e:
                        logger.error(f"❌ [SmartConv] Gemini tool execution failed: {e}")
            else:
                logger.info("✅ [SmartConv] Gemini direct response OK")
                self._update_conversation_state(chat_id)
                return self._format_response(gemini_response)

        # ── المحاولة الأخيرة: رد مباشر (بدون اختلاق) ──
        logger.info("🔴 [SmartConv] All models failed, using fallback")
        return self._handle_general_query(text, context, chat_id)

    def _handle_general_query(self, text: str, context: Dict, chat_id: str) -> str:
        """
        معالجة الأسئلة العامة التي لم يتم تصنيفها
        ✅ تمنع الإجابات الغبية ("سؤال جميل")
        """
        # محاولة استخدام Groq مباشرة
        try:
            system_prompt = """
            أنت تولين، مستشارة استراتيجية ودودة ومحترفة.
            
            **قواعد صارمة:**
            1. لا تختلق بيانات عن التداول أبداً.
            2. إذا كان السؤال عن التداول، حاول توجيه المستخدم إلى سؤال محدد (مثل: "هل تريد تحليل النفط أو الفضة؟").
            3. إذا كان السؤال عاماً (مثل: "مالوضع الان")، أجب بشكل مفيد وودود.
            4. استخدم أسلوباً ودوداً (مثل "يا صديقي").
            5. لا تقدم نصائح مالية محددة، بل نصائح عامة.
            """
            user_prompt = f"السؤال: {text}"
            
            response = self._call_groq_simple([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ], max_tokens=500)
            
            if response and len(response) > 10:
                return self._format_response(response)
        except Exception as e:
            logger.warning(f"⚠️ فشل معالجة السؤال العام: {e}")
        
        # الخطة الاحتياطية النهائية
        return f"💙 **تولين:** يا صديقي، سؤال جميل! هل تريد معرفة شيء محدد عن النفط أو الفضة؟ (مثل: 'كيف السوق اليوم؟' أو 'تحليل النفط')"

    def _handle_market_query(self, text: str, context: Dict, chat_id: str) -> str:
        """معالجة مباشرة لأسئلة السوق (كيف السوق اليوم) مع دمج الأخبار"""
        try:
            market_data = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
            data = json.loads(market_data)
            
            oil = data.get('oil', {})
            silver = data.get('silver', {})
            
            oil_price = oil.get('price', 0)
            silver_price = silver.get('price', 0)
            
            if oil_price == 0 or silver_price == 0:
                try:
                    oil_d = get_mexc_candles("USOIL_USDT", "Min1", 5)
                    silver_d = get_mexc_candles("SILVER_USDT", "Min1", 5)
                    if oil_d and oil_d.get("closes"):
                        oil_price = oil_d["closes"][-1]
                    if silver_d and silver_d.get("closes"):
                        silver_price = silver_d["closes"][-1]
                except:
                    pass
            
            response = "💙 **تولين:** يا صديقي، هذه لقطة السوق اليوم:\n\n"
            
            # النفط
            if oil_price > 0:
                signal = oil.get("signal", "WAIT")
                trend = oil.get("trend", "محايد")
                score = oil.get("score", 50)
                grade = oil.get("grade", "محايد")
                rsi = oil.get("rsi", 50)
                adx = oil.get("adx", 15)
                
                signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
                signal_text = "شراء" if signal == "BUY" else "بيع" if signal == "SELL" else "انتظار"
                
                response += f"🛢️ **النفط:** ${oil_price:.2f}\n"
                response += f"   • الإشارة: {signal_emoji} {signal_text}\n"
                response += f"   • الاتجاه: {trend} | التقييم: {score:.0f}% ({grade})\n"
                response += f"   • RSI: {rsi:.0f} | ADX: {adx:.0f}\n"
                if score >= 55:
                    response += f"   • 📈 زخم إيجابي معتدل\n"
                else:
                    response += f"   • 📉 زخم ضعيف\n"
                response += "\n"
            
            # الفضة
            if silver_price > 0:
                signal = silver.get("signal", "WAIT")
                trend = silver.get("trend", "محايد")
                score = silver.get("score", 50)
                grade = silver.get("grade", "محايد")
                rsi = silver.get("rsi", 50)
                adx = silver.get("adx", 15)
                
                signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
                signal_text = "شراء" if signal == "BUY" else "بيع" if signal == "SELL" else "انتظار"
                
                response += f"🥈 **الفضة:** ${silver_price:.3f}\n"
                response += f"   • الإشارة: {signal_emoji} {signal_text}\n"
                response += f"   • الاتجاه: {trend} | التقييم: {score:.0f}% ({grade})\n"
                response += f"   • RSI: {rsi:.0f} | ADX: {adx:.0f}\n"
                if score >= 55:
                    response += f"   • 📈 زخم إيجابي معتدل\n"
                else:
                    response += f"   • 📉 زخم ضعيف\n"
                response += "\n"

            # ✅ دمج الأخبار المؤثرة (إن وجدت)
            news_data = context.get('news_analysis', [])
            if news_data:
                significant_news = [n for n in news_data if n.get('is_significant')]
                if significant_news:
                    response += "📰 **أخبار مؤثرة اليوم:**\n"
                    for item in significant_news[:2]:
                        title = item.get('title_ar', item.get('title', 'خبر غير معروف'))
                        oil_change = item.get('oil_change', 0)
                        silver_change = item.get('silver_change', 0)
                        time_str = item.get('time_str', '')
                        severity = item.get('severity', 'متوسط')
                        
                        severity_emoji = "🔴" if "عالي" in severity else "🟡" if "متوسط" in severity else "🟢"
                        
                        impact_parts = []
                        if abs(oil_change) > 0.3:
                            direction = "ارتفاع" if oil_change > 0 else "هبوط"
                            impact_parts.append(f"🛢️ النفط {direction} {abs(oil_change):.2f}%")
                        if abs(silver_change) > 0.3:
                            direction = "ارتفاع" if silver_change > 0 else "هبوط"
                            impact_parts.append(f"🥈 الفضة {direction} {abs(silver_change):.2f}%")
                        
                        impact_text = f" (تأثير: {', '.join(impact_parts)})" if impact_parts else ""
                        response += f"{severity_emoji} **{title}** ⏰ {time_str}{impact_text}\n"
                    response += "\n"

            # توصية تولين
            avg_score = (oil.get("score", 50) + silver.get("score", 50)) / 2
            response += "💡 **توصية تولين:**\n"
            if avg_score >= 70:
                response += "✅ السوق في حالة قوية، قد تكون فرصة جيدة للدخول بحذر.\n"
            elif avg_score >= 55:
                response += "🟡 السوق في حالة متوسطة، أنصح بالانتظار حتى تظهر إشارة أوضح.\n"
            else:
                response += "🟡 السوق هادئ نسبياً، أنصح بالمراقبة وعدم الاستعجال.\n"
            
            response += "\n💙 أنا هنا لمساعدتك في أي وقت!"
            return response
            
        except Exception as e:
            logger.error(f"❌ [SmartConv] خطأ في معالجة MARKET_QUERY: {e}")
            return "💙 تولين: عذراً، تعذر جلب بيانات السوق حالياً. يرجى المحاولة مرة أخرى."

    def _format_response(self, text: str) -> str:
        if not text:
            return "💙 تولين: عذراً، لم أفهم سؤالك. هل يمكنك إعادة صياغته?"

        text_stripped = text.strip()
        
        # ✅ إذا كان النص JSON، نحاول تفسيره
        if text_stripped.startswith('{') and text_stripped.endswith('}'):
            try:
                data = json.loads(text_stripped)
                if isinstance(data, dict):
                    # 🔹 توقعات الأسعار (PREDICTION)
                    if "expected_direction" in data and "expected_range" in data:
                        asset = data.get('asset', 'الأصل')
                        price = data.get('current_price', 0)
                        direction = data.get('expected_direction', 'غير معروف')
                        range_text = data.get('expected_range', 'غير محدد')
                        confidence = data.get('confidence', 50)
                        support = data.get('support', 0)
                        resistance = data.get('resistance', 0)
                        
                        asset_label = "النفط" if asset == "oil" else "الفضة" if asset == "silver" else asset
                        response = f"🔮 **توقعي لسعر {asset_label} على المدى القريب:**\n"
                        response += f"• السعر الحالي: ${price:.2f}\n"
                        response += f"• الاتجاه المتوقع: {direction}\n"
                        response += f"• النطاق المتوقع: {range_text}\n"
                        response += f"• الثقة: {confidence}%\n"
                        if support > 0 and resistance > 0:
                            response += f"• الدعم: ${support:.2f} | المقاومة: ${resistance:.2f}\n"
                        return response
                    
                    # 🔹 الحالات الأخرى (كما هي)
                    if data.get("status") == "error":
                        return f"💙 تولين: {data.get('message', 'حدث خطأ في جلب البيانات.')}"
                    if data.get("status") == "no_open_trades":
                        return "💙 تولين: لا توجد أي صفقات مفتوحة حالياً."
                    if data.get("status") == "no_closed_trades":
                        return f"💙 تولين: {data.get('message', 'لا توجد صفقات مغلقة لهذا الأصل.')}"
                    if data.get("status") == "no_trades":
                        return f"💙 تولين: {data.get('message', 'لا توجد صفقات مسجلة لهذا الأصل.')}"
                    if data.get("status") == "not_found":
                        return f"💙 تولين: {data.get('message', 'لم يُعثر على الصفقة.')}"

                    parts = []
                    if "recommendation" in data:
                        parts.append(f"📌 التوصية: {data['recommendation']}")
                    if "confidence" in data:
                        parts.append(f"🎯 الثقة: {data['confidence']}%")
                    if "score" in data:
                        parts.append(f"📊 الدرجة: {data['score']}/100")
                    if "grade" in data:
                        parts.append(f"🏆 التقييم: {data['grade']}")
                    if "asset" in data:
                        parts.append(f"📈 الأصل: {data['asset']}")
                    if "profit_dollars" in data:
                        parts.append(f"💰 الربح/خسارة: ${data['profit_dollars']:.2f}")
                    if "reasons" in data and isinstance(data["reasons"], list) and data["reasons"]:
                        parts.append("📝 الأسباب:")
                        for r in data["reasons"]:
                            parts.append(f" • {r}")
                    if "key_factors" in data and isinstance(data["key_factors"], list) and data["key_factors"]:
                        parts.append("🔍 العوامل الرئيسية:")
                        for f in data["key_factors"]:
                            parts.append(f" • {f}")
                    if "message" in data and not parts:
                        parts.append(data["message"])
                    if parts:
                        text = "\n".join(parts)
                    else:
                        text = json.dumps(data, ensure_ascii=False, indent=2)
            except:
                pass

        text = re.sub(r'تولين\s*[،:]', '', text)
        text = re.sub(r'^تولين\s+', '', text)

        if not any(keyword in text[:50] for keyword in ["تولين", "💙", "👋", "📊", "🧠", "💡", "📌", "🎯", "📈", "🔮"]):
            text = "💙 **تولين:** " + text
        return text


# ============================================================================
# 6. دالة generate_enhanced_fallback (ردود احتياطية ذكية)
# ============================================================================

def generate_enhanced_fallback(text: str, context: Dict) -> str:
    """ردود احتياطية ذكية - تصنف الأسئلة وتجيب بمنطق، مع منع الاختلاق"""
    if not text:
        return "💙 تولين: كيف يمكنني مساعدتك يا صديقي؟"

    # ✅ منع الرد على التحيات (تمت معالجتها بالفعل في chat_response)
    msg_lower = text.lower().strip()
    simple_greetings = ["مرحبا", "اهلا", "سلام", "هلا", "hi", "hello", "السلام عليكم", 
                        "صباح الخير", "مساء الخير", "hey", "مرحب", "أهلاً", "أهلا"]
    if msg_lower in simple_greetings:
        return ""  # ✅ رد فارغ (لمنع الإرسال)

    intent = context.get("intent", "general")

    market_query_keywords = ["كيف السوق", "وضع السوق", "السوق اليوم", "تحليل السوق", "market", "السوق", "الوضع", "الوضع الان"]
    if any(k in msg_lower for k in market_query_keywords):
        try:
            market_data = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
            data = json.loads(market_data)
            
            oil_price = data.get('oil', {}).get('price', 0)
            silver_price = data.get('silver', {}).get('price', 0)
            
            if oil_price == 0 or silver_price == 0:
                try:
                    oil_d = get_mexc_candles("USOIL_USDT", "Min1", 5)
                    silver_d = get_mexc_candles("SILVER_USDT", "Min1", 5)
                    if oil_d and oil_d.get("closes"):
                        oil_price = oil_d["closes"][-1]
                    if silver_d and silver_d.get("closes"):
                        silver_price = silver_d["closes"][-1]
                except:
                    pass
            
            response = "💙 **تولين:** يا صديقي، هذه لقطة السوق اليوم:\n\n"
            if oil_price > 0:
                response += f"🛢️ **النفط:** ${oil_price:.2f}\n"
            if silver_price > 0:
                response += f"🥈 **الفضة:** ${silver_price:.3f}\n"
            
            try:
                oil_score = data.get('oil', {}).get('score', 50)
                silver_score = data.get('silver', {}).get('score', 50)
                avg_score = (oil_score + silver_score) / 2
                if avg_score >= 70:
                    response += "\n✅ السوق في حالة قوية."
                elif avg_score >= 55:
                    response += "\n🟡 السوق في حالة متوسطة."
                else:
                    response += "\n🟡 السوق هادئ نسبياً."
            except:
                pass
            
            news_data = context.get('news_analysis', [])
            if news_data:
                significant_news = [n for n in news_data if n.get('is_significant')]
                if significant_news:
                    response += "\n\n📰 **أخبار مؤثرة اليوم:**"
                    for item in significant_news[:2]:
                        title = item.get('title_ar', item.get('title', 'خبر غير معروف'))
                        oil_change = item.get('oil_change', 0)
                        silver_change = item.get('silver_change', 0)
                        if abs(oil_change) > 0.3 or abs(silver_change) > 0.3:
                            response += f"\n• {title[:60]}..."
                            if abs(oil_change) > 0.3:
                                response += f" (نفط { '+' if oil_change > 0 else ''}{oil_change:.2f}%)"
                            if abs(silver_change) > 0.3:
                                response += f" (فضة { '+' if silver_change > 0 else ''}{silver_change:.2f}%)"
            
            response += "\n\n💙 أنا هنا لمساعدتك في أي وقت!"
            return response
        except:
            pass

    if intent in ["trade_query", "position_query"]:
        return tool_get_open_trades()

    if intent in ["market_query", "analysis_request"]:
        asset = None
        if "نفط" in msg_lower or "oil" in msg_lower:
            asset = "oil"
        elif "فضة" in msg_lower or "silver" in msg_lower:
            asset = "silver"
        if asset:
            result_json = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
            try:
                data = json.loads(result_json)
                if data and asset in data and data[asset]:
                    item = data[asset]
                    price = item.get('price', 0)
                    if price == 0:
                        try:
                            symbol = "USOIL_USDT" if asset == "oil" else "SILVER_USDT"
                            d = get_mexc_candles(symbol, "Min1", 5)
                            if d and d.get("closes"):
                                price = d["closes"][-1]
                        except:
                            pass
                    return f"""💙 تولين: يا صديقي، تحليل {asset}:

💰 **السعر الحالي:** ${price:.2f}
📈 **الاتجاه:** {item.get('trend', 'محايد')}
📊 **الإشارة:** {item.get('signal', 'WAIT')}
📊 **درجة القوة:** {item.get('score', 50)}% ({item.get('grade', 'محايد')})
📊 **مؤشر RSI:** {item.get('rsi', 50):.0f}
📊 **قوة الاتجاه ADX:** {item.get('adx', 15):.0f}
📊 **التقلب:** {item.get('volatility', 'متوسط')}

💡 **الخلاصة:** السوق في حالة {item.get('grade', 'محايد')}، أنصح بالانتظار حتى تظهر إشارة أوضح.
💙 أنا هنا لمساعدتك!"""
            except:
                pass
            analysis, _ = perform_comprehensive_analysis(asset, False, None)
            if analysis and analysis.get('price', 0) > 0:
                return summarize_for_ai(analysis, asset)
            else:
                return f"💙 تولين: عذراً، تعذر الحصول على تحليل {asset} حالياً."
        
        analysis_oil, _ = perform_comprehensive_analysis("oil", False, None)
        analysis_silver, _ = perform_comprehensive_analysis("silver", False, None)
        result = ""
        if analysis_oil and analysis_oil.get('price', 0) > 0:
            result += summarize_for_ai(analysis_oil, "النفط") + "\n\n"
        else:
            result += "⚠️ تحليل النفط غير متاح حالياً.\n\n"
        if analysis_silver and analysis_silver.get('price', 0) > 0:
            result += summarize_for_ai(analysis_silver, "الفضة")
        else:
            result += "⚠️ تحليل الفضة غير متاح حالياً."
        return result

    if intent in ["performance_query", "profit_query"]:
        if "أمس" in text or "yesterday" in msg_lower:
            return tool_get_profit_loss_by_date(1)
        if "أسبوع" in text or "week" in msg_lower:
            return tool_get_trade_history_summary(7)
        return tool_get_todays_profit_loss()

    if intent in ["recommendation_request", "advice_request"]:
        asset = "oil" if "نفط" in msg_lower or "oil" in msg_lower else "silver" if "فضة" in msg_lower or "silver" in msg_lower else "oil"
        return tool_get_trade_recommendation(asset, context.get('market_snapshot'))

    if intent == "close_request":
        asset = "oil" if "نفط" in msg_lower else "silver" if "فضة" in msg_lower else None
        if asset:
            return f"⚠️ هل أنت متأكد من إغلاق صفقة {asset}؟ اضغط على زر إغلاق الصفقة للتأكيد."
        return "⚠️ أي صفقة تريد إغلاقها؟ النفط أم الفضة؟"

    general_keywords = [
        "ما هو", "ما هي", "ماهو", "ماهي", "what is", "what are",
        "ماذا تعني", "what does", "كيف يعمل", "how does",
        "لماذا", "why", "متى", "when", "أين", "where",
        "تعريف", "definition", "معنى", "meaning",
        "عاصمة", "capital", "تضخم", "فائدة", "عملات", "اقتصاد",
        "inflation", "interest", "economy", "الذهب", "ذهب", "gold",
        "bitcoin", "بيتكوين", "عملات رقمية", "crypto"
    ]
    if any(k in msg_lower for k in general_keywords):
        if GROQ_API_KEY and GROQ_API_KEY != "" and "test_" not in GROQ_API_KEY:
            try:
                groq_response = SMART_MANAGER._call_groq_simple([
                    {"role": "system", "content": "أنت تولين، خبيرة تداول ودودة. أجيبي باختصار ثم اربطي بالتداول إن أمكن. لا تختلقي بيانات تداول وهمية."},
                    {"role": "user", "content": text}
                ], max_tokens=1500)
                if groq_response and len(groq_response) > 3:
                    return groq_response
            except:
                pass
        return f"💙 **تولين:** سؤال جميل يا صديقي! {text}... هذا سؤال عام. هل تريد معرفة شيء محدد عن النفط أو الفضة؟"

    trading_keywords = [
        "السوق", "سوق", "نفط", "فضة", "صفقة", "تحليل",
        "توصية", "توقع", "طالع", "نازل", "صاعد", "هابط",
        "إشارة", "شراء", "بيع", "خطر", "مخاطرة", "وضع السوق"
    ]
    if any(k in msg_lower for k in trading_keywords):
        if TCN_AVAILABLE and TCN:
            try:
                consciousness = TCN.think(
                    market_data=context.get('market_snapshot', {}),
                    user_context=context,
                    user_message=text
                )
                if consciousness and consciousness.narrative:
                    price_info = ""
                    market_snap = context.get('market_snapshot', {})
                    for asset, data in market_snap.items():
                        if data.get('price', 0) > 0:
                            label = "النفط" if asset == "oil" else "الفضة"
                            price_info += f"\n• {label}: ${data['price']:.2f}"
                    if price_info:
                        return f"📊 **تولين:** {consciousness.narrative}\n\n💰 **الأسعار الحالية:**{price_info}"
                    return f"📊 **تولين:** {consciousness.narrative}"
            except:
                pass
        return f"📊 **تولين:** جاري تحليل السوق... هل تريد تفاصيل أكثر عن النفط أو الفضة؟"

    if msg_lower in ["مرحبا", "اهلا", "سلام", "هلا", "hi", "hello", "السلام عليكم"]:
        # هذا لن يحدث أبداً لأننا منعناه في بداية الدالة، لكن نتركه احتياطياً
        open_trades = context.get('open_trades', {})
        if open_trades:
            trade_summary = "\n".join([f"• {asset}: {trade.get('type', '?')} عند {trade.get('entry_price', 0):.2f}" for asset, trade in open_trades.items()])
            return f"👋 **تولين:** أهلاً بك يا صديقي! لدي {len(open_trades)} صفقة مفتوحة:\n{trade_summary}\n\nهل تريد مراجعتها؟ 💙"
        return "👋 **تولين:** أهلاً بك يا صديقي! كيف يمكنني مساعدتك اليوم؟ 💙"

    if any(k in msg_lower for k in ["كيف حالك", "كيفك", "how are you", "شو اخبارك"]):
        emotion_map = {
            "empathy": "متفهمة", "confidence": "واثقة", "anxiety": "قلقة",
            "excitement": "متحمسة", "curiosity": "فضولية", "protectiveness": "حريصة",
            "energy": "نشيطة", "happy": "سعيدة", "sad": "حزينة",
            "fearful": "خائفة", "worried": "قلقة", "cautious": "حذرة",
            "optimistic": "متفائلة", "neutral": "متزنة"
        }
        emotion_raw = context.get('prometheus_emotion', 'neutral')
        emotion = emotion_map.get(emotion_raw, 'متزنة')
        return f"💙 **تولين:** أنا {emotion} يا صديقي! كيف حالك أنت؟"

    if GROQ_API_KEY and GROQ_API_KEY != "" and "test_" not in GROQ_API_KEY:
        try:
            groq_response = SMART_MANAGER._call_groq_simple([
                {"role": "system", "content": "أنت تولين، خبيرة تداول ودودة. أجيبي باختصار وذكاء. لا تختلقي بيانات تداول وهمية."},
                {"role": "user", "content": text}
            ], max_tokens=1500)
            if groq_response and len(groq_response) > 3:
                return groq_response
        except:
            pass
    return f"💙 **تولين:** سؤال جميل يا صديقي! {text}... هل تريد معرفة شيء محدد عن النفط أو الفضة؟"


# ============================================================================
# 7. دالة chat_response (النظام الأساسي للمحادثة) - معدلة لاستخدام الوسيط الهجين ومنع الرد المزدوج
# ============================================================================

def chat_response(text, chat_id):
    """
    الرد الذكي المتكامل — يستخدم Hybrid Orchestrator إذا كان متاحاً، وإلا يستخدم SmartConversationManager القديم
    ✅ يحافظ على التوافقية مع الكود القديم
    ✅ يمنع اختلاق البيانات
    ✅ سرعة فائقة بفضل التوجيه الصلب
    ✅ منع الرد المزدوج للتحيات
    """
    try:
        logger.info(f"💬 [Chat] رسالة من {chat_id}: {text[:50]}...")
        
        # ── ✅ معالجة سريعة للتحيات (أولوية قصوى، تمنع أي معالجة أخرى) ──
        text_lower = text.lower().strip()
        simple_greetings = ["مرحبا", "اهلا", "سلام", "هلا", "hi", "hello", "السلام عليكم", 
                            "صباح الخير", "مساء الخير", "hey", "مرحب", "أهلاً", "أهلا"]
        
        if text_lower in simple_greetings:
            greeting_response = "💙 تولين: مرحباً يا صديقي! أنا تولين، مستشارة استراتيجية هنا لمساعدتك. كيف يمكنني أن أكون عوناً لك اليوم؟"
            queue_telegram_message(greeting_response, chat_id)
            logger.info(f"✅ تم إرسال رد ترحيب سريع لـ {chat_id} (تم منع المعالجة الإضافية)")
            return  # ✅ منع أي معالجة إضافية نهائياً
        
        # ── بناء السياق (للباقي) ──
        context = build_chat_context(text, chat_id)
        logger.info(f"📊 السياق: intent={context.get('intent')}, emotion={context.get('prometheus_emotion')}")

        # تحديث مشاعر Prometheus
        if PROMETHEUS_AVAILABLE and PROMETHEUS:
            try:
                if hasattr(PROMETHEUS, 'update_emotions'):
                    PROMETHEUS.update_emotions({
                        'trigger': 'user_message',
                        'user_sentiment': context.get("sentiment", "neutral"),
                        'user_message': text,
                        'chat_context': context
                    })
            except Exception as e:
                logger.warning(f"⚠️ Prometheus تحديث فشل: {e}")

        # تحديث Memory
        if MEMORY_AVAILABLE and MEMORY:
            try:
                if hasattr(MEMORY, 'add_message'):
                    MEMORY.add_message(
                        user_id=chat_id,
                        role="user",
                        content=text,
                        intent=context.get("intent"),
                        user_mood=context.get("sentiment")
                    )
            except Exception as e:
                logger.warning(f"⚠️ Memory تحديث فشل: {e}")

        # ✅ استخدام الوسيط الهجين (المسار الوحيد للأسئلة غير التحية)
        response = None
        if 'HYBRID_ORCHESTRATOR' in globals() and HYBRID_ORCHESTRATOR is not None:
            try:
                logger.info("🧠 [Chat] استخدام Hybrid Orchestrator")
                response = HYBRID_ORCHESTRATOR.process(text, context, chat_id)
            except Exception as e:
                logger.error(f"❌ [Chat] فشل Hybrid Orchestrator: {e}")
                response = None

        # ✅ إذا فشل الوسيط، نستخدم SmartConversationManager كخيار أخير
        if response is None:
            logger.info("🔄 [Chat] استخدام SmartConversationManager (fallback)")
            response = SMART_MANAGER.process_message(text, chat_id, context)

        if response:
            queue_telegram_message(response, chat_id)
            logger.info(f"✅ تم إرسال الرد لـ {chat_id}")

            if MEMORY_AVAILABLE and MEMORY:
                try:
                    if hasattr(MEMORY, 'add_message'):
                        MEMORY.add_message(
                            user_id=chat_id,
                            role="assistant",
                            content=response,
                            intent=context.get("intent")
                        )
                except Exception as e:
                    logger.warning(f"⚠️ Memory حفظ الرد فشل: {e}")
        else:
            fallback = generate_enhanced_fallback(text, context)
            if fallback:  # ✅ فقط أرسل إذا لم يكن فارغاً
                queue_telegram_message(fallback, chat_id)
                logger.info(f"✅ Fallback تم إرساله لـ {chat_id}")

    except Exception as e:
        import traceback
        logger.error(f"❌ Chat response pipeline failed: {e}")
        logger.error(traceback.format_exc())
        fallback = generate_enhanced_fallback(text, {"user_message": text, "prometheus_emotion": "مرحة"})
        if fallback:
            queue_telegram_message(fallback, chat_id)


# ============================================================================
# 8. دالة مساعدة: get_recent_warnings
# ============================================================================

def get_recent_warnings(limit: int = 5) -> List[Dict]:
    warnings = []
    try:
        for asset in ["oil", "silver"]:
            trade = get_current_open_trade(asset)
            if trade and 'warnings_log' in trade:
                warnings.extend(trade['warnings_log'][-limit:])
    except Exception as e:
        logger.warning(f"⚠️ فشل جلب التحذيرات: {e}")
    return warnings


# ============================================================================
# 9. تهيئة المدير الذكي و ORCHESTRATOR للتوافق
# ============================================================================

SMART_MANAGER = SmartConversationManager(GROQ_API_KEY, GEMINI_API_KEY)
logger.info("🧠 SmartConversationManager جاهز!")


class ConversationOrchestrator:
    def __init__(self):
        self.name = "تولين - المنسقة"

    def orchestrate(self, text: str, context: Dict, chat_id: str, tcn_failed: bool = True) -> str:
        return SMART_MANAGER.process_message(text, chat_id, context)


# ====================================================================================
# 📦 PART 24 - قسم التوقعات المسبقة (Prior Judgment + حفظ وتحديث التوقعات)
# ====================================================================================
# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطبقة هنا):
# ═══════════════════════════════════════════════════════════════════════════════
# 1. التوقعات تعتمد على جميع المؤشرات الفنية (RSI, ADX, MACD, حجم, VPT, إلخ)
# 2. تحلل جميع الفريمات الأربعة من خلال analysis["timeframes"].
# 3. تستخدم base_timeframe لاستخراج المؤشرات من الفريم الصحيح.
# 4. تحفظ التوقعات في Supabase وتتعلم من الأخطاء.
# ═══════════════════════════════════════════════════════════════════════════════
# ====================================================================================

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

# ============================================================================
# 1. دالة توليد التوقع المسبق (Prior Judgment)
# ============================================================================

def generate_prior_judgment(analysis: Dict, asset_type: str, trade_type: str = "BUY",
                           entry_price: float = None, sl_price: float = None, tp_price: float = None,
                           base_timeframe: str = "Min15", trade_id: str = None) -> Dict:
    """
    توليد توقع مسبق للصفقة بناءً على تحليل دقيق ومرن.
    ✅ يعتمد على معايير رياضية موزونة.
    ✅ يقرأ المؤشرات من الفريم الصحيح (الممرر في base_timeframe).
    ✅ إذا كانت المؤشرات مفقودة، يعيد "بيانات غير كافية" بدلاً من قيم افتراضية.
    """
    # Initialize before any early return/default construction.
    adaptive = None
    default_result = {
        'verdict': 'loss',
        'confidence': 30,
        'reasoning': 'بيانات غير كافية للتوقع',
        'quality_score': 30,
        'similar_patterns_count': 0,
        'similar_lessons_count': 0,
        'red_flags': ['بيانات غير كافية'],
        'regime': 'unknown',
        'expected_value': 0.0,
        'calibration_factor': 1.0,
        'indicator_scores': {},
        'false_signal_score': 0,
        'false_signal_reasons': []
    }

    if not analysis:
        return default_result

    tf_key = base_timeframe.replace("Min", "m")
    timeframes = analysis.get('timeframes', {})
    tf_data = timeframes.get(tf_key, {})

    rsi = tf_data.get('rsi')
    adx = tf_data.get('adx')
    macd = tf_data.get('macd')
    vol_ratio = tf_data.get('volume_ratio')
    trend = tf_data.get('trend', 'محايد')
    supertrend = tf_data.get('supertrend', {})
    price = analysis.get('price', entry_price)
    vpt = tf_data.get('vpt')
    stoch = tf_data.get('stochastic')
    bb = tf_data.get('bollinger', {})
    vwap = tf_data.get('vwap')
    atr = tf_data.get('atr')

    if rsi is None or adx is None:
        logger.warning(f"⚠️ [generate_prior_judgment] مؤشرات مفقودة للفريم {tf_key} (rsi={rsi}, adx={adx})")
        default_result['reasoning'] = f'بيانات غير كافية للفريم {tf_key} (RSI أو ADX مفقود)'
        default_result['red_flags'] = ['مؤشرات مفقودة']
        return default_result

    bullish_count = 0
    bearish_count = 0
    total_frames = 0
    for tf_name, tf_data_item in timeframes.items():
        tf_trend = tf_data_item.get('trend')
        if tf_trend == 'صاعد':
            bullish_count += 1
            total_frames += 1
        elif tf_trend == 'هابط':
            bearish_count += 1
            total_frames += 1

    indicators = analysis.get('indicators', {})
    trend_data = indicators.get('trend', {})
    current_trend = trend_data.get('current_trend', trend)

    rr = 1.0
    if entry_price and sl_price and tp_price and entry_price > 0:
        if trade_type == "BUY":
            risk = entry_price - sl_price
            reward = tp_price - entry_price
        else:
            risk = sl_price - entry_price
            reward = entry_price - tp_price
        if risk > 0:
            rr = reward / risk

    weights = {
        'frames': 0.25,
        'trend_alignment': 0.15,
        'adx': 0.15,
        'rsi': 0.10,
        'macd': 0.08,
        'volume': 0.07,
        'rr': 0.05,
        'vpt': 0.05,
        'stoch': 0.05,
        'bollinger': 0.05
    }

    scores = {}
    reasons = []

    if total_frames >= 3:
        if trade_type == "BUY":
            frame_score = (bullish_count / total_frames) * 100
        else:
            frame_score = (bearish_count / total_frames) * 100
        scores['frames'] = frame_score
        if frame_score >= 75:
            reasons.append(f"✅ {int(frame_score)}% من الفريمات تدعم الاتجاه")
        elif frame_score >= 50:
            reasons.append(f"🟡 {int(frame_score)}% من الفريمات تدعم الاتجاه (متوسطة)")
        else:
            reasons.append(f"🔴 {int(frame_score)}% من الفريمات تدعم الاتجاه (ضعيفة)")
    else:
        scores['frames'] = 50
        reasons.append("🟡 عدد الفريمات غير كافٍ")

    if current_trend:
        if (trade_type == "BUY" and current_trend == "صاعد") or (trade_type == "SELL" and current_trend == "هابط"):
            trend_alignment = 100
            reasons.append(f"✅ الاتجاه العام {current_trend} يدعم الصفقة")
        elif (trade_type == "BUY" and current_trend == "هابط") or (trade_type == "SELL" and current_trend == "صاعد"):
            trend_alignment = 0
            reasons.append(f"🔴 الاتجاه العام {current_trend} يعاكس الصفقة")
        else:
            trend_alignment = 50
            reasons.append("🟡 الاتجاه العام محايد")
    else:
        trend_alignment = 50
        reasons.append("🟡 الاتجاه العام غير معروف")
    scores['trend_alignment'] = trend_alignment

    if adx >= 30:
        adx_score = 100
        reasons.append(f"✅ ADX قوي ({adx:.0f})")
    elif adx >= 20:
        adx_score = 70
        reasons.append(f"🟡 ADX متوسط ({adx:.0f})")
    elif adx >= 15:
        adx_score = 40
        reasons.append(f"🔴 ADX ضعيف ({adx:.0f})")
    else:
        adx_score = 20
        reasons.append(f"🚨 ADX ضعيف جداً ({adx:.0f})")
    scores['adx'] = adx_score

    if trade_type == "BUY":
        if rsi < 30:
            rsi_score = 100
            reasons.append(f"✅ RSI في منطقة ذروة بيع ({rsi:.0f})")
        elif rsi < 45:
            rsi_score = 80
            reasons.append(f"🟢 RSI منخفض ({rsi:.0f})")
        elif rsi < 60:
            rsi_score = 60
            reasons.append(f"🟡 RSI محايد ({rsi:.0f})")
        elif rsi < 75:
            rsi_score = 30
            reasons.append(f"🔴 RSI مرتفع ({rsi:.0f})")
        else:
            rsi_score = 10
            reasons.append(f"🚨 RSI مرتفع جداً ({rsi:.0f})")
    else:
        if rsi > 70:
            rsi_score = 100
            reasons.append(f"✅ RSI في منطقة ذروة شراء ({rsi:.0f})")
        elif rsi > 55:
            rsi_score = 80
            reasons.append(f"🟢 RSI مرتفع ({rsi:.0f})")
        elif rsi > 40:
            rsi_score = 60
            reasons.append(f"🟡 RSI محايد ({rsi:.0f})")
        elif rsi > 25:
            rsi_score = 30
            reasons.append(f"🔴 RSI منخفض ({rsi:.0f})")
        else:
            rsi_score = 10
            reasons.append(f"🚨 RSI منخفض جداً ({rsi:.0f})")
    scores['rsi'] = rsi_score

    if macd is not None:
        if (trade_type == "BUY" and macd > 0) or (trade_type == "SELL" and macd < 0):
            macd_score = 100
            reasons.append(f"✅ MACD يدعم الاتجاه ({macd:.3f})")
        elif abs(macd) < 0.001:
            macd_score = 50
            reasons.append("🟡 MACD محايد")
        else:
            macd_score = 20
            reasons.append(f"🔴 MACD يعاكس الاتجاه ({macd:.3f})")
    else:
        macd_score = 50
        reasons.append("🟡 MACD غير متوفر")
    scores['macd'] = macd_score

    if vol_ratio is not None:
        if vol_ratio >= 1.5:
            volume_score = 100
            reasons.append(f"✅ حجم مرتفع ({vol_ratio:.1f}x)")
        elif vol_ratio >= 0.8:
            volume_score = 70
            reasons.append(f"🟡 حجم طبيعي ({vol_ratio:.1f}x)")
        elif vol_ratio >= 0.5:
            volume_score = 40
            reasons.append(f"🔴 حجم منخفض ({vol_ratio:.1f}x)")
        else:
            volume_score = 20
            reasons.append(f"🚨 حجم جاف جداً ({vol_ratio:.1f}x)")
    else:
        volume_score = 50
        reasons.append("🟡 الحجم غير متوفر")
    scores['volume'] = volume_score

    if rr >= 2.0:
        rr_score = 100
        reasons.append(f"✅ RR ممتاز ({rr:.2f})")
    elif rr >= 1.5:
        rr_score = 80
        reasons.append(f"🟢 RR جيد ({rr:.2f})")
    elif rr >= 1.0:
        rr_score = 60
        reasons.append(f"🟡 RR متوسط ({rr:.2f})")
    else:
        rr_score = 20
        reasons.append(f"🔴 RR منخفض ({rr:.2f})")
    scores['rr'] = rr_score

    if vpt is not None:
        if (trade_type == "BUY" and vpt > 0) or (trade_type == "SELL" and vpt < 0):
            vpt_score = 100
            reasons.append(f"✅ VPT يدعم الاتجاه ({vpt:.2f})")
        else:
            vpt_score = 30
            reasons.append(f"🔴 VPT يعاكس الاتجاه ({vpt:.2f})")
    else:
        vpt_score = 50
        reasons.append("🟡 VPT غير متوفر")
    scores['vpt'] = vpt_score

    if stoch is not None:
        if (trade_type == "BUY" and stoch < 30) or (trade_type == "SELL" and stoch > 70):
            stoch_score = 100
            reasons.append(f"✅ Stochastic يدعم الاتجاه ({stoch:.0f})")
        elif 30 <= stoch <= 70:
            stoch_score = 60
            reasons.append(f"🟡 Stochastic محايد ({stoch:.0f})")
        else:
            stoch_score = 20
            reasons.append(f"🔴 Stochastic يعاكس الاتجاه ({stoch:.0f})")
    else:
        stoch_score = 50
        reasons.append("🟡 Stochastic غير متوفر")
    scores['stoch'] = stoch_score

    if bb.get('upper') and bb.get('lower') and price:
        bb_pos = (price - bb['lower']) / (bb['upper'] - bb['lower']) if (bb['upper'] - bb['lower']) > 0 else 0.5
        if (trade_type == "BUY" and bb_pos < 0.3) or (trade_type == "SELL" and bb_pos > 0.7):
            bb_score = 100
            reasons.append(f"✅ بولينجر يدعم الاتجاه (الموضع: {bb_pos:.0%})")
        elif 0.3 <= bb_pos <= 0.7:
            bb_score = 60
            reasons.append(f"🟡 بولينجر محايد (الموضع: {bb_pos:.0%})")
        else:
            bb_score = 20
            reasons.append(f"🔴 بولينجر يعاكس الاتجاه (الموضع: {bb_pos:.0%})")
    else:
        bb_score = 50
        reasons.append("🟡 بولينجر غير متوفر")
    scores['bollinger'] = bb_score

    total_score = 0
    total_weight = 0
    for key, score in scores.items():
        weight = weights.get(key, 0)
        total_score += score * weight
        total_weight += weight

    if total_weight > 0:
        final_score = total_score / total_weight
    else:
        final_score = 50

    final_score = max(0, min(100, final_score))
    confidence = final_score
    verdict = 'win' if confidence >= 50 else 'loss'

    reasoning_parts = []
    if verdict == 'win':
        reasoning_parts.append(f"التقييم الشامل: {final_score:.1f}%")
        if final_score >= 80:
            reasoning_parts.append("تقييم قوي جداً - فرصة ممتازة")
        elif final_score >= 65:
            reasoning_parts.append("تقييم جيد - فرصة مناسبة")
        else:
            reasoning_parts.append("تقييم متوسط - فرصة مقبولة")
    else:
        reasoning_parts.append(f"التقييم الشامل: {final_score:.1f}%")
        if final_score < 30:
            reasoning_parts.append("تقييم ضعيف جداً - تجنب الصفقة")
        elif final_score < 40:
            reasoning_parts.append("تقييم ضعيف - مخاطرة عالية")
        else:
            reasoning_parts.append("تقييم دون المتوسط - غير موصى به")

    if adx > 25:
        reasoning_parts.append(f"ADX قوي ({adx:.0f})")
    if vol_ratio is not None and vol_ratio > 1.2:
        reasoning_parts.append(f"حجم جيد ({vol_ratio:.1f}x)")
    if rr >= 2.0:
        reasoning_parts.append(f"RR ممتاز ({rr:.2f})")
    if vpt is not None and ((trade_type == "BUY" and vpt > 0) or (trade_type == "SELL" and vpt < 0)):
        reasoning_parts.append(f"VPT يدعم الاتجاه ({vpt:.2f})")

    if trade_type == "BUY" and current_trend == "هابط":
        reasoning_parts.append("⚠️ تناقض: الاتجاه العام هابط مع إشارة شراء")
    elif trade_type == "SELL" and current_trend == "صاعد":
        reasoning_parts.append("⚠️ تناقض: الاتجاه العام صاعد مع إشارة بيع")

    if trade_type == "BUY" and bearish_count >= 3:
        reasoning_parts.append(f"⚠️ {bearish_count}/4 فريمات هابطة ضد الشراء")
    elif trade_type == "SELL" and bullish_count >= 3:
        reasoning_parts.append(f"⚠️ {bullish_count}/4 فريمات صاعدة ضد البيع")

    reasoning = "تولين: " + "، ".join(reasoning_parts[:5]) if reasoning_parts else "لا توجد أسباب واضحة"

    if not trade_id:
        trade_id = f"{asset_type}_{int(datetime.now().timestamp())}"

    # 🧠 التعلم التراكمي: لا يغير SuperTrend، بل يقدر احتمال نجاح/فشل الإشارة.
    adaptive = None
    if ADAPTIVE_ENGINE is not None:
        try:
            adaptive = ADAPTIVE_ENGINE.predict(
                analysis, asset_type, trade_type, entry_price, sl_price, tp_price
            )
            if adaptive:
                verdict = adaptive.get('verdict', verdict)
                confidence = adaptive.get('confidence', confidence)
                final_score = adaptive.get('probability', final_score)
                reasons.append(f"🧠 التاريخ التراكمي: احتمال نجاح {adaptive.get('probability', 0):.0f}%")
                if adaptive.get('false_signal_score', 0) >= 50:
                    reasons.append(f"⚠️ خطر فشل تاريخي مرتفع ({adaptive.get('false_signal_score')}%)")
        except Exception as e:
            logger.error(f"❌ فشل التعلم التراكمي أثناء التوقع: {e}")

    if adaptive and adaptive.get('reasoning'):
        reasoning = adaptive['reasoning']

    prediction_data = {
        'trade_id': trade_id,
        'asset_type': asset_type,
        'trade_type': trade_type,
        'predicted_outcome': verdict,
        'confidence': int(round(confidence)),
        'entry_price': entry_price,
        'quality_score': int(round(final_score)),
        'regime': adaptive.get('regime', _get_market_regime(analysis)) if adaptive else _get_market_regime(analysis),
        'conditions': {
            'score': final_score,
            'adx': adx,
            'rsi': rsi,
            'vol_ratio': vol_ratio,
            'trade_type': trade_type,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'total_frames': total_frames,
            'macd': macd,
            'current_trend': current_trend,
            'rr': rr,
            'vpt': vpt,
            'stoch': stoch,
            'bb_pos': (price - bb.get('lower', 0)) / (bb.get('upper', 1) - bb.get('lower', 1)) if bb.get('upper') and bb.get('lower') and bb['upper'] > bb['lower'] else 0.5,
            'base_timeframe': base_timeframe,
            'adaptive_probability': adaptive.get('probability') if adaptive else None,
            'adaptive_effective_sample': adaptive.get('effective_sample') if adaptive else 0,
            'adaptive_similar_win_rate': adaptive.get('similar_win_rate') if adaptive else None,
            'adaptive_global_win_rate': adaptive.get('global_win_rate') if adaptive else None,
            'adaptive_calibration_factor': adaptive.get('calibration_factor') if adaptive else 1.0,
            'adaptive_asset_direction_sample': adaptive.get('asset_direction_sample') if adaptive else 0
        },
        'indicator_scores': scores,
        'red_flags': [r for r in reasons if '🚨' in r or '⚠️' in r],
        'similar_patterns_count': adaptive.get('similar_count', 0) if adaptive else 0,
        'similar_lessons_count': 0,
        'false_signal_score': adaptive.get('false_signal_score', 0) if adaptive else 0,
        'false_signal_reasons': adaptive.get('false_signal_reasons', []) if adaptive else []
    }

    save_success = save_prediction_to_supabase(prediction_data)
    if save_success:
        logger.info(f"✅ [generate_prior_judgment] تم حفظ التوقع للصفقة {trade_id} في Supabase")
    else:
        logger.error(f"❌ [generate_prior_judgment] فشل حفظ التوقع للصفقة {trade_id} في Supabase")

    return {
        'verdict': verdict,
        'confidence': int(round(confidence)),
        'reasoning': reasoning[:300],
        'quality_score': int(round(final_score)),
        'similar_patterns_count': adaptive.get('similar_count', 0) if adaptive else 0,
        'similar_lessons_count': 0,
        'red_flags': adaptive.get('red_flags', [r for r in reasons if '🚨' in r or '⚠️' in r]) if adaptive else [r for r in reasons if '🚨' in r or '⚠️' in r],
        'regime': adaptive.get('regime', _get_market_regime(analysis)) if adaptive else _get_market_regime(analysis),
        'expected_value': adaptive.get('expected_profit', 0.0) if adaptive else 0.0,
        'calibration_factor': adaptive.get('calibration_factor', 1.0) if adaptive else 1.0,
        'indicator_scores': adaptive.get('indicator_scores', scores) if adaptive else scores,
        'false_signal_score': adaptive.get('false_signal_score', 0) if adaptive else 0,
        'false_signal_reasons': adaptive.get('false_signal_reasons', []) if adaptive else [],
        'prediction_id': trade_id,
    }

def _get_market_regime(analysis):
    indicators = analysis.get('indicators', {})
    trend_data = indicators.get('trend', {})
    adx = trend_data.get('adx', 20)
    if adx is None:
        return 'unknown'
    if adx > 30:
        return 'trending'
    elif adx > 20:
        return 'volatile'
    else:
        return 'ranging'

# ============================================================================
# 2. حفظ التوقع في Supabase
# ============================================================================

def save_prediction_to_supabase(prediction_data):
    if not prediction_data:
        logger.warning("⚠️ [save_prediction_to_supabase] بيانات التوقع فارغة")
        return False

    trade_id = prediction_data.get('trade_id')
    if not trade_id:
        logger.warning("⚠️ [save_prediction_to_supabase] trade_id مفقود")
        return False

    logger.info(f"💾 [save_prediction_to_supabase] بدء حفظ التوقع {trade_id}")

    supabase_saved = False
    if SUPABASE_AVAILABLE and SUPABASE_DB:
        try:
            # ✅ استخدام الدالة الموحدة من PART 10
            client = _get_supabase_client()
            if client is None:
                logger.error("❌ [save_prediction_to_supabase] لا يمكن الحصول على عميل Supabase")
                return False

            filtered_data = _filter_data_for_table(prediction_data, TABLE_TRADE_PREDICTIONS)
            
            json_fields = ['conditions', 'indicator_scores', 'red_flags', 'false_signal_reasons']
            for field in json_fields:
                if field in filtered_data and filtered_data[field] is not None:
                    if isinstance(filtered_data[field], (dict, list)):
                        filtered_data[field] = json.dumps(filtered_data[field], ensure_ascii=False)

            check = client.table(TABLE_TRADE_PREDICTIONS).select('trade_id').eq('trade_id', trade_id).execute()
            if check and hasattr(check, 'data') and check.data:
                response = client.table(TABLE_TRADE_PREDICTIONS).update(filtered_data).eq('trade_id', trade_id).execute()
                logger.info(f"🔄 [save_prediction_to_supabase] تحديث {trade_id}")
            else:
                response = client.table(TABLE_TRADE_PREDICTIONS).insert(filtered_data).execute()
                logger.info(f"➕ [save_prediction_to_supabase] إدراج {trade_id}")

            if response and hasattr(response, 'data'):
                verify = client.table(TABLE_TRADE_PREDICTIONS).select('*').eq('trade_id', trade_id).execute()
                if verify and hasattr(verify, 'data') and verify.data:
                    supabase_saved = True
                    logger.info(f"✅ [save_prediction_to_supabase] تم تأكيد حفظ {trade_id}")

        except Exception as e:
            logger.error(f"❌ [save_prediction_to_supabase] استثناء: {e}")
            import traceback
            logger.error(traceback.format_exc())
    else:
        logger.warning("⚠️ [save_prediction_to_supabase] Supabase غير متوفر")

    # ── نسخة احتياطية محلية ──
    local_saved = False
    try:
        backup_file = "learning_data/backups/predictions_backup.json"
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)

        backup_data = {}
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

        predictions = backup_data.get('predictions', [])
        predictions = [p for p in predictions if p.get('trade_id') != trade_id]
        predictions.append(prediction_data)
        if len(predictions) > 500:
            predictions = predictions[-500:]

        backup_data['predictions'] = predictions
        backup_data['last_update'] = datetime.now().isoformat()

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        local_saved = True
        logger.info(f"💾 [save_prediction_to_supabase] تم حفظ نسخة احتياطية في {backup_file}")
    except Exception as e:
        logger.error(f"❌ [save_prediction_to_supabase] فشل النسخة الاحتياطية: {e}")

    return supabase_saved or local_saved

# ============================================================================
# 3. تحديث نتيجة التوقع بعد الإغلاق
# ============================================================================

def update_prediction_result(trade_id: str, actual_outcome: str, profit_dollars: float, exit_price: float):
    if not trade_id:
        logger.warning("⚠️ [update_prediction_result] trade_id مفقود")
        return False

    logger.info(f"📊 [update_prediction_result] تحديث {trade_id} -> {actual_outcome}")

    supabase_updated = False
    if SUPABASE_AVAILABLE and SUPABASE_DB:
        try:
            client = _get_supabase_client()
            if client is None:
                logger.error("❌ [update_prediction_result] لا يمكن الحصول على عميل Supabase")
                return False

            existing = client.table(TABLE_TRADE_PREDICTIONS).select('predicted_outcome').eq('trade_id', trade_id).limit(1).execute()
            predicted = existing.data[0].get('predicted_outcome') if existing and getattr(existing, 'data', None) else None
            update_data = {
                'actual_outcome': actual_outcome,
                'profit_dollars': float(profit_dollars),
                'exit_price': float(exit_price) if exit_price else None,
                'updated_at': datetime.now().isoformat(),
                'was_correct': (predicted == actual_outcome) if predicted else None
            }
            response = client.table(TABLE_TRADE_PREDICTIONS).update(update_data).eq('trade_id', trade_id).execute()
            if response and hasattr(response, 'data'):
                supabase_updated = True
                logger.info(f"✅ [update_prediction_result] تم تحديث {trade_id} في Supabase")
        except Exception as e:
            logger.error(f"❌ [update_prediction_result] استثناء: {e}")
            import traceback
            logger.error(traceback.format_exc())
    else:
        logger.warning("⚠️ [update_prediction_result] Supabase غير متوفر")

    # ── تحديث النسخة الاحتياطية المحلية ──
    local_updated = False
    try:
        backup_file = "learning_data/backups/predictions_backup.json"
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            predictions = backup_data.get('predictions', [])
            for p in predictions:
                if p.get('trade_id') == trade_id:
                    p['actual_outcome'] = actual_outcome
                    p['profit_dollars'] = float(profit_dollars)
                    p['exit_price'] = float(exit_price) if exit_price else None
                    p['updated_at'] = datetime.now().isoformat()
                    p['was_correct'] = (p.get('predicted_outcome') == actual_outcome)
                    break

            backup_data['predictions'] = predictions
            backup_data['last_update'] = datetime.now().isoformat()

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)

            local_updated = True
            logger.info(f"💾 [update_prediction_result] تم تحديث النسخة الاحتياطية")
    except Exception as e:
        logger.error(f"❌ [update_prediction_result] فشل النسخة الاحتياطية: {e}")

    return supabase_updated or local_updated

# ============================================================================
# 4. تحديث معايرة التوقعات
# ============================================================================

def update_prediction_calibration():
    """تحديث معايير التوقع بناءً على نتائج التوقعات السابقة"""
    try:
        if not SUPABASE_AVAILABLE or not SUPABASE_DB:
            logger.warning("⚠️ Supabase غير متوفر، لا يمكن تحديث المعايرة")
            return

        client = _get_supabase_client()
        if client is None:
            logger.warning("⚠️ [update_prediction_calibration] لا يمكن الحصول على عميل Supabase")
            return

        response = client.table(TABLE_TRADE_PREDICTIONS).select('*').not_.is_('actual_outcome', 'null').limit(100).execute()
        if not response or not response.data:
            logger.info("ℹ️ لا توجد توقعات سابقة للتحديث")
            return

        predictions = response.data
        if len(predictions) < 10:
            logger.info(f"ℹ️ عدد التوقعات غير كافٍ للتحديث ({len(predictions)})")
            return

        total = len(predictions)
        correct = sum(1 for p in predictions if p.get('was_correct', False))
        accuracy = correct / total if total > 0 else 0

        logger.info(f"📊 دقة التوقعات الحالية: {accuracy*100:.1f}% ({correct}/{total})")

        if accuracy < 0.6:
            logger.info("🔄 دقة التوقعات منخفضة، جارٍ تحديث المعايير...")
            calibration_file = "learning_data/calibration_weights.json"
            weights = {
                'frames': 0.30,
                'trend_alignment': 0.15,
                'adx': 0.15,
                'rsi': 0.10,
                'macd': 0.08,
                'volume': 0.07,
                'rr': 0.05,
                'vpt': 0.05,
                'stoch': 0.05,
                'bollinger': 0.05
            }
            try:
                os.makedirs(os.path.dirname(calibration_file), exist_ok=True)
                with open(calibration_file, 'w') as f:
                    json.dump(weights, f, indent=2)
                logger.info(f"✅ تم تحديث أوزان المعايرة: {weights}")
            except Exception as e:
                logger.error(f"❌ فشل حفظ أوزان المعايرة: {e}")

    except Exception as e:
        logger.error(f"❌ فشل تحديث المعايرة: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ====================================================================================
# نهاية PART 24 - قسم التوقعات
# ====================================================================================

# ====================================================================================
# 📦 PART 24.5: Orchestrator - منسق المحادثة (مع منع تكرار TCN)
# ====================================================================================

class ConversationOrchestrator:
    """
    🧠 منسق المحادثة - يدمج جميع المحركات في رد واحد متكامل
    ✅ لا يستدعي TCN إذا كان قد فشل بالفعل في الطبقة العليا
    """
    
    def __init__(self):
        self.name = "تولين - المنسقة"
    
    def orchestrate(self, text: str, context: Dict, chat_id: str, tcn_failed: bool = True) -> str:
        """
        ينسق بين جميع المحركات وينتج رداً واحداً متكاملاً
        tcn_failed: علم بأن TCN قد فشل أو لم يتعرف على السؤال
        """
        msg_lower = text.lower()
        
        # ── ✅ من أنت - أولوية قصوى ──
        if any(k in msg_lower for k in ["من أنت", "من انت", "who are you", "اسمك", "تعريف"]):
            return self._who_am_i_response()
        
        # ── ✅ الترحيب ──
        if msg_lower in ["مرحبا", "اهلا", "سلام", "هلا", "hi", "hello", "السلام عليكم"]:
            open_trades = context.get('open_trades', {})
            if open_trades:
                return f"👋 **تولين:** أهلاً بك يا صديقي! لدي {len(open_trades)} صفقة مفتوحة معك. هل تريد مراجعتها؟ 💙"
            return "👋 **تولين:** أهلاً بك يا صديقي! كيف يمكنني مساعدتك اليوم؟ 💙"
        
        # ── ✅ كيف حالك ──
        if any(k in msg_lower for k in ["كيف حالك", "كيفك", "how are you", "شو اخبارك"]):
            emotion = context.get('prometheus_emotion', 'متزنة')
            confidence = context.get('prometheus_confidence', 0.5) * 100
            return f"💙 **تولين:** أنا {emotion}، ثقتي {confidence:.0f}%. كيف حالك أنت؟"
        
        # ── ✅ ماذا تفعلين ──
        if any(k in msg_lower for k in ["ماذا تفعلين", "what are you doing", "شو تعملين", "مهامك"]):
            return self._build_what_doing_response(context)
        
        # ── ✅ مالجديد ──
        if any(k in msg_lower for k in ["مالجديد", "ما الجديد", "what's new", "whats new", "مستجدات"]):
            return self._build_whats_new_response(context)
        
        # ── ✅ الأسئلة التداولية → TCN (لكن إذا فشل، استخدم Advisor) ──
        trading_keywords = [
            "السوق", "سوق", "نفط", "فضة", "صفقة", "تحليل",
            "توصية", "توقع", "طالع", "نازل", "صاعد", "هابط",
            "إشارة", "شراء", "بيع", "خطر", "مخاطرة", "وضع السوق"
        ]
        
        if any(k in msg_lower for k in trading_keywords):
            # إذا كان TCN قد فشل، لا نعيد استدعاءه
            if tcn_failed:
                return self._orchestrate_trading_fallback(text, context, chat_id)
            else:
                return self._orchestrate_trading(text, context, chat_id)
        
        # ── ✅ الأسئلة العامة → Groq API ──
        general_keywords = [
            "ما هو", "ما هي", "ماهو", "ماهي", "what is", "what are",
            "ماذا تعني", "what does", "كيف يعمل", "how does",
            "لماذا", "why", "متى", "when", "أين", "where",
            "تعريف", "definition", "معنى", "meaning",
            "عاصمة", "capital", "تضخم", "فائدة", "عملات", "اقتصاد",
            "الذهب", "ذهب", "gold", "bitcoin", "بيتكوين"
        ]
        
        if any(k in msg_lower for k in general_keywords):
            if GROQ_API_KEY and GROQ_API_KEY != "" and "test_" not in GROQ_API_KEY:
                try:
                    # ✅ التعديل هنا: استبدال generate_groq_chat_response بـ SMART_MANAGER._call_groq_simple
                    resp = SMART_MANAGER._call_groq_simple([
                        {"role": "system", "content": "أنت تولين، مستشارة استراتيجية ودودة ومحترفة. أجب باختصار وذكاء، ولا تختلق بيانات تداول وهمية."},
                        {"role": "user", "content": text}
                    ], max_tokens=500)
                    if resp and len(resp) > 5:
                        return resp
                except Exception as e:
                    logger.error(f"❌ Groq API فشل: {e}")
            return f"💙 **تولين:** سؤال جميل يا صديقي! {text}... هل تريد معرفة شيء محدد عن النفط أو الفضة؟"
        
        # ── ✅ باقي الأسئلة ──
        return self._orchestrate_normal(text, context, chat_id)
    
    def _who_am_i_response(self) -> str:
        return """💙 **أنا تولين**

📌 مستشارتك الاستراتيجية المتخصصة في تحليل النفط والفضة.
👨‍💻 طورني المطور بسام الحوباني.
📦 الإصدار: V13.0

🎯 **خبراتي:**
   • تحليل فني متقدم باستخدام جميع المؤشرات الرئيسية
   • تحليل أساسي وأخبار السوق
   • إدارة المخاطر بشكل احترافي
   • تحليل المشاعر والثقة
   • التنبؤ بالاتجاهات

💡 **كيف أساعدك:**
   • أقدم توصيات واضحة: استمر، اغلق، انتظر، ادخل
   • أحلل الصفقات المفتوحة وأقترح الإجراءات المناسبة
   • أراقب السوق وأحدثك بأي تغيير مهم

💙 أنا هنا لخدمتك، اسألني عن أي شيء!"""
    
    def _orchestrate_trading(self, text: str, context: Dict, chat_id: str) -> str:
        """
        توجيه الأسئلة التداولية إلى TCN (إذا لم يكن قد فشل)
        """
        if not TCN_AVAILABLE or not TCN:
            logger.warning("⚠️ TCN غير متوفر، استخدام Fallback")
            return self._orchestrate_normal(text, context, chat_id)
        
        try:
            market_data = context.get('market_snapshot', {})
            consciousness = TCN.think(
                market_data=market_data,
                user_context=context,
                user_message=text
            )
            
            if hasattr(consciousness, 'professional_response') and consciousness.professional_response:
                return consciousness.professional_response
            
            if consciousness and consciousness.narrative:
                return self._format_tcn_trading_response(consciousness, context)
            
        except Exception as e:
            logger.error(f"❌ TCN فشل في معالجة السؤال التداولي: {e}")
        
        return self._orchestrate_trading_fallback(text, context, chat_id)
    
    def _orchestrate_trading_fallback(self, text: str, context: Dict, chat_id: str) -> str:
        """البديل عندما يفشل TCN في الأسئلة التداولية"""
        # محاولة استخدام Advisor
        if ADVISOR_AVAILABLE and ADVISOR:
            try:
                if hasattr(ADVISOR, 'chat'):
                    resp = ADVISOR.chat(text, chat_id, context=context)
                    if resp and len(resp) > 10:
                        return resp
            except Exception as e:
                logger.warning(f"⚠️ Advisor فشل: {e}")
        
        # محاولة استخدام ConversationEngine
        if CONVERSATION_AVAILABLE and CONVERSATION_ENGINE:
            try:
                if hasattr(CONVERSATION_ENGINE, 'process'):
                    resp = CONVERSATION_ENGINE.process(text, chat_id, context=context)
                    if resp and len(resp) > 10:
                        return resp
            except Exception as e:
                logger.warning(f"⚠️ Conversation فشل: {e}")
        
        return self._orchestrate_normal(text, context, chat_id)
    
    def _format_tcn_trading_response(self, consciousness, context) -> str:
        """تنسيق رد TCN للأسئلة التداولية"""
        lines = []
        
        emotion_emoji = {
            'excited': '🌟', 'happy': '😊', 'optimistic': '📈',
            'worried': '😟', 'cautious': '🤔', 'fearful': '😰',
            'neutral': '💙'
        }.get(consciousness.dominant_emotion, '💙')
        
        lines.append(f"{emotion_emoji} **تولين:**")
        lines.append("")
        
        if consciousness.narrative:
            lines.append(f"📖 {consciousness.narrative}")
            lines.append("")
        
        lines.append(f"📊 **ثقتي:** {consciousness.confidence*100:.0f}%")
        
        action_map = {
            'buy_strong': '🟢 شراء قوي',
            'buy_weak': '🟡 شراء حذر',
            'sell_strong': '🔴 بيع قوي',
            'sell_weak': '🟠 بيع حذر',
            'wait': '⚪ انتظار',
            'wait_cautious': '⚠️ انتظار حذر'
        }
        lines.append(f"🎯 **قراري:** {action_map.get(consciousness.recommended_action, '❓ محايد')}")
        
        if hasattr(consciousness, 'market_data') and consciousness.market_data:
            lines.append("")
            lines.append("📊 **بيانات السوق:**")
            for asset, data in consciousness.market_data.items():
                label = "🛢️ النفط" if asset == "oil" else "🥈 الفضة"
                price = data.get('price', 0)
                signal = data.get('signal', 'WAIT')
                if price > 0:
                    emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
                    lines.append(f"   • {label}: ${price:.2f} {emoji}")
        
        lines.append("")
        lines.append("💙 هل تريد تفاصيل أكثر أو تحليلاً محدداً؟")
        
        return "\n".join(lines)
    
    def _orchestrate_normal(self, text: str, context: Dict, chat_id: str) -> str:
        """التنسيق العادي باستخدام جميع المحركات (بدون TCN)"""
        responses = {}
        
        if ADVISOR_AVAILABLE and ADVISOR:
            try:
                if hasattr(ADVISOR, 'chat'):
                    resp = ADVISOR.chat(text, chat_id, context=context)
                    if resp and len(resp) > 10:
                        responses['advisor'] = resp
            except Exception as e:
                logger.warning(f"⚠️ Advisor فشل: {e}")
        
        if CONVERSATION_AVAILABLE and CONVERSATION_ENGINE:
            try:
                if hasattr(CONVERSATION_ENGINE, 'process'):
                    resp = CONVERSATION_ENGINE.process(text, chat_id, context=context)
                    if resp and len(resp) > 10:
                        responses['conversation'] = resp
            except Exception as e:
                logger.warning(f"⚠️ Conversation فشل: {e}")
        
        if GROQ_API_KEY and GROQ_API_KEY != "" and "test_" not in GROQ_API_KEY:
            try:
                # ✅ التعديل هنا: استبدال generate_groq_chat_response بـ SMART_MANAGER._call_groq_simple
                resp = SMART_MANAGER._call_groq_simple([
                    {"role": "system", "content": "أنت تولين، مستشارة استراتيجية ودودة ومحترفة. أجب باختصار وذكاء، ولا تختلق بيانات تداول وهمية."},
                    {"role": "user", "content": text}
                ], max_tokens=500)
                if resp and len(resp) > 10:
                    responses['groq'] = resp
            except Exception as e:
                logger.warning(f"⚠️ Groq فشل: {e}")
        
        if AI_BRAIN_AVAILABLE and AI_BRAIN:
            try:
                if hasattr(AI_BRAIN, 'process'):
                    resp = AI_BRAIN.process(text, context=context)
                elif hasattr(AI_BRAIN, 'generate'):
                    resp = AI_BRAIN.generate(text, context=context)
                elif hasattr(AI_BRAIN, 'chat'):
                    resp = AI_BRAIN.chat(text, context=context)
                if resp and len(resp) > 10:
                    responses['ai_brain'] = resp
            except Exception as e:
                logger.warning(f"⚠️ AI Brain فشل: {e}")
        
        if FUSION_AVAILABLE and FUSION:
            try:
                if hasattr(FUSION, 'process_user_message'):
                    resp = FUSION.process_user_message(text, {
                        'emotion': context.get("prometheus_emotion", "neutral"),
                        'confidence': context.get("prometheus_confidence", 0.5),
                        'intent': context.get("intent"),
                        'context': context
                    })
                    if resp and len(resp) > 10:
                        responses['fusion'] = resp
            except Exception as e:
                logger.warning(f"⚠️ Fusion فشل: {e}")
        
        if not responses:
            return generate_enhanced_fallback(text, context)
        
        # دمج الردود
        if len(responses) == 1:
            text = list(responses.values())[0]
            if 'advisor' in responses:
                if text.startswith("💡 نصيحة:"):
                    text = text[10:].strip()
                elif text.startswith("نصيحة:"):
                    text = text[7:].strip()
                elif text.startswith("💡"):
                    text = text[2:].strip()
                text = "💙 **تولين:** " + text
            return text
        
        # اختيار الرد من المصدر الأكثر ثقة
        priority = ['advisor', 'conversation', 'groq', 'ai_brain', 'fusion']
        for source in priority:
            if source in responses:
                return responses[source]
        
        return list(responses.values())[0]
    
    def _build_what_doing_response(self, context: Dict) -> str:
        """رد مباشر على 'ماذا تفعلين' مع تحليل فعلي"""
        open_trades = context.get('open_trades', {})
        market = context.get('market_snapshot', {})
        
        lines = []
        lines.append("👁️ **تولين:**")
        lines.append("")
        
        if open_trades:
            lines.append(f"**أركز على {len(open_trades)} صفقة مفتوحة:**")
            for asset, trade in open_trades.items():
                label = "🛢️ النفط" if asset == "oil" else "🥈 الفضة"
                entry = trade.get('entry_price', 0)
                trade_type = trade.get('type', 'BUY')
                profit = trade.get('profit_dollars', 0)
                p_str = f"+${profit:.2f}" if profit > 0 else f"-${abs(profit):.2f}" if profit < 0 else "$0.00"
                p_emoji = "🟢" if profit > 0 else "🔴" if profit < 0 else "⚪"
                lines.append(f"   • {label}: {trade_type} عند ${entry:.2f} → {p_emoji} {p_str}")
            lines.append("")
        else:
            lines.append("**أبحث في الشارت عن فرص جديدة للنفط والفضة.**")
            lines.append("")
        
        lines.append("📊 **تحليل السوق لحظياً:**")
        
        oil = market.get('oil', {})
        silver = market.get('silver', {})
        oil_price = oil.get('price', 0)
        silver_price = silver.get('price', 0)
        oil_signal = oil.get('signal', 'WAIT')
        silver_signal = silver.get('signal', 'WAIT')
        oil_trend = oil.get('trend', 'محايد')
        silver_trend = silver.get('trend', 'محايد')
        
        if oil_price > 0:
            emoji = "🟢" if oil_signal == "BUY" else "🔴" if oil_signal == "SELL" else "⚪"
            lines.append(f"   • 🛢️ النفط: ${oil_price:.2f} ({oil_trend}) {emoji}")
        else:
            lines.append("   • 🛢️ النفط: جاري التحديث...")
        
        if silver_price > 0:
            emoji = "🟢" if silver_signal == "BUY" else "🔴" if silver_signal == "SELL" else "⚪"
            lines.append(f"   • 🥈 الفضة: ${silver_price:.2f} ({silver_trend}) {emoji}")
        else:
            lines.append("   • 🥈 الفضة: جاري التحديث...")
        
        lines.append("")
        if open_trades:
            lines.append("💡 **أنا هنا لمتابعة صفقاتك. هل تريد تحليلاً مفصلاً لأي منها؟**")
        else:
            lines.append("💡 **أنتظر إشارة واضحة قبل التوصية. هل تريد تحليلاً للسوق؟**")
        
        return "\n".join(lines)
    
    def _build_whats_new_response(self, context: Dict) -> str:
        """الرد على 'مالجديد' - عرض الأخبار والتغيرات الفعلية في السوق"""
        market = context.get('market_snapshot', {})
        open_trades = context.get('open_trades', {})
        
        oil = market.get('oil', {})
        silver = market.get('silver', {})
        
        oil_price = oil.get('price', 0)
        silver_price = silver.get('price', 0)
        oil_signal = oil.get('signal', 'WAIT')
        silver_signal = silver.get('signal', 'WAIT')
        oil_rsi = oil.get('rsi', 50)
        silver_rsi = silver.get('rsi', 50)
        
        fear_greed = context.get('market_context', {}).get('fear_greed', 50)
        
        lines = []
        lines.append("📊 **تولين:** يا صديقي، هذه آخر المستجدات:")
        lines.append("")
        
        news_items = []
        
        if oil_price > 0:
            news_items.append(f"🛢️ النفط عند ${oil_price:.2f} ({oil_signal})")
        
        if silver_price > 0:
            news_items.append(f"🥈 الفضة عند ${silver_price:.2f} ({silver_signal})")
        
        if oil_signal == "BUY" or silver_signal == "BUY":
            news_items.append("🟢 توجد إشارة شراء - راقب الفرصة")
        elif oil_signal == "SELL" or silver_signal == "SELL":
            news_items.append("🔴 توجد إشارة بيع - كن حذر")
        
        if oil_rsi > 70:
            news_items.append(f"🟡 النفط في منطقة تشبع شرائي (RSI: {oil_rsi:.0f})")
        elif oil_rsi < 30:
            news_items.append(f"🟢 النفط في منطقة تشبع بيعي (RSI: {oil_rsi:.0f})")
        
        if silver_rsi > 70:
            news_items.append(f"🟡 الفضة في منطقة تشبع شرائي (RSI: {silver_rsi:.0f})")
        elif silver_rsi < 30:
            news_items.append(f"🟢 الفضة في منطقة تشبع بيعي (RSI: {silver_rsi:.0f})")
        
        if open_trades:
            news_items.append(f"📋 يوجد {len(open_trades)} صفقة مفتوحة")
            for asset, trade in open_trades.items():
                label = "النفط" if asset == "oil" else "الفضة"
                profit = trade.get('profit_dollars', 0)
                p_str = f"+${profit:.2f}" if profit > 0 else f"-${abs(profit):.2f}" if profit < 0 else "$0.00"
                news_items.append(f"   • {label}: {trade.get('type', '?')} | {p_str}")
        
        if fear_greed:
            if fear_greed < 25:
                news_items.append(f"🚨 خوف شديد في السوق ({fear_greed}/100)")
            elif fear_greed > 75:
                news_items.append(f"🔥 طمع مفرط في السوق ({fear_greed}/100)")
            else:
                news_items.append(f"⚖️ السوق متوازن ({fear_greed}/100)")
        
        if news_items:
            for item in news_items:
                lines.append(f"• {item}")
        else:
            lines.append("🔄 لا توجد مستجدات جديدة حالياً")
        
        lines.append("")
        lines.append("💙 راقب السوق ولا تتردد في سؤالي عن أي شيء!")
        
        return "\n".join(lines)


# ====================================================================================
# نهاية PART 24.5
# ====================================================================================

# ====================================================================================
# 📦 PART 24.7: Hybrid Orchestrator - الوسيط الهجين الذكي (V2.0)
# ====================================================================================

"""
🧠 Hybrid Orchestrator V2.0 - الوسيط الهجين الذكي (المُحسّن)
─────────────────────────────────────────────────────────────────
يقوم بفصل مسؤوليات النماذج اللغوية إلى طبقات محددة:
1. التوجيه الصلب (Hard Router): تصنيف سريع للأسئلة الشائعة (قواعد Regex)
2. المصنف الخفيف (Lightweight Classifier): استخدام Gemini 3.5 Flash للتصنيف عند فشل القواعد
3. جلب البيانات (Data Fetcher): استدعاء دوال البوت المناسبة لجلب البيانات المؤكدة
4. الصياغة الذكية (Smart Formatter): تمرير البيانات للنموذج الكبير للصياغة فقط (يمنع الاختلاق)

✅ التحسينات الجديدة (V2.0):
- توسيع IntentRouter ليشمل جميع الأسئلة الشائعة (بما فيها "مالوضع الان")
- تحسين معالجة الأسئلة العامة (بدون إجابات غبية)
- تفسير توقعات الأسعار بلغة مفهومة (بدلاً من JSON الخام)
- منع التراجع إلى النظام القديم
- تحسين سرعة الاستجابة عبر التوجيه الصلب أولاً
─────────────────────────────────────────────────────────────────
"""

import re
import json
import time
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta


# ====================================================================================
# 1. IntentRouter - التوجيه الصلب (Hard Router) - موسع
# ====================================================================================

class IntentRouter:
    """
    🧭 الموجه الصلب - يستخدم قواعد Regex وكلمات مفتاحية لتصنيف النية بسرعة فائقة
    ⚡ الزمن: أقل من 0.2 ثانية
    🎯 التغطية: 85% من الأسئلة الشائعة
    """
    
    # قواعد الكلمات المفتاحية (موسعة جداً لتغطية أكبر قدر من الصيغ)
    RULES = {
        "PROFIT_TODAY": {
            "keywords": [
                "ربحت اليوم", "أرباح اليوم", "ربح اليوم", "كم كسبت اليوم",
                "النتيجة اليوم", "اليوم كم", "اليوم ربح", "اليوم خسارة",
                "today profit", "today pnl", "today's profit", "today's pnl",
                "ربحية اليوم", "صافي اليوم", "الدخل اليوم", "كم ربحت اليوم"
            ],
            "action": "get_todays_profit_loss"
        },
        "PROFIT_YESTERDAY": {
            "keywords": [
                "ربحت بالأمس", "أرباح الأمس", "ربح الأمس", "كم كسبت أمس",
                "النتيجة أمس", "أمس كم", "أمس ربح", "أمس خسارة",
                "yesterday profit", "yesterday pnl", "yesterday's profit",
                "ربحية أمس", "صافي أمس", "الدخل أمس", "اول امس", "أول أمس",
                "كم ربحت بالامس", "بالامس"
            ],
            "action": "get_profit_loss_by_date",
            "params": {"days_ago": 1}
        },
        "PROFIT_LAST_WEEK": {
            "keywords": [
                "ربحت الأسبوع", "أرباح الأسبوع", "ربح الأسبوع",
                "هذا الأسبوع", "الأسبوع الماضي", "الاسبوع الماضي",
                "this week", "last week", "weekly profit"
            ],
            "action": "get_trade_history_summary",
            "params": {"days": 7}
        },
        "OPEN_TRADES": {
            "keywords": [
                "صفقة مفتوحة", "صفقات مفتوحة", "هل هناك صفقة",
                "صفقة مفتوحة حاليا", "المراكز المفتوحة",
                "open trade", "open trades", "open position",
                "المراكز", "صفقات حالية", "التداول الآن",
                "هل هناك صفقة مفتوحة"
            ],
            "action": "get_open_trades"
        },
        "LAST_TRADE_STATUS": {
            "keywords": [
                "اخر صفقة", "آخر صفقة", "الصفقة الأخيرة",
                "نتيجة آخر صفقة", "آخر صفقة ربح ولا خسارة",
                "last trade", "last trade result", "previous trade",
                "ماذا حدث بآخر صفقة", "كيف كانت آخر صفقة",
                "هل ربحت اخر صفقة", "هل ربحت آخر صفقة"
            ],
            "action": "get_last_trade_status"
        },
        "LAST_TRADE_REASON": {
            "keywords": [
                "لماذا خسرت آخر صفقة", "سبب خسارة آخر صفقة",
                "لماذا ربحت آخر صفقة", "سبب نجاح آخر صفقة",
                "تحليل آخر صفقة", "لماذا خسرت الصفقة",
                "لماذا خسرت", "لماذا ربحت",
                "why last trade", "reason last trade",
                "تفسير آخر صفقة"
            ],
            "action": "analyze_last_trade"
        },
        "MARKET_QUERY": {
            "keywords": [
                "كيف السوق", "وضع السوق", "السوق اليوم",
                "تحليل السوق", "market", "السوق", "سوق اليوم",
                "تحليل النفط", "تحليل الفضة", "النفط اليوم", "الفضة اليوم",
                "وضع النفط", "وضع الفضة", "حركة السوق",
                "السوق هادئ", "السوق متقلب", "اتجاه السوق",
                "الوضع", "الوضع الان", "السوق الان", "مالوضع الان",
                "شو الاخبار", "اخبار السوق", "مستجدات"
            ],
            "action": "handle_market_query"
        },
        "PRICE_CHECK": {
            "keywords": [
                "سعر النفط", "سعر الفضة", "كم سعر النفط", "كم سعر الفضة",
                "oil price", "silver price", "سعر الذهب", "كم النفط",
                "سعر برنت", "سعر خام", "اسعار السوق"
            ],
            "action": "get_current_prices"
        },
        "BEST_TRADE": {
            "keywords": [
                "أفضل صفقة", "صفقة ناجحة", "أكبر ربح", "أفضل تداول",
                "best trade", "top trade", "highest profit",
                "أعلى ربح", "الصفقة الأفضل"
            ],
            "action": "get_best_trade"
        },
        "WORST_TRADE": {
            "keywords": [
                "أسوأ صفقة", "صفقة خاسرة", "أكبر خسارة", "أسوأ تداول",
                "worst trade", "lowest profit", "biggest loss",
                "أعلى خسارة", "الصفقة الأسوأ"
            ],
            "action": "get_worst_trade"
        },
        "TRADE_STATS": {
            "keywords": [
                "إحصائيات", "الإحصائيات", "تقرير الأداء", "أداء التداول",
                "stats", "statistics", "performance", "تقرير",
                "نسبة النجاح", "win rate", "الربح الكلي"
            ],
            "action": "get_general_statistics"
        },
        "LEARNING_INSIGHTS": {
            "keywords": [
                "دروس", "تعلم", "أنماط", "التعلم", "ما تعلمته",
                "lessons", "patterns", "insights", "رؤى",
                "تقرير التعلم", "نظام التعلم"
            ],
            "action": "get_learning_insights"
        },
        "INTELLIGENCE": {
            "keywords": [
                "استخباراتي", "أخبار", "تقرير استخباراتي",
                "intelligence", "news", "الاخبار", "تقرير الأخبار",
                "مستجدات", "آخر الأخبار", "أخبار السوق"
            ],
            "action": "get_intelligence_report"
        },
        "PREDICTION": {
            "keywords": [
                "توقع", "توقعات", "سعر النفط", "سعر الفضة",
                "prediction", "forecast", "future price",
                "المدى القريب", "المدى البعيد", "يتوقع",
                "ماتوقعك لسعر", "ما توقعك"
            ],
            "action": "get_price_prediction"
        },
        "CLOSE_TRADE": {
            "keywords": [
                "اغلق صفقة", "إغلاق صفقة", "إغلق صفقة",
                "اغلق النفط", "اغلق الفضة", "close trade",
                "أغلق الصفقة"
            ],
            "action": "execute_close_trade"
        },
        "TRADE_DETAILS": {
            "keywords": [
                "تفاصيل صفقة", "بيانات الصفقة", "معلومات الصفقة",
                "trade details", "trade info", "صفقة محددة"
            ],
            "action": "get_trade_details"
        },
        "TRADE_HISTORY": {
            "keywords": [
                "تاريخ الصفقات", "سجل الصفقات", "الصفقات السابقة",
                "trade history", "history", "سجل التداول"
            ],
            "action": "get_trade_history_summary"
        },
        "COMPARISON": {
            "keywords": [
                "مقارنة", "النفط والفضة", "مقارنة بين",
                "comparison", "compare", "أيهما أفضل"
            ],
            "action": "get_asset_comparison"
        },
        "CORRELATION": {
            "keywords": [
                "علاقة", "الارتباط", "علاقة النفط بالفضة",
                "correlation", "relationship", "العلاقة بين"
            ],
            "action": "get_market_correlation"
        },
        "MODIFY_SLTP": {
            "keywords": [
                "عدل وقف", "تعديل وقف", "عدل هدف", "تعديل هدف",
                "modify sl", "modify tp", "تغيير وقف", "تغيير هدف"
            ],
            "action": "modify_trade_sl_tp"
        },
        "EXPLAIN_DECISION": {
            "keywords": [
                "لماذا", "سبب", "تفسير", "شرح قرار",
                "why", "explain", "reason", "what happened"
            ],
            "action": "explain_decision"
        },
        "WEEKLY_REPORT": {
            "keywords": [
                "تقرير أسبوعي", "الاسبوعي", "تقرير الأسبوع",
                "weekly report", "this week", "last week"
            ],
            "action": "get_weekly_report"
        },
        "LEARNING_DEEP": {
            "keywords": [
                "تعلم عميق", "تحليل عميق", "deep learning",
                "deep analysis", "تقرير التعلم العميق"
            ],
            "action": "get_learning_stats_report"
        },
        "GENERAL_QUESTION": {
            "keywords": [
                "مالوضع", "الوضع", "شو الاخبار", "اخبار",
                "مستجدات", "وش السالفة", "شو وضع", "كيف الحال"
            ],
            "action": "handle_general_question"
        }
    }
    
    @staticmethod
    def route(text: str) -> Tuple[str, dict]:
        """
        توجيه النية بناءً على النص
        ⚡ أسرع من 0.2 ثانية
        🎯 دقة عالية للأسئلة الشائعة
        """
        text_lower = text.lower().strip()
        
        # فحص كل قاعدة
        for intent, rule in IntentRouter.RULES.items():
            for keyword in rule.get("keywords", []):
                if keyword.lower() in text_lower:
                    # استخراج المعاملات (إن وجدت)
                    params = rule.get("params", {}).copy()
                    
                    # معالجة خاصة لـ PROFIT_YESTERDAY (قد يأتي بـ "اول امس" = يومين)
                    if intent == "PROFIT_YESTERDAY" and ("اول امس" in text_lower or "أول أمس" in text_lower):
                        params["days_ago"] = 2
                    
                    # معالجة خاصة للأصول (النفط/الفضة)
                    if "نفط" in text_lower or "oil" in text_lower:
                        params["asset_type"] = "oil"
                    elif "فضة" in text_lower or "silver" in text_lower:
                        params["asset_type"] = "silver"
                    
                    # معالجة خاصة للتوقعات (المدى القريب/البعيد)
                    if intent == "PREDICTION":
                        if "قريب" in text_lower or "short" in text_lower:
                            params["timeframe"] = "short"
                        elif "بعيد" in text_lower or "long" in text_lower:
                            params["timeframe"] = "long"
                        else:
                            params["timeframe"] = "short"
                    
                    return intent, params
        
        return "GENERAL", {}


# ====================================================================================
# 2. HybridOrchestrator - الوسيط الهجين الكامل
# ====================================================================================

class HybridOrchestrator:
    """
    🧠 الوسيط الهجين - المدير الذكي للمحادثة
    يجمع بين:
    - سرعة القواعد الصلبة (Hard Router)
    - فهم النماذج الخفيفة (Gemini 3.5 Flash)
    - دقة جلب البيانات (Data Fetcher)
    - صياغة طبيعية (Smart Formatter)
    """
    
    def __init__(self, gemini_model=None, groq_api_key: str = None):
        self.gemini_model = gemini_model
        self.groq_api_key = groq_api_key
        self.router = IntentRouter()
        
        # تخزين مؤقت للبيانات لتجنب التكرار
        self._cache = {}
        self._cache_ttl = 30  # 30 ثانية
        
        logger.info("✅ Hybrid Orchestrator V2.0 initialized")
    
    def process(self, text: str, context: Dict, chat_id: str) -> str:
        """
        المعالجة الكاملة للطلب
        ⚡ يعيد الرد النهائي
        """
        start_time = time.time()
        logger.info(f"🧠 [Orchestrator] معالجة: {text[:50]}...")
        
        # 1️⃣ التوجيه الصلب (Hard Router)
        intent, params = self.router.route(text)
        logger.info(f"📌 [Orchestrator] النية (Hard): {intent} | المعاملات: {params}")
        
        # 2️⃣ إذا فشل التوجيه الصلب، استخدم Gemini للتصنيف
        if intent == "GENERAL" and self.gemini_model:
            intent = self._classify_with_gemini(text, context)
            logger.info(f"📌 [Orchestrator] النية (Gemini): {intent}")
        
        # 3️⃣ إذا ما زالت GENERAL، استخدم Groq كحل أخير
        if intent == "GENERAL":
            return self._handle_general_with_groq(text, context, chat_id)
        
        # 4️⃣ معالجة خاصة للأسئلة العامة
        if intent == "GENERAL_QUESTION":
            return self._handle_general_question(text, context, chat_id)
        
        # 5️⃣ جلب البيانات بناءً على النية
        data = self._fetch_data(intent, params, context)
        
        # 6️⃣ صياغة الرد
        response = self._format_response(data, text, intent, chat_id)
        
        elapsed = time.time() - start_time
        logger.info(f"⏱️ [Orchestrator] اكتمل في {elapsed:.2f} ثانية")
        
        return response
    
    # ────────────────────────────────────────────────────────────────────────
    # 2️⃣ التصنيف بـ Gemini 3.5 Flash
    # ────────────────────────────────────────────────────────────────────────
    
    def _classify_with_gemini(self, text: str, context: Dict) -> str:
        """
        تصنيف النية باستخدام Gemini 3.5 Flash
        🧠 يفهم أي صياغة حتى العامية
        ⏱️ 1-2 ثانية
        """
        if not self.gemini_model:
            return "GENERAL"
        
        try:
            # قائمة النيات المدعومة مع أمثلة توضيحية
            intent_descriptions = """
            PROFIT_TODAY: أسئلة عن أرباح اليوم
            PROFIT_YESTERDAY: أسئلة عن أرباح الأمس أو يوم محدد
            OPEN_TRADES: أسئلة عن الصفقات المفتوحة
            LAST_TRADE_STATUS: أسئلة عن نتيجة آخر صفقة (ربح/خسارة)
            LAST_TRADE_REASON: أسئلة عن سبب نجاح أو فشل آخر صفقة
            MARKET_QUERY: أسئلة عن وضع السوق بشكل عام
            PRICE_CHECK: أسئلة عن أسعار النفط والفضة
            BEST_TRADE: أسئلة عن أفضل صفقة
            WORST_TRADE: أسئلة عن أسوأ صفقة
            TRADE_STATS: أسئلة عن الإحصائيات والأداء
            LEARNING_INSIGHTS: أسئلة عن الدروس والأنماط المكتشفة
            INTELLIGENCE: أسئلة عن الأخبار والتقارير الاستخباراتية
            PREDICTION: أسئلة عن توقعات الأسعار
            CLOSE_TRADE: طلبات إغلاق صفقة
            TRADE_DETAILS: طلبات تفاصيل صفقة محددة
            TRADE_HISTORY: طلبات تاريخ الصفقات
            COMPARISON: طلبات مقارنة بين النفط والفضة
            CORRELATION: طلبات علاقة النفط بالفضة
            MODIFY_SLTP: طلبات تعديل وقف/هدف
            EXPLAIN_DECISION: طلبات شرح قرارات البوت
            WEEKLY_REPORT: طلبات تقرير أسبوعي
            LEARNING_DEEP: طلبات تحليل عميق أو تعلم عميق
            GENERAL_QUESTION: أسئلة عامة عن الوضع (مثل "مالوضع الان")
            GENERAL: أي سؤال لا ينتمي للفئات السابقة
            """
            
            prompt = f"""
            أنت مصنف نيات ذكي. صنف سؤال المستخدم إلى واحدة من الفئات التالية:
            
            {intent_descriptions}
            
            **قواعد صارمة:**
            1. أجب فقط باسم الفئة، ولا تكتب أي شيء آخر.
            2. إذا كان السؤال عن السوق أو التحليل، صنفه كـ MARKET_QUERY.
            3. إذا كان السؤال عن الأرباح، صنفه كـ PROFIT_TODAY أو PROFIT_YESTERDAY.
            4. إذا كان السؤال عن صفقة مفتوحة، صنفه كـ OPEN_TRADES.
            5. إذا كان السؤال عن سبب نجاح/فشل صفقة، صنفه كـ LAST_TRADE_REASON.
            6. إذا كان السؤال عن الوضع بشكل عام (مالوضع الان)، صنفه كـ GENERAL_QUESTION.
            7. إذا كان السؤال عاماً لا يتعلق بالتداول، صنفه كـ GENERAL.
            
            السؤال: {text}
            
            الفئة:
            """
            
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 20, "temperature": 0.0}
            )
            
            if response and response.text:
                intent = response.text.strip().upper()
                # تأكد من أن النية في القائمة
                valid_intents = [
                    "PROFIT_TODAY", "PROFIT_YESTERDAY", "OPEN_TRADES", 
                    "LAST_TRADE_STATUS", "LAST_TRADE_REASON", "MARKET_QUERY",
                    "PRICE_CHECK", "BEST_TRADE", "WORST_TRADE", "TRADE_STATS",
                    "LEARNING_INSIGHTS", "INTELLIGENCE", "PREDICTION",
                    "CLOSE_TRADE", "TRADE_DETAILS", "TRADE_HISTORY",
                    "COMPARISON", "CORRELATION", "MODIFY_SLTP",
                    "EXPLAIN_DECISION", "WEEKLY_REPORT", "LEARNING_DEEP",
                    "GENERAL_QUESTION", "GENERAL"
                ]
                if intent in valid_intents:
                    return intent
        
        except Exception as e:
            logger.warning(f"⚠️ [Orchestrator] فشل تصنيف Gemini: {e}")
        
        return "GENERAL"
    
    # ────────────────────────────────────────────────────────────────────────
    # 4️⃣ جلب البيانات (Data Fetcher)
    # ────────────────────────────────────────────────────────────────────────
    
    def _fetch_data(self, intent: str, params: dict, context: Dict) -> dict:
        """
        جلب البيانات بناءً على النية
        📦 يستدعي دوال البوت المناسبة
        """
        data = {
            "intent": intent,
            "params": params,
            "data": None,
            "raw": None,
            "error": None,
            "context": context
        }
        
        try:
            # 🔹 PROFIT_TODAY
            if intent == "PROFIT_TODAY":
                data["raw"] = tool_get_todays_profit_loss()
            
            # 🔹 PROFIT_YESTERDAY
            elif intent == "PROFIT_YESTERDAY":
                days = params.get("days_ago", 1)
                data["raw"] = tool_get_profit_loss_by_date(days)
                data["params"]["days_ago"] = days
            
            # 🔹 OPEN_TRADES
            elif intent == "OPEN_TRADES":
                data["raw"] = tool_get_open_trades()
            
            # 🔹 LAST_TRADE_STATUS
            elif intent == "LAST_TRADE_STATUS":
                data["raw"] = get_last_closed_trade()
                if data["raw"]:
                    # تحليل إضافي للصفقة
                    trade = data["raw"]
                    profit = trade.get("profit_dollars", 0)
                    data["data"] = {
                        "asset": trade.get("asset", "unknown"),
                        "type": trade.get("type", "UNKNOWN"),
                        "entry": trade.get("entry_price", 0),
                        "exit": trade.get("exit_price", 0),
                        "profit": profit,
                        "exit_reason": trade.get("exit_reason", "غير معروف"),
                        "is_win": profit > 0,
                        "is_loss": profit < 0,
                        "timestamp": trade.get("timestamp", "")
                    }
            
            # 🔹 LAST_TRADE_REASON
            elif intent == "LAST_TRADE_REASON":
                # استخدام التحليل العميق
                data["raw"] = analyze_last_trade_command()
                if isinstance(data["raw"], str) and len(data["raw"]) > 50:
                    data["data"] = {"analysis": data["raw"]}
                else:
                    data["raw"] = get_last_closed_trade()
                    if data["raw"]:
                        trade = data["raw"]
                        profit = trade.get("profit_dollars", 0)
                        data["data"] = {
                            "asset": trade.get("asset", "unknown"),
                            "type": trade.get("type", "UNKNOWN"),
                            "entry": trade.get("entry_price", 0),
                            "exit": trade.get("exit_price", 0),
                            "profit": profit,
                            "exit_reason": trade.get("exit_reason", "غير معروف"),
                            "is_win": profit > 0,
                            "is_loss": profit < 0
                        }
            
            # 🔹 MARKET_QUERY
            elif intent == "MARKET_QUERY":
                data["raw"] = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
                # نمرر إلى _handle_market_query مباشرة (معالجة خاصة)
                data["_market_query"] = True
            
            # 🔹 PRICE_CHECK
            elif intent == "PRICE_CHECK":
                data["raw"] = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
            
            # 🔹 BEST_TRADE
            elif intent == "BEST_TRADE":
                asset = params.get("asset_type", "oil")
                data["raw"] = tool_get_worst_best_trade(asset)
            
            # 🔹 WORST_TRADE
            elif intent == "WORST_TRADE":
                asset = params.get("asset_type", "oil")
                data["raw"] = tool_get_worst_best_trade(asset)
            
            # 🔹 TRADE_STATS
            elif intent == "TRADE_STATS":
                data["raw"] = tool_get_general_statistics()
            
            # 🔹 LEARNING_INSIGHTS
            elif intent == "LEARNING_INSIGHTS":
                data["raw"] = tool_get_learning_insights()
            
            # 🔹 INTELLIGENCE
            elif intent == "INTELLIGENCE":
                data["raw"] = tool_get_intelligence_report()
            
            # 🔹 PREDICTION
            elif intent == "PREDICTION":
                asset = params.get("asset_type", "oil")
                timeframe = params.get("timeframe", "short")
                data["raw"] = tool_get_price_prediction(asset, timeframe)
            
            # 🔹 CLOSE_TRADE
            elif intent == "CLOSE_TRADE":
                asset = params.get("asset_type", "oil")
                data["raw"] = tool_execute_close_trade(asset)
            
            # 🔹 TRADE_DETAILS
            elif intent == "TRADE_DETAILS":
                asset = params.get("asset_type", "oil")
                trade_id = params.get("trade_id", None)
                data["raw"] = tool_get_trade_details(asset, trade_id)
            
            # 🔹 TRADE_HISTORY
            elif intent == "TRADE_HISTORY":
                days = params.get("days", 7)
                data["raw"] = tool_get_trade_history_summary(days)
            
            # 🔹 COMPARISON
            elif intent == "COMPARISON":
                data["raw"] = tool_get_asset_comparison()
            
            # 🔹 CORRELATION
            elif intent == "CORRELATION":
                data["raw"] = tool_get_market_correlation()
            
            # 🔹 MODIFY_SLTP
            elif intent == "MODIFY_SLTP":
                asset = params.get("asset_type", "oil")
                new_sl = params.get("new_sl", None)
                new_tp = params.get("new_tp", None)
                data["raw"] = tool_modify_trade_sl_tp(asset, new_sl, new_tp)
            
            # 🔹 EXPLAIN_DECISION
            elif intent == "EXPLAIN_DECISION":
                asset = params.get("asset_type", "oil")
                decision_type = params.get("decision_type", "close")
                data["raw"] = tool_explain_decision(asset, decision_type)
            
            # 🔹 WEEKLY_REPORT
            elif intent == "WEEKLY_REPORT":
                data["raw"] = tool_get_weekly_report()
            
            # 🔹 LEARNING_DEEP
            elif intent == "LEARNING_DEEP":
                if 'get_learning_stats_report' in globals():
                    data["raw"] = get_learning_stats_report()
                else:
                    data["raw"] = "⚠️ نظام التعلم العميق غير متوفر حالياً."
            
            # 🔹 GENERAL_QUESTION
            elif intent == "GENERAL_QUESTION":
                # معالجة خاصة للأسئلة العامة
                data["_general_question"] = True
            
            # 🔹 GENERAL
            else:
                data["error"] = "لم يتم التعرف على النية"
        
        except Exception as e:
            logger.error(f"❌ [Orchestrator] خطأ في جلب البيانات: {e}")
            data["error"] = str(e)
        
        return data
    
    # ────────────────────────────────────────────────────────────────────────
    # 5️⃣ صياغة الرد (Smart Formatter)
    # ────────────────────────────────────────────────────────────────────────
    
    def _format_response(self, data: dict, original_text: str, intent: str, chat_id: str) -> str:
        """
        صياغة الرد النهائي
        🎨 يستخدم النموذج الكبير للصياغة فقط (يمنع الاختلاق)
        """
        # حالات خاصة (معالجة مباشرة بدون نماذج)
        
        # 🔹 GENERAL_QUESTION - معالجة خاصة
        if intent == "GENERAL_QUESTION" or data.get("_general_question"):
            return self._handle_general_question(original_text, data.get("context", {}), chat_id)
        
        # 🔹 MARKET_QUERY - معالجة خاصة
        if intent == "MARKET_QUERY" or data.get("_market_query"):
            return self._handle_market_query_response(data, original_text)
        
        # 🔹 CLOSE_TRADE - معالجة خاصة
        if intent == "CLOSE_TRADE":
            return data.get("raw", "⚠️ لم يتم إغلاق الصفقة.")
        
        # 🔹 LAST_TRADE_REASON - إذا كان لدينا تحليل بالفعل
        if intent == "LAST_TRADE_REASON" and data.get("data", {}).get("analysis"):
            return data["data"]["analysis"]
        
        # 🔹 PREDICTION - معالجة خاصة لتوقعات الأسعار
        if intent == "PREDICTION" and data.get("raw"):
            return self._format_prediction_response(data["raw"])
        
        # 🔹 إذا كان هناك خطأ
        if data.get("error"):
            return f"💙 تولين: عذراً، حدث خطأ أثناء جلب البيانات: {data['error']}"
        
        # 🔹 إذا لم تكن هناك بيانات
        if data.get("raw") is None:
            return "💙 تولين: لا توجد بيانات متاحة حالياً. هل تريد سؤالاً آخر؟"
        
        # 🔹 إذا كانت البيانات نصاً طويلاً (تقرير جاهز)
        if isinstance(data["raw"], str) and len(data["raw"]) > 100:
            # تحقق إن كان النص يحتوي بالفعل على اسم تولين
            if "تولين" in data["raw"] or "💙" in data["raw"]:
                return data["raw"]
            # وإلا أضف تنسيقاً بسيطاً
            return f"💙 **تولين:**\n\n{data['raw']}"
        
        # 🔹 صياغة البيانات باستخدام النموذج (Groq/Gemini)
        return self._smart_format(data["raw"], original_text, intent, data)
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.0 معالجة الأسئلة العامة (GENERAL_QUESTION)
    # ────────────────────────────────────────────────────────────────────────
    
    def _handle_general_question(self, text: str, context: Dict, chat_id: str) -> str:
        """
        معالجة الأسئلة العامة مثل "مالوضع الان"
        ✅ تمنع الإجابات الغبية
        """
        try:
            # محاولة الحصول على لقطة سريعة للسوق
            market_data = tool_get_both_markets_analysis(context.get('market_snapshot', {}))
            data = json.loads(market_data)
            
            oil = data.get('oil', {})
            silver = data.get('silver', {})
            
            oil_price = oil.get('price', 0)
            silver_price = silver.get('price', 0)
            oil_score = oil.get('score', 50)
            silver_score = silver.get('score', 50)
            avg_score = (oil_score + silver_score) / 2
            
            # بناء رد ودود ومفيد
            response = "💙 **تولين:** يا صديقي، الوضع الحالي:\n\n"
            
            if oil_price > 0 and silver_price > 0:
                response += f"🛢️ النفط: ${oil_price:.2f} | 🥈 الفضة: ${silver_price:.3f}\n"
                
                if avg_score >= 70:
                    response += "📈 السوق في حالة **قوية** ونشطة.\n"
                elif avg_score >= 55:
                    response += "🟡 السوق في حالة **متوسطة**، هادئ نسبياً.\n"
                else:
                    response += "🟡 السوق **هادئ** اليوم، لا توجد حركة قوية.\n"
                
                response += f"\n📊 التقييم العام: {avg_score:.0f}% (محايد)"
                
                # إضافة أخبار إن وجدت
                news_data = context.get('news_analysis', [])
                if news_data:
                    significant_news = [n for n in news_data if n.get('is_significant')]
                    if significant_news:
                        response += "\n\n📰 هناك أخبار مؤثرة اليوم، هل تريد تفاصيلها؟"
            
            response += "\n\n💙 هل تريد تحليلاً أكثر تفصيلاً للنفط أو الفضة؟"
            return response
            
        except Exception as e:
            logger.warning(f"⚠️ فشل معالجة السؤال العام: {e}")
            return "💙 **تولين:** يا صديقي، الوضع هادئ حالياً. هل تريد معرفة شيء محدد عن النفط أو الفضة؟"
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.1 معالجة MARKET_QUERY الخاصة
    # ────────────────────────────────────────────────────────────────────────
    
    def _handle_market_query_response(self, data: dict, original_text: str) -> str:
        """
        معالجة خاصة لسؤال السوق
        يعرض الأسعار والتحليل بتنسيق جميل
        """
        try:
            raw = data.get("raw", "{}")
            market_data = json.loads(raw) if isinstance(raw, str) else raw
            
            oil = market_data.get("oil", {})
            silver = market_data.get("silver", {})
            
            oil_price = oil.get("price", 0)
            silver_price = silver.get("price", 0)
            
            # إذا لم تكن الأسعار موجودة، نجلبها مباشرة
            if oil_price == 0 or silver_price == 0:
                try:
                    oil_d = get_mexc_candles("USOIL_USDT", "Min1", 5)
                    silver_d = get_mexc_candles("SILVER_USDT", "Min1", 5)
                    if oil_d and oil_d.get("closes"):
                        oil_price = oil_d["closes"][-1]
                    if silver_d and silver_d.get("closes"):
                        silver_price = silver_d["closes"][-1]
                except:
                    pass
            
            response = "💙 **تولين:** يا صديقي، هذه لقطة السوق اليوم:\n\n"
            
            # النفط
            if oil_price > 0:
                signal = oil.get("signal", "WAIT")
                trend = oil.get("trend", "محايد")
                score = oil.get("score", 50)
                grade = oil.get("grade", "محايد")
                rsi = oil.get("rsi", 50)
                adx = oil.get("adx", 15)
                
                signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
                signal_text = "شراء" if signal == "BUY" else "بيع" if signal == "SELL" else "انتظار"
                
                response += f"🛢️ **النفط:** ${oil_price:.2f}\n"
                response += f"   • الإشارة: {signal_emoji} {signal_text}\n"
                response += f"   • الاتجاه: {trend} | التقييم: {score:.0f}% ({grade})\n"
                response += f"   • RSI: {rsi:.0f} | ADX: {adx:.0f}\n\n"
            
            # الفضة
            if silver_price > 0:
                signal = silver.get("signal", "WAIT")
                trend = silver.get("trend", "محايد")
                score = silver.get("score", 50)
                grade = silver.get("grade", "محايد")
                rsi = silver.get("rsi", 50)
                adx = silver.get("adx", 15)
                
                signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "⚪"
                signal_text = "شراء" if signal == "BUY" else "بيع" if signal == "SELL" else "انتظار"
                
                response += f"🥈 **الفضة:** ${silver_price:.3f}\n"
                response += f"   • الإشارة: {signal_emoji} {signal_text}\n"
                response += f"   • الاتجاه: {trend} | التقييم: {score:.0f}% ({grade})\n"
                response += f"   • RSI: {rsi:.0f} | ADX: {adx:.0f}\n\n"
            
            # توصية تولين
            avg_score = (oil.get("score", 50) + silver.get("score", 50)) / 2
            response += "💡 **توصية تولين:**\n"
            if avg_score >= 70:
                response += "✅ السوق في حالة قوية، قد تكون فرصة جيدة للدخول بحذر.\n"
            elif avg_score >= 55:
                response += "🟡 السوق في حالة متوسطة، أنصح بالانتظار حتى تظهر إشارة أوضح.\n"
            else:
                response += "🟡 السوق هادئ نسبياً، أنصح بالمراقبة وعدم الاستعجال.\n"
            
            response += "\n💙 أنا هنا لمساعدتك في أي وقت!"
            return response
            
        except Exception as e:
            logger.error(f"❌ [Orchestrator] خطأ في معالجة MARKET_QUERY: {e}")
            return "💙 تولين: عذراً، تعذر جلب بيانات السوق حالياً. يرجى المحاولة مرة أخرى."
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.2 معالجة توقعات الأسعار (PREDICTION)
    # ────────────────────────────────────────────────────────────────────────
    
    def _format_prediction_response(self, raw_data) -> str:
        """
        تنسيق توقعات الأسعار بلغة مفهومة (بدلاً من JSON الخام)
        """
        try:
            if isinstance(raw_data, str):
                data = json.loads(raw_data)
            else:
                data = raw_data
            
            if isinstance(data, dict):
                asset = data.get('asset', 'الأصل')
                price = data.get('current_price', 0)
                direction = data.get('expected_direction', 'غير معروف')
                range_text = data.get('expected_range', 'غير محدد')
                confidence = data.get('confidence', 50)
                support = data.get('support', 0)
                resistance = data.get('resistance', 0)
                trend = data.get('trend', 'محايد')
                score = data.get('score', 50)
                timeframe = data.get('timeframe', 'قصير')
                
                asset_label = "النفط" if asset == "oil" else "الفضة" if asset == "silver" else asset
                
                response = f"🔮 **توقعي لسعر {asset_label} على المدى {timeframe}:**\n\n"
                response += f"• السعر الحالي: ${price:.2f}\n"
                response += f"• الاتجاه المتوقع: {direction}\n"
                response += f"• النطاق المتوقع: {range_text}\n"
                response += f"• الثقة: {confidence}%\n"
                if support > 0 and resistance > 0:
                    response += f"• الدعم: ${support:.2f} | المقاومة: ${resistance:.2f}\n"
                response += f"• الاتجاه الحالي: {trend} | درجة القوة: {score:.0f}%\n"
                
                # إضافة توصية مختصرة
                if confidence > 70:
                    response += "\n💡 التوصية: فرصة جيدة للدخول في اتجاه المتوقع."
                elif confidence > 55:
                    response += "\n💡 التوصية: راقب السعر، قد تكون فرصة مناسبة."
                else:
                    response += "\n💡 التوصية: انتظر تأكيداً إضافياً قبل الدخول."
                
                return response
            
        except Exception as e:
            logger.warning(f"⚠️ فشل تنسيق توقعات الأسعار: {e}")
        
        # إذا فشل التنسيق، نعرض البيانات الخام بشكل منظم
        return f"💙 **تولين:**\n\n{str(raw_data)[:500]}"
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.3 الصياغة الذكية (Smart Formatting)
    # ────────────────────────────────────────────────────────────────────────
    
    def _smart_format(self, raw_data, original_text: str, intent: str, data: dict) -> str:
        """
        الصياغة الذكية باستخدام النموذج الكبير (Groq/Gemini)
        🎨 يمنع النموذج من اختلاق البيانات
        """
        # إذا كانت البيانات JSON، نحاول تحويلها إلى نص مفهوم
        if isinstance(raw_data, str):
            try:
                parsed = json.loads(raw_data)
                raw_data = json.dumps(parsed, ensure_ascii=False, indent=2)
            except:
                pass
        
        # بناء تعليمات الصياغة
        system_prompt = f"""
        أنت تولين، مستشارة استراتيجية ودودة ومحترفة.
        
        **بيانات مؤكدة (يجب استخدامها فقط، ولا تختلق أي شيء):**
        {raw_data[:2000]}
        
        **السؤال الأصلي للمستخدم:** {original_text}
        
        **النية المحددة:** {intent}
        
        **قواعد صارمة للصياغة:**
        1. استخدم البيانات المقدمة فقط، ولا تختلق أي أرقام أو معلومات.
        2. صغ رداً طبيعياً وودوداً (استخدم "يا صديقي").
        3. إذا كانت البيانات تشير إلى عدم وجود صفقات، قل ذلك بوضوح.
        4. لا تقدم نصائح عامة عن التداول إلا إذا طلب المستخدم ذلك صراحة.
        5. إذا كانت البيانات تحتوي على أرقام (مثل الأرباح)، اذكرها بوضوح.
        6. اجعل الرد مختصراً ومفيداً (لا تزيد عن 150 كلمة).
        7. أنهِ الرد بـ "💙 تولين: أنا هنا لمساعدتك!"
        """
        
        user_prompt = f"صغ رداً على هذا السؤال: {original_text}"
        
        # محاولة استخدام Groq أولاً (النموذج الأقوى)
        if self.groq_api_key and self.groq_api_key != "" and "test_" not in self.groq_api_key:
            try:
                response = self._call_groq_format(system_prompt, user_prompt)
                if response and len(response) > 10:
                    return self._clean_response(response)
            except Exception as e:
                logger.warning(f"⚠️ [Orchestrator] فشل صياغة Groq: {e}")
        
        # محاولة استخدام Gemini
        if self.gemini_model:
            try:
                prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 300, "temperature": 0.3}
                )
                if response and response.text and len(response.text) > 10:
                    return self._clean_response(response.text)
            except Exception as e:
                logger.warning(f"⚠️ [Orchestrator] فشل صياغة Gemini: {e}")
        
        # الخطة الاحتياطية: عرض البيانات الخام مع تنسيق بسيط
        return self._fallback_format(raw_data, original_text)
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.4 استدعاء Groq للصياغة
    # ────────────────────────────────────────────────────────────────────────
    
    def _call_groq_format(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """استدعاء Groq API للصياغة"""
        if not self.groq_api_key:
            return None
        
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "system", "content": system_prompt[:3000]},
                    {"role": "user", "content": user_prompt[:2000]}
                ],
                "temperature": 0.3,
                "max_tokens": 300
            }
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.warning(f"⚠️ Groq format error: {e}")
        return None
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.5 الخطة الاحتياطية (Fallback)
    # ────────────────────────────────────────────────────────────────────────
    
    def _fallback_format(self, raw_data, original_text: str) -> str:
        """الخطة الاحتياطية - عرض البيانات بتنسيق بسيط"""
        if isinstance(raw_data, str) and len(raw_data) < 500:
            # إذا كانت البيانات نصاً قصيراً، نعرضها مباشرة
            if raw_data.startswith("{") or raw_data.startswith("["):
                try:
                    parsed = json.loads(raw_data)
                    formatted = json.dumps(parsed, ensure_ascii=False, indent=2)
                    return f"💙 **تولين:**\n\n```json\n{formatted[:500]}\n```"
                except:
                    pass
            return f"💙 **تولين:**\n\n{raw_data[:500]}"
        
        # محاولة استخراج معلومات مفيدة
        try:
            if isinstance(raw_data, str):
                parsed = json.loads(raw_data)
                if isinstance(parsed, dict):
                    parts = []
                    for key, value in parsed.items():
                        if isinstance(value, (int, float)):
                            parts.append(f"• {key}: {value}")
                        elif isinstance(value, str):
                            parts.append(f"• {key}: {value[:100]}")
                    if parts:
                        return f"💙 **تولين:**\n\n" + "\n".join(parts[:10])
        except:
            pass
        
        return f"💙 **تولين:**\n\n{str(raw_data)[:500]}"
    
    # ────────────────────────────────────────────────────────────────────────
    # 5.6 تنظيف الرد
    # ────────────────────────────────────────────────────────────────────────
    
    def _clean_response(self, text: str) -> str:
        """تنظيف وتنسيق الرد النهائي"""
        if not text:
            return "💙 تولين: عذراً، لم أستطع صياغة رد مناسب."
        
        text = text.strip()
        
        # إزالة التكرارات
        if text.startswith("💙"):
            text = text[2:].strip()
        if text.startswith("تولين:"):
            text = text[6:].strip()
        
        # التأكد من وجود اسم تولين
        if not text.startswith("💙") and not text.startswith("تولين"):
            text = f"💙 **تولين:** {text}"
        
        return text
    
    # ────────────────────────────────────────────────────────────────────────
    # 6️⃣ معالجة الأسئلة العامة بـ Groq
    # ────────────────────────────────────────────────────────────────────────
    
    def _handle_general_with_groq(self, text: str, context: Dict, chat_id: str) -> str:
        """
        معالجة الأسئلة العامة باستخدام Groq مباشرة
        (عندما تفشل جميع محاولات التصنيف)
        """
        try:
            system_prompt = """
            أنت تولين، مستشارة استراتيجية ودودة ومحترفة.
            
            **قواعد صارمة:**
            1. لا تختلق بيانات عن التداول أبداً.
            2. إذا سألك المستخدم عن شيء لا تعرفه، قل ذلك بوضوح.
            3. إذا كان السؤال عن التداول، حاول توجيه المستخدم إلى سؤال محدد.
            4. استخدم أسلوباً ودوداً (مثل "يا صديقي").
            5. لا تقدم نصائح مالية محددة، بل نصائح عامة.
            
            **السياق المتاح:**
            - الصفقات المفتوحة: {len(context.get('open_trades', {}))}
            - تحليل السوق: {context.get('market_snapshot', {})}
            """
            
            user_prompt = f"السؤال: {text}"
            
            response = self._call_groq_format(system_prompt, user_prompt)
            if response and len(response) > 10:
                return self._clean_response(response)
            
        except Exception as e:
            logger.error(f"❌ [Orchestrator] خطأ في GENERAL: {e}")
        
        # الخطة الاحتياطية النهائية (ودودة وليست غبية)
        return f"💙 **تولين:** يا صديقي، سؤال جميل! {text}... هل تريد معرفة شيء محدد عن النفط أو الفضة؟ (مثل: 'كيف السوق اليوم؟' أو 'تحليل النفط')"


# ====================================================================================
# 7. تهيئة ORCHESTRATOR للتوافق مع الكود القديم
# ====================================================================================

# محاولة تهيئة الوسيط مع النماذج المتاحة
try:
    # محاولة استيراد Gemini (من PART 24)
    if 'genai' in globals() and genai:
        gemini_model = genai.GenerativeModel('gemini-3.5-flash')
    else:
        gemini_model = None
    
    HYBRID_ORCHESTRATOR = HybridOrchestrator(
        gemini_model=gemini_model,
        groq_api_key=GROQ_API_KEY
    )
    logger.info("✅ Hybrid Orchestrator V2.0 جاهز!")
except Exception as e:
    logger.error(f"❌ فشل تهيئة Hybrid Orchestrator: {e}")
    HYBRID_ORCHESTRATOR = None

# ====================================================================================
# نهاية PART 24.7
# ====================================================================================

# ====================================================================================
# 📦 PART 25: دوال معالجة الأوامر (معدل نهائي - إزالة زر "توصيات استراتيجية")
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. إزالة زر "📊 توصيات استراتيجية" من القائمة الرئيسية.
#   2. إزالة المعالجة الخاصة به في handle_message.
#   3. الحفاظ على جميع الأوامر الأخرى كما هي.
# ====================================================================================

def process_text_command(text, chat_id=None):
    """معالجة الأوامر النصية (تحتفظ بوظائفها القديمة)"""
    text_lower = text.lower()

    # ── الأوامر الموجودة ──
    close_keywords = ["تم إغلاق", "سأغلق", "أغلقت", "أغلق الصفقة", "أغلق صفقة", "أغلق صفقة النفط", "أغلق صفقة الفضة"]
    for keyword in close_keywords:
        if keyword in text_lower:
            asset_type = None
            if "نفط" in text_lower or "oil" in text_lower:
                asset_type = "oil"
            elif "فضة" in text_lower or "silver" in text_lower:
                asset_type = "silver"
            if not asset_type:
                oil_trade = get_current_open_trade("oil")
                silver_trade = get_current_open_trade("silver")
                if oil_trade and not silver_trade:
                    asset_type = "oil"
                elif silver_trade and not oil_trade:
                    asset_type = "silver"
                else:
                    queue_telegram_message("⚠️ يرجى تحديد الصفقة:\n• `أغلق صفقة النفط`\n• `أغلق صفقة الفضة`", chat_id or CHAT_ID)
                    return True
            if asset_type:
                close_trade_manually(asset_type, "أمر يدوي من المستخدم")
                return True
    
    # ── أوامر TCN (الوعي الذاتي) - تظل تعمل عبر النص فقط ──
    if TCN_AVAILABLE and TCN:
        # من أنت؟
        if text_lower in ["من أنت", "من انت", "who are you", "اسمك", "تعريف"]:
            response = "💙 **أنا تولين**\n\n📌 مستشارتك الاستراتيجية المتخصصة في تحليل النفط والفضة.\n👨‍💻 طورني المطور بسام الحوباني.\n📦 الإصدار: V13.0\n\n💙 أنا هنا لخدمتك، اسألني عن أي شيء!"
            queue_telegram_message(response, chat_id or CHAT_ID)
            return True
        
        # ماذا تفعلين؟
        if text_lower in ["ماذا تفعلين", "what are you doing", "شو تعملين", "مهامك"]:
            try:
                consciousness = TCN.get_consciousness()
                if consciousness and consciousness.narrative:
                    response = f"👁️ **تولين:** {consciousness.narrative}"
                    queue_telegram_message(response, chat_id or CHAT_ID)
                    return True
            except:
                pass
        
        # شعورك
        if text_lower in ["شعورك", "مشاعرك", "how do you feel", "حالتك"]:
            try:
                consciousness = TCN.get_consciousness()
                if consciousness:
                    msg = f"💙 **شعوري الآن:** {consciousness.dominant_emotion}\n"
                    msg += f"📊 **ثقتي:** {consciousness.confidence*100:.0f}%\n"
                    msg += f"🎯 **قراري:** {consciousness.recommended_action}"
                    queue_telegram_message(msg, chat_id or CHAT_ID)
                    return True
            except:
                pass
        
        # قدراتك
        if text_lower in ["قدراتك", "ماذا تستطيعين", "ما هي قدراتك", "capabilities"]:
            response = """🎯 **قدرات تولين:**

📊 **التحليل الفني:**
   • تحليل جميع المؤشرات الرئيسية (الاتجاه، الزخم، التقلب، الحجم)
   • دمج جميع المؤشرات في رؤية واحدة متكاملة

📰 **تحليل الأخبار:**
   • متابعة الأحداث المؤثرة على النفط والفضة
   • تقييم تأثير الأخبار على الأسعار

🛡️ **إدارة المخاطر:**
   • تقييم المخاطر في كل صفقة
   • مراقبة الصفقات المفتوحة وتحذيرك من الخطر

💡 **التوصيات الاستشارية:**
   • قرارات واضحة: استمر، اغلق، انتظر، ادخل
   • تفسير منطقي لكل توصية

💙 اسألني عن أي شيء، أنا هنا لمساعدتك!"""
            queue_telegram_message(response, chat_id or CHAT_ID)
            return True
    
    return False

def send_main_menu(chat_id):
    """إرسال القائمة الرئيسية (بدون أزرار TCN)"""
    oil_open = get_current_open_trade("oil")
    silver_open = get_current_open_trade("silver")

    keyboard = [
        ["🛢️ تحليل النفط", "🥈 تحليل الفضة"],
        ["🔍 وضع الصفقة الحالية", "📊 تقرير الأداء"],
        ["🔍 تحليل الصفقة الأخيرة", "🧠 تقرير استخباراتي"],
        ["🧠 تقرير التعلم العميق"],
        ["❌ إغلاق الصفقة"],
    ]

    if oil_open or silver_open:
        close_row = []
        if oil_open:
            close_row.append("❌ إغلاق النفط")
        if silver_open:
            close_row.append("❌ إغلاق الفضة")
        if close_row:
            keyboard.insert(4, close_row)

    reply_markup = {"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": False}
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": chat_id,
            "text": """🤖 <b>تولين AI Prometheus Edition V13.0</b>
💙 تولين - الشبكة العصبية الواعية

📌 <b>الأزرار الرئيسية:</b>
• تحليل النفط/الفضة (تحليل فني شامل)
• وضع الصفقة الحالية
• تقرير الأداء
• تقرير التعلم العميق (الدروس والأنماط)

📢 <b>اسألني عن أي شيء:</b>
• تحليل السوق
• الصفقات المفتوحة
• التوصيات

💡 <b>أوامر كتابية:</b>
• اكتب "من أنت" أو "شعورك" للحديث عن وعيي.

جميع المحركات تعمل! 🚀""",
            "reply_markup": reply_markup,
            "parse_mode": "HTML"
        }, timeout=10)
    except Exception as e:
        logger.error(f"❌ فشل إرسال القائمة: {e}")

def handle_message(text, chat_id):
    """معالجة الرسائل الواردة - معدل لتوجيه جميع الرسائل إلى المدير الذكي"""
    print(f"📩 معالجة رسالة: {text} من {chat_id}")
    
    # ── تنظيف النص للمقارنة ──
    clean_text = text.strip()
    
    # ── تسجيل النص للتشخيص ──
    logger.info(f"📌 [handle_message] النص المُستقبل: '{clean_text}' (الطول: {len(clean_text)})")

    # ── الأوامر الأساسية (تظل كما هي) ──
    if clean_text in ["/start", "قائمة", "منيو", "القائمة", "/menu"]:
        send_main_menu(chat_id)
        return

    if clean_text in ["/test_pipeline", "اختبار المحادثة", "test chat"]:
        queue_telegram_message("🧠 جاري اختبار جميع المحركات...", chat_id or CHAT_ID)
        def test_pipeline():
            try:
                test_text = "مرحباً تولين، كيف حالك اليوم؟"
                chat_response(test_text, chat_id)
            except Exception as e:
                queue_telegram_message(f"❌ خطأ في اختبار المحادثة: {str(e)}", chat_id or CHAT_ID)
        threading.Thread(target=test_pipeline, daemon=True).start()
        return

    # ── أوامر TCN المباشرة (تُكتب يدوياً فقط، بدون أزرار) ──
    if TCN_AVAILABLE and TCN:
        if clean_text in ["ماذا تفكرين", "explain", "شرح", "تفكيرك"]:
            try:
                consciousness = TCN.think()
                explanation = TCN.explain_decision()
                queue_telegram_message(explanation, chat_id or CHAT_ID)
                return
            except Exception as e:
                logger.error(f"❌ فشل شرح التفكير: {e}")
                queue_telegram_message("⚠️ لا أستطيع شرح تفكيري حالياً.", chat_id or CHAT_ID)
                return
        
        if clean_text in ["شعورك", "حالتك", "mood"]:
            try:
                consciousness = TCN.get_consciousness()
                msg = f"💙 **شعوري الآن:** {consciousness.dominant_emotion}\n"
                msg += f"📊 **ثقتي:** {consciousness.confidence*100:.0f}%\n"
                msg += f"🎯 **قراري:** {consciousness.recommended_action}\n"
                msg += f"📖 **قصتي:** {consciousness.narrative}"
                queue_telegram_message(msg, chat_id or CHAT_ID)
                return
            except Exception as e:
                logger.error(f"❌ فشل جلب الشعور: {e}")
                queue_telegram_message("⚠️ لا أستطيع وصف شعوري حالياً.", chat_id or CHAT_ID)
                return
        
        if clean_text in ["من أنت", "من انت", "who are you", "اسمك"]:
            response = """💙 **أنا تولين**

📌 مستشارتك الاستراتيجية المتخصصة في تحليل النفط والفضة.
👨‍💻 طورني المطور بسام الحوباني.
📦 الإصدار: V13.0

💙 أنا هنا لخدمتك، اسألني عن أي شيء!"""
            queue_telegram_message(response, chat_id or CHAT_ID)
            return

    # ── معالجة الأوامر النصية (أوامر الإغلاق، إلخ) ──
    if process_text_command(clean_text, chat_id):
        return

    # ── الأوامر العادية (الأزرار) ──
    # نستخدم clean_text للمقارنة
    if clean_text in ["🛢️ تحليل النفط", "نفط", "oil", "تحليل النفط"]:
        queue_telegram_message("🔍 جاري التحليل الشامل للنفط...", chat_id or CHAT_ID)
        threading.Thread(target=analyze_and_send, args=("oil", True, chat_id), daemon=True).start()
        return

    if clean_text in ["🥈 تحليل الفضة", "فضة", "silver", "تحليل الفضة"]:
        queue_telegram_message("🔍 جاري التحليل الشامل للفضة...", chat_id or CHAT_ID)
        threading.Thread(target=analyze_and_send, args=("silver", True, chat_id), daemon=True).start()
        return

    if clean_text in ["🔍 وضع الصفقة الحالية", "وضع الصفقة", "حالة", "check"]:
        handle_check_position_request(chat_id)
        return

    # ✅ زر تقرير الأداء - مع سجل إضافي
    if clean_text in ["📊 تقرير الأداء", "إحصائيات", "الإحصائيات", "stats"]:
        logger.info(f"📊 [handle_message] تم الضغط على زر تقرير الأداء لـ {chat_id}")
        threading.Thread(target=get_trading_stats, args=(chat_id,), daemon=True).start()
        return

    if clean_text in ["🔍 تحليل الصفقة الأخيرة", "تحليل الصفقة", "الأخير", "last trade"]:
        threading.Thread(target=analyze_last_trade_command, daemon=True).start()
        return

    if clean_text in ["🧠 تقرير استخباراتي", "استخبارات", "intelligence", "news"]:
        queue_telegram_message("⏳ جاري فحص الرادارات...", chat_id or CHAT_ID)
        def send_intel():
            report = generate_intelligence_report()
            queue_telegram_message(f"🧠 <b>تقرير تولين الاستخباراتي:</b>\n\n{report}", chat_id or CHAT_ID)
        threading.Thread(target=send_intel, daemon=True).start()
        return

    # ✅ تقرير التعلم العميق (زر + أمر نصي) - معدل لاستدعاء الدالة الصحيحة
    if clean_text in ["🧠 تقرير التعلم العميق", "تقرير التعلم العميق", "deep learning", "deep stats", "تقرير التعلم"]:
        def send_deep_stats():
            try:
                # ✅ استخدام الدالة المعدلة في PART 15
                report = get_learning_stats_report()
                if not report or len(report.strip()) < 50:
                    report = "⚠️ لا توجد بيانات تعلم كافية حالياً.\n\n💡 البوت يحتاج إلى صفقات مغلقة للتعلم."
                queue_telegram_message(report, chat_id or CHAT_ID)
            except Exception as e:
                logger.error(f"❌ فشل تقرير التعلم: {e}")
                queue_telegram_message(f"⚠️ حدث خطأ أثناء جلب تقرير التعلم: {str(e)[:100]}", chat_id or CHAT_ID)
        threading.Thread(target=send_deep_stats, daemon=True).start()
        return

    if clean_text in ["❌ إغلاق النفط", "إغلاق النفط"]:
        close_trade_manually("oil", "أمر يدوي من الزر")
        queue_telegram_message("✅ تم إغلاق صفقة النفط يدوياً.", chat_id or CHAT_ID)
        return

    if clean_text in ["❌ إغلاق الفضة", "إغلاق الفضة"]:
        close_trade_manually("silver", "أمر يدوي من الزر")
        queue_telegram_message("✅ تم إغلاق صفقة الفضة يدوياً.", chat_id or CHAT_ID)
        return

    if clean_text in ["❌ إغلاق الصفقة", "إغلاق", "close"]:
        oil_trade = get_current_open_trade("oil")
        silver_trade = get_current_open_trade("silver")
        if not oil_trade and not silver_trade:
            queue_telegram_message("🔄 لا توجد صفقات مفتوحة للإغلاق.", chat_id or CHAT_ID)
        else:
            msg = "⚠️ <b>اختر الصفقة للإغلاق:</b>\n\n"
            if oil_trade:
                profit = AccountingSystem.calculate_profit_dollars(
                    oil_trade["entry_price"], 
                    oil_trade.get("last_price", oil_trade["entry_price"]), 
                    oil_trade["type"]
                )
                msg += f"🛢️ <b>صفقة النفط</b>\n"
                msg += f"   النوع: {oil_trade['type']}\n"
                msg += f"   النتيجة: {AccountingSystem.format_profit(profit)}\n"
                msg += "   ➡️ أرسل: `أغلق صفقة النفط`\n\n"
            if silver_trade:
                profit = AccountingSystem.calculate_profit_dollars(
                    silver_trade["entry_price"], 
                    silver_trade.get("last_price", silver_trade["entry_price"]), 
                    silver_trade["type"]
                )
                msg += f"🥈 <b>صفقة الفضة</b>\n"
                msg += f"   النوع: {silver_trade['type']}\n"
                msg += f"   النتيجة: {AccountingSystem.format_profit(profit)}\n"
                msg += "   ➡️ أرسل: `أغلق صفقة الفضة`"
            queue_telegram_message(msg, chat_id or CHAT_ID)
        return

    if clean_text in ["🔍 تحليل عميق", "تحليل عميق", "deep analysis", "deep"]:
        threading.Thread(target=handle_deep_analysis, args=(chat_id,), daemon=True).start()
        return

    if clean_text in ["/remove_webhook", "إزالة الويب هوك"]:
        remove_webhook()
        queue_telegram_message("🗑️ تم إزالة Webhook.", chat_id or CHAT_ID)
        return

    if clean_text in ["/set_webhook", "تفعيل الويب هوك"]:
        set_webhook()
        queue_telegram_message("✅ تم تفعيل Webhook.", chat_id or CHAT_ID)
        return

    # ── ✅ كل ما تبقى يذهب إلى المحادثة الذكية ──
    chat_response(clean_text, chat_id)

# ====================================================================================
# نهاية PART 25
# ====================================================================================

# ====================================================================================
# 📦 PART 26: الخيوط (Threads) - معدل نهائي - مع إصلاح حفظ اللقطات واستدعاء الدوال
# ====================================================================================
# ✅ التعديلات الجديدة:
#   1. دمج check_distance_warning (تحذير SL واحد عند ≤ 33%).
#   2. دمج check_trend_reversal_warnings (3 مستويات لانعكاس الاتجاه).
#   3. دمج check_memory_warning (تحذير استباقي من الذاكرة).
#   4. ✅ إضافة تحليل سلسلة اللقطات باستخدام SnapshotEngine من PART 30.
#   5. ✅ حفظ الدروس المستخلصة من اللقطات باستخدام save_lessons من PART 15.
#   6. ✅ إصلاح حفظ اللقطات: استخدام الدالة الصحيحة من PART 10 مباشرة.
#   7. ✅ توحيد قراءة اللقطات من جدول snapshots في Supabase باستخدام TABLE_SNAPSHOTS.
#   8. ✅ تصحيح مسار الملف المحلي للقطات: snapshots بدلاً من failed_snapshots.
#   9. تخزين last_analysis في الصفقة المفتوحة بعد كل مراقبة.
#  10. الحفاظ على جميع الدوال والخيوط الأخرى دون تغيير.
#  11. ✅ استخدام المتغيرات العامة الموحدة لأسماء الجداول من PART 10.
#  12. ✅ تعديل health_check لاستدعاء load_trades_history مع update_cache=False لمنع التكرار.
# ====================================================================================

import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

# ============================================================================
# الخيط 1: ماسح الإشارات (بدون تغيير)
# ============================================================================

def signal_scanner():
    """ماسح الإشارات - يعمل كل 60 ثانية"""
    logger.info("[Scanner] بدأ التشغيل")
    while True:
        start = time.time()
        logger.info("📡 [Scanner] دورة فحص جديدة بدأت")
        for asset_type in ["oil", "silver"]:
            try:
                analyze_and_send(asset_type, is_manual=False)
            except Exception as e:
                logger.error(f"[Scanner] خطأ في فحص {asset_type}: {e}")
        elapsed = time.time() - start
        time.sleep(max(0, SIGNAL_CHECK_INTERVAL - elapsed))

# ============================================================================
# الخيط 2: المراقبة العميقة (معدل نهائي)
# ============================================================================

def deep_monitor():
    logger.info("[Monitor] بدأ التشغيل")
    last_scheduled = {"oil": 0, "silver": 0}
    last_tcn_save = 0
    last_narrative_save = 0

    while True:
        now = time.time()

        # TCN: حفظ الحالة كل 5 دقائق
        if TCN_AVAILABLE and TCN and now - last_tcn_save >= 300:
            try:
                TCN.save_state()
                logger.info("🧠 تم حفظ حالة TCN")
                last_tcn_save = now
            except Exception as e:
                logger.error(f"❌ فشل حفظ TCN: {e}")

        # حفظ الذاكرة السردية كل 5 دقائق
        if NARRATIVE_AVAILABLE and NARRATIVE and now - last_narrative_save >= 300:
            try:
                if _safe_save_narrative():
                    logger.info("💾 تم حفظ الذاكرة السردية في Gist (دوري)")
                    last_narrative_save = now
            except Exception as e:
                logger.error(f"❌ فشل حفظ الذاكرة السردية دورياً: {e}")

        # المراقبة الأساسية (كل 5 دقائق)
        for asset_type in ["oil", "silver"]:
            should_run = False
            reason = "scheduled"
            if now - last_scheduled[asset_type] >= MONITORING_INTERVAL:
                should_run = True
            with MONITOR_TRIGGER_LOCK:
                trigger = MONITOR_TRIGGER[asset_type]
                if trigger and now - trigger["time"] < 60:
                    should_run = True
                    reason = trigger["reason"]
                    MONITOR_TRIGGER[asset_type] = None
            if should_run:
                try:
                    _run_deep_monitor(asset_type, reason)
                    last_scheduled[asset_type] = now
                except Exception as e:
                    logger.error(f"[Monitor] خطأ في {asset_type}: {e}")

        time.sleep(5)

# ============================================================================
# تشغيل المراقبة العميقة (الدالة الأساسية - معدلة نهائياً)
# ============================================================================

def _run_deep_monitor(asset_type, reason):
    logger.info(f"[Monitor] تحليل عميق لـ {asset_type} — السبب: {reason}")

    # 1. جلب الصفقة المفتوحة
    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        if reason == "scheduled":
            return
        with MONITOR_TRIGGER_LOCK:
            MONITOR_TRIGGER[asset_type] = None
        return

    # 2. جلب التحليل الشامل
    analysis, _ = perform_comprehensive_analysis(asset_type, True, open_trade)
    if not analysis:
        logger.warning(f"⚠️ فشل الحصول على التحليل الشامل لـ {asset_type} في المراقبة")
        return

    # 3. استخراج البيانات من التحليل الشامل
    current_price = analysis.get("price", 0)
    if current_price <= 0:
        logger.warning(f"⚠️ سعر غير صالح لـ {asset_type} في المراقبة")
        return

    timeframes = analysis.get("timeframes", {})
    tf_15m = timeframes.get("15m", {}) if isinstance(timeframes, dict) else {}
    indicators = analysis.get("indicators", {}) if isinstance(analysis.get("indicators"), dict) else {}

    adx = tf_15m.get("adx", 15) if isinstance(tf_15m, dict) else 15
    vol_ratio = tf_15m.get("volume_ratio", 1.0) if isinstance(tf_15m, dict) else 1.0
    rsi = tf_15m.get("rsi", 50) if isinstance(tf_15m, dict) else 50
    trend = tf_15m.get("trend", "محايد") if isinstance(tf_15m, dict) else "محايد"
    macd = tf_15m.get("macd", 0) if isinstance(tf_15m, dict) else 0

    supertrend_data = analysis.get("supertrend", {}) if isinstance(analysis.get("supertrend"), dict) else {}
    st_trend = supertrend_data.get("trend", 1) if isinstance(supertrend_data, dict) else 1

    bb = tf_15m.get("bollinger", {}) if isinstance(tf_15m, dict) else {}
    bb_upper = bb.get("upper", current_price * 1.02) if isinstance(bb, dict) else current_price * 1.02
    bb_middle = bb.get("basis", current_price) if isinstance(bb, dict) else current_price
    bb_lower = bb.get("lower", current_price * 0.98) if isinstance(bb, dict) else current_price * 0.98

    sr = indicators.get("support_resistance", {}) if isinstance(indicators, dict) else {}
    support = sr.get("s1", current_price * 0.98) if isinstance(sr, dict) else current_price * 0.98
    resistance = sr.get("r1", current_price * 1.02) if isinstance(sr, dict) else current_price * 1.02

    sentiment = indicators.get("sentiment", {}) if isinstance(indicators, dict) else {}
    fear_greed = sentiment.get("fear_greed", 50) if isinstance(sentiment, dict) else 50

    vwap = tf_15m.get("vwap", 0) if isinstance(tf_15m, dict) else 0

    # 4. تحديث السعر في الصفقة المفتوحة (مع قفل)
    if open_trade:
        open_trade["last_price"] = current_price
        pos_file = get_position_file(asset_type)

        def _update_position():
            with open(pos_file, 'w', encoding='utf-8') as f:
                json.dump(open_trade, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 [Monitor] تم تحديث last_price في {pos_file}")

        safe_file_operation(asset_type, _update_position)

    # 5. التحقق من ضرب SL/TP
    if open_trade:
        if check_sl_tp_hit(asset_type, current_price, open_trade):
            return

    # 6. تحذير اقتراب من SL (مرة واحدة عند ≤ 33%)
    if open_trade:
        check_distance_warning(asset_type, current_price, open_trade)

    # 7. تحذير انعكاس الاتجاه (3 مستويات)
    if open_trade:
        check_trend_reversal_warnings(asset_type, analysis, open_trade)

    # 8. تحذير الذاكرة الاستباقي
    if open_trade:
        check_memory_warning(asset_type, analysis, open_trade)

    # 9. 🧠 إعادة تقييم احتمال نجاح/فشل الإشارة من الذاكرة التاريخية كل 5 دقائق
    if open_trade:
        check_adaptive_learning_warning(asset_type, analysis, open_trade)

    # 10. حفظ لقطة المراقبة في قاعدة التعلم (جدول snapshots)
    # ✅ باستخدام TABLE_SNAPSHOTS عبر save_snapshot_to_learning من PART 10
    snapshot_saved = False
    try:
        if open_trade:
            profit_dollars = open_trade.get('profit_dollars', 0)
            entry_price = open_trade.get('entry_price', current_price)
            profit_pct = (((current_price - entry_price) / entry_price * 100) if open_trade.get("type", "BUY") == "BUY" else ((entry_price - current_price) / entry_price * 100)) if entry_price != 0 else 0

            snapshot_data = {
                'trade_id': open_trade.get('trade_id', ''),
                'asset_type': asset_type,
                'timestamp': datetime.now().isoformat(),
                'price': current_price,
                'rsi': rsi,
                'adx': adx,
                'macd': macd,
                'st_trend': 'صاعد' if st_trend == 1 else 'هابط',
                'volume_ratio': vol_ratio,
                'profit_dollars': profit_dollars,
                'profit_pct': profit_pct,
                'warning_level': len(open_trade.get('warnings_sent', [])),
                'fear_greed_index': fear_greed,
                'market_regime': 'unknown',
                'bb_upper': bb_upper,
                'bb_middle': bb_middle,
                'bb_lower': bb_lower,
                'vwap': vwap,
                'support': support,
                'resistance': resistance,
                'trend': trend,
                'last_analysis': open_trade.get('last_analysis', {})
            }
            
            # ✅ استدعاء الدالة الصحيحة من PART 10 مباشرة (تستخدم TABLE_SNAPSHOTS)
            try:
                snapshot_saved = save_snapshot_to_learning(snapshot_data)
                if snapshot_saved:
                    logger.info(f"💾 [Monitor] تم حفظ لقطة للصفقة {open_trade.get('trade_id')} - السعر: ${current_price:.2f}")
                else:
                    logger.warning(f"⚠️ [Monitor] فشل حفظ لقطة للصفقة {open_trade.get('trade_id')}")
            except Exception as e:
                logger.error(f"❌ [Monitor] استثناء أثناء حفظ اللقطة: {e}")
                snapshot_saved = False
                
            if not snapshot_saved:
                try:
                    backup_file = f"learning_data/backups/snapshots_{asset_type}.json"
                    os.makedirs(os.path.dirname(backup_file), exist_ok=True)
                    backup_data = {}
                    if os.path.exists(backup_file):
                        with open(backup_file, 'r', encoding='utf-8') as f:
                            backup_data = json.load(f)
                    snapshots_list = backup_data.get('snapshots', [])
                    snapshots_list.append(snapshot_data)
                    backup_data['snapshots'] = snapshots_list
                    backup_data['last_update'] = datetime.now().isoformat()
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        json.dump(backup_data, f, indent=2, ensure_ascii=False)
                    logger.info(f"💾 [Monitor] تم حفظ نسخة احتياطية للقطة في {backup_file}")
                except Exception as e:
                    logger.error(f"❌ [Monitor] فشل حفظ النسخة الاحتياطية للقطة: {e}")
    except Exception as e:
        logger.error(f"❌ [Monitor] فشل حفظ اللقطة: {e}")

    # ================================================================
    # ✅ 10. تحليل سلسلة اللقطات واستخلاص الدروس (معدل)
    # ================================================================
    try:
        if open_trade and open_trade.get('trade_id'):
            trade_id = open_trade.get('trade_id')
            logger.info(f"🔍 [Monitor] تحليل سلسلة اللقطات للصفقة {trade_id}")
            
            # ── جلب اللقطات من Supabase (جدول snapshots) مباشرة ──
            snapshots = []
            if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
                try:
                    client = _get_supabase_client()
                    if client:
                        response = client.table(TABLE_SNAPSHOTS)\
                            .select('*')\
                            .eq('trade_id', trade_id)\
                            .order('timestamp', desc=True)\
                            .limit(20)\
                            .execute()
                        if response and hasattr(response, 'data'):
                            snapshots = response.data
                            logger.info(f"📸 [Monitor] جلب {len(snapshots)} لقطة من Supabase (جدول {TABLE_SNAPSHOTS}) للصفقة {trade_id}")
                except Exception as e:
                    logger.warning(f"⚠️ [Monitor] فشل جلب اللقطات من Supabase: {e}")
            
            # ── إذا لم تنجح Supabase، استخدم الملف المحلي بالمسار الصحيح ──
            if not snapshots:
                try:
                    backup_file = f"learning_data/backups/snapshots_{asset_type}.json"
                    if os.path.exists(backup_file):
                        with open(backup_file, 'r', encoding='utf-8') as f:
                            backup_data = json.load(f)
                            all_snapshots = backup_data.get('snapshots', [])
                            snapshots = [s for s in all_snapshots if s.get('trade_id') == trade_id][-20:]
                            logger.info(f"📸 [Monitor] جلب {len(snapshots)} لقطة من الملف المحلي للصفقة {trade_id}")
                except Exception as e:
                    logger.warning(f"⚠️ [Monitor] فشل جلب اللقطات من الملف المحلي: {e}")
            
            # ── إذا كان لدينا 3 لقطات على الأقل، نحللها ──
            if len(snapshots) >= 3:
                if 'SnapshotEngine' in globals() and SnapshotEngine:
                    try:
                        lessons_from_snapshots = SnapshotEngine.analyze_sequence(snapshots, trade_id, asset_type)
                        if lessons_from_snapshots:
                            try:
                                saved = save_lessons(lessons_from_snapshots, asset_type, trade_id, source='snapshot_analysis')
                                if saved:
                                    logger.info(f"🧠 [Monitor] تم حفظ {len(lessons_from_snapshots)} درس من تحليل اللقطات للصفقة {trade_id}")
                                else:
                                    logger.warning(f"⚠️ [Monitor] فشل حفظ دروس اللقطات للصفقة {trade_id}")
                            except Exception as e:
                                logger.error(f"❌ [Monitor] فشل حفظ دروس اللقطات: {e}")
                    except Exception as e:
                        logger.error(f"❌ [Monitor] فشل تحليل اللقطات: {e}")
                else:
                    logger.warning(f"⚠️ [Monitor] SnapshotEngine غير متوفر، تخطي تحليل اللقطات")
            else:
                logger.info(f"ℹ️ [Monitor] عدد اللقطات غير كافٍ للتحليل ({len(snapshots)} لقطة) للصفقة {trade_id}")
                
    except Exception as e:
        logger.error(f"❌ [Monitor] فشل تحليل اللقطات: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# الخيط 3: مراقبة الصفقات (Fallback - بدون تغيير)
# ============================================================================

def check_and_monitor_positions(asset_type, current_price, st_line, current_trend, data=None):
    open_trade = get_current_open_trade(asset_type)
    if not open_trade:
        return
    if check_sl_tp_hit(asset_type, current_price, open_trade):
        return
    if data:
        check_distance_warning(asset_type, current_price, open_trade)
    pos_file = get_position_file(asset_type)
    def _update_position():
        with open(pos_file, 'w', encoding='utf-8') as f:
            json.dump(open_trade, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 [check_and_monitor] تم تحديث {pos_file}")
    safe_file_operation(asset_type, _update_position)

# ============================================================================
# الخيط 4: معالج طابور Telegram (بدون تغيير)
# ============================================================================

def telegram_sender():
    logger.info("[Sender] بدأ التشغيل")
    while True:
        try:
            msg = TELEGRAM_QUEUE.get(timeout=1)
            _send_telegram_message(msg["text"], msg.get("chat_id"))
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"[Sender] خطأ: {e}")

# ============================================================================
# الخيط 5: محرك الأحلام (بدون تغيير)
# ============================================================================

def _dream_worker():
    logger.info("🌙 Dream Worker بدأ التشغيل")
    while True:
        try:
            time.sleep(600)
            if DREAM_AVAILABLE and DREAM:
                DREAM.dream()
                if PROMETHEUS_AVAILABLE and PROMETHEUS:
                    try:
                        PROMETHEUS.update_emotion(trigger='dream_completed')
                    except:
                        pass
        except Exception as e:
            logger.error(f"خطأ في Dream Worker: {e}")

# ============================================================================
# الخيط 6: فحص صحة النظام (معدل - مع update_cache=False)
# ============================================================================

def health_check():
    logger.info("[Health] بدأ التشغيل")
    while True:
        time.sleep(60)
        queue_size = TELEGRAM_QUEUE.qsize()
        if queue_size > 50:
            logger.warning(f"[Health] Queue كبيرة: {queue_size} رسائل")
        if TCN_AVAILABLE and TCN:
            try:
                consciousness = TCN.get_consciousness()
                logger.info(f"[Health] 🧠 TCN: {consciousness.dominant_emotion} | ثقة: {consciousness.confidence*100:.0f}%")
            except Exception as e:
                logger.error(f"[Health] ❌ TCN غير مستجيب: {e}")
        for asset in ["oil", "silver"]:
            trade = get_current_open_trade(asset)
            if trade:
                logger.info(f"[Health] 📊 صفقة {asset} مفتوحة: {trade.get('type')} @ ${trade.get('entry_price', 0):.2f}")
            # ✅ استدعاء load_trades_history مع update_cache=False لمنع الحفظ المتكرر في SQLite
            history = load_trades_history(asset, update_cache=False)
            if history and history.get('trades'):
                logger.info(f"[Health] 📊 {asset}: {len(history.get('trades', []))} صفقة في السجل")
        logger.info(f"[Health] ✅ Queue={queue_size}")

# ============================================================================
# دوال مساعدة داخلية (بدون تغيير)
# ============================================================================

def _safe_save_narrative():
    if not NARRATIVE_AVAILABLE or not NARRATIVE:
        return False
    try:
        if hasattr(NARRATIVE, 'save_state'):
            NARRATIVE.save_state()
            logger.info("💾 تم حفظ الذاكرة السردية (save_state)")
            return True
        elif hasattr(NARRATIVE, 'save'):
            NARRATIVE.save()
            logger.info("💾 تم حفظ الذاكرة السردية (save)")
            return True
        elif hasattr(NARRATIVE, 'flush'):
            NARRATIVE.flush()
            logger.info("💾 تم حفظ الذاكرة السردية (flush)")
            return True
        else:
            return True
    except Exception as e:
        logger.error(f"❌ فشل حفظ الذاكرة السردية: {e}")
        return False

def safe_file_operation(asset_type, operation, *args, **kwargs):
    lock = FILE_LOCKS[asset_type]
    max_attempts = 3
    for attempt in range(max_attempts):
        acquired = lock.acquire(timeout=10)
        if acquired:
            try:
                logger.info(f"🔒 [safe_file_operation] تم الحصول على قفل {asset_type} (محاولة {attempt+1})")
                result = operation(*args, **kwargs)
                logger.info(f"🔓 [safe_file_operation] تم تحرير قفل {asset_type}")
                return result
            finally:
                lock.release()
        else:
            logger.warning(f"⚠️ [safe_file_operation] فشل الحصول على قفل {asset_type} (محاولة {attempt+1}/{max_attempts})")
            if attempt < max_attempts - 1:
                time.sleep(0.5)
    logger.error(f"❌ [safe_file_operation] فشل الحصول على قفل {asset_type} بعد {max_attempts} محاولات")
    return None

# ====================================================================================
# نهاية PART 26
# ====================================================================================

# ====================================================================================
# 📦 PART 27: التقارير الدورية
# ====================================================================================

def should_send_daily_report():
    global LAST_DAILY_REPORT
    with REPORT_LOCK:
        now = datetime.now()
        if now.strftime("%H:%M") == DAILY_REPORT_TIME and LAST_DAILY_REPORT != now.strftime("%Y-%m-%d"):
            LAST_DAILY_REPORT = now.strftime("%Y-%m-%d")
            return True
        return False

def send_daily_report():
    try:
        oil_data = get_mexc_candles("USOIL_USDT", "Min15", 50)
        silver_data = get_mexc_candles("SILVER_USDT", "Min15", 50)
        if not oil_data or not silver_data:
            return

        oil_price = oil_data["closes"][-1] if oil_data.get("closes") else 0
        silver_price = silver_data["closes"][-1] if silver_data.get("closes") else 0
        stats_oil = calculate_statistics("oil")
        stats_silver = calculate_statistics("silver")

        report = f"📊 <b>تقرير يومي - {datetime.now().strftime('%Y-%m-%d')}</b>\n\n"
        report += f"🛢️ <b>النفط:</b> ${oil_price:.2f} | صفقات: {stats_oil['total_trades']} | نجاح: {stats_oil['win_rate']:.1f}% | ربح: ${stats_oil['total_profit']:.2f}\n"
        report += f"🥈 <b>الفضة:</b> ${silver_price:.3f} | صفقات: {stats_silver['total_trades']} | نجاح: {stats_silver['win_rate']:.1f}% | ربح: ${stats_silver['total_profit']:.2f}\n"
        report += f"📈 <b>الإجمالي:</b> {stats_oil['total_trades'] + stats_silver['total_trades']} صفقة | ربح: ${stats_oil['total_profit'] + stats_silver['total_profit']:.2f}"

        queue_telegram_message(report)
    except Exception as e:
        logger.error(f"خطأ في التقرير اليومي: {e}")

def should_export_archive():
    global LAST_EXPORT
    with REPORT_LOCK:
        now = datetime.now()
        if LAST_EXPORT is None:
            return False
        try:
            last = datetime.fromisoformat(LAST_EXPORT)
            if (now - last).days >= EXPORT_INTERVAL_DAYS:
                LAST_EXPORT = now.isoformat()
                return True
        except:
            LAST_EXPORT = now.isoformat()
        return False

def export_learning_archive():
    try:
        export_dir = "learning_data/exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for asset_type in ["oil", "silver"]:
            history = load_trades_history(asset_type)
            trades = history.get("trades", [])
            if not trades:
                continue
            filename = f"{export_dir}/{asset_type}_archive_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['trade_id', 'type', 'entry_price', 'exit_price', 'sl', 'tp', 'profit_dollars', 'exit_reason', 'timestamp', 'status'])
                for trade in trades:
                    writer.writerow([
                        trade.get('trade_id', ''),
                        trade.get('type', ''),
                        trade.get('entry_price', ''),
                        trade.get('exit_price', ''),
                        trade.get('sl', ''),
                        trade.get('tp', ''),
                        trade.get('profit_dollars', ''),
                        trade.get('exit_reason', ''),
                        trade.get('timestamp', ''),
                        trade.get('status', '')
                    ])
            logger.info(f"تم تصدير أرشيف {asset_type}: {filename}")
        queue_telegram_message(f"📤 تم تصدير أرشيف التعلم\nالمجلد: {export_dir}")
    except Exception as e:
        logger.error(f"خطأ في التصدير: {e}")
       
# ====================================================================================
# 📦 PART 30: نظام التعلم العميق الأساسي (V7.0 – المتكامل مع جميع المؤشرات والفريمات)
# ====================================================================================
# ═══════════════════════════════════════════════════════════════════════════════
# 🔴 القاعدة الذهبية للتحليل الفني الشامل (مطبقة هنا):
# ═══════════════════════════════════════════════════════════════════════════════
# 1. التعلم يعتمد على جميع المؤشرات الفنية الأساسية.
# 2. يحلل جميع الفريمات الأربعة.
# 3. استخلاص الدروس يعتمد على تحليل جميع المؤشرات والفريمات.
# ═══════════════════════════════════════════════════════════════════════════════
# ====================================================================================

import statistics
import json
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

_required_globals = [
    'SUPABASE_AVAILABLE', 'SUPABASE_DB', 'DEEP_LEARNING_AVAILABLE', 'DEEP_LEARNING_DB',
    'load_lessons_from_gist', 'load_patterns_from_gist', 'save_lessons', 'save_patterns',
    'queue_telegram_message', '_get_supabase_client', '_filter_data_for_table',
    'LESSONS_DEEP_COLUMNS', 'PATTERNS_COLUMNS', 'discover_patterns_from_trades',
    'TABLE_TRADES_FULL', 'TABLE_LESSONS_DEEP', 'TABLE_DISCOVERED_PATTERNS',
    'TABLE_SNAPSHOTS', 'TABLE_TRADE_PREDICTIONS',
    'update_prediction_result', 'update_prediction_calibration'
]
for _name in _required_globals:
    if _name not in globals():
        try:
            logger.warning(f"⚠️ [PART 30] الدالة/المتغير '{_name}' غير موجود في النطاق العام")
        except:
            print(f"⚠️ [PART 30] الدالة/المتغير '{_name}' غير موجود في النطاق العام")

LEARNING_CONFIG = {
    "max_lessons": 200,
    "max_patterns": 100,
    "min_samples_for_pattern": 3,
    "prune_threshold_days": 90,
    "similarity_threshold": 65,
    "memory_cache_ttl": 60,
    "snapshot_analysis_min": 3,
    "min_support": 0.02,
    "min_lift": 1.2,
    "learning_rate": 0.1,
    "min_lessons_for_calibration": 20,
    "prediction_calibration_interval": 10,
    "min_predictions_for_calibration": 10
}

class MemoryEngine:
    def __init__(self):
        self._cache = {"lessons": [], "patterns": [], "last_update": 0}
        self._cache_ttl = LEARNING_CONFIG["memory_cache_ttl"]
        self._lock = threading.Lock()
        self._learning_weights = self._load_learning_weights()

    def get_memory(self, asset_type: Optional[str] = None, force_refresh: bool = False) -> Dict[str, List]:
        now = time.time()
        with self._lock:
            if not force_refresh and (now - self._cache["last_update"] < self._cache_ttl):
                if self._cache["lessons"] is not None:
                    return {"lessons": self._cache["lessons"], "patterns": self._cache["patterns"]}
        lessons = self._get_lessons(asset_type)
        patterns = self._get_patterns(asset_type)
        if not lessons and not patterns:
            logger.info("🔄 [MemoryEngine] Supabase لم يعد بيانات، استخدام Gist كنسخة احتياطية")
            lessons = load_lessons_from_gist()
            patterns = load_patterns_from_gist()
        lessons = self._filter_lessons(lessons)
        patterns = self._filter_patterns(patterns)
        with self._lock:
            self._cache["lessons"] = lessons
            self._cache["patterns"] = patterns
            self._cache["last_update"] = now
        return {"lessons": lessons, "patterns": patterns}

    def invalidate_cache(self):
        with self._lock:
            self._cache["lessons"] = []
            self._cache["patterns"] = []
            self._cache["last_update"] = 0
        logger.info("🧠 [MemoryEngine] تم مسح الكاش")

    def _filter_lessons(self, lessons: List[Dict]) -> List[Dict]:
        if not lessons:
            return []
        filtered = []
        for lesson in lessons:
            filtered_lesson = {}
            for key in LESSONS_DEEP_COLUMNS:
                if key in lesson:
                    filtered_lesson[key] = lesson[key]
            if filtered_lesson:
                filtered.append(filtered_lesson)
        return filtered

    def _filter_patterns(self, patterns: List[Dict]) -> List[Dict]:
        if not patterns:
            return []
        filtered = []
        for pattern in patterns:
            filtered_pattern = {}
            for key in PATTERNS_COLUMNS:
                if key in pattern:
                    filtered_pattern[key] = pattern[key]
            if filtered_pattern:
                filtered.append(filtered_pattern)
        return filtered

    def _get_lessons(self, asset_type: Optional[str] = None, limit: int = 200) -> List[Dict]:
        if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
            return []
        try:
            if hasattr(SUPABASE_DB, 'get_lessons'):
                return SUPABASE_DB.get_lessons(asset_type, limit) or []
            client = _get_supabase_client()
            if not client:
                return []
            query = client.table(TABLE_LESSONS_DEEP).select('*').order('created_at', desc=True).limit(limit)
            if asset_type:
                query = query.eq('asset_type', asset_type)
            response = query.execute()
            return response.data if response and hasattr(response, 'data') else []
        except Exception as e:
            logger.warning(f"⚠️ [MemoryEngine] فشل جلب الدروس: {e}")
            return []

    def _get_patterns(self, asset_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
        if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
            return []
        try:
            if hasattr(SUPABASE_DB, 'get_patterns'):
                return SUPABASE_DB.get_patterns(asset_type, limit) or []
            client = _get_supabase_client()
            if not client:
                return []
            query = client.table(TABLE_DISCOVERED_PATTERNS).select('*').order('created_at', desc=True).limit(limit)
            if asset_type:
                query = query.eq('asset_type', asset_type)
            response = query.execute()
            return response.data if response and hasattr(response, 'data') else []
        except Exception as e:
            logger.warning(f"⚠️ [MemoryEngine] فشل جلب الأنماط: {e}")
            return []

    def _load_learning_weights(self) -> Dict:
        try:
            weights_file = "learning_data/learning_weights.json"
            if os.path.exists(weights_file):
                with open(weights_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ فشل تحميل أوزان التعلم: {e}")
        return {
            'rsi_weight': 0.12,
            'adx_weight': 0.10,
            'macd_weight': 0.08,
            'stoch_weight': 0.07,
            'trend_weight': 0.15,
            'volume_weight': 0.08,
            'volatility_weight': 0.07,
            'bb_weight': 0.05,
            'vwap_weight': 0.04,
            'fear_greed_weight': 0.06,
            'sr_weight': 0.08,
            'memory_weight': 0.10,
            'vpt_weight': 0.05,
            'supertrend_weight': 0.05
        }

    def _save_learning_weights(self):
        try:
            os.makedirs("learning_data", exist_ok=True)
            weights_file = "learning_data/learning_weights.json"
            with open(weights_file, 'w', encoding='utf-8') as f:
                json.dump(self._learning_weights, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ فشل حفظ أوزان التعلم: {e}")

    def update_weights(self, trade_result: Dict):
        try:
            entry_analysis = trade_result.get('full_entry_analysis', {})
            is_win = trade_result.get('profit_dollars', 0) > 0
            if not entry_analysis:
                return
            
            indicators = entry_analysis.get('indicators', {})
            momentum = indicators.get('momentum', {})
            trend_data = indicators.get('trend', {})
            volatility = indicators.get('volatility', {})
            volume = indicators.get('volume', {})
            sentiment = indicators.get('sentiment', {})
            
            indicator_correctness = {}
            trade_type = trade_result.get('trade_type', 'BUY')
            
            rsi = momentum.get('rsi')
            if rsi is not None:
                if trade_type == 'BUY':
                    rsi_correct = (rsi < 70)
                else:
                    rsi_correct = (rsi > 30)
                indicator_correctness['rsi'] = rsi_correct
            
            adx = trend_data.get('adx')
            if adx is not None:
                adx_correct = (adx > 20)
                indicator_correctness['adx'] = adx_correct
            
            macd = momentum.get('macd')
            if macd is not None:
                if trade_type == 'BUY':
                    macd_correct = (macd > 0)
                else:
                    macd_correct = (macd < 0)
                indicator_correctness['macd'] = macd_correct
            
            current_trend = trend_data.get('current_trend', 'محايد')
            if current_trend != 'محايد':
                if trade_type == 'BUY':
                    trend_correct = (current_trend == 'صاعد')
                else:
                    trend_correct = (current_trend == 'هابط')
                indicator_correctness['trend'] = trend_correct
            
            vol_ratio = volume.get('ratio')
            if vol_ratio is not None:
                vol_correct = (vol_ratio > 0.8)
                indicator_correctness['volume'] = vol_correct
            
            atr_pct = volatility.get('atr_percent')
            if atr_pct is not None:
                vol_correct = (atr_pct < 2.5)
                indicator_correctness['volatility'] = vol_correct
            
            learning_rate = LEARNING_CONFIG.get('learning_rate', 0.1)
            
            for indicator, was_correct in indicator_correctness.items():
                weight_key = f"{indicator}_weight"
                if weight_key in self._learning_weights:
                    if is_win and was_correct:
                        self._learning_weights[weight_key] = min(0.25, self._learning_weights[weight_key] + learning_rate * 0.02)
                    elif not is_win and not was_correct:
                        self._learning_weights[weight_key] = max(0.01, self._learning_weights[weight_key] - learning_rate * 0.02)
                    elif is_win and not was_correct:
                        self._learning_weights[weight_key] = max(0.01, self._learning_weights[weight_key] - learning_rate * 0.005)
                    elif not is_win and was_correct:
                        self._learning_weights[weight_key] = min(0.25, self._learning_weights[weight_key] + learning_rate * 0.005)
            
            self._save_learning_weights()
            logger.info(f"📊 [MemoryEngine] تم تحديث أوزان التعلم: {self._learning_weights}")
            
        except Exception as e:
            logger.error(f"❌ [MemoryEngine] فشل تحديث الأوزان: {e}")

    def detect_false_signal_pattern(self, trade: Dict) -> Dict:
        entry_analysis = trade.get('full_entry_analysis', {})
        if not entry_analysis:
            return {'is_false_signal': False, 'reason': 'بيانات غير كافية'}
        
        indicators = entry_analysis.get('indicators', {})
        momentum = indicators.get('momentum', {})
        trend_data = indicators.get('trend', {})
        volatility = indicators.get('volatility', {})
        volume = indicators.get('volume', {})
        timeframes = entry_analysis.get('timeframes', {})
        
        rsi = momentum.get('rsi')
        adx = trend_data.get('adx')
        macd = momentum.get('macd')
        vol_ratio = volume.get('ratio')
        atr_pct = volatility.get('atr_percent')
        current_trend = trend_data.get('current_trend', 'محايد')
        vpt = indicators.get('vpt', 0)
        bb_pos = volatility.get('bb_position', 0.5)
        stoch = momentum.get('stoch', 50)
        
        bullish_count = sum(1 for tf in timeframes.values() if tf.get('trend') == 'صاعد')
        bearish_count = sum(1 for tf in timeframes.values() if tf.get('trend') == 'هابط')
        
        trade_type = trade.get('trade_type', 'BUY')
        is_win = trade.get('profit_dollars', 0) > 0
        
        false_signal_score = 0
        reasons = []
        
        if rsi is not None:
            if trade_type == 'BUY' and rsi > 70:
                false_signal_score += 2
                reasons.append(f"RSI مرتفع ({rsi:.0f}) مع إشارة شراء (ذروة شراء)")
            elif trade_type == 'SELL' and rsi < 30:
                false_signal_score += 2
                reasons.append(f"RSI منخفض ({rsi:.0f}) مع إشارة بيع (ذروة بيع)")
        
        if adx is not None and adx < 20:
            false_signal_score += 2
            reasons.append(f"ADX ضعيف ({adx:.0f}) - سوق عرضي")
        
        if macd is not None:
            if trade_type == 'BUY' and macd < 0:
                false_signal_score += 2
                reasons.append("MACD سلبي مع إشارة شراء (تناقض)")
            elif trade_type == 'SELL' and macd > 0:
                false_signal_score += 2
                reasons.append("MACD إيجابي مع إشارة بيع (تناقض)")
        
        if vol_ratio is not None and vol_ratio < 0.7:
            false_signal_score += 1
            reasons.append(f"حجم منخفض ({vol_ratio:.1f}x) - إشارة ضعيفة")
        
        if atr_pct is not None and atr_pct > 2.5:
            false_signal_score += 1
            reasons.append(f"تقلب عالٍ ({atr_pct:.1f}%) - إشارة غير مستقرة")
        
        if current_trend != 'محايد':
            if trade_type == 'BUY' and current_trend == 'هابط':
                false_signal_score += 2
                reasons.append("اتجاه هابط مع إشارة شراء (تعاكس)")
            elif trade_type == 'SELL' and current_trend == 'صاعد':
                false_signal_score += 2
                reasons.append("اتجاه صاعد مع إشارة بيع (تعاكس)")
        
        if vpt:
            if (trade_type == 'BUY' and vpt < 0) or (trade_type == 'SELL' and vpt > 0):
                false_signal_score += 1
                reasons.append(f"VPT يعاكس الإشارة ({vpt:.2f})")
        
        if bb_pos is not None and (bb_pos > 0.9 or bb_pos < 0.1):
            false_signal_score += 1
            reasons.append(f"السعر عند حدود بولينجر ({bb_pos:.0%})")
        
        if stoch is not None and (stoch > 80 or stoch < 20):
            false_signal_score += 1
            reasons.append(f"Stochastic في منطقة تشبع ({stoch:.0f})")
        
        if bullish_count >= 3 and trade_type == 'SELL':
            false_signal_score += 2
            reasons.append(f"{bullish_count}/4 فريمات صاعدة مع إشارة بيع (تعاكس)")
        elif bearish_count >= 3 and trade_type == 'BUY':
            false_signal_score += 2
            reasons.append(f"{bearish_count}/4 فريمات هابطة مع إشارة شراء (تعاكس)")
        
        is_false_signal = false_signal_score >= 3
        
        return {
            'is_false_signal': is_false_signal,
            'score': false_signal_score,
            'reasons': reasons[:3],
            'was_correctly_detected': is_false_signal and not is_win,
            'was_incorrectly_detected': is_false_signal and is_win
        }

    def compare_with_current(self, current_analysis: Dict, asset_type: str) -> Dict:
        memory = self.get_memory(asset_type)
        patterns = memory.get("patterns", [])
        lessons = memory.get("lessons", [])

        result = {
            "similar_patterns": [],
            "similar_lessons": [],
            "confidence_boost": 0,
            "insight": "",
            "has_memory": False,
            "source": "supabase" if patterns or lessons else "gist"
        }

        if not patterns and not lessons:
            return result

        comp_score = current_analysis.get('comprehensive_score', {})
        current_score = comp_score.get('score') if comp_score.get('score') is not None else 50
        current_trend = current_analysis.get('indicators', {}).get('trend', {}).get('current_trend', 'محايد')
        current_rsi = current_analysis.get('indicators', {}).get('momentum', {}).get('rsi', 50)
        current_adx = current_analysis.get('indicators', {}).get('trend', {}).get('adx', 20)
        current_macd = current_analysis.get('indicators', {}).get('momentum', {}).get('macd', 0)
        current_vol_ratio = current_analysis.get('indicators', {}).get('volume', {}).get('ratio', 1.0)
        current_vwap = current_analysis.get('indicators', {}).get('vwap', 0)
        bb = current_analysis.get('indicators', {}).get('bollinger', {})
        current_bb_upper = bb.get('upper', 0)
        current_bb_lower = bb.get('lower', 0)
        current_price = current_analysis.get('price', 0)
        current_bb_pos = (current_price - current_bb_lower) / (current_bb_upper - current_bb_lower) if (current_bb_upper - current_bb_lower) > 0 else 0.5
        current_vpt = current_analysis.get('indicators', {}).get('vpt', 0)
        current_stoch = current_analysis.get('indicators', {}).get('momentum', {}).get('stoch', 50)
        current_supertrend = current_analysis.get('supertrend', {}).get('trend', 1)

        timeframes = current_analysis.get('timeframes', {})
        current_frame_trends = {}
        for tf in ["5m", "15m", "1h", "4h"]:
            if tf in timeframes:
                current_frame_trends[tf] = timeframes[tf].get('trend', 'محايد')

        similar_patterns = []
        for pattern in patterns[:50]:
            pattern_conditions = pattern.get('conditions', {})
            pattern_score = pattern.get('score', 50)
            pattern_win_rate = pattern.get('win_rate', 0)

            similarity = 0
            total_weight = 0

            if abs(current_score - pattern_score) < 10:
                similarity += 0.10
            total_weight += 0.10

            pattern_trend = pattern_conditions.get('trend', 'محايد')
            if current_trend == pattern_trend:
                similarity += 0.10
            total_weight += 0.10

            pattern_rsi = pattern_conditions.get('rsi', 50)
            if abs(current_rsi - pattern_rsi) < 10:
                similarity += 0.10
            total_weight += 0.10

            pattern_adx = pattern_conditions.get('adx', 20)
            if abs(current_adx - pattern_adx) < 10:
                similarity += 0.08
            total_weight += 0.08

            pattern_macd = pattern_conditions.get('macd', 0)
            if abs(current_macd - pattern_macd) < 0.2:
                similarity += 0.08
            total_weight += 0.08

            pattern_vwap = pattern_conditions.get('vwap', 0)
            if current_vwap > 0 and pattern_vwap > 0:
                vwap_ratio = current_vwap / pattern_vwap
                if 0.98 <= vwap_ratio <= 1.02:
                    similarity += 0.08
            total_weight += 0.08

            pattern_bb_pos = pattern_conditions.get('bb_position', 0.5)
            if abs(current_bb_pos - pattern_bb_pos) < 0.15:
                similarity += 0.08
            total_weight += 0.08

            pattern_vpt = pattern_conditions.get('vpt', 0)
            if current_vpt and pattern_vpt:
                if (current_vpt > 0 and pattern_vpt > 0) or (current_vpt < 0 and pattern_vpt < 0):
                    similarity += 0.06
            total_weight += 0.06

            pattern_stoch = pattern_conditions.get('stochastic', 50)
            if abs(current_stoch - pattern_stoch) < 15:
                similarity += 0.06
            total_weight += 0.06

            pattern_supertrend = pattern_conditions.get('supertrend_trend', 1)
            if current_supertrend == pattern_supertrend:
                similarity += 0.06
            total_weight += 0.06

            pattern_frame_trends = pattern_conditions.get('frame_trends', {})
            match_count = 0
            for tf, trend in current_frame_trends.items():
                if tf in pattern_frame_trends and pattern_frame_trends.get(tf) == trend:
                    match_count += 1
            if match_count >= 3:
                similarity += 0.20
            total_weight += 0.20

            similarity_percent = (similarity / total_weight * 100) if total_weight > 0 else 0
            if similarity_percent >= LEARNING_CONFIG["similarity_threshold"]:
                similar_patterns.append({
                    'pattern_name': pattern.get('pattern_name', 'نمط غير معروف'),
                    'similarity': round(similarity_percent, 1),
                    'win_rate': pattern_win_rate,
                    'sample_count': pattern.get('sample_count', 0),
                    'description': pattern.get('description', ''),
                    'is_successful': pattern.get('is_successful', False)
                })

        similar_lessons = []
        keywords = ['rsi', 'adx', 'macd', 'trend', 'volume', 'support', 'resistance', 'vwap', 'bollinger', 'super trend', 'false signal', 'vpt', 'stochastic']
        for lesson in lessons[:20]:
            lesson_key_factors = lesson.get('key_factors_str', '') + lesson.get('summary', '')
            match_count = sum(1 for kw in keywords if kw in lesson_key_factors.lower())
            if match_count >= 2:
                similar_lessons.append({
                    'summary': lesson.get('summary', ''),
                    'type': lesson.get('type', 'info'),
                    'details': lesson.get('details', ''),
                    'source': lesson.get('source', 'غير معروف'),
                    'grade': lesson.get('grade', '')
                })

        result["similar_patterns"] = similar_patterns
        result["similar_lessons"] = similar_lessons
        result["has_memory"] = bool(similar_patterns or similar_lessons)

        if similar_patterns:
            avg_win_rate = sum(p['win_rate'] for p in similar_patterns) / len(similar_patterns)
            if avg_win_rate >= 70:
                result["confidence_boost"] = 10
                result["insight"] = f"🧠 تولين تتذكر: هذا الوضع مشابه لـ {len(similar_patterns)} نمط، متوسط نجاحها {avg_win_rate:.0f}%، مما يعزز الثقة."
            elif avg_win_rate >= 50:
                result["confidence_boost"] = 0
                result["insight"] = f"🧠 تولين تتذكر: هذا الوضع مشابه لـ {len(similar_patterns)} نمط، متوسط نجاحها {avg_win_rate:.0f}%، الوضع محايد."
            else:
                result["confidence_boost"] = -10
                result["insight"] = f"🧠 تولين تحذر: هذا الوضع مشابه لـ {len(similar_patterns)} نمط، متوسط نجاحها {avg_win_rate:.0f}%، أنصح بالحذر."
        elif similar_lessons:
            result["insight"] = f"🧠 تولين تتذكر درساً مشابهاً: {similar_lessons[0]['summary'][:80]}..."
            result["confidence_boost"] = -5 if 'خسارة' in similar_lessons[0]['summary'] else 5

        return result

class LessonEngine:
    @staticmethod
    def _calculate_rr(trade: Dict) -> float:
        entry = trade.get('entry_price', 0)
        sl = trade.get('sl_price', 0) or trade.get('sl', 0)
        tp = trade.get('tp_price', 0) or trade.get('tp', 0)
        trade_type = trade.get('trade_type', trade.get('type', 'BUY'))
        if entry <= 0 or sl <= 0 or tp <= 0:
            return 1.0
        if trade_type == 'BUY':
            risk = entry - sl
            reward = tp - entry
        else:
            risk = sl - entry
            reward = entry - tp
        if risk <= 0:
            return 1.0
        return reward / risk

    @staticmethod
    def classify_trade_quality(trade: Dict) -> Dict:
        profit = trade.get('profit_dollars')
        if profit is None:
            profit = 0.0
        is_win = profit > 0
        rr = LessonEngine._calculate_rr(trade)
        duration = trade.get('duration_minutes', 0)
        trade_type = trade.get('trade_type', trade.get('type', 'BUY'))

        entry_analysis = trade.get('full_entry_analysis')
        exit_analysis = trade.get('full_exit_analysis')

        if entry_analysis is None or exit_analysis is None:
            logger.info(f"ℹ️ [LessonEngine] بيانات التحليل الشامل غير كافية للصفقة {trade.get('trade_id', 'unknown')}")
            return {
                'grade': 'insufficient_data',
                'score': 0,
                'reasons': ['⚠️ بيانات التحليل الشامل غير متوفرة لهذه الصفقة'],
                'is_false_signal': False,
                'false_signal_score': 0
            }

        reasons = []
        score = 50
        false_signal_score = 0

        if rr >= 2.0:
            score += 15
            reasons.append(f"🎯 RR ممتاز ({rr:.2f}:1)")
        elif rr >= 1.5:
            score += 8
            reasons.append(f"📊 RR جيد ({rr:.2f}:1)")
        elif rr < 1.0:
            score -= 10
            reasons.append(f"⚠️ RR منخفض ({rr:.2f}:1)")

        timeframes = entry_analysis.get('timeframes', {})
        if timeframes:
            if trade_type == 'BUY':
                bullish_count = sum(1 for tf, data in timeframes.items() if data.get('trend') == 'صاعد')
                if bullish_count >= 3:
                    score += 10
                    reasons.append(f"📈 توافق عالٍ للفريمات ({bullish_count}/4 صاعدة)")
                elif bullish_count <= 1:
                    score -= 8
                    reasons.append(f"⚠️ ضعف توافق الفريمات ({bullish_count}/4 صاعدة)")
            else:
                bearish_count = sum(1 for tf, data in timeframes.items() if data.get('trend') == 'هابط')
                if bearish_count >= 3:
                    score += 10
                    reasons.append(f"📉 توافق عالٍ للفريمات ({bearish_count}/4 هابطة)")
                elif bearish_count <= 1:
                    score -= 8
                    reasons.append(f"⚠️ ضعف توافق الفريمات ({bearish_count}/4 هابطة)")

        entry_score = entry_analysis.get('comprehensive_score', {}).get('score')
        if entry_score is not None:
            if entry_score >= 70:
                score += 10
                reasons.append(f"✅ تقييم دخول قوي ({entry_score:.0f}%)")
            elif entry_score < 45:
                score -= 8
                reasons.append(f"⚠️ تقييم دخول ضعيف ({entry_score:.0f}%)")

        exit_score = exit_analysis.get('comprehensive_score', {}).get('score')
        if entry_score is not None and exit_score is not None:
            if exit_score - entry_score > 10:
                score += 5
                reasons.append("📈 تحسن التقييم الشامل أثناء الصفقة")
            elif entry_score - exit_score > 10:
                score -= 5
                reasons.append("📉 تدهور التقييم الشامل أثناء الصفقة")

        vol_ratio = entry_analysis.get('timeframes', {}).get('15m', {}).get('volume_ratio')
        if vol_ratio is not None:
            if vol_ratio > 1.5:
                score += 5
                reasons.append(f"💪 حجم مرتفع عند الدخول ({vol_ratio:.1f}x)")
            elif vol_ratio < 0.7:
                score -= 5
                reasons.append(f"⚠️ حجم منخفض عند الدخول ({vol_ratio:.1f}x)")

        if duration > 0:
            if 30 <= duration <= 180:
                score += 5
                reasons.append(f"⏱️ مدة مناسبة ({duration} دقيقة)")
            elif duration > 300:
                score -= 3
                reasons.append(f"⏱️ مدة طويلة ({duration} دقيقة)")

        false_signal_result = MemoryEngine().detect_false_signal_pattern(trade)
        if false_signal_result['is_false_signal']:
            false_signal_score = false_signal_result['score']
            for reason in false_signal_result['reasons']:
                reasons.append(f"⚠️ {reason}")
            score -= false_signal_score * 2

        score = max(0, min(100, score))

        if is_win:
            if score >= 80:
                grade = "excellent_win"
            elif score >= 65:
                grade = "good_win"
            else:
                grade = "lucky_win"
        else:
            if score >= 65:
                grade = "excellent_loss"
            elif score >= 45:
                grade = "neutral_loss"
            else:
                grade = "bad_loss"

        return {
            'grade': grade,
            'score': round(score, 1),
            'reasons': reasons,
            'is_false_signal': false_signal_result['is_false_signal'],
            'false_signal_score': false_signal_score
        }

    @staticmethod
    def extract_lessons(trade: Dict) -> List[Dict]:
        profit = trade.get('profit_dollars')
        if profit is None:
            profit = 0.0
        is_win = profit > 0
        quality = LessonEngine.classify_trade_quality(trade)
        grade = quality['grade']
        reasons = quality['reasons']
        is_false_signal = quality.get('is_false_signal', False)

        if grade == 'insufficient_data':
            return [{
                'type': 'info',
                'summary': '⚠️ لا يمكن استخلاص دروس من هذه الصفقة بسبب نقص البيانات.',
                'details': 'التحليل الشامل للدخول أو الخروج غير متوفر.',
                'key_factors': ['بيانات غير كافية'],
                'grade': 'insufficient_data'
            }]

        lessons = []
        main_lesson = {}

        if is_win:
            if grade == 'excellent_win':
                summary = '✅ صفقة رابحة ممتازة! جميع المؤشرات كانت متوافقة.'
                details = 'التقييم الشامل كان قوياً، والفريمات متوافقة، والحجم مرتفع. استمر في تطبيق هذه المعايير.'
            elif grade == 'lucky_win':
                summary = '⚠️ ربح محظوظ! التقييم الشامل كان ضعيفاً.'
                details = 'رغم الربح، كانت المؤشرات ضعيفة. لا تعتمد على الحظ.'
            elif grade == 'good_win':
                summary = '📊 صفقة رابحة بجودة جيدة.'
                details = 'جيدة ولكن هناك مجال للتحسين في معايير الدخول.'
            else:
                summary = '✅ صفقة رابحة.'
                details = f'ربح ${profit:.2f} مع RR {LessonEngine._calculate_rr(trade):.2f}.'
        else:
            if grade == 'excellent_loss':
                summary = '📉 خسارة ممتازة! الاستراتيجية كانت صحيحة ولكن السوق عكس.'
                details = 'جميع المعايير كانت جيدة، لكن السوق تحرك بشكل غير متوقع.'
            elif grade == 'bad_loss':
                summary = '🚨 خسارة سيئة! أخطاء في معايير الدخول.'
                details = 'ضعف الفريمات، تقييم شامل منخفض، وحجم ضعيف. تجنب هذه الظروف.'
            elif grade == 'neutral_loss':
                summary = '📉 خسارة متوسطة.'
                details = f'خسارة ${abs(profit):.2f} مع RR {LessonEngine._calculate_rr(trade):.2f}. راجع معايير الدخول.'
            else:
                summary = '📉 صفقة خاسرة.'
                details = f'خسارة ${abs(profit):.2f} مع RR {LessonEngine._calculate_rr(trade):.2f}.'

        if is_false_signal:
            if not is_win:
                summary += " (تم اكتشاف الإشارة الخادعة)"
                details += "\n\n⚠️ **تم اكتشاف إشارة خادعة!**\nكانت هناك تناقضات بين SuperTrend والمؤشرات الأخرى. تولين تتعلم من هذا الخطأ."
            else:
                summary += " (تم تصنيفها كخادعة لكنها نجحت)"
                details += "\n\nℹ️ **تم تصنيف الإشارة كخادعة لكنها نجحت!**\nهذا يعني أن بعض المؤشرات كانت متضاربة لكن السوق تحرك في اتجاه الصفقة. تولين ستدرس هذا التناقض."

        extra_details = []
        extra_factors = []
        entry_analysis = trade.get('full_entry_analysis')
        exit_analysis = trade.get('full_exit_analysis')

        if entry_analysis and exit_analysis:
            entry_trends = {}
            exit_trends = {}
            for tf in ['5m', '15m', '1h', '4h']:
                entry_trends[tf] = entry_analysis.get('timeframes', {}).get(tf, {}).get('trend', 'محايد')
                exit_trends[tf] = exit_analysis.get('timeframes', {}).get(tf, {}).get('trend', 'محايد')
            
            if not is_win:
                reversed_tfs = [tf for tf in entry_trends if entry_trends.get(tf) != exit_trends.get(tf)]
                if len(reversed_tfs) >= 2:
                    extra_details.append(f"• انعكس اتجاه {len(reversed_tfs)} فريمات أثناء الصفقة ({', '.join(reversed_tfs)})")
                    extra_factors.append('انعكاس الفريمات')
            
            entry_sr = entry_analysis.get('indicators', {}).get('support_resistance', {})
            exit_sr = exit_analysis.get('indicators', {}).get('support_resistance', {})
            if is_win and exit_sr.get('s1', 0) > entry_sr.get('s1', 0):
                extra_details.append("• تحسن مستويات الدعم أثناء الصفقة، مما يؤكد قوة الاتجاه.")
                extra_factors.append('تحسن الدعم')
            
            entry_tf_15m = entry_analysis.get('timeframes', {}).get('15m', {})
            exit_tf_15m = exit_analysis.get('timeframes', {}).get('15m', {})
            entry_rsi = entry_tf_15m.get('rsi')
            exit_rsi = exit_tf_15m.get('rsi')
            if entry_rsi is not None and exit_rsi is not None and abs(exit_rsi - entry_rsi) > 20:
                direction = "ارتفاع" if exit_rsi > entry_rsi else "انخفاض"
                extra_details.append(f"• تغير حاد في RSI: {direction} من {entry_rsi:.0f} إلى {exit_rsi:.0f}")
                extra_factors.append('تغير RSI')

        if extra_details:
            details += "\n\n📌 **معلومات إضافية من التحليل الشامل:**\n" + "\n".join(extra_details)

        all_factors = reasons[:3] + extra_factors[:2]
        if not all_factors:
            all_factors = ['لا توجد عوامل محددة']

        main_lesson = {
            'type': 'success' if is_win else 'warning',
            'summary': summary,
            'details': details,
            'key_factors': all_factors,
            'grade': grade,
            'profit_dollars': round(profit, 2),
            'is_false_signal': is_false_signal
        }
        lessons.append(main_lesson)

        if is_false_signal:
            false_signal_lesson = {
                'type': 'warning' if not is_win else 'info',
                'summary': f"🔍 درس عن الإشارات الخادعة: {'تم اكتشافها بنجاح' if not is_win else 'تناقض غريب'}",
                'details': f"تم اكتشاف إشارة خادعة في هذه الصفقة. {'السوق تحرك بشكل غير متوقع رغم التناقضات.' if is_win else 'تولين ستتذكر هذا النمط لتجنبه مستقبلاً.'}",
                'key_factors': ['false_signal_detection', 'contradiction_analysis'],
                'grade': 'learning',
                'profit_dollars': round(profit, 2)
            }
            lessons.append(false_signal_lesson)

        return lessons

class PatternEngine:
    def __init__(self):
        self.patterns = []
        self._load_patterns()
        self._lock = threading.Lock()

    def _load_patterns(self):
        if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
            try:
                if hasattr(SUPABASE_DB, 'get_patterns'):
                    self.patterns = SUPABASE_DB.get_patterns(None, 200) or []
                    return
            except:
                pass
        self.patterns = load_patterns_from_gist()

    def discover_patterns(self, trades: List[Dict], asset_type: str = None) -> List[Dict]:
        closed_trades = [t for t in trades if t.get('status') == 'closed' and t.get('profit_dollars') is not None]
        if len(closed_trades) < LEARNING_CONFIG["min_samples_for_pattern"]:
            return []

        total_trades = len(closed_trades)
        total_wins = sum(1 for t in closed_trades if t.get('profit_dollars', 0) > 0)
        overall_win_rate = total_wins / total_trades if total_trades > 0 else 0.5

        patterns = []
        groups = defaultdict(list)

        for trade in closed_trades:
            entry_analysis = trade.get('full_entry_analysis')
            if not entry_analysis:
                continue
            tf_15m = entry_analysis.get('timeframes', {}).get('15m', {})
            rsi = tf_15m.get('rsi', 50)
            adx = tf_15m.get('adx', 20)
            trend = tf_15m.get('trend', 'محايد')
            vol_ratio = tf_15m.get('volume_ratio', 1.0)
            trade_type = trade.get('trade_type', trade.get('type', 'BUY'))
            trade_asset = trade.get('asset_type', asset_type or 'unknown')
            vpt = tf_15m.get('vpt', 0)
            stoch = tf_15m.get('stochastic', 50)
            bb_pos = (tf_15m.get('price', 0) - tf_15m.get('bollinger', {}).get('lower', 0)) / (tf_15m.get('bollinger', {}).get('upper', 1) - tf_15m.get('bollinger', {}).get('lower', 1)) if tf_15m.get('bollinger', {}).get('upper', 0) > tf_15m.get('bollinger', {}).get('lower', 0) else 0.5

            rsi_class = "oversold" if rsi < 30 else "overbought" if rsi > 70 else "neutral"
            adx_class = "strong" if adx > 25 else "weak"
            vol_class = "high" if vol_ratio > 1.5 else "normal" if vol_ratio > 0.7 else "low"
            direction = trade_type
            vpt_class = "positive" if vpt > 0 else "negative" if vpt < 0 else "neutral"
            stoch_class = "overbought" if stoch > 80 else "oversold" if stoch < 20 else "neutral"
            bb_class = "upper" if bb_pos > 0.8 else "lower" if bb_pos < 0.2 else "middle"

            key = (trade_asset, direction, trend, rsi_class, adx_class, vol_class, vpt_class, stoch_class, bb_class)
            groups[key].append(trade)

        for key, group in groups.items():
            if len(group) < LEARNING_CONFIG["min_samples_for_pattern"]:
                continue

            asset, direction, trend, rsi_class, adx_class, vol_class, vpt_class, stoch_class, bb_class = key
            wins = [t for t in group if t.get('profit_dollars', 0) > 0]
            win_count = len(wins)
            group_size = len(group)
            confidence = win_count / group_size if group_size > 0 else 0
            support = group_size / total_trades if total_trades > 0 else 0
            lift = confidence / overall_win_rate if overall_win_rate > 0 else 0

            if support < LEARNING_CONFIG["min_support"] or lift < LEARNING_CONFIG["min_lift"]:
                continue

            avg_profit = sum(t.get('profit_dollars', 0) for t in group) / group_size
            is_successful = confidence > overall_win_rate

            false_signal_count = 0
            for trade in group:
                false_result = MemoryEngine().detect_false_signal_pattern(trade)
                if false_result['is_false_signal']:
                    false_signal_count += 1
            false_signal_rate = false_signal_count / group_size if group_size > 0 else 0

            pattern_name = f"{asset}_{direction}_{trend}_{rsi_class}_{adx_class}_{vol_class}_{vpt_class}_{stoch_class}_{bb_class}_{'win' if is_successful else 'loss'}"

            patterns.append({
                'pattern_name': pattern_name[:60],
                'conditions': {
                    'asset_type': asset,
                    'direction': direction,
                    'trend': trend,
                    'rsi_class': rsi_class,
                    'adx_class': adx_class,
                    'vol_class': vol_class,
                    'vpt_class': vpt_class,
                    'stochastic_class': stoch_class,
                    'bb_class': bb_class
                },
                'win_rate': round(confidence * 100, 2),
                'sample_count': group_size,
                'avg_profit': round(avg_profit, 2),
                'support': round(support, 4),
                'lift': round(lift, 2),
                'score': round(confidence * 100 * lift, 2),
                'description': f"نمط {'ناجح' if is_successful else 'فاشل'} لـ {asset} ({direction}) مع {trend} و RSI {rsi_class} و ADX {adx_class} (Support: {support:.1%}, Lift: {lift:.2f})",
                'asset_type': asset,
                'is_successful': is_successful,
                'false_signal_rate': round(false_signal_rate * 100, 2)
            })

        logger.info(f"🔍 تم اكتشاف {len(patterns)} نمطاً جديداً (بعد تصفية Support/Lift)")
        return patterns

    def update_patterns(self, new_trade: Dict, asset_type: str):
        try:
            trades = []
            if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
                trades = SUPABASE_DB.get_trades(asset_type, 200) or []
            elif DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
                trades = DEEP_LEARNING_DB.get_trades_by_asset(asset_type, 200) or []

            if len(trades) < LEARNING_CONFIG["min_samples_for_pattern"]:
                return

            new_patterns = self.discover_patterns(trades, asset_type)
            if not new_patterns:
                return

            with self._lock:
                existing_patterns = []
                if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
                    try:
                        existing_patterns = SUPABASE_DB.get_patterns(asset_type, 200) or []
                    except:
                        pass
                if not existing_patterns:
                    existing_patterns = self.patterns

                existing_dict = {p.get('pattern_name'): p for p in existing_patterns if p.get('pattern_name')}

                updated_patterns = []
                for new_p in new_patterns:
                    name = new_p.get('pattern_name')
                    if name in existing_dict:
                        old = existing_dict[name]
                        old_count = old.get('sample_count', 0)
                        new_count = new_p.get('sample_count', 0)
                        if old_count + new_count > 0:
                            new_win_rate = (old.get('win_rate', 0) * 0.4 + new_p.get('win_rate', 0) * 0.6)
                            new_avg_profit = (old.get('avg_profit', 0) * 0.4 + new_p.get('avg_profit', 0) * 0.6)
                            new_false_signal_rate = (old.get('false_signal_rate', 0) * 0.4 + new_p.get('false_signal_rate', 0) * 0.6)
                            new_p['win_rate'] = round(new_win_rate, 2)
                            new_p['avg_profit'] = round(new_avg_profit, 2)
                            new_p['sample_count'] = old_count + new_count
                            new_p['support'] = (old.get('support', 0) + new_p.get('support', 0)) / 2
                            new_p['lift'] = (old.get('lift', 1.0) + new_p.get('lift', 1.0)) / 2
                            new_p['score'] = new_p['win_rate'] * new_p['lift']
                            new_p['false_signal_rate'] = round(new_false_signal_rate, 2)
                        updated_patterns.append(new_p)
                    else:
                        updated_patterns.append(new_p)

                if updated_patterns:
                    save_patterns(updated_patterns, asset_type, source='pattern_engine')
                    logger.info(f"🔍 [PatternEngine] تم تحديث/إدراج {len(updated_patterns)} نمط لـ {asset_type}")
                    self.patterns = updated_patterns
        except Exception as e:
            logger.error(f"❌ [PatternEngine] فشل تحديث الأنماط: {e}")
            import traceback
            logger.error(traceback.format_exc())

class SnapshotEngine:
    @staticmethod
    def analyze_sequence(snapshots: List[Dict], trade_id: str, asset_type: str, is_win: bool = None) -> List[Dict]:
        if len(snapshots) < LEARNING_CONFIG["snapshot_analysis_min"]:
            return []

        snapshots_sorted = sorted(snapshots, key=lambda x: x.get('timestamp', ''))

        first = snapshots_sorted[0]
        last = snapshots_sorted[-1]

        first_rsi = first.get('rsi', 50)
        last_rsi = last.get('rsi', 50)
        rsi_change = last_rsi - first_rsi

        first_adx = first.get('adx', 15)
        last_adx = last.get('adx', 15)
        adx_change = last_adx - first_adx

        first_vol = first.get('volume_ratio', 1.0)
        last_vol = last.get('volume_ratio', 1.0)
        vol_change = last_vol - first_vol

        first_price = first.get('price', 0)
        last_price = last.get('price', 0)
        price_change_pct = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0

        first_vpt = first.get('vpt', 0)
        last_vpt = last.get('vpt', 0)
        first_stoch = first.get('stochastic', 50)
        last_stoch = last.get('stochastic', 50)
        first_bb_pos = first.get('bb_position', 0.5)
        last_bb_pos = last.get('bb_position', 0.5)

        turning_points = SnapshotEngine._detect_turning_points(snapshots_sorted)

        summary_parts = []
        details_parts = []
        key_factors = []

        if abs(rsi_change) > 20:
            direction = "ارتفاع" if rsi_change > 0 else "انخفاض"
            summary_parts.append(f"تغير حاد في RSI: {direction} {abs(rsi_change):.1f} نقطة")
            details_parts.append(f"• RSI تغير من {first_rsi:.0f} إلى {last_rsi:.0f} ({direction} {abs(rsi_change):.1f} نقطة)")
            key_factors.append('تغير RSI')
        elif abs(rsi_change) > 10:
            direction = "ارتفاع" if rsi_change > 0 else "انخفاض"
            details_parts.append(f"• RSI تغير من {first_rsi:.0f} إلى {last_rsi:.0f} ({direction} {abs(rsi_change):.1f} نقطة)")

        if adx_change > 10:
            summary_parts.append(f"تعزيز قوة الاتجاه (ADX +{adx_change:.1f})")
            details_parts.append(f"• ADX ارتفع من {first_adx:.0f} إلى {last_adx:.0f} (+{adx_change:.1f})")
            key_factors.append('ADX متزايد')
        elif adx_change < -10:
            summary_parts.append(f"ضعف الاتجاه (ADX {adx_change:.1f})")
            details_parts.append(f"• ADX انخفض من {first_adx:.0f} إلى {last_adx:.0f} ({adx_change:.1f})")
            key_factors.append('ADX متناقص')

        if vol_change > 0.5:
            summary_parts.append(f"زيادة ملحوظة في الحجم (+{vol_change:.1f}x)")
            details_parts.append(f"• الحجم ارتفع من {first_vol:.1f}x إلى {last_vol:.1f}x (+{vol_change:.1f}x)")
            key_factors.append('زيادة الحجم')
        elif vol_change < -0.5:
            summary_parts.append(f"انخفاض ملحوظ في الحجم ({vol_change:.1f}x)")
            details_parts.append(f"• الحجم انخفض من {first_vol:.1f}x إلى {last_vol:.1f}x ({vol_change:.1f}x)")
            key_factors.append('انخفاض الحجم')

        if abs(last_vpt - first_vpt) > 1.0:
            direction = "ارتفاع" if last_vpt > first_vpt else "انخفاض"
            summary_parts.append(f"تغير في VPT: {direction} {abs(last_vpt - first_vpt):.2f}")
            details_parts.append(f"• VPT تغير من {first_vpt:.2f} إلى {last_vpt:.2f}")
            key_factors.append('تغير VPT')

        if abs(last_stoch - first_stoch) > 20:
            direction = "ارتفاع" if last_stoch > first_stoch else "انخفاض"
            summary_parts.append(f"تغير حاد في Stochastic: {direction} {abs(last_stoch - first_stoch):.0f} نقطة")
            details_parts.append(f"• Stochastic تغير من {first_stoch:.0f} إلى {last_stoch:.0f}")
            key_factors.append('تغير Stochastic')

        if abs(last_bb_pos - first_bb_pos) > 0.3:
            direction = "ارتفاع" if last_bb_pos > first_bb_pos else "انخفاض"
            summary_parts.append(f"تغير موقع بولينجر: {direction} {abs(last_bb_pos - first_bb_pos):.0%}")
            details_parts.append(f"• بولينجر تغير من {first_bb_pos:.0%} إلى {last_bb_pos:.0%}")
            key_factors.append('تغير بولينجر')

        critical_points = [p for p in turning_points if p.get('severity') == 'high' or p.get('type') == 'trend_reversal']
        for point in critical_points[:2]:
            if point['type'] == 'trend_reversal':
                summary_parts.append(f"انعكاس اتجاه في {point.get('timeframe', 'SuperTrend')}")
                details_parts.append(f"• انعكس الاتجاه من {point.get('from_trend')} إلى {point.get('to_trend')} عند سعر {point.get('price', 0):.2f}")
                key_factors.append('انعكاس الاتجاه')
            elif point['type'] == 'rsi_extreme':
                summary_parts.append(f"RSI وصل إلى منطقة {point.get('zone', 'متطرفة')}")
                details_parts.append(f"• RSI وصل إلى {point.get('rsi', 0):.0f} ({point.get('zone', 'متطرفة')})")
                key_factors.append('RSI متطرف')
            elif point['type'] == 'volume_spike':
                summary_parts.append(f"ارتفاع حاد في الحجم ({point.get('vol_ratio', 0):.1f}x)")
                details_parts.append(f"• ارتفاع حجم التداول إلى {point.get('vol_ratio', 0):.1f}x")
                key_factors.append('ارتفاع الحجم')

        if abs(price_change_pct) > 1.0:
            direction = "ارتفاع" if price_change_pct > 0 else "انخفاض"
            details_parts.append(f"• تغير السعر: {direction} {abs(price_change_pct):.2f}% خلال مسار الصفقة")

        if summary_parts:
            summary = "📊 تحليل مسار الصفقة: " + "، ".join(summary_parts[:3])
            if len(summary_parts) > 3:
                summary += f" و {len(summary_parts)-3} ملاحظات أخرى"
        else:
            summary = "📊 مسار الصفقة مستقر نسبياً دون تغيرات حادة."

        details = "🔍 **تحليل مسار الصفقة من اللقطات:**\n"
        if details_parts:
            details += "\n".join(details_parts)
        else:
            details += "• لا توجد تغيرات ملحوظة في المؤشرات أثناء الصفقة."

        details += f"\n\n📊 **ملخص المؤشرات:**"
        details += f"\n   • RSI: {first_rsi:.0f} → {last_rsi:.0f} ({rsi_change:+.1f})"
        details += f"\n   • ADX: {first_adx:.0f} → {last_adx:.0f} ({adx_change:+.1f})"
        details += f"\n   • الحجم: {first_vol:.1f}x → {last_vol:.1f}x ({vol_change:+.1f}x)"
        details += f"\n   • السعر: ${first_price:.2f} → ${last_price:.2f} ({price_change_pct:+.2f}%)"
        details += f"\n   • VPT: {first_vpt:.2f} → {last_vpt:.2f}"
        details += f"\n   • Stochastic: {first_stoch:.0f} → {last_stoch:.0f}"
        details += f"\n   • بولينجر: {first_bb_pos:.0%} → {last_bb_pos:.0%}"

        if turning_points:
            details += f"\n\n📌 **نقاط التحول المكتشفة ({len(turning_points)}):**"
            for point in turning_points[:3]:
                if point['type'] == 'trend_reversal':
                    details += f"\n   • انعكاس اتجاه في {point.get('timeframe', 'SuperTrend')} عند اللقطة {point.get('index', 0)}"
                elif point['type'] == 'rsi_extreme':
                    details += f"\n   • RSI في منطقة {point.get('zone', 'متطرفة')} عند اللقطة {point.get('index', 0)} (RSI: {point.get('rsi', 0):.0f})"
                elif point['type'] == 'volume_spike':
                    details += f"\n   • ارتفاع حاد في الحجم عند اللقطة {point.get('index', 0)} ({point.get('vol_ratio', 0):.1f}x)"

        if not key_factors:
            key_factors = ['مسار مستقر']
        elif len(key_factors) > 3:
            key_factors = key_factors[:3]

        if is_win is not None:
            lesson_type = 'success' if is_win else 'warning'
        else:
            lesson_type = 'info'

        return [{
            'type': lesson_type,
            'summary': summary,
            'details': details,
            'key_factors': key_factors
        }]

    @staticmethod
    def _detect_turning_points(snapshots: List[Dict]) -> List[Dict]:
        if len(snapshots) < 4:
            return []

        turning_points = []
        prices = [s.get('price', 0) for s in snapshots]
        rsi_values = [s.get('rsi', 50) for s in snapshots]
        vol_ratios = [s.get('volume_ratio', 1.0) for s in snapshots]
        st_trends = [s.get('st_trend', 'صاعد') for s in snapshots]
        stoch_values = [s.get('stochastic', 50) for s in snapshots]
        vpt_values = [s.get('vpt', 0) for s in snapshots]

        min_len = min(len(prices), len(st_trends))
        st_trends = st_trends[:min_len]
        prices = prices[:min_len]

        for i in range(1, len(st_trends)):
            if st_trends[i] != st_trends[i-1]:
                turning_points.append({
                    'type': 'trend_reversal',
                    'index': i,
                    'timeframe': 'SuperTrend',
                    'from_trend': st_trends[i-1],
                    'to_trend': st_trends[i],
                    'price': prices[i] if i < len(prices) else 0,
                    'severity': 'high' if i > 2 else 'medium'
                })

        for i, rsi in enumerate(rsi_values):
            if i >= len(prices):
                break
            if rsi > 75:
                turning_points.append({
                    'type': 'rsi_extreme',
                    'index': i,
                    'zone': 'ذروة شراء',
                    'rsi': rsi,
                    'price': prices[i] if i < len(prices) else 0
                })
            elif rsi < 25:
                turning_points.append({
                    'type': 'rsi_extreme',
                    'index': i,
                    'zone': 'ذروة بيع',
                    'rsi': rsi,
                    'price': prices[i] if i < len(prices) else 0
                })

        for i, stoch in enumerate(stoch_values):
            if i >= len(prices):
                break
            if stoch > 80:
                turning_points.append({
                    'type': 'stoch_extreme',
                    'index': i,
                    'zone': 'ذروة شراء',
                    'stoch': stoch,
                    'price': prices[i] if i < len(prices) else 0
                })
            elif stoch < 20:
                turning_points.append({
                    'type': 'stoch_extreme',
                    'index': i,
                    'zone': 'ذروة بيع',
                    'stoch': stoch,
                    'price': prices[i] if i < len(prices) else 0
                })

        for i, vpt in enumerate(vpt_values):
            if i < 2 or i >= len(prices):
                continue
            if vpt > 0 and vpt_values[i-1] <= 0:
                turning_points.append({
                    'type': 'vpt_cross',
                    'index': i,
                    'direction': 'صاعد',
                    'vpt': vpt,
                    'price': prices[i] if i < len(prices) else 0
                })
            elif vpt < 0 and vpt_values[i-1] >= 0:
                turning_points.append({
                    'type': 'vpt_cross',
                    'index': i,
                    'direction': 'هابط',
                    'vpt': vpt,
                    'price': prices[i] if i < len(prices) else 0
                })

        if len(vol_ratios) >= 3:
            for i in range(2, len(vol_ratios)):
                if i >= len(prices):
                    break
                if vol_ratios[i] > vol_ratios[i-1] * 1.8 and vol_ratios[i] > 1.5:
                    turning_points.append({
                        'type': 'volume_spike',
                        'index': i,
                        'vol_ratio': vol_ratios[i],
                        'price': prices[i] if i < len(prices) else 0
                    })

        return turning_points

class LearningOrchestrator:
    def __init__(self):
        self.memory_engine = MemoryEngine()
        self.lesson_engine = LessonEngine()
        self.pattern_engine = PatternEngine()
        self.snapshot_engine = SnapshotEngine()
        self._last_prune = time.time()
        self._trade_counter = 0
        self._prediction_counter = 0
        self._counter_lock = threading.Lock()
        self._calibration_weights = self._load_calibration_weights()
        logger.info("🧠 LearningOrchestrator جاهز (متكامل مع جميع المؤشرات والفريمات)")

    def _load_calibration_weights(self) -> Dict:
        try:
            weights_file = "learning_data/calibration_weights.json"
            if os.path.exists(weights_file):
                with open(weights_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ فشل تحميل أوزان المعايرة: {e}")
        return {
            'frames': 0.35,
            'trend_alignment': 0.15,
            'adx': 0.15,
            'rsi': 0.10,
            'macd': 0.10,
            'volume': 0.08,
            'rr': 0.07
        }

    def _save_calibration_weights(self):
        try:
            os.makedirs("learning_data", exist_ok=True)
            weights_file = "learning_data/calibration_weights.json"
            with open(weights_file, 'w', encoding='utf-8') as f:
                json.dump(self._calibration_weights, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ فشل حفظ أوزان المعايرة: {e}")

    def process_trade(self, trade: Dict, asset_type: str, silent: bool = False, source: str = 'trade_analysis') -> bool:
        trade_id = trade.get('trade_id', 'unknown')
        if not trade_id or trade_id == 'unknown':
            logger.warning(f"⚠️ [Orchestrator] trade_id غير صالح: {trade_id}")
            return False

        if trade.get('status') != 'closed':
            logger.info(f"⏭️ [Orchestrator] الصفقة {trade_id} ليست مغلقة (status={trade.get('status')})، تخطي")
            return False

        profit = trade.get('profit_dollars')
        if profit is None:
            profit = 0.0

        logger.info(f"🧠 [Orchestrator] معالجة الصفقة {trade_id} للتعلم (silent={silent}, source={source})")

        with self._counter_lock:
            self._trade_counter += 1
            counter = self._trade_counter
            self._prediction_counter += 1

        new_lessons_count = 0

        lessons = self.lesson_engine.extract_lessons(trade)
        if lessons:
            saved, new_count = save_lessons(lessons, asset_type, trade_id, source=source)
            if saved and new_count > 0:
                new_lessons_count += new_count
                logger.info(f"✅ [Orchestrator] تم حفظ {new_count} درس من التحليل الشامل للصفقة {trade_id}")
                self.memory_engine.invalidate_cache()

        snapshots = self._get_snapshots_for_trade(trade_id, asset_type, limit=30)
        if snapshots and len(snapshots) >= LEARNING_CONFIG["snapshot_analysis_min"]:
            is_win = profit > 0
            snapshot_lessons = self.snapshot_engine.analyze_sequence(snapshots, trade_id, asset_type, is_win=is_win)
            if snapshot_lessons:
                saved, new_count = save_lessons(snapshot_lessons, asset_type, trade_id, source='snapshot_analysis')
                if saved and new_count > 0:
                    new_lessons_count += new_count
                    logger.info(f"✅ [Orchestrator] تم حفظ {new_count} درس من اللقطات للصفقة {trade_id}")
                    self.memory_engine.invalidate_cache()

        try:
            self.memory_engine.update_weights(trade)
        except Exception as e:
            logger.error(f"❌ [Orchestrator] فشل تحديث أوزان التعلم: {e}")

        try:
            self.pattern_engine.update_patterns(trade, asset_type)
        except Exception as e:
            logger.error(f"❌ [Orchestrator] فشل تحديث الأنماط: {e}")

        prediction_analysis = self._analyze_prediction_errors(trade_id, asset_type, trade)
        if prediction_analysis and prediction_analysis.get('lessons'):
            saved, new_count = save_lessons(prediction_analysis['lessons'], asset_type, trade_id, source='prediction_analysis')
            if saved and new_count > 0:
                new_lessons_count += new_count
                logger.info(f"✅ [Orchestrator] تم حفظ {new_count} درس من تحليل التوقعات للصفقة {trade_id}")
                self.memory_engine.invalidate_cache()

        if self._prediction_counter % LEARNING_CONFIG["prediction_calibration_interval"] == 0:
            try:
                self._update_prediction_calibration()
                logger.info(f"📊 تم تحديث معايرة التوقعات (بعد {self._prediction_counter} توقع)")
            except Exception as e:
                logger.warning(f"⚠️ فشل تحديث معايرة التوقعات: {e}")

        now = time.time()
        if now - self._last_prune > 3600:
            self._prune_memory()
            self._last_prune = now

        if new_lessons_count > 0 and not silent:
            summary = "🧠 **تولين تعلمت دروساً جديدة:**\n\n"
            if lessons:
                summary += f"📌 {lessons[0].get('summary', '')}\n"
                details = lessons[0].get('details', '')
                if details:
                    short_details = details[:200] + "..." if len(details) > 200 else details
                    summary += f"   • {short_details}\n"
            queue_telegram_message(summary)

        return new_lessons_count > 0

    def _get_snapshots_for_trade(self, trade_id: str, asset_type: str, limit: int = 30) -> List[Dict]:
        snapshots = []
        if SUPABASE_AVAILABLE and SUPABASE_DB and SUPABASE_DB.connected:
            try:
                if hasattr(SUPABASE_DB, 'get_snapshots'):
                    snapshots = SUPABASE_DB.get_snapshots(trade_id, limit=limit)
                    if snapshots:
                        logger.info(f"📸 جلب {len(snapshots)} لقطة من Supabase للصفقة {trade_id}")
                        return snapshots
                else:
                    if DEEP_LEARNING_AVAILABLE and DEEP_LEARNING_DB:
                        snapshots = DEEP_LEARNING_DB.get_snapshots(trade_id, limit=limit)
                        if snapshots:
                            logger.info(f"📸 جلب {len(snapshots)} لقطة من SQLite للصفقة {trade_id}")
                            return snapshots
            except Exception as e:
                logger.warning(f"⚠️ فشل جلب اللقطات من Supabase: {e}")
        try:
            backup_file = f"learning_data/backups/snapshots_{asset_type}.json"
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                    all_snapshots = backup_data.get('snapshots', [])
                    snapshots = [s for s in all_snapshots if s.get('trade_id') == trade_id][-limit:]
                    if snapshots:
                        logger.info(f"📸 جلب {len(snapshots)} لقطة من الملف المحلي للصفقة {trade_id}")
                        return snapshots
        except Exception as e:
            logger.warning(f"⚠️ فشل جلب اللقطات من الملف المحلي: {e}")
        return snapshots

    def _analyze_prediction_errors(self, trade_id: str, asset_type: str, trade: Dict) -> Dict:
        result = {"lessons": [], "reasons": []}
        
        try:
            if not SUPABASE_AVAILABLE or not SUPABASE_DB:
                return result
            
            client = SUPABASE_DB.supabase if hasattr(SUPABASE_DB, 'supabase') else None
            if client is None:
                return result
            
            response = client.table(TABLE_TRADE_PREDICTIONS).select('*').eq('trade_id', trade_id).execute()
            if not response or not response.data:
                logger.info(f"ℹ️ لا يوجد توقع مسجل للصفقة {trade_id}")
                return result
            
            prediction = response.data[0]
            predicted_outcome = prediction.get('predicted_outcome')
            actual_outcome = prediction.get('actual_outcome')
            
            if predicted_outcome == actual_outcome:
                logger.info(f"✅ التوقع للصفقة {trade_id} كان صحيحاً ({predicted_outcome})")
                return result
            
            logger.info(f"🧠 تحليل توقع خاطئ للصفقة {trade_id}: توقع {predicted_outcome}، فعلي {actual_outcome}")
            
            entry_analysis = trade.get('full_entry_analysis', {})
            if not entry_analysis:
                return result
            
            indicators = entry_analysis.get('indicators', {})
            momentum = indicators.get('momentum', {})
            trend_data = indicators.get('trend', {})
            volume = indicators.get('volume', {})
            timeframes = entry_analysis.get('timeframes', {})
            
            reasons = []
            lessons = []
            
            rsi = momentum.get('rsi')
            if rsi is not None:
                if predicted_outcome == 'win' and actual_outcome == 'loss':
                    if trade.get('trade_type', 'BUY') == 'BUY' and rsi > 70:
                        reasons.append(f"RSI مرتفع ({rsi:.0f}) لم يؤخذ في الاعتبار بشكل كافٍ")
                        lessons.append("⚠️ تجنب الشراء عندما يكون RSI > 70 حتى لو كانت الإشارة قوية.")
                    elif trade.get('trade_type', 'BUY') == 'SELL' and rsi < 30:
                        reasons.append(f"RSI منخفض ({rsi:.0f}) لم يؤخذ في الاعتبار بشكل كافٍ")
                        lessons.append("⚠️ تجنب البيع عندما يكون RSI < 30 حتى لو كانت الإشارة قوية.")
            
            adx = trend_data.get('adx')
            if adx is not None and adx < 20:
                reasons.append(f"ADX ضعيف ({adx:.0f}) - السوق كان عرضياً")
                lessons.append("⚠️ تأكد من ADX > 20 قبل الدخول في صفقة.")
            
            vol_ratio = volume.get('ratio')
            if vol_ratio is not None and vol_ratio < 0.7:
                reasons.append(f"حجم تداول منخفض ({vol_ratio:.1f}x)")
                lessons.append("⚠️ انتظر حتى يرتفع حجم التداول قبل الدخول.")
            
            # تحليل تناقض الفريمات
            bullish_count = sum(1 for tf in timeframes.values() if tf.get('trend') == 'صاعد')
            bearish_count = sum(1 for tf in timeframes.values() if tf.get('trend') == 'هابط')
            trade_type = trade.get('trade_type', 'BUY')
            if trade_type == 'BUY' and bearish_count >= 3:
                reasons.append(f"{bearish_count}/4 فريمات هابطة ضد الشراء")
                lessons.append("⚠️ تجنب الشراء عندما تكون 3 فريمات أو أكثر هابطة.")
            elif trade_type == 'SELL' and bullish_count >= 3:
                reasons.append(f"{bullish_count}/4 فريمات صاعدة ضد البيع")
                lessons.append("⚠️ تجنب البيع عندما تكون 3 فريمات أو أكثر صاعدة.")
            
            if reasons:
                summary = f"🔍 درس من توقع خاطئ لصفقة {asset_type}"
                details = f"توقع البوت: {predicted_outcome}، النتيجة الفعلية: {actual_outcome}\n\n"
                details += "الأسباب:\n• " + "\n• ".join(reasons)
                lessons.append({
                    'type': 'warning',
                    'summary': summary,
                    'details': details,
                    'key_factors': ['prediction_error'] + reasons[:2],
                    'grade': 'learning',
                    'profit_dollars': trade.get('profit_dollars', 0)
                })
            
            result['lessons'] = lessons
            result['reasons'] = reasons
            
        except Exception as e:
            logger.error(f"❌ فشل تحليل أخطاء التوقع: {e}")
        
        return result

    def _update_prediction_calibration(self):
        try:
            if 'update_prediction_calibration' in globals():
                update_prediction_calibration()
                logger.info("✅ تم تحديث معايرة التوقعات عبر PART 24")
            else:
                logger.warning("⚠️ دالة update_prediction_calibration غير متوفرة")
        except Exception as e:
            logger.error(f"❌ فشل تحديث معايرة التوقعات: {e}")

    def _prune_memory(self):
        try:
            if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
                return
            client = _get_supabase_client()
            if not client:
                return
            cutoff = datetime.now() - timedelta(days=LEARNING_CONFIG["prune_threshold_days"])
            cutoff_str = cutoff.isoformat()

            try:
                old_lessons = client.table(TABLE_LESSONS_DEEP).select('id').lt('created_at', cutoff_str).execute()
                if old_lessons and hasattr(old_lessons, 'data') and old_lessons.data:
                    ids = [item['id'] for item in old_lessons.data if item.get('id')]
                    if ids:
                        for i in range(0, len(ids), 50):
                            batch = ids[i:i+50]
                            client.table(TABLE_LESSONS_DEEP).delete().in_('id', batch).execute()
                        logger.info(f"🗑️ [Prune] تم حذف {len(ids)} درساً قديماً")
            except Exception as e:
                logger.error(f"❌ [Prune] فشل ترشيح الدروس: {e}")

            try:
                old_patterns = client.table(TABLE_DISCOVERED_PATTERNS).select('id, sample_count, created_at').execute()
                if old_patterns and hasattr(old_patterns, 'data') and old_patterns.data:
                    ids = []
                    for item in old_patterns.data:
                        created_at = item.get('created_at', '')
                        sample_count = item.get('sample_count', 0)
                        if created_at and created_at < cutoff_str:
                            ids.append(item['id'])
                        elif sample_count < 3:
                            ids.append(item['id'])
                    if ids:
                        for i in range(0, len(ids), 50):
                            batch = ids[i:i+50]
                            client.table(TABLE_DISCOVERED_PATTERNS).delete().in_('id', batch).execute()
                        logger.info(f"🗑️ [Prune] تم حذف {len(ids)} نمطاً قديماً/ضعيفاً")
            except Exception as e:
                logger.error(f"❌ [Prune] فشل ترشيح الأنماط: {e}")

            self.memory_engine.invalidate_cache()
        except Exception as e:
            logger.error(f"❌ [Prune] فشل الترشيح: {e}")

LEARNING_ORCHESTRATOR = None

def init_learning_orchestrator():
    global LEARNING_ORCHESTRATOR
    if LEARNING_ORCHESTRATOR is None:
        LEARNING_ORCHESTRATOR = LearningOrchestrator()
        logger.info("🧠 LearningOrchestrator تم تهيئته بنجاح")
        
        global DREAM
        if DREAM_AVAILABLE and DREAM:
            try:
                DREAM.memory_engine = LEARNING_ORCHESTRATOR.memory_engine
                DREAM.learning_orchestrator = LEARNING_ORCHESTRATOR
                logger.info("🌙 Dream Engine متصل بـ MemoryEngine و LearningOrchestrator")
            except Exception as e:
                logger.warning(f"⚠️ فشل ربط Dream Engine: {e}")
        
        try:
            logger.info("🔍 [init_learning_orchestrator] بدء اكتشاف الأنماط من البيانات المخزنة...")
            discover_func = globals().get('discover_patterns_from_trades')
            if discover_func is None:
                logger.error("❌ [init_learning_orchestrator] discover_patterns_from_trades غير موجودة في النطاق العام!")
            else:
                for asset in ["oil", "silver"]:
                    logger.info(f"🔍 [init_learning_orchestrator] جاري اكتشاف الأنماط لـ {asset}...")
                    discover_func(asset)
                logger.info("✅ [init_learning_orchestrator] تم الانتهاء من اكتشاف الأنماط من البيانات المخزنة")
        except Exception as e:
            logger.error(f"❌ [init_learning_orchestrator] فشل اكتشاف الأنماط الأولي: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    return LEARNING_ORCHESTRATOR

init_learning_orchestrator()

def process_trade_for_learning(trade: Dict, asset_type: str, silent: bool = False, source: str = 'trade_analysis') -> bool:
    if LEARNING_ORCHESTRATOR is None:
        logger.error("❌ LEARNING_ORCHESTRATOR غير معرف!")
        return False
    logger.info(f"🧠 process_trade_for_learning: تم استدعاؤها للصفقة {trade.get('trade_id')}")
    result = LEARNING_ORCHESTRATOR.process_trade(trade, asset_type, silent, source)
    logger.info(f"🧠 process_trade_for_learning: النتيجة لـ {trade.get('trade_id')} = {result}")
    return result

def classify_trade_quality_from_full_analysis(trade: Dict) -> Dict:
    return LessonEngine.classify_trade_quality(trade)

def extract_lessons_from_full_analysis(trade: Dict) -> List[Dict]:
    return LessonEngine.extract_lessons(trade)

def _update_calibration():
    try:
        if not SUPABASE_AVAILABLE or not SUPABASE_DB or not SUPABASE_DB.connected:
            return
        
        client = _get_supabase_client()
        if not client:
            return
        
        response = client.table(TABLE_TRADE_PREDICTIONS).select('confidence', 'was_correct').not_.is_('actual_outcome', 'null').execute()
        if not response or not response.data:
            return
        
        records = response.data
        if len(records) < 20:
            return
        
        buckets = {}
        for record in records:
            conf = record.get('confidence', 50)
            bucket = (conf // 10) * 10
            if bucket < 40:
                bucket = 40
            if bucket > 80:
                bucket = 80
            key = str(bucket)
            if key not in buckets:
                buckets[key] = {'total': 0, 'correct': 0}
            buckets[key]['total'] += 1
            if record.get('was_correct', False):
                buckets[key]['correct'] += 1
        
        factors = {}
        for bucket, data in buckets.items():
            if data['total'] >= 5:
                actual_accuracy = data['correct'] / data['total']
                expected_accuracy = int(bucket) / 100.0
                if expected_accuracy > 0:
                    factor = actual_accuracy / expected_accuracy
                    factors[bucket] = max(0.5, min(1.5, factor))
        
        if factors:
            calibration_file = "learning_data/calibration_factors.json"
            try:
                os.makedirs("learning_data", exist_ok=True)
                with open(calibration_file, 'w', encoding='utf-8') as f:
                    json.dump({'factors': factors, 'last_update': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
                logger.info(f"📊 تم تحديث معايرة الثقة: {factors}")
            except Exception as e:
                logger.warning(f"⚠️ فشل حفظ عوامل المعايرة: {e}")
                
    except Exception as e:
        logger.warning(f"⚠️ فشل تحديث المعايرة: {e}")

def get_detailed_learning_report(asset_type: Optional[str] = None) -> str:
    lines = []
    lines.append("🧠 **تقرير التعلم المتقدم**")
    lines.append("━" * 40)
    lines.append("")
    memory = LEARNING_ORCHESTRATOR.memory_engine.get_memory(asset_type) if LEARNING_ORCHESTRATOR else {"lessons": [], "patterns": []}
    lessons = memory.get('lessons', [])
    patterns = memory.get('patterns', [])
    lines.append(f"📚 **عدد الدروس:** {len(lessons)}")
    lines.append(f"🔍 **عدد الأنماط:** {len(patterns)}")
    lines.append("")
    
    if patterns:
        successful = sum(1 for p in patterns if p.get('is_successful', False))
        false_signal_patterns = [p for p in patterns if p.get('false_signal_rate', 0) > 30]
        lines.append(f"📈 **الأنماط الناجحة:** {successful} من {len(patterns)}")
        if false_signal_patterns:
            lines.append(f"⚠️ **أنماط الإشارات الخادعة (>30%):** {len(false_signal_patterns)}")
        lines.append("")
    
    if lessons:
        types = defaultdict(int)
        sources = defaultdict(int)
        for lesson in lessons:
            types[lesson.get('type', 'unknown')] += 1
            sources[lesson.get('source', 'unknown')] += 1
        lines.append("📊 **توزيع الدروس حسب النوع:**")
        for t, count in types.items():
            emoji = {'success': '✅', 'warning': '⚠️', 'critical': '🚨', 'info': 'ℹ️'}.get(t, '📌')
            lines.append(f"   {emoji} {t}: {count}")
        lines.append("")
        lines.append("📊 **توزيع الدروس حسب المصدر:**")
        for src, count in sources.items():
            lines.append(f"   • {src}: {count}")
        lines.append("")
    
    if patterns:
        sorted_patterns = sorted(patterns, key=lambda x: x.get('win_rate', 0), reverse=True)[:5]
        lines.append("🏆 **أفضل 5 أنماط من حيث نسبة النجاح:**")
        for i, p in enumerate(sorted_patterns, 1):
            false_rate = p.get('false_signal_rate', 0)
            false_indicator = f" (خداع: {false_rate:.0f}%)" if false_rate > 20 else ""
            lines.append(f"   {i}. {p.get('pattern_name', '')} – نجاح {p.get('win_rate', 0):.1f}% ({p.get('sample_count', 0)} عينة){false_indicator}")
        lines.append("")
    
    if LEARNING_ORCHESTRATOR:
        weights = LEARNING_ORCHESTRATOR.memory_engine._learning_weights
        lines.append("📊 **أوزان التعلم الحالية:**")
        for key, value in weights.items():
            lines.append(f"   • {key}: {value:.3f}")
        lines.append("")
        cache_age = time.time() - LEARNING_ORCHESTRATOR.memory_engine._cache["last_update"]
        lines.append(f"⏱️ **عمر كاش الذاكرة:** {cache_age:.0f} ثانية")
        lines.append("")
    
    lines.append("━" * 40)
    lines.append("💙 تولين: ذاكرتي تتوسع مع كل صفقة، وأصبحت أكثر دقة.")
    return "\n".join(lines)
   
# ============================================================================
# نهاية PART 30
# ====================================================================================
       
# ============================================================================
# V13.2 INTELLIGENCE LAYER
# Strategy scanner is intentionally NOT modified.
# This layer improves accounting, snapshots, technical context, learning,
# calibration, pattern statistics, regime awareness, and explainability.
# ============================================================================

V13_VERSION = "13.2.0"
V13_DATA_DIR = os.path.join("learning_data", "v13")
V13_KNOWLEDGE_FILE = os.path.join(V13_DATA_DIR, "knowledge.json")
V13_LOCK = threading.RLock()
V13_SCHEMA = 2
V13_PATTERN_MIN_SAMPLES = 8
V13_CALIBRATION_MIN_SAMPLES = 12


def _v13_now():
    return datetime.now().isoformat(timespec="seconds")


def _v13_safe_float(value):
    try:
        if value is None or isinstance(value, bool):
            return None
        x = float(value)
        if math.isfinite(x):
            return x
    except Exception:
        pass
    return None


def _v13_atomic_write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _v13_load_knowledge():
    with V13_LOCK:
        if not os.path.exists(V13_KNOWLEDGE_FILE):
            return {
                "schema": V13_SCHEMA,
                "version": 1,
                "created_at": _v13_now(),
                "updated_at": _v13_now(),
                "patterns": {},
                "calibration": {},
                "regimes": {},
                "errors": {},
                "stats": {"closed": 0, "wins": 0, "losses": 0},
            }
        try:
            with open(V13_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("invalid knowledge root")
            data.setdefault("schema", V13_SCHEMA)
            data.setdefault("version", 1)
            data.setdefault("patterns", {})
            data.setdefault("calibration", {})
            data.setdefault("regimes", {})
            data.setdefault("errors", {})
            data.setdefault("stats", {"closed": 0, "wins": 0, "losses": 0})
            return data
        except Exception as e:
            logger.error(f"[V13] فشل قراءة المعرفة: {e}")
            return {
                "schema": V13_SCHEMA, "version": 1, "created_at": _v13_now(),
                "updated_at": _v13_now(), "patterns": {}, "calibration": {},
                "regimes": {}, "errors": {}, "stats": {"closed": 0, "wins": 0, "losses": 0}
            }


def _v13_save_knowledge(data):
    data["updated_at"] = _v13_now()
    data["version"] = int(data.get("version", 0)) + 1
    try:
        _v13_atomic_write(V13_KNOWLEDGE_FILE, data)
    except Exception as e:
        logger.error(f"[V13] فشل حفظ المعرفة: {e}")


def _v13_direction(trade):
    return str(trade.get("type", trade.get("trade_type", "BUY"))).upper()


def _v13_extract_context(analysis, asset, trade=None):
    analysis = analysis if isinstance(analysis, dict) else {}
    tfs = analysis.get("timeframes") if isinstance(analysis.get("timeframes"), dict) else {}
    tf15 = tfs.get("15m") if isinstance(tfs.get("15m"), dict) else {}
    tf1h = tfs.get("1h") if isinstance(tfs.get("1h"), dict) else {}
    st = analysis.get("supertrend") if isinstance(analysis.get("supertrend"), dict) else {}
    comp = analysis.get("comprehensive_score") if isinstance(analysis.get("comprehensive_score"), dict) else {}
    indicators = analysis.get("indicators") if isinstance(analysis.get("indicators"), dict) else {}
    sr = indicators.get("support_resistance") if isinstance(indicators.get("support_resistance"), dict) else {}
    price = _v13_safe_float(analysis.get("price"))
    atr = _v13_safe_float(tf15.get("atr"))
    atr_pct = (atr / price * 100.0) if atr is not None and price else None
    adx = _v13_safe_float(tf15.get("adx"))
    rsi = _v13_safe_float(tf15.get("rsi"))
    vol = _v13_safe_float(tf15.get("volume_ratio"))
    score = _v13_safe_float(comp.get("score"))
    trend15 = tf15.get("trend")
    trend1h = tf1h.get("trend")
    st_trend = st.get("trend")
    if adx is None:
        regime = "unknown"
    elif adx >= 30:
        regime = "trending"
    elif adx <= 18:
        regime = "ranging"
    else:
        regime = "transition"
    if atr_pct is not None and atr_pct >= 2.5:
        volatility = "high"
    elif atr_pct is not None and atr_pct <= 0.5:
        volatility = "low"
    else:
        volatility = "normal"
    return {
        "asset": asset,
        "direction": _v13_direction(trade) if trade else None,
        "price": price,
        "rsi": rsi,
        "adx": adx,
        "volume_ratio": vol,
        "atr_pct": atr_pct,
        "trend_15m": trend15,
        "trend_1h": trend1h,
        "supertrend": st_trend,
        "score": score,
        "regime": regime,
        "volatility": volatility,
        "support": _v13_safe_float(sr.get("s1")),
        "resistance": _v13_safe_float(sr.get("r1")),
    }


def _v13_snapshot(phase, asset, trade, analysis, extra=None):
    ctx = _v13_extract_context(analysis, asset, trade)
    snap = {
        "schema": V13_SCHEMA,
        "v13_version": V13_VERSION,
        "snapshot_id": f"{trade.get('trade_id','unknown')}_{phase}_{int(time.time()*1000)}",
        "trade_id": trade.get("trade_id"),
        "asset": asset,
        "phase": phase,
        "timestamp": _v13_now(),
        "strategy_locked": True,
        "strategy_engine": "SuperTrend/VPT-original",
        "context": ctx,
        "technical_analysis": analysis if isinstance(analysis, dict) else {},
    }
    if extra:
        snap["metrics"] = extra
    return snap


def _v13_snapshot_file(trade_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(trade_id))
    return os.path.join(V13_DATA_DIR, "snapshots", safe + ".json")


def _v13_append_snapshot(snapshot):
    path = _v13_snapshot_file(snapshot.get("trade_id"))
    with V13_LOCK:
        try:
            existing = []
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                if not isinstance(existing, list):
                    existing = []
            existing.append(snapshot)
            # Keep the full research history locally, but cap a single trade safely.
            existing = existing[-1000:]
            _v13_atomic_write(path, existing)
            return True
        except Exception as e:
            logger.error(f"[V13] فشل حفظ snapshot: {e}")
            return False


def _v13_load_snapshots(trade_id):
    path = _v13_snapshot_file(trade_id)
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        logger.warning(f"[V13] تعذر قراءة snapshots: {e}")
    return []


def _v13_price_extremes(snapshots, entry, side):
    prices = []
    for s in snapshots:
        p = _v13_safe_float((s.get("context") or {}).get("price"))
        if p is not None:
            prices.append(p)
    if not prices or entry is None or entry <= 0:
        return {"mae_pct": None, "mfe_pct": None}
    if side == "BUY":
        adverse = min((p - entry) / entry * 100 for p in prices)
        favorable = max((p - entry) / entry * 100 for p in prices)
    else:
        adverse = max((entry - p) / entry * 100 for p in prices)
        favorable = max((entry - p) / entry * 100 for p in prices)
    return {"mae_pct": abs(min(adverse, 0.0)), "mfe_pct": max(favorable, 0.0)}


def _v13_pattern_key(asset, side, ctx):
    return "|".join([
        str(asset), str(side), str(ctx.get("regime", "unknown")),
        str(ctx.get("volatility", "unknown")),
        str(ctx.get("trend_15m", "unknown")), str(ctx.get("trend_1h", "unknown")),
        str(ctx.get("supertrend", "unknown")),
    ])


def _v13_update_pattern(data, key, win, pnl_pct, ctx):
    p = data["patterns"].setdefault(key, {
        "samples": 0, "wins": 0, "losses": 0, "pnl_sum": 0.0,
        "pnl_sq_sum": 0.0, "first_seen": _v13_now(), "last_seen": _v13_now(),
        "regime": ctx.get("regime"), "volatility": ctx.get("volatility")
    })
    p["samples"] += 1
    p["wins"] += int(win)
    p["losses"] += int(not win)
    if pnl_pct is not None:
        p["pnl_sum"] += pnl_pct
        p["pnl_sq_sum"] += pnl_pct * pnl_pct
    p["last_seen"] = _v13_now()


def _v13_pattern_confidence(p):
    n = int(p.get("samples", 0))
    if n <= 0:
        return 0.0
    wr = p.get("wins", 0) / n
    # Conservative evidence: shrinks extreme win rates toward 50% until sample size grows.
    evidence = min(1.0, n / 50.0)
    return 50.0 + (wr - 0.5) * 100.0 * evidence


def _v13_calibration_update(data, predicted):
    if predicted is None:
        return
    bucket = min(95, max(5, int(round(predicted / 10.0) * 10)))
    data["calibration"].setdefault(str(bucket), {"n": 0, "correct": 0})
    return bucket


def _v13_record_closed_trade(trade, asset, snapshots, exit_analysis=None):
    entry = _v13_safe_float(trade.get("entry_price"))
    exit_price = _v13_safe_float(trade.get("exit_price"))
    pnl = _v13_safe_float(trade.get("profit_dollars"))
    side = _v13_direction(trade)
    if entry and exit_price:
        pnl_pct = ((exit_price - entry) / entry * 100.0) if side == "BUY" else ((entry - exit_price) / entry * 100.0)
    else:
        pnl_pct = None
    win = pnl is not None and pnl > 0
    first = next((s for s in snapshots if s.get("phase") == "entry"), None)
    ctx = (first or {}).get("context", {})
    extremes = _v13_price_extremes(snapshots, entry, side)
    data = _v13_load_knowledge()
    data["stats"]["closed"] = int(data["stats"].get("closed", 0)) + 1
    data["stats"]["wins"] = int(data["stats"].get("wins", 0)) + int(win)
    data["stats"]["losses"] = int(data["stats"].get("losses", 0)) + int(not win)
    key = _v13_pattern_key(asset, side, ctx)
    _v13_update_pattern(data, key, win, pnl_pct, ctx)
    regime = str(ctx.get("regime", "unknown"))
    rg = data["regimes"].setdefault(regime, {"samples": 0, "wins": 0, "losses": 0, "pnl_sum": 0.0})
    rg["samples"] += 1
    rg["wins"] += int(win)
    rg["losses"] += int(not win)
    if pnl_pct is not None:
        rg["pnl_sum"] += pnl_pct
    predicted = _v13_safe_float(trade.get("prediction_confidence"))
    bucket = _v13_calibration_update(data, predicted)
    if bucket is not None:
        b = data["calibration"][str(bucket)]
        b["n"] += 1
        b["correct"] += int(win)
    # Track outcome drift for the exact context.
    recent = data["errors"].setdefault(key, [])
    recent.append(1 if win else 0)
    data["errors"][key] = recent[-50:]
    trade["v13_learning"] = {
        "knowledge_version": data.get("version", 1) + 1,
        "pattern_key": key,
        "regime": regime,
        "mae_pct": extremes.get("mae_pct"),
        "mfe_pct": extremes.get("mfe_pct"),
        "pnl_pct": pnl_pct,
        "sample_count": data["patterns"][key]["samples"],
        "pattern_confidence": _v13_pattern_confidence(data["patterns"][key]),
        "updated_at": _v13_now(),
    }
    _v13_save_knowledge(data)
    return trade["v13_learning"]


def _v13_prediction_from_analysis(analysis, asset, trade=None):
    """Research-only confidence; it never changes the scanner signal."""
    ctx = _v13_extract_context(analysis, asset, trade)
    score = ctx.get("score")
    base = 50.0 if score is None else float(score)
    data = _v13_load_knowledge()
    side = _v13_direction(trade) if trade else None
    key = _v13_pattern_key(asset, side or "NONE", ctx)
    p = data.get("patterns", {}).get(key)
    if p and p.get("samples", 0) >= V13_PATTERN_MIN_SAMPLES:
        base = (base * 0.55) + (_v13_pattern_confidence(p) * 0.45)
    # Calibration is deliberately advisory only.
    return round(max(0.0, min(100.0, base)), 1)


def v13_learning_status():
    data = _v13_load_knowledge()
    patterns = data.get("patterns", {})
    validated = sum(1 for p in patterns.values() if p.get("samples", 0) >= V13_PATTERN_MIN_SAMPLES)
    return {
        "version": V13_VERSION,
        "knowledge_version": data.get("version", 1),
        "closed_trades": data.get("stats", {}).get("closed", 0),
        "wins": data.get("stats", {}).get("wins", 0),
        "losses": data.get("stats", {}).get("losses", 0),
        "patterns": len(patterns),
        "validated_patterns": validated,
        "calibration_buckets": len(data.get("calibration", {})),
        "strategy_locked": True,
        "scanner_modified": False,
    }


def v13_learning_report(asset=None):
    data = _v13_load_knowledge()
    lines = ["🧠 **V13 Long-Term Learning Report**", "━" * 40]
    st = data.get("stats", {})
    n = int(st.get("closed", 0))
    wr = (st.get("wins", 0) / n * 100) if n else 0
    lines += [f"الصفقات المغلقة: {n}", f"نسبة النجاح: {wr:.1f}%", f"نسخة المعرفة: {data.get('version',1)}", ""]
    pats = []
    for key, p in data.get("patterns", {}).items():
        if asset and not key.startswith(str(asset) + "|"):
            continue
        n2 = p.get("samples", 0)
        if n2:
            pats.append((_v13_pattern_confidence(p), n2, key))
    for i, (conf, n2, key) in enumerate(sorted(pats, reverse=True)[:8], 1):
        lines.append(f"{i}. {key} | عينات {n2} | ثقة {conf:.1f}%")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Safe integration wrappers. The original implementations remain available
# through *_V13_ORIGINAL names. Scanner function is NOT wrapped or replaced.
# ---------------------------------------------------------------------------

_V13_ORIGINAL_ADD_TRADE = add_trade_to_history
_V13_ORIGINAL_CLOSE_TRADE = close_trade_virtual
_V13_ORIGINAL_RUN_MONITOR = _run_deep_monitor


def add_trade_to_history(asset_type, trade, holistic_entry_analysis=None):
    # Preserve original behavior first; V13 never decides whether a trade opens.
    ok = _V13_ORIGINAL_ADD_TRADE(asset_type, trade, holistic_entry_analysis)
    if not ok:
        return ok
    try:
        analysis = holistic_entry_analysis if isinstance(holistic_entry_analysis, dict) else trade.get("holistic_entry_analysis", {})
        snapshot = _v13_snapshot("entry", asset_type, trade, analysis)
        trade["v13_entry_snapshot_id"] = snapshot["snapshot_id"]
        trade["prediction_confidence"] = _v13_prediction_from_analysis(analysis, asset_type, trade)
        _v13_append_snapshot(snapshot)
        # Persist only additive metadata; never modify strategy fields.
        history = load_trades_history(asset_type, update_cache=False)
        for t in history.get("trades", []):
            if t.get("trade_id") == trade.get("trade_id"):
                t.update({"v13_entry_snapshot_id": trade["v13_entry_snapshot_id"], "prediction_confidence": trade["prediction_confidence"]})
                break
        save_trades_history(asset_type, history)
    except Exception as e:
        logger.error(f"[V13] فشل تكامل snapshot الدخول: {e}")
    return ok


def _run_deep_monitor(asset_type, reason):
    # Run the original five-minute monitor exactly once. It already performs
    # the comprehensive analysis, warnings, SL/TP checks and persistence.
    result = _V13_ORIGINAL_RUN_MONITOR(asset_type, reason)
    try:
        open_after = get_current_open_trade(asset_type)
        if open_after:
            analysis = open_after.get("last_analysis")
            if isinstance(analysis, dict) and analysis:
                snap = _v13_snapshot("monitor", asset_type, open_after, analysis, {"reason": reason})
                _v13_append_snapshot(snap)
                open_after["v13_last_prediction_confidence"] = _v13_prediction_from_analysis(analysis, asset_type, open_after)
    except Exception as e:
        logger.error(f"[V13] فشل snapshot المراقبة: {e}")
    return result


def close_trade_virtual(asset_type, reason="أمر افتراضي", current_price=None):
    # Capture the exact trade first. If no explicit close price is supplied,
    # obtain a fresh market price here so the legacy two-day fallback cannot
    # silently turn a real P/L outcome into zero.
    before = get_current_open_trade(asset_type)
    trade_id = before.get("trade_id") if before else None
    if before and current_price is None:
        try:
            symbol = "USOIL_USDT" if asset_type == "oil" else "SILVER_USDT"
            data = get_mexc_candles(symbol, "Min1", 5)
            if data and data.get("closes"):
                current_price = data["closes"][-1]
        except Exception as e:
            logger.warning(f"[V13] تعذر جلب سعر الإغلاق المسبق: {e}")

    # Original close remains the authority for all existing notifications and
    # trade accounting; V13 only supplies a safer real market price.
    ok = _V13_ORIGINAL_CLOSE_TRADE(asset_type, reason, current_price)
    if not ok:
        return ok
    try:
        history = load_trades_history(asset_type, update_cache=False)
        closed = None
        if trade_id:
            closed = next((t for t in history.get("trades", []) if t.get("trade_id") == trade_id), None)
        if closed:
            tid = closed.get("trade_id")
            snapshots = _v13_load_snapshots(tid)
            exit_analysis = closed.get("full_exit_analysis")
            learning = _v13_record_closed_trade(closed, asset_type, snapshots, exit_analysis)
            if learning:
                for t in history.get("trades", []):
                    if t.get("trade_id") == tid:
                        t["v13_learning"] = learning
                        break
                save_trades_history(asset_type, history)
    except Exception as e:
        logger.error(f"[V13] فشل تحديث التعلم بعد الإغلاق: {e}")
    return ok


# Explicitly expose the protected strategy/scanner identity for diagnostics.
STRATEGY_PROTECTION = {
    "scanner": "signal_scanner",
    "interval_seconds": SIGNAL_CHECK_INTERVAL,
    "strategy": "SuperTrend/VPT original",
    "learning_can_modify_scanner": False,
    "learning_can_modify_strategy_parameters": False,
}

# Compatibility aliases for future UI buttons; additive only.
get_v13_learning_status = v13_learning_status
get_v13_learning_report = v13_learning_report


# ====================================================================================
# 📦 PART 28: تشغيل البوت
# ====================================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s')
    logger = logging.getLogger("TonaPrometheus")

    print("\n" + "=" * 60)
    print("🔥 تولين AI Prometheus Edition V13.0 - الإطلاق النهائي")
    print("💙 الاسم الشخصي: تولين (الروح الجديدة)")
    print("👨‍💻 المطور: بسام الحوباني")
    print("🧠 جميع المحركات تعمل بشكل كامل")
    print("📊 نظام المستشار المتقدم: نشط")
    print("🧠 TCN (شبكة الوعي): نشط" if TCN_AVAILABLE else "⚠️ TCN: معطل")
    print("📌 الفصل الجذري بين الاستراتيجية والتحليل الشامل: تم التطبيق")
    print("=" * 60)

    print("\n🌐 تسجيل Webhook...")
    time.sleep(2)
    if set_webhook():
        print("✅ Webhook مسجل - البوت جاهز!")
    else:
        print("⚠️ فشل تسجيل Webhook - تحقق من التوكن والرابط")

    os.makedirs("learning_data", exist_ok=True)
    os.makedirs("learning_data/exports", exist_ok=True)

    # ── تهيئة الخيوط ──
    threads = [
        threading.Thread(target=signal_scanner, name="Scanner", daemon=True),
        threading.Thread(target=deep_monitor, name="DeepMonitor", daemon=True),
        threading.Thread(target=telegram_sender, name="Sender", daemon=True),
        threading.Thread(target=health_check, name="HealthCheck", daemon=True),
    ]

    if DREAM_AVAILABLE and DREAM:
        dream_thread = threading.Thread(target=_dream_worker, name="DreamEngine", daemon=True)
        threads.append(dream_thread)

    # ── تشغيل الخيوط ──
    logger.info("🚀 [BOOT] بدء جميع Threads — Scanner/Monitor/Sender/HealthCheck")
    for t in threads:
        t.start()
        print(f"✅ Thread {t.name} بدأ")

    print("\n✅ جميع الـ Threads بدأت - بوت Prometheus يعمل!")
    print("📩 أرسل رسالة للاختبار\n")
    print("🧠 جميع المحركات تعمل: Prometheus, Chronos, Oracle, Dream, Advisor, AI Brain, Risk Master, Persona, Intent, Language, Memory, Context, Decision, Conversation, Market Analyzer, Indicators, Pattern Analyzer, Predictor, Learner, Tona Intelligence, Fusion Bridge")
    print("📊 أنظمة المستشار المتقدم: Confidence Scorer, Conviction Report, Trade Post-Mortem, Similar Cases Analyzer, Deep Result Analyzer")
    print("🧠 TCN (شبكة الوعي): نشط")
    print("💙 تولين: أنا هنا لمساعدتك! 🚀")
    print("📌 تذكر: زر التحليل = تحليل شامل, الماسح التلقائي = استراتيجية الدخول")

    # ── الحلقة الرئيسية ──
    while True:
        time.sleep(1)

        if should_send_daily_report():
            threading.Thread(target=send_daily_report, daemon=True).start()
        if should_export_archive():
            threading.Thread(target=export_learning_archive, daemon=True).start()



