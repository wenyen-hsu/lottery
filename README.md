# 抽獎系統 - 部署指南

## 系統架構

前後端分離架構：
- 前端：純靜態網頁（Netlify）
- 後端：Flask API（Render）
- 資料庫：SQLite

## 部署步驟

### 1. GitHub 倉庫準備

1. 建立 GitHub 倉庫
2. 上傳以下檔案結構：
   ```
   lottery/
   ├── api.py             # 後端 API 主程式
   ├── lottery.py         # 抽獎邏輯核心
   ├── requirements.txt   # Python 依賴
   ├── Dockerfile        # Docker 配置
   └── frontend/         # 前端檔案
       ├── index.html    # 主頁面
       ├── netlify.toml  # Netlify 配置
       └── _redirects    # Netlify 路由配置
   ```

### 2. 部署後端 (Render)

1. 登入 [Render](https://render.com/)
2. 建立新的 Web Service
3. 連接 GitHub 倉庫
4. 配置設定：
   - Name: lottery-backend（或自訂名稱）
   - Runtime: Docker
   - Branch: main
   - Root Directory: lottery（根據你的倉庫結構調整）
   - Region: 選擇靠近你的地區
5. 環境變數（Environment Variables）：
   - 不需要額外設定
6. 點擊 "Create Web Service"
7. 等待部署完成（首次部署可能需要 5-10 分鐘）
8. 記下生成的 URL（例如：https://lottery-backend.onrender.com）

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
7. 記下生成的網址（例如：https://your-lottery-app.netlify.app）

### 4. 連接前後端

1. 訪問 Netlify 部署的網站
2. 在頁面上方的 API 設定區塊中：
   - 輸入 Render 的後端 URL（完整網址，例如：https://lottery-backend.onrender.com）
   - 點擊 "連接後端服務"
3. 看到 "✅ 後端服務連接成功！" 訊息表示設定完成

## API 端點說明

後端 API 提供以下端點：

```
GET  /participants      # 獲取所有參與者列表
POST /add_participant   # 新增參與者
POST /draw             # 進行抽獎
POST /reset            # 重置抽獎狀態
POST /clear_all        # 清除所有參與者
```

### API 使用範例

1. 新增參與者：
```javascript
POST /add_participant
Content-Type: application/json

{
    "names": "張三 李四 王五"
}
```

2. 抽獎：
```javascript
POST /draw
Content-Type: application/json

{
    "count": 2  // 抽出人數
}
```

## 功能說明

### 主要功能
- 新增參與者（支持批次新增，用空格分隔多個名字）
- 抽獎（可指定抽出人數）
- 重置抽獎狀態（已抽中的人可再次參與）
- 清除所有參與者（危險操作，需謹慎使用）

### 使用注意事項
- 第一次使用需要設定 API 網址
- API 網址會儲存在瀏覽器的 localStorage
- 支援多人同時使用
- Render 免費方案可能有休眠機制，首次連接可能需要等待 30 秒左右

## 故障排除

1. API 連接失敗
   - 確認 Render 後端服務正在運行（首次連接可能需要等待喚醒）
   - 檢查 API 網址是否正確（必須包含 https://）
   - 查看瀏覽器 Console 的錯誤訊息
   - 確認 API 網址沒有多餘的斜線或空格

2. 資料不同步
   - 清除瀏覽器快取
   - 重新整理頁面
   - 檢查網路請求狀態（瀏覽器開發者工具 Network 分頁）

3. 部署問題
   - Render：確認 Dockerfile 正確配置
   - Netlify：確認 netlify.toml 和 _redirects 檔案存在

## 安全性說明

- 後端已啟用 CORS，允許前端跨域請求
- 資料儲存在 SQLite 資料庫
- API 未實作認證機制，適合內部使用
- Render 免費方案在閒置時會休眠，首次請求可能較慢

## 技術棧

- 前端：
  - HTML5
  - JavaScript (ES6+)
  - Bootstrap 5.3
  - localStorage API

- 後端：
  - Python 3.9
  - Flask 3.0.2
  - Flask-CORS 4.0.0
  - SQLite3
  - Docker

- 部署平台：
  - Render (後端)
  - Netlify (前端)

## 開發者注意事項

- 建議在修改程式碼後先在本地測試
- 本地測試方式：
  ```bash
  # 後端
  python api.py  # 會在 http://localhost:5000 運行

  # 前端
  # 使用任何靜態檔案伺服器，例如 Python 的 http.server
  cd frontend
  python -m http.server 8000  # 會在 http://localhost:8000 運行
  ```

## 貢獻指南

歡迎提出 issues 和 pull requests！

1. Fork 專案
2. 建立特性分支
3. 提交變更
4. 發送 Pull Request

## 授權

MIT License
