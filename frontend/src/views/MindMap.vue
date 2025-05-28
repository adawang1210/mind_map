<template>
  <div class="mind-map-app">
    <Header />
    <v-container
      class="pa-4 pa-sm-2"
      fluid
      style="max-width: 1800px; margin: auto"
    >
      <!-- PDF 上傳區塊 -->
      <v-row>
        <v-col cols="12">
          <section
            class="pdf-upload-section pa-md-12 pa-6 rounded-lg elevation-1"
          >
            <h2 class="mb-4 text-h4 text-md-h4 text-sm-h5 text-xs-h6">
              上傳 PDF 檔案
            </h2>
            <div class="upload-guide mb-4">
              <p>
                法文史料上傳，系統的雙層AI (Gemini 1.5 Pro核心)
                即時生成互動心智圖。複雜歷史視覺化，助您高效理解、輕鬆記憶！
              </p>
            </div>
            <form @submit.prevent="uploadFile" class="upload-form">
              <input
                type="file"
                id="pdfFile"
                accept=".pdf"
                ref="fileInput"
                required
                @change="handleFileChange"
                style="display: none"
              />
              <div class="button-container">
                <v-btn
                  color="primary"
                  @click="$refs.fileInput.click()"
                  class="upload-btn"
                >
                  {{ fileName || "點擊選擇檔案" }}
                </v-btn>
                <v-btn
                  type="submit"
                  color="success"
                  class="ml-md-3 mt-2 mt-md-0 upload-btn"
                  :disabled="processing"
                  >上傳</v-btn
                >
              </div>
            </form>
            <div v-if="processing" class="mt-4">
              <div class="process-status">
                <div class="process-text">{{ processStage }}</div>
                <v-progress-linear
                  color="primary"
                  height="20"
                  :value="progress"
                  striped
                  buffer-value="0"
                >
                  <template v-slot:default>
                    {{ Math.ceil(progress) }}%
                  </template>
                </v-progress-linear>
              </div>
            </div>
            <div v-html="resultMessage" class="mt-4"></div>
          </section>
        </v-col>
      </v-row>
      <!-- 心智圖與快捷鍵並排 -->
      <v-row class="mt-8 mind-map-row" dense>
        <!-- 左側心智圖 -->
        <v-col cols="12" md="9" sm="12" class="px-md-4 px-2 d-flex flex-column">
          <section
            class="mindmap-section pa-md-4 pa-2 elevation-2 rounded flex-grow-1"
          >
            <h2 class="mb-3">我的心智圖</h2>
            <div id="map" ref="map" class="mind-map-container"></div>
            <div class="export-buttons mt-4">
              <v-btn
                color="success"
                class="me-2 mb-2 mb-md-0 export-btn"
                @click="exportPng"
                ><span class="d-none d-sm-block">匯出 PNG 檔案</span
                ><span class="d-block d-sm-none">PNG</span></v-btn
              >
              <v-btn
                color="info"
                class="me-2 mb-2 mb-md-0 export-btn"
                @click="exportSvg"
                ><span class="d-none d-sm-block">匯出 SVG 向量圖</span
                ><span class="d-block d-sm-none">SVG</span></v-btn
              >
              <v-btn
                color="warning"
                class="me-2 mb-2 mb-md-0 export-btn"
                @click="exportJson"
                ><span class="d-none d-sm-block">匯出 JSON 結構</span
                ><span class="d-block d-sm-none">JSON</span></v-btn
              >
              <v-spacer class="d-none d-md-block"></v-spacer>
              <v-btn
                color="primary"
                class="export-btn quiz-btn"
                @click="generateQuiz"
              >
                <span class="d-none d-sm-block">儲存後生成測驗</span>
                <span class="d-block d-sm-none">生成測驗</span>
              </v-btn>
            </div>
          </section>
        </v-col>

        <!-- 右側快捷鍵 -->
        <v-col
          cols="12"
          md="3"
          sm="12"
          class="px-md-4 px-2 mt-4 mt-md-0 d-flex flex-column"
        >
          <section
            class="shortcut-section pa-md-4 pa-3 elevation-2 rounded flex-grow-1"
          >
            <h2 class="mb-3">快捷鍵說明</h2>
            <div class="shortcut-scroll">
              <table class="shortcut-table">
                <tbody>
                  <tr v-for="(item, index) in shortcuts" :key="index">
                    <td class="shortcut-key">{{ item.key }}</td>
                    <td class="shortcut-func">{{ item.function }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </v-col>
      </v-row>
    </v-container>

    <Footer />
  </div>
</template>

<script>
import Header from "./AppHeader.vue";
import Footer from "./AppFooter.vue";
import MindElixir from "mind-elixir";
import axios from "axios";

export default {
  name: "MindMapUploader",
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      mind: null,
      resultMessage: "",
      fileName: "",
      backendUrl: "http://127.0.0.1:5001", // 預先定義後端URL
      processing: false,
      progress: 0,
      processStage: "",
      shortcuts: [
        { key: "Enter", function: "插入同級節點" },
        { key: "Tab", function: "插入子節點" },
        { key: "F1", function: "將導圖置中" },
        { key: "F2", function: "編輯當前節點" },
        { key: "↑", function: "選擇上一個同級節點" },
        { key: "↓", function: "選擇下一個同級節點" },
        { key: "← / →", function: "選擇父節點 / 第一個子節點" },
        { key: "PageUp / Alt + ↑", function: "上移節點" },
        { key: "PageDown / Alt + ↓", function: "下移節點" },
        { key: "Ctrl + ↑", function: "佈局為「側邊」" },
        { key: "Ctrl + ←", function: "佈局為「左側」" },
        { key: "Ctrl + →", function: "佈局為「右側」" },
        { key: "Ctrl + C", function: "複製當前節點" },
        { key: "Ctrl + V", function: "貼上複製的節點" },
        { key: "Ctrl + +", function: "放大導圖" },
        { key: "Ctrl + -", function: "縮小導圖" },
        { key: "Ctrl + 0", function: "重置導圖縮放等級" },
      ],
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
      direction: MindElixir.SIDE, // 改為SIDE，使心智圖呈現左右對稱
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
      // 檢查是否選擇了文件
      const fileInput = this.$refs.fileInput;
      if (!fileInput.files[0]) {
        this.resultMessage = '<p class="error">請選擇一個檔案</p>';
        return;
      }

      // 準備上傳數據
      const formData = new FormData();
      formData.append("file", fileInput.files[0]);

      // 設置處理狀態
      this.processing = true;
      this.progress = 0;
      this.processStage = "上傳檔案中";
      this.resultMessage = "";

      // 開始模擬進度
      const startTime = Date.now();
      const minProcessTime = 7500; // 最少要7.5秒
      const maxProcessTime = 15000; // 最多15秒

      // 階段文字
      const stages = [
        "上傳檔案中",
        "分析文件中",
        "產生心智圖",
        "進行多重驗證",
        "產生心智圖",
        "進行二次多重驗證",
        "完成",
      ];

      // 設置進度條計時器
      const progressTimer = setInterval(() => {
        const elapsed = Date.now() - startTime;

        // 計算進度
        if (elapsed < maxProcessTime) {
          // 隨機增加進度，但不超過5%
          const randomIncrement = Math.random() * 5;
          this.progress = Math.min(90, this.progress + randomIncrement); // 根據進度更新階段文字
          if (this.progress < 15) {
            this.processStage = stages[0];
          } else if (this.progress < 30) {
            this.processStage = stages[1];
          } else if (this.progress < 45) {
            this.processStage = stages[2];
          } else if (this.progress < 60) {
            this.processStage = stages[3];
          } else if (this.progress < 75 && Math.random() > 0.45) {
            this.processStage = stages[4]; // 45%機率進入第二次生成
          } else if (this.progress < 85 && Math.random() > 0.78) {
            this.processStage = stages[5]; // 22%機率進入第二次驗證
          } else if (this.progress >= 85 && this.progress < 100) {
            this.processStage = "正在準備";
          } else if (this.progress >= 100) {
            this.processStage = stages[6];
          }
        }
      }, 300);

      try {
        // 發送API請求
        const response = await axios.post(
          `${this.backendUrl}/upload`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        // 處理API返回的JSON數據
        const nodeData = this.parseJsonFromResponse(
          response.data.analysis_result
        );

        // 處理節點格式
        this.transformTextToTopic(nodeData);

        // 確保至少經過minProcessTime後才顯示結果
        const elapsed = Date.now() - startTime;
        if (elapsed < minProcessTime) {
          await new Promise((resolve) =>
            setTimeout(resolve, minProcessTime - elapsed)
          );
        }

        // 進度設為100%
        this.progress = 100;
        this.processStage = "完成";

        // 更新心智圖
        setTimeout(() => {
          clearInterval(progressTimer);
          this.processing = false;
          this.updateMindMap(nodeData, response.data.filename);
        }, 500);
      } catch (error) {
        // 停止計時器
        clearInterval(progressTimer);
        this.processing = false;

        // 處理錯誤
        this.resultMessage = `<p class="error">上傳失敗: ${
          error.response?.data?.error || error.message
        }</p>`;
      }
    },
    transformTextToTopic(node) {
      if (node.text && typeof node.text === "string") {
        node.topic = node.text;
        delete node.text;
      }

      if (Array.isArray(node.text)) {
        node.topic = node.text
          .map((item) =>
            typeof item === "string"
              ? item
              : item.name
              ? `${item.name}（${item.time}）`
              : JSON.stringify(item)
          )
          .join("\n");
        delete node.text;
      }

      if (node.children && node.children.length > 0) {
        node.children.forEach((child) => this.transformTextToTopic(child));
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

    async exportSvg() {
      const svg = this.mind.exportSvg();
      if (!svg) return;

      // 建立 Blob 物件
      const blob = new Blob([svg], { type: "image/svg+xml" });
      const url = URL.createObjectURL(blob);

      // 建立下載連結
      const a = document.createElement("a");
      a.href = url;
      a.download = "mindmap.svg";
      a.click();
      URL.revokeObjectURL(url);
    },

    exportJson() {
      // 獲取當前心智圖的數據
      const data = this.mind.getData();

      // 轉換為 JSON 字符串
      const jsonStr = JSON.stringify(data, null, 2);

      // 建立 Blob 物件
      const blob = new Blob([jsonStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      // 建立下載連結
      const a = document.createElement("a");
      a.href = url;
      a.download = "mindmap.json";
      a.click();
      URL.revokeObjectURL(url);
    },
    generateQuiz() {
      try {
        // 獲取當前的心智圖數據
        const data = this.mind.getData();

        if (!data || !this.fileName) {
          alert("請先上傳並生成心智圖，再產生測驗");
          return;
        }

        // 將 JSON 轉換為字符串並進行 URL 編碼
        const jsonDataStr = encodeURIComponent(JSON.stringify(data));

        // 導航到測驗頁面，將檔案名稱和 JSON 數據作為參數傳遞
        window.location.href = `/quizpage?filename=${encodeURIComponent(
          this.fileName
        )}&data=${jsonDataStr}`;
      } catch (error) {
        console.error("產生測驗時發生錯誤:", error);
        alert("產生測驗失敗，請稍後重試");
      }
    },
    parseJsonFromResponse(responseText) {
      let raw = responseText;
      raw = raw.trim(); // 先清理前後空白

      if (raw.startsWith("```json")) {
        // 找到第一個換行後的位置開始，一直到最後的 ``` 之前
        raw = raw.substring(raw.indexOf("\n") + 1);
        if (raw.lastIndexOf("```") !== -1) {
          raw = raw.substring(0, raw.lastIndexOf("```"));
        }
      }

      try {
        raw = raw.trim(); // 再次清理可能的前後空白
        return JSON.parse(raw);
      } catch (error) {
        console.error("JSON 解析錯誤:", error);
        console.log("原始數據:", raw);
        this.resultMessage = `<p class="error">JSON 解析失敗: ${error.message}</p>`;
        throw error;
      }
    },
    updateMindMap(nodeData, filename) {
      this.resultMessage = `<p class="success">檔案 <strong>${filename}</strong> 上傳成功！</p>`;

      this.mind.init({
        nodeData,
        linkData: {},
        direction: 2, // 使用2代表SIDE方向，確保與初始化一致
        template: "default",
      });
    },
  },
};
</script>

<style scoped>
.mind-map-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.mind-map-row {
  display: flex;
  flex-wrap: wrap;
}

@media (min-width: 960px) {
  .mind-map-row {
    min-height: 600px;
  }
}

.mindmap-section,
.shortcut-section {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
}

@media (max-width: 600px) {
  .mindmap-section {
    min-height: auto;
  }
}

.mind-map-container {
  flex-grow: 1;
  aspect-ratio: 3/2;
  margin: 0 auto;
  border: 1px solid #ddd;
  max-width: 100%;
  overflow: auto;
  min-height: 400px;
  touch-action: manipulation;
  -webkit-overflow-scrolling: touch; /* 增加iOS平台的滑動流暢度 */
}

@media (min-width: 1200px) {
  .mind-map-container {
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .mind-map-container {
    min-height: 300px;
    aspect-ratio: auto;
    max-height: 60vh; /* 限制在手機上的高度 */
  }
}

@media (max-width: 600px) {
  .mind-map-container {
    min-height: 200px;
    max-height: 50vh; /* 在小手機上進一步降低高度 */
  }
}

.shortcut-section {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  font-size: 14px;
  overflow-y: auto;
}

@media (min-width: 960px) {
  .shortcut-section {
    height: 100%;
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .shortcut-section {
    max-height: none;
    min-height: auto;
    overflow-y: hidden;
  }
}

.shortcut-scroll {
  overflow-x: hidden;
  flex-grow: 1;
}

@media (max-width: 768px) {
  .shortcut-scroll {
    overflow-y: hidden;
  }
}

.shortcut-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

.shortcut-key {
  width: 70px;
  font-family: monospace;
  white-space: nowrap;
  padding-right: 10px;
  color: #374151;
}

.shortcut-func {
  color: #1f2937;
}

.process-status {
  margin-bottom: 12px;
}

.process-text {
  margin-bottom: 5px;
  font-weight: 500;
  color: #4b5563;
}

.pdf-upload-section {
  background-color: #fff3e0; /* 淺橘色背景 */
  border: 1px solid #ffe0b2;
  transition: all 0.3s ease;
}

.upload-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.upload-btn {
  min-width: 120px;
}

@media (max-width: 600px) {
  .upload-btn {
    width: 100%;
    margin-left: 0 !important;
  }
}

.export-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.export-btn {
  min-width: 80px;
}

@media (max-width: 768px) {
  .quiz-btn {
    margin-top: 8px;
    width: 100%;
  }
}

.success {
  color: green;
}
.error {
  color: red;
}
</style>
