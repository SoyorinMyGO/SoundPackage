import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { userThemeStore } from "./store/theme.js";
import { createPinia } from "pinia";

const app = createApp(App);

const pinia = createPinia()
app.use(pinia)

app.mount('#app')

// 挂载当前全局主题
// const themeStore = userThemeStore()
// themeStore.initTheme()

import { nextTick } from 'vue';
nextTick(() => {
    try {
        const themeStore = userThemeStore();
        themeStore.initTheme();
        console.log('主题初始化成功');
    } catch (error) {
        console.error('主题初始化失败:', error);
    }
});