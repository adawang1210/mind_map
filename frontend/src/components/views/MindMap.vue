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
          topic: "節點標題",
          id: "root",
          style: {
            fontSize: "24",
            color: "#000000",
            background: "#ffffff"
          },
          expanded: true,
          root: true,
          parent: null,
          tags: ["歷史", "重點"],
          icons: ["⭐"],
          hyperLink: "https://example.com",
          image: {
            url: "data:image/jpeg;base64,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",
            height: 90,
            width: 90
          },
          children: [
            {
              topic: "子節點 1",
              id: "child1",
              parent: "root"
            },
            {
              topic: "子節點 2",
              id: "child2",
              parent: "root"
            }
          ]
        },
        linkData: {},
        direction: 1,
        template: "default"
      }
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
