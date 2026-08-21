FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "1", "--timeout", "300", "--bind", "0.0.0.0:10000", "main:app"]
