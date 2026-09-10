import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {useLocalStorage} from "../utils/LocalStorage/use_storage.ts";

export const userThemeStore = defineStore('theme',() => {
    const currentTheme = useLocalStorage('app_theme', 'dark');

    const themes = {
        light: {
            name: "light",
            windowControl_bg: '#FFFFFF',
            head: '#EFF6FD',
            sidebar: '#EFF6FD',
            background: '#FFFFFF',
            textColor: '#424242',
            borderColor: '#E5E7EB',
            cardColor: '#EFF6FD',
            primaryColor: '#248ff8',
            secondaryColor: '#f5f5f5',
            hover: '#dcdcdc',
            backgroundImg: '',
        },
        dark: {
            name: "dark",
            windowControl_bg: 'rgb(12 12 12 / 0.8)',
            head: 'rgb(9 8 8 / 0.8)',
            sidebar: 'rgb(9 8 8 / 0.8)',
            background: 'rgb(17 17 20 / 0.8)',
            textColor: '#eff6fd',
            borderColor: '#1c1b1b',
            cardColor: '#151515',
            primaryColor: '#4c8bf5',
            secondaryColor: 'rgb(49 48 48 / 0.9)',
            hover: 'rgb(230 230 230 / 0.3)',
            backgroundImg: '',
        }
    };

    // getters
    const getCurrentTheme = computed(() => currentTheme.value);
    const getThemeConfig = computed(() => themes[currentTheme.value] ?? themes.dark);
    const getAllThemes = computed(() =>
        Object.keys(themes).map(key => ({
            id: key,
            name: themes[key].name,
            primaryColor: themes[key].primaryColor,
        })));

    // actions
    function setTheme(themeName) {
        if (!themeName || !themes[themeName]) {
            console.warn(`未识别的主题: ${themeName}`)
            return
        }
        currentTheme.value = themeName
        applyTheme()
    }

    function applyTheme() {
        /**
         * 用于应用主题颜色
         * 通过修改CSS变量来加载主体颜色
         **/
        const theme = themes[currentTheme.value] ?? themes.dark
        document.documentElement.style.setProperty('--head', theme.head)
        document.documentElement.style.setProperty('--sidebar', theme.sidebar)
        document.documentElement.style.setProperty('--background', theme.background)
        document.documentElement.style.setProperty('--textColor', theme.textColor)
        document.documentElement.style.setProperty('--primaryColor', theme.primaryColor)
        document.documentElement.style.setProperty('--secondaryColor', theme.secondaryColor)
        document.documentElement.style.setProperty('--windowControl_bg', theme.windowControl_bg)
        document.documentElement.style.setProperty('--hover', theme.hover)
        document.documentElement.style.setProperty('--cardColor', theme.cardColor)
        document.documentElement.style.setProperty('--borderColor', theme.borderColor)
    }

    function initTheme() {
        if (!themes[currentTheme.value]) {
            currentTheme.value = 'dark'
        }
        applyTheme()
        console.log("已完成初始化")
    }

    return {
        currentTheme,
        themes,
        getCurrentTheme,
        getThemeConfig,
        getAllThemes,
        setTheme,
        applyTheme,
        initTheme
    };
})