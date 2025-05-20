<template>
  <v-container class="pa-4" style="max-width: 1800px; margin: auto;">
    <h1 class="text-center mb-6"></h1>

    <!-- PDF 上傳區塊 -->
    <v-row>
      <v-col cols="12">
        <section class="pdf-upload-section pa-4">
          <h2 class="mb-3">上傳 PDF 檔案</h2>
          <form @submit.prevent="uploadFile">
            <input
              type="file"
              id="pdfFile"
              accept=".pdf"
              ref="fileInput"
              required
              @change="handleFileChange"
              style="display: none"
            />
            <v-btn color="primary" @click="$refs.fileInput.click()">
              {{ fileName || '點擊選擇檔案' }}
            </v-btn>
            <v-btn type="submit" color="success" class="ml-3">
              上傳
            </v-btn>
          </form>
          <div v-html="resultMessage" class="mt-4"></div>
        </section>
      </v-col>
    </v-row>

    <!-- 心智圖與快捷鍵並排 -->
    <v-row class="mt-8" dense>
      <!-- 左側心智圖 5/6 -->
      <v-col cols="12" md="10">
        <section class="mindmap-section pa-4 elevation-2 rounded">
          <h2 class="mb-3">我的心智圖</h2>
          <div
            id="map"
            ref="map"
            style="border: 1px solid #ddd; height: 1000px; width: 100%;"
          ></div>
          <v-btn color="success" class="mt-4" @click="exportPng">匯出為 PNG</v-btn>
        </section>
      </v-col>

      <!-- 右側快捷鍵 1/6 -->
      <v-col cols="12" md="2">
        <section
          class="shortcut-section pa-4 elevation-2 rounded"
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
</template>

<script>
import MindElixir from 'mind-elixir'
import axios from 'axios'

export default {
  name: 'MindMapUploader',
  data() {
    return {
      mind: null,
      resultMessage: '',
      fileName: '',
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
        { key: 'Ctrl + ↑', function: '佈局為「側邊」' },
        { key: 'Ctrl + ←', function: '佈局為「左側」' },
        { key: 'Ctrl + →', function: '佈局為「右側」' },
        { key: 'Ctrl + C', function: '複製當前節點' },
        { key: 'Ctrl + V', function: '貼上複製的節點' },
        { key: 'Ctrl + +', function: '放大導圖' },
        { key: 'Ctrl + -', function: '縮小導圖' },
        { key: 'Ctrl + 0', function: '重置導圖縮放等級' },
      ],
      example: {
        nodeData: {
          id: 'root',
          topic: '中心主題',
          root: true,
          children: [],
        },
        linkData: {},
        direction: 1,
        template: 'default',
      },
    }
  },
  mounted() {
    const options = {
      el: '#map',
      direction: MindElixir.LEFT,
      draggable: true,
      contextMenu: true,
      toolBar: true,
      nodeMenu: true,
      keypress: true,
    }

    this.mind = new MindElixir(options)
    this.mind.init(this.example)
  },
  methods: {
    handleFileChange(event) {
      this.fileName = event.target.files[0].name
    },
    async uploadFile() {
      const fileInput = this.$refs.fileInput
      if (!fileInput.files[0]) {
        this.resultMessage = '<p class="error">請選擇一個檔案</p>'
        return
      }

      const formData = new FormData()
      formData.append('file', fileInput.files[0])

      try {
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        let raw = response.data.analysis_result
        raw = raw.replace(/^```json\s*/, '').replace(/```$/, '')

        const nodeData = JSON.parse(raw)
        this.transformTextToTopic(nodeData)

        this.resultMessage = `
          <p class="success">檔案 <strong>${response.data.filename}</strong> 上傳成功！</p>`

        this.mind.init({
          nodeData,
          linkData: {},
          direction: 1,
          template: 'default',
        })
      } catch (error) {
        this.resultMessage = `<p class="error">上傳失敗: ${error.response?.data?.error || error.message}</p>`
      }
    },
    transformTextToTopic(node) {
      if (node.text && typeof node.text === 'string') {
        node.topic = node.text
        delete node.text
      }

      if (Array.isArray(node.text)) {
        node.topic = node.text
          .map((item) =>
            typeof item === 'string'
              ? item
              : item.name
              ? `${item.name}（${item.time}）`
              : JSON.stringify(item)
          )
          .join('\n')
        delete node.text
      }

      if (node.children && node.children.length > 0) {
        node.children.forEach((child) => this.transformTextToTopic(child))
      }
    },
    async exportPng() {
      const blob = await this.mind.exportPng()
      if (!blob) return
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'mindmap.png'
      a.click()
      URL.revokeObjectURL(url)
    },
  },
}
</script>

<style scoped>
.shortcut-section {
  max-height: 1000px;
  overflow-y: auto;
  background-color: #fff;
  font-size: 14px;
}

.shortcut-scroll {
  overflow-x: hidden;
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

.success {
  color: green;
}
.error {
  color: red;
}
</style>
