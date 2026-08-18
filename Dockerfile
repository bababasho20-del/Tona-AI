FROM python:3.10-slim

WORKDIR /app

# نسخ متطلبات Python وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# ✅ تشغيل Flask مباشرة باستخدام python (بدون Gunicorn)
CMD ["python", "main.py"]
