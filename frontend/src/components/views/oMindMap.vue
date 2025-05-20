<template>
  <div class="container">
    <h1>心智圖與 PDF 上傳</h1>

    <!-- 🌟 Flex 容器：將主要功能與快捷鍵說明左右排列 -->
    <div class="main-content">
      
      <!-- 📄 左側區塊：PDF 上傳 + 心智圖 -->
      <div class="main-functions">
        <!-- PDF Upload Section -->
        <section class="pdf-upload-section">
          <h2>上傳 PDF 檔案</h2>
          <form @submit.prevent="uploadFile">
            <div class="file-upload">
              <input
                type="file"
                id="pdfFile"
                accept=".pdf"
                ref="fileInput"
                required
                @change="handleFileChange"
              />
              <label for="pdfFile" class="file-label">
                <span v-if="!fileName">點擊選擇檔案</span>
                <span v-else>{{ fileName }}</span>
              </label>
              <button type="submit" class="upload-button">上傳</button>
            </div>
          </form>
          <div id="result" v-html="resultMessage"></div>
        </section>

        <!-- Mind Map Section -->
        <section class="mind-map-section">
          <h2>我的心智圖</h2>
          <div id="map" ref="map"></div>
          <button @click="exportPng" class="export-button">匯出為 PNG</button>
        </section>
      </div>

      <!-- ⌨️ 右側區塊：快捷鍵說明 -->
      <div class="shortcut-panel">
        <h2 class="text-lg font-semibold mb-3">⌨️ 快捷鍵說明</h2>
        <table class="w-full text-left table-auto border-separate border-spacing-y-1">
          <thead class="hidden">
            <tr>
              <th>快捷鍵</th>
              <th>功能</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in shortcuts" :key="index">
              <td class="font-mono text-gray-700 pr-2 whitespace-nowrap">{{ item.key }}</td>
              <td class="text-gray-800">{{ item.function }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import MindElixir from "mind-elixir";
import axios from "axios";

export default {
  name: "MindMapUploader",
  data() {
    return {
      mind: null,
      resultMessage: "",
      fileName: "",
      example: {
        nodeData: {
          id: "root",
          topic: "中心主題",
          root: true,
          children: [],
        },
        linkData: {},
        direction: 1,
        template: "default",
      },
      shortcuts: [
        { key: 'Enter', function: '插入同級節點' },
        { key: 'Tab', function: '插入子節點' },
        { key: 'F1', function: '將導圖置中' },
        { key: 'F2', function: '編輯當前節點' },
        { key: '↑', function: '選擇上一個同級節點' },
        { key: '↓', function: '選擇下一個同級節點' },
        { key: '← / →', function: '選擇父節點 / 第一個子節點' },
        { key: 'PageUp / Alt + ↑', function: '上移節點' },
        { key: 'PageDown / Alt + ↓', function: '下移節點' },
        { key: 'Ctrl + ↑', function: '佈局切換為「側邊」' },
        { key: 'Ctrl + ←', function: '佈局切換為「左側」' },
        { key: 'Ctrl + →', function: '佈局切換為「右側」' },
        { key: 'Ctrl + C', function: '複製當前節點' },
        { key: 'Ctrl + V', function: '貼上複製的節點' },
        { key: 'Ctrl + +', function: '放大導圖' },
        { key: 'Ctrl + -', function: '縮小導圖' },
        { key: 'Ctrl + 0', function: '重置導圖縮放等級' },
      ]
    };
  },
  mounted() {
    const options = {
      el: "#map",
      direction: MindElixir.LEFT,
      draggable: true,
      contextMenu: true,
      toolBar: true,
      nodeMenu: true,
      keypress: true,
    };

    this.mind = new MindElixir(options);
    this.mind.init(this.example);
  },
  methods: {
    handleFileChange(event) {
      this.fileName = event.target.files[0].name;
    },
    async uploadFile() {
      const fileInput = this.$refs.fileInput;
      if (!fileInput.files[0]) {
        this.resultMessage = '<p class="error">請選擇一個檔案</p>';
        return;
      }

      const formData = new FormData();
      formData.append("file", fileInput.files[0]);

      try {
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        let raw = response.data.analysis_result;
        raw = raw.replace(/^```json\s*/, "").replace(/```$/, "");
        const nodeData = JSON.parse(raw);
        this.transformTextToTopic(nodeData);

        this.resultMessage = `
          <p class="success">檔案 <strong>${response.data.filename}</strong> 上傳成功！</p>`;

        this.mind.init({
          nodeData,
          linkData: {},
          direction: 1,
          template: "default",
        });
      } catch (error) {
        this.resultMessage = `<p class="error">上傳失敗: ${error.response?.data?.error || error.message}</p>`;
      }
    },
    transformTextToTopic(node) {
      if (node.text && typeof node.text === "string") {
        node.topic = node.text;
        delete node.text;
      }

      if (Array.isArray(node.text)) {
        node.topic = node.text.map(item =>
          typeof item === "string"
            ? item
            : item.name
              ? `${item.name}（${item.time}）`
              : JSON.stringify(item)
        ).join("\n");
        delete node.text;
      }

      if (node.children && node.children.length > 0) {
        node.children.forEach(child => this.transformTextToTopic(child));
      }
    },
    async exportPng() {
      const blob = await this.mind.exportPng();
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "mindmap.png";
      a.click();
      URL.revokeObjectURL(url);
    },
  },
};
</script>

<style scoped>
/* 整體容器 */
.container {
  max-width: 1200px;
  margin: 50px auto;
  text-align: center;
}

/* 🌟 Flex 排版容器：左右排列主功能與快捷鍵說明 */
.main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

/* 📄 左邊主功能區域 */
.main-functions {
  flex: 2;
  text-align: center;
}

/* ⌨️ 右側快捷鍵說明區域 */
.shortcut-panel {
  flex: 1;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  padding: 16px;
  font-size: 14px;
  text-align: left;
}

/* 上傳區域 */
.pdf-upload-section {
  margin-bottom: 40px;
}

.pdf-upload-section h2,
.mind-map-section h2 {
  font-size: 1.6em;
  margin-bottom: 20px;
}

.file-upload {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

input[type="file"] {
  display: none;
}

.file-label {
  display: inline-block;
  padding: 10px 20px;
  background-color: #f5f5f5;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  color: #333;
}

.file-label:hover {
  background-color: #ddd;
}

.upload-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.upload-button:hover {
  background-color: #0056b3;
}

/* 心智圖區域 */
#map {
  height: 500px;
  width: 100%;
  border: 1px solid #ddd;
  margin-bottom: 20px;
}

.export-button {
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

.export-button:hover {
  background-color: #218838;
}

#result {
  margin-top: 20px;
  text-align: left;
}

.success {
  color: green;
}

.error {
  color: red;
}
</style>
