import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from './plugins/vuetify'
import axios from 'axios';

// 配置 axios
axios.defaults.baseURL = 'http://localhost:5001';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

// 添加請求攔截器
axios.interceptors.request.use(
  config => {
    config.withCredentials = true;
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

createApp(App).use(router).use(vuetify).mount('#app')