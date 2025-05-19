<template>
  <div class="container">
    <h1>上傳 PDF 檔案</h1>
    <form @submit.prevent="uploadFile">
      <input type="file" id="pdfFile" accept=".pdf" ref="fileInput" required />
      <button type="submit">上傳</button>
    </form>
    <div id="result" v-html="resultMessage"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "PdfUploader",
  data() {
    return {
      resultMessage: "",
    };
  },
  methods: {
  async uploadFile() {
    const fileInput = this.$refs.fileInput;
    if (!fileInput.files[0]) {
      this.resultMessage = '<p class="error">請選擇一個檔案</p>';
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
      const response = await axios.post("http://127.0.0.1:5001/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = response.data;

      this.resultMessage = `
        <p class="success">檔案 ${data.filename} 上傳成功！</p>
        <pre style="white-space: pre-wrap;">${data.response_text}</pre>
        <p>Prompt Tokens: ${data.prompt_token}</p>
        <p>Output Tokens: ${data.output_token}</p>
      `;
    } catch (error) {
      this.resultMessage = `<p class="error">上傳失敗: ${error.response?.data?.error || error.message}</p>`;
    }
  },
},

};
</script>

<style scoped>
/* 保持原樣 */
</style>
