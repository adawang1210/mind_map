# 🧠 MindMap PDF Analyzer

一個 Vue.js 前端 + Flask 後端的心智圖應用，支援使用者上傳 PDF 檔案，並由 AI 分析內容，自動生成思維導圖。

## ✨ 專案功能

- ✅ 上傳 PDF 並送至後端解析
- ✅ 使用 Gemini API 提取歷史或文學分析結構
- ✅ 使用 [MindElixir](https://github.com/ssshooter/mind-elixir-core) 動態呈現心智圖
- ✅ 支援心智圖節點選取、編輯與操作
- ✅ 導出心智圖為 PNG 圖檔

## 🖼️ 介面預覽

## 📦 前端技術

- Vue 3
- MindElixir（思維導圖）
- Axios（與 Flask 後端溝通）

## 🔙 後端技術

- Python Flask
- Gemini API（分析 PDF 文本並產出 `nodeData` 結構）

## 📂 專案結構

├── backend
│   ├── app.py
│   ├── pdf_processor.py # Gemini Ai 處理 pdf 長文
│   └── uploads
├── frontend
│   ├── README.md
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   ├── src
│   │   ├── components/views
│   │   ├── MindMap.vue
│   │   ├── PdfUploader
│   └── vue.config.js
└── structure.txt
```

## 🚀 快速啟動

### 📦 安裝前端

```bash
cd frontend
npm install
npm run serve
```

前端將在 http://localhost:8080 運行

### 🐍 啟動後端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

後端將在 http://localhost:5001 運行

## 📤 導出心智圖為 PNG

只需點擊「匯出為 PNG」按鈕，即可將當前導圖保存為圖片。

## 📘 License

MIT License © 2025

# Mind App - 智能學習助手

這是一個基於 React 和 Flask 的智能學習助手應用，可以幫助用戶分析 PDF 文件並生成相關的測驗題目。

## 功能特點

- PDF 文件上傳和分析
- 使用 Google Gemini API 進行智能分析
- 自動生成測驗題目
- 互動式測驗界面
- 即時評分和結果展示

## 技術棧

### 前端
- React
- TypeScript
- Ant Design
- React Router

### 後端
- Flask
- Google Generative AI
- PyPDF2
- Flask-CORS

## 安裝說明

### 後端設置

1. 進入後端目錄：
```bash
cd backend
```

2. 創建並激活虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用: venv\Scripts\activate
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 設置環境變量：
```bash
export GOOGLE_API_KEY='your_api_key_here'  # 在 Windows 上使用: set GOOGLE_API_KEY=your_api_key_here
```

### 前端設置

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```

## 運行應用

1. 啟動後端服務器：
```bash
cd backend
python app.py
```
後端服務器將在 http://localhost:5001 運行

2. 啟動前端開發服務器：
```bash
cd frontend
npm start
```
前端應用將在 http://localhost:3000 運行

## 使用說明

1. 打開瀏覽器訪問 http://localhost:3000
2. 點擊"上傳 PDF"按鈕選擇要分析的 PDF 文件
3. 等待文件分析完成
4. 查看分析結果
5. 點擊"開始測驗"進行測驗
6. 完成測驗後查看得分和結果

## 注意事項

- 確保已正確設置 Google API 密鑰
- 上傳的 PDF 文件必須是有效的文本格式
- 建議使用較小的 PDF 文件以獲得更好的性能

## 項目結構

```
mind_app/
├── backend/
│   ├── app.py
│   ├── pdf_processor.py
│   ├── quiz_generator.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   └── index.tsx
│   └── package.json
└── README.md
```

## 貢獻指南

1. Fork 本項目
2. 創建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 許可證

本項目採用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 文件