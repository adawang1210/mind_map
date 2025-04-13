<template>
  <div class="container">
    <h1>上傳 PDF 檔案</h1>
    <form @submit.prevent="uploadFile">
      <input type="file" id="pdfFile" accept=".pdf" ref="fileInput" required>
      <button type="submit">上傳</button>
    </form>
    <div id="result" v-html="resultMessage"></div>
  </div>
</template>

<script>
export default {
  name: 'PdfUploader',
  data() {
    return {
      resultMessage: ''
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
      formData.append('file', fileInput.files[0]);

      try {
        const response = await fetch('http://localhost:3000/upload', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();

        if (response.ok) {
          this.resultMessage = `
            <p class="success">檔案 ${data.filename} 上傳成功！</p>
            <p>頁數: ${data.pages}</p>
          `;
        } else {
          this.resultMessage = `<p class="error">錯誤: ${data.error}</p>`;
        }
      } catch (error) {
        this.resultMessage = `<p class="error">上傳失敗: ${error.message}</p>`;
      }
    }
  }
};
</script>

<style scoped>
/* 保持原樣 */
</style>