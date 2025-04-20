<template>
  <div class="container">
    <h1>心智圖與 PDF 上傳</h1>

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

        // 去除 markdown 語法
        raw = raw.replace(/^```json\s*/, "").replace(/```$/, "");

        // 解析並轉換 text 為 topic
        const nodeData = JSON.parse(raw);
        this.transformTextToTopic(nodeData);

        this.resultMessage = `
          <p class="success">檔案 <strong>${response.data.filename}</strong> 上傳成功！</p>`;

        // 更新 MindMap
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
.container {
  max-width: 1000px;
  margin: 50px auto;
  text-align: center;
}

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
