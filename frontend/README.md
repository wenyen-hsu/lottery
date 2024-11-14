# 抽獎系統前端

## 環境設定

### 開發環境
開發環境下，API 預設指向 `http://localhost:5000`

### 生產環境
部署到 Netlify 時，需要在 Netlify 的環境變數設定中配置：
- REACT_APP_API_URL: 設定為您的 API 網域，例如 "https://your-api-domain.com"

## 本地開發
1. 確保後端 API 服務已經啟動
2. 使用 Live Server 或其他 HTTP 服務器運行前端
3. 在瀏覽器中訪問本地服務器地址

## 部署說明
1. 將代碼推送到 GitHub
2. 在 Netlify 中連接您的 GitHub 倉庫
3. 設定環境變數 REACT_APP_API_URL
4. 部署完成後即可使用
