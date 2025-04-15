<template>
  <div class="mind-map-container">
    <h1>我的心智圖</h1>
    <div id="map" ref="map"></div>
    <button @click="exportPng">匯出為 PNG</button>
  </div>
</template>

<script>
import MindElixir from "mind-elixir";

export default {
  name: "MindMap",
  data() {
    return {
      mind: null,
      example: {
        // 這裡是 dummy data 的內容
        nodeData: {
          id: "root",
          topic: "中心主題",
          root: true,
          children: [
            {
              topic: "主題 A",
              id: "a1",
              direction: "right",
              children: [
                { topic: "子主題 A1", id: "a1-1" },
                { topic: "子主題 A2", id: "a1-2" },
              ],
            },
            {
              topic: "主題 B",
              id: "b1",
              direction: "left",
              children: [
                { topic: "子主題 B1", id: "b1-1" },
                { topic: "子主題 B2", id: "b1-2" },
              ],
            },
          ],
        },
        linkData: {},
        direction: 1, // 1: 左右結構, 2: 垂直結構
        template: "default",
      },
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
    this.mind.init(this.example); // 使用內建的 dummy data

    this.mind.bus.addListener("selectNode", (node) => {
      console.log("選擇的節點:", node);
    });

    this.mind.bus.addListener("operation", (operation) => {
      console.log("操作:", operation);
    });
  },
  methods: {
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
.mind-map-container {
  max-width: 1000px;
  margin: 50px auto;
  text-align: center;
}

#map {
  height: 500px;
  width: 100%;
  border: 1px solid #ddd;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
