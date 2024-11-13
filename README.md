# 抽獎系統 - 部署指南

## 系統架構

前後端分離架構：
- 前端：純靜態網頁（Netlify）
- 後端：Flask API（Render）
- 資料庫：SQLite

## 部署步驟

### 1. GitHub 倉庫準備

1. 建立 GitHub 倉庫
2. 上傳以下檔案：
   ```
   lottery/
   ├── api.py
   ├── lottery.py
   ├── requirements.txt
   └── frontend/
       └── index.html
   ```

### 2. 部署後端 (Render)

1. 登入 [Render](https://render.com/)
2. 建立新的 Web Service
3. 連接 GitHub 倉庫
4. 配置設定：
   - Name: lottery-backend
   - Runtime: Python
   - Branch: main
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api:app`
   - Region: 選擇靠近你的地區
5. 點擊 "Create Web Service"
6. 等待部署完成
7. 記下生成的 URL（例如：https://lottery-backend.onrender.com）

### 3. 部署前端 (Netlify)

1. 登入 [Netlify](https://www.netlify.com/)
2. 點擊 "Add new site" > "Import an existing project"
3. 連接 GitHub 倉庫
4. 配置設定：
   - Base directory: `lottery/frontend`
   - Build command: 留空
   - Publish directory: `.`
5. 點擊 "Deploy site"
6. 等待部署完成
7. 記下生成的網址（例如：https://lotterysiemens.netlify.app）

### 4. 連接前後端

1. 訪問 Netlify 部署的網站
2. 在 API 設定區塊輸入 Render 的後端 URL
3. 點擊 "連接後端服務"

## 功能說明

### 主要功能
- 新增參與者（支持批次）
- 抽獎
- 重置抽獎狀態
- 清除所有參與者

### 使用注意事項
- 第一次使用需要設定 API 網址
- API 網址會儲存在瀏覽器 localStorage
- 支援多人同時使用

## 故障排除

1. API 連接失敗
   - 確認 Render 後端服務正在運行
   - 檢查 API 網址是否正確
   - 查看瀏覽器 Console 錯誤訊息

2. 資料不同步
   - 清除瀏覽器快取
   - 重新整理頁面
   - 檢查網路請求狀態

## 安全性提醒

- 後端已啟用 CORS
- 資料儲存在 SQLite
- Render 免費方案可能有休眠機制

## 技術棧

- 前端：HTML, JavaScript, Bootstrap
- 後端：Python, Flask
- 部署：Render, Netlify
- 資料庫：SQLite

## 開發者

歡迎提出 issues 和 pull requests！
