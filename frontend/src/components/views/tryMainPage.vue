<template>
  <div class="container relative min-h-screen bg-gray-50">
    <h1 class="text-2xl font-bold p-4">心智圖與 PDF 上傳</h1>
    <PDFLoader />
    <MindMap />
    <ShortcutHelp />
  </div>
</template>

<script>
import PDFLoader from "@/components/views/PDFLoader.vue";
import MindMap from "@/components/views/MindMap.vue";
import ShortcutHelp from "@/components/views/ShortcutHelp.vue";

export default {
  name: "MainPage",
  components: {
    PDFLoader,
    MindMap,
    ShortcutHelp
  }
};
</script>
