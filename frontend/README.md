# 抽獎系統 - 前端部署指南

## 部署說明

### Netlify 部署步驟

1. 登入 Netlify
2. 選擇 "Add new site" > "Import an existing project"
3. 連接 GitHub 倉庫
4. 配置設定：
   - Base directory: `lottery/frontend`
   - Build command: 留空
   - Publish directory: `.`

### 重要配置檔案

- `index.html`: 主要前端頁面
- `netlify.toml`: Netlify 路由和標頭配置
- `_redirects`: 路由重定向配置

### API 連接

- 預設 API 輸入框提供一個範例 Render URL
- 第一次使用時，請在 API 設定區塊輸入您的後端 API URL
- API URL 將儲存在瀏覽器的 localStorage

### 常見問題

1. 無法連接後端
   - 確認 API URL 正確
   - 檢查後端服務是否正在運行
   - 確認 CORS 設定

2. 部署後無法訪問
   - 檢查 Netlify 部署日誌
   - 確認路由配置正確
   - 驗證 netlify.toml 設定

## 本地開發

使用任何靜態文件伺服器，例如：

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server
```

## 技術棧

- HTML5
- JavaScript (ES6+)
- Bootstrap 5.3
- localStorage API
