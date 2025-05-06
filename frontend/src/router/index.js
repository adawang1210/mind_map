import { createRouter, createWebHistory } from "vue-router";
import PdfUploader from "../components/views/PdfUploader.vue";
import MindMap from "../components/views/MindMap.vue";
import QuizPage from "../components/views/QuizPage.vue";

const routes = [
  { path: "/", redirect: "/mindmap" },
  { path: "/pdfupload", name: "PdfUploader", component: PdfUploader },
  { path: "/mindmap", name: "MindMap", component: MindMap },
  { path: "/quizpage", name: "QuizPage", component: QuizPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
