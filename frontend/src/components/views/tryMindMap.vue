<template>
  <section class="mind-map-section">
    <h2>我的心智圖</h2>
    <div id="map" ref="map"></div>
    <button @click="exportPng" class="export-button">匯出為 PNG</button>
  </section>
</template>

<script>
import MindElixir from "mind-elixir";

export default {
  name: "MindMap",
  data() {
    return {
      mind: null
    };
  },
  mounted() {
    this.mind = new MindElixir({
      el: this.$refs.map,
      data: {
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
        }
    }
};
</script>

<style scoped>
.mind-map-section {
  padding: 20px;
  background-color: #f9f9f9;
}
.export-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}
#map {
  width: 100%;
  height: 500px;
  border: 1px solid #ddd;
}
</style>
