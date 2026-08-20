<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 顶部栏 -->
    <Head :isCollapsed="isCollapsed" @toggle="toggleCollapsed"></Head>
    <div class="content">
      <!-- 侧边栏 -->
      <Sidebar :isCollapsed="isCollapsed" @collapse-request="setCollapsed"></Sidebar>
      <div class="main-view">
        <!-- 主视图 -->
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "./Sidebar.vue";
import Head from "./Head.vue";
import {ref} from "vue";

const isCollapsed = ref(false)
function toggleCollapsed(){
  isCollapsed.value = !isCollapsed.value;
}
function setCollapsed(val){
  isCollapsed.value = val;
}
</script>

<style scoped>
html, body, .main-container { height: 100%; }
.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.content {
  display: flex;
  flex-direction: row;
  flex: 1 1 auto;
  min-height: 0;
  height: 100%;
}

.main-view {
  flex: 1;
  background-color: var(--background);
  overflow: auto;
  padding: 12px;
  border-radius: 12px 0 0 0;
}
</style>