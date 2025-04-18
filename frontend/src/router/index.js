import { createRouter, createWebHistory } from "vue-router";
import PdfUploader from "../components/views/PdfUploader.vue";
import MindMap from "../components/views/MindMap.vue";

const routes = [
  { path: "/", redirect: "/pdfupload" },
  { path: "/pdfupload", name: "PdfUploader", component: PdfUploader },
  { path: "/mindmap", name: "MindMap", component: MindMap },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
