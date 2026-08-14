<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 顶部栏 -->
    <Head :isCollapsed="isCollapsed" @toggle="toggleCollapsed"></Head>
    <div class="content">
      <!-- 侧边栏 -->
      <Sidebar :isCollapsed="isCollapsed"></Sidebar>
      <div class="main-view">
        <!-- 主视图 -->
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "../components/Sidebar.vue";
import Head from "../components/Head.vue";
import {ref} from "vue";

const isCollapsed = ref(true)
function toggleCollapsed(){
  isCollapsed.value = !isCollapsed.value;
}
</script>

<style scoped>
html, body, .main-container { height: 100%; }
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