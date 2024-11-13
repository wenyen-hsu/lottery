# 抽獎系統

這是一個網頁版抽獎系統，採用前後端分離架構，前端可部署在 Netlify，後端可部署在支援 Python 的雲端平台。

## 系統架構

- 前端：純靜態網頁（HTML + JavaScript）
- 後端：Flask API 服務
- 資料庫：SQLite

## 部署說明

### 前端部署（Netlify）

1. **準備工作**
   - 註冊 [Netlify](https://www.netlify.com/) 帳號
   - 安裝 Git（如果尚未安裝）

2. **部署步驟**
   ```bash
   # 1. 建立新的 Git 倉庫
   git init
   
   # 2. 只添加前端相關文件
   git add frontend/*
   
   # 3. 提交更改
   git commit -m "Initial commit"
   
   # 4. 在 Netlify 上：
   # - 點擊 "New site from Git"
   # - 選擇你的 Git 倉庫
   # - 設定部署配置：
   #   - Build command: 留空
   #   - Publish directory: frontend
   # - 點擊 "Deploy site"
   ```

3. **部署完成後**
   - Netlify 會提供一個網址（例如：https://your-site.netlify.app）
   - 可以在網站設定中更改為自訂網域

### 後端部署（Render）

1. **準備工作**
   - 註冊 [Render](https://render.com/) 帳號
   - 將專案推送到 GitHub

2. **部署步驟**
   ```bash
   # 1. 在 Render 上：
   # - 點擊 "New Web Service"
   # - 選擇你的 GitHub 倉庫
   # - 設定部署配置：
   #   - Runtime: Python 3
   #   - Build Command: pip install -r requirements.txt
   #   - Start Command: gunicorn api:app
   ```

3. **環境設定**
   - 確保在 Render 的環境變數中設定：
     - `PYTHON_VERSION`: 3.9
     - `PORT`: 5000

### 連接前後端

1. **獲取後端 API 網址**
   - 在 Render 的服務頁面找到你的 API 網址
   - 格式類似：https://your-api.onrender.com

2. **設定前端 API 連接**
   - 第一次訪問網站時，會要求輸入 API 網址
   - 輸入 Render 提供的 API 網址
   - 系統會將設定儲存在瀏覽器中

## 本地開發說明

### 後端開發

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **運行後端服務**
   ```bash
   python api.py
   ```
   服務會在 http://localhost:5000 運行

### 前端開發

1. **使用任何靜態檔案伺服器**
   例如使用 Python 的內建伺服器：
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   前端會在 http://localhost:8000 運行

2. **設定本地 API 網址**
   - 訪問前端網頁
   - 輸入本地 API 網址：http://localhost:5000

## 系統功能

- 批次輸入多個參與者（空格分隔）
- 即時顯示參與者列表
- 指定抽獎人數進行抽獎
- 顯示抽獎結果
- 一鍵重置功能

## 檔案結構

```
lottery/
├── frontend/               # 前端檔案（部署到 Netlify）
│   ├── index.html         # 主要網頁
│   └── netlify.toml       # Netlify 配置
├── api.py                 # 後端 API 服務
├── lottery.py             # 抽獎核心邏輯
├── requirements.txt       # Python 依賴
└── README.md             # 說明文件
```

## 注意事項

1. **CORS 設定**
   - 後端已啟用 CORS 支援
   - 允許所有來源的請求

2. **資料持久化**
   - 資料儲存在 SQLite 資料庫
   - Render 會在每次部署時重置檔案系統
   - 建議使用外部資料庫服務（如需要永久儲存）

3. **安全性考慮**
   - 前端儲存 API 網址在 localStorage
   - 建議在正式環境中加入適當的認證機制

## 故障排除

1. **無法連接到 API**
   - 確認 API 網址是否正確
   - 檢查後端服務是否正常運行
   - 確認瀏覽器 Console 中的錯誤訊息

2. **部署問題**
   - Netlify：檢查部署日誌
   - Render：查看建置和運行日誌

3. **資料不同步**
   - 清除瀏覽器快取
   - 重新載入頁面
   - 檢查網路請求狀態

## 技術支援

如遇到技術問題：
1. 檢查瀏覽器 Console 的錯誤訊息
2. 查看後端服務的日誌
3. 確認網路連接狀態
4. 檢查 API 網址設定
