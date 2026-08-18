FROM python:3.10-slim

WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# ✅ استخدام Gunicorn مع خيار --preload وعامل واحد فقط
# --preload: يتم تحميل الكود قبل fork العمال، مما يضمن بدء الخيوط مرة واحدة فقط
# --workers 1: لتجنب أي تعارض بين العمال
# --timeout 300: مهلة 5 دقائق لتجنب SIGTERM من Render
CMD ["gunicorn", "--preload", "--workers", "1", "--timeout", "300", "--bind", "0.0.0.0:10000", "main:app"]
