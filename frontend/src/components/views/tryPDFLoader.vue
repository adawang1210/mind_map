<template>
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
</template>

<script>
import axios from "axios";

export default {
  name: "PDFLoader",
  data() {
    return {
      fileName: "",
      resultMessage: ""
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.fileName = file.name;
      }
    },
    async uploadFile() {
      const fileInput = this.$refs.fileInput;
      if (!fileInput.files.length) return;

      const formData = new FormData();
      formData.append("file", fileInput.files[0]);

      try {
        const response = await axios.post("/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        this.resultMessage = response.data.message || "上傳成功！";
      } catch (error) {
        this.resultMessage = "上傳失敗：" + error.message;
      }
    }
  }
};
</script>
