# 🧠 MindMap PDF Analyzer

一個 Vue.js 前端 + Flask 後端的心智圖應用，支援使用者上傳 PDF 檔案，並由 AI 分析內容，自動生成思維導圖。

## ✨ 專案功能

- ✅ PDF 文件上傳與分析
- ✅ 使用 Gemini API 進行智能分析
- ✅ 自動生成心智圖
- ✅ 互動式測驗界面
- ✅ 即時評分和結果展示
- ✅ 美觀的首頁設計

## 📦 技術架構

### 前端
- Vue 3
- Vue Router
- Axios（API 請求）
- MindElixir（思維導圖渲染）

### 後端
- Python Flask
- Google Generative AI (Gemini-1.5-pro)
- Sentence Transformers（語義分析）
- Flask-CORS（跨域支持）

## 📂 主要組件

- `HomePage.vue`: 應用首頁
- `MindMap.vue`: 思維導圖視圖
- `QuizPage.vue`: 測驗頁面
- `AppFooter.vue`: 頁面底部組件

## 🚀 快速啟動

### 前端設置

```bash
cd frontend
npm install
npm run serve
```

前端將在 http://localhost:8080 運行

### 後端設置

```bash
cd backend
pip install -r requirements.txt
python app.py
```

後端將在 http://localhost:5001 運行

## 🔑 API 配置

在使用前需要設置 Gemini API 密鑰：

1. 獲取 Google Gemini API 密鑰
2. 在 `backend/pdf_processor.py` 中配置 API 密鑰

## 🌐 路由配置

- `/`: 重定向到首頁
- `/homepage`: 應用首頁
- `/mindmap`: 思維導圖頁面
- `/quizpage`: 測驗頁面

## 📝 開發說明

- 後端使用多代理系統進行文本分析和驗證
- 前端實現了響應式設計
- 支持跨域請求
- 包含錯誤處理和 API 請求限流

## 📄 License

MIT License © 2024