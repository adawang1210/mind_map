<template>
  <div id="app">
    <MindMap />
  </div>
</template>

<script>
// import PdfUploader from './components/PdfUploader.vue';
import MindMap from './components/MindMap.vue';

export default {
  name: 'App',
  components: {
    MindMap
  }
};
</script>

<style>
/* 如果有全局樣式，可以保留這裡 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>