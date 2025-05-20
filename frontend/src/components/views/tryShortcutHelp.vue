<template>
  <div class="fixed top-4 right-4 bg-white shadow-lg rounded-xl p-4 max-w-sm text-sm z-50">
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
</template>

<script setup>
const shortcuts = [
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
</script>
