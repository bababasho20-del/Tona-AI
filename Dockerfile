FROM python:3.10-slim

WORKDIR /app

# نسخ ملف المتطلبات أولاً لتخزينها في الكاش (cache)
COPY requirements.txt .

# تثبيت التبعيات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# تشغيل البوت
CMD ["gunicorn", "main:app"]
