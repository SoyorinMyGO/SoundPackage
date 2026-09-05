<template>
  <div class="app" :style="{ backgroundImage: `url(${imgURL})` }">
    <!-- 专门的可拖拽标题栏，仅此区域可拖动 -->
    <div class="titlebar glass-background">
      <WindowControls />
      <img src="./assets/MyGO.ico" alt="" class="logo" />
      <span class="title">SoYoVoice</span>
    </div>
    <!-- 主内容 -->
    <div class="main-content">
      <Home/>
    </div>
  </div>
</template>

<script setup>
import WindowControls from './components/WindowControl.vue'
import Home from './views/Home.vue'
import * as url from "node:url";

const imgURL = new URL("./assets/background.png", import.meta.url).href;
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  width: 100%;
  height: 100vh;
  background: #131010;
  color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
  background-size: cover;
}

.titlebar {
  -webkit-app-region: drag;
  height: 46px;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  z-index: 900;
  border-radius: 12px 12px 0 0;
  background: var(--windowControl_bg);
}

.titlebar .title {
  color: var(--textColor);
}

.titlebar .logo {
  width: 25px;
  height: 25px;
  margin: 17px;
  left: 0;
}
.main-content {
  height: calc(100vh - 46px);
  margin-top: 46px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: stretch;
}

/* 所有可交互元素不能拖动（否则无法点击） */
button, input, a {
  -webkit-app-region: no-drag;
}
</style>