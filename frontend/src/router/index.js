import { createRouter, createWebHistory } from "vue-router";
// import PdfUploader from "../components/views/PdfUploader.vue";
import MindMap from "../components/views/MindMap.vue";
<<<<<<< HEAD
=======
import QuizPage from "../components/views/QuizPage.vue";
import HomePage from "../components/views/HomePage.vue";
>>>>>>> 5dd14878bdcd6016d508721442c0b92a9ea8f816

const routes = [
  { path: "/", redirect: "/mindmap" },
  // { path: "/pdfupload", name: "PdfUploader", component: PdfUploader },
  { path: "/mindmap", name: "MindMap", component: MindMap },
<<<<<<< HEAD
=======
  { path: "/quizpage", name: "QuizPage", component: QuizPage },
  { path: "/homepage", name: "HomePage", component: HomePage },
>>>>>>> 5dd14878bdcd6016d508721442c0b92a9ea8f816
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;