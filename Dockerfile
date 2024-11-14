# 使用輕量級的 Python 映像檔作為基礎
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式檔案到容器中
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 建立並設定 SQLite 資料庫目錄
RUN mkdir -p /app/data
ENV SQLITE_DB_PATH=/app/data/lottery.db

# 開放 5000 port
EXPOSE 5000

# 使用 python 啟動應用程式
CMD ["python", "api.py"]
