import { createRouter, createWebHistory } from "vue-router";
import MindMap from "../components/views/MindMap.vue";
import QuizPage from "../components/views/QuizPage.vue";
import HomePage from "../components/views/HomePage.vue";

const routes = [
  { path: "/", redirect: "/homepage" },
  { path: "/mindmap", name: "MindMap", component: MindMap },
  { path: "/quizpage", name: "QuizPage", component: QuizPage },
  { path: "/homepage", name: "HomePage", component: HomePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;