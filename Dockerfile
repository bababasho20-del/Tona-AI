FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ تشغيل Flask مباشرة (بدون Gunicorn)
CMD ["python", "main.py"]
