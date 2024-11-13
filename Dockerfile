# 使用輕量級的 Python 映像檔作為基礎
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式檔案到容器中
COPY requirements.txt .
COPY lottery.py .
COPY app.py .
COPY templates ./templates

# 安裝應用程式依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 開放 5000 port
EXPOSE 5000

# 使用 gunicorn 啟動應用程式
# --bind 0.0.0.0:5000：監聽所有網路介面的 5000 port
# --workers 4：使用 4 個 worker 處理請求
# --timeout 120：請求超時時間為 120 秒
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
