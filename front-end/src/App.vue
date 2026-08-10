<template>
  <div class="app">
    <!-- 专门的可拖拽标题栏，仅此区域可拖动 -->
    <div class="titlebar">
      <WindowControls />
    </div>
    <!-- 主内容 -->
    <div class="main-content">
      <Home />
    </div>
  </div>
</template>

<script setup>
import WindowControls from './components/WindowControl.vue'
import Home from './views/Home.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  width: 100%;
  height: 100%;
  background: #131010;
  color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
}

.titlebar {
  -webkit-app-region: drag;
  height: 40px;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end; /* 控制按钮显示在右侧 */
  z-index: 900;
}

.main-content {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 40px;
}

/* 所有可交互元素不能拖动（否则无法点击） */
button, input, a, .no-drag {
  -webkit-app-region: no-drag;
}
</style>