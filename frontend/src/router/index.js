import { createRouter, createWebHistory } from "vue-router";
// import PdfUploader from "../components/views/PdfUploader.vue";
import MindMap from "../components/views/MindMap.vue";
import QuizPage from "../components/views/QuizPage.vue";
import HomePage from "../components/views/HomePage.vue";

const routes = [
  { path: "/", redirect: "/mindmap" },
  // { path: "/pdfupload", name: "PdfUploader", component: PdfUploader },
  { path: "/mindmap", name: "MindMap", component: MindMap },
  { path: "/quizpage", name: "QuizPage", component: QuizPage },
  { path: "/homepage", name: "HomePage", component: HomePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
