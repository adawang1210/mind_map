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
│   ├── app.py
│   ├── pdf_processor.py  # Gemini Ai處理pdf長文
│   └── uploads
├── frontend
│   ├── README.md
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   ├── src
│   │     ├── components/views
│   │                      ├── MindMap.vue
│   │                      ├── PdfUploader
│   └── vue.config.js
└── structure.txt
shell
複製
編輯

## 🚀 快速啟動

### 📦 安裝前端

```bash
cd frontend
npm install
npm run serve

🐍 啟動後端
cd backend
pip install -r requirements.txt
python app.py
Flask 預設會跑在 http://127.0.0.1:5000，前端會呼叫 /upload API 來處理 PDF 分析。

🧠 Gemini 回傳格式（範例）
後端會回傳符合 MindElixir 的 nodeData 結構：

📤 導出心智圖為 PNG
只需點擊「匯出為 PNG」按鈕，即可將當前導圖保存為圖片。

📘 License
MIT License © 2025

