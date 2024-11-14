# 使用輕量級的 Python 映像檔作為基礎
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式檔案到容器中
COPY requirements.txt .
COPY lottery.py .
COPY api.py .

# 建立並設定 SQLite 資料庫目錄
RUN mkdir -p /app/data
ENV SQLITE_DB_PATH=/app/data/lottery.db

# 安裝應用程式依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV FLASK_APP=api.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# 開放 5000 port
EXPOSE 5000

# 使用 gunicorn 啟動應用程式
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "api:app"]
