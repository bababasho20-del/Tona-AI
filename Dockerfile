FROM python:3.10-slim

WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# ✅ تشغيل Flask مباشرة (بدون Gunicorn)
# هذا يضمن عمل الخيوط الخلفية (Scanner و Monitor) بشكل صحيح
CMD ["python", "main.py"]
