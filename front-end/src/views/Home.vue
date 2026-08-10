<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 顶部栏 -->
    <Head></Head>
    <div class="content">
      <!-- 侧边栏 -->
      <Sidebar></Sidebar>
      <div class="main-view">
        <!-- 主视图 -->
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "./Sidebar.vue";
import Head from "./Head.vue";
</script>

<style scoped>
html, body, #app, .main-container { height: 100%; }
.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
}

.content {
  display: flex;
  flex: 1 1 auto;
  min-height: 0;
}

.main-view {
  flex: 1 1 auto;
  background-color: var(--background);
  overflow: auto;
  padding: 12px;
  border-radius: 12px 0 0 0;
}
</style>
