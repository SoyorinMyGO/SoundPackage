<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 顶部栏 -->
    <Head :isCollapsed="isCollapsed" @toggle="toggleCollapsed" @submit="setSearch"/>
    <!--主内容-->
    <div class="content">
      <!-- 侧边栏 -->
      <Sidebar :isCollapsed="isCollapsed" @collapse-request="setCollapsed"/>
      <!-- 主视图 -->
      <HomeMain :search="keyword"/>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "./Sidebar.vue";
import Head from "./Head.vue";
import {ref} from "vue";
import HomeMain from "./HomeMain.vue";

// 侧边栏折叠
const isCollapsed = ref(false)
function toggleCollapsed(){
  isCollapsed.value = !isCollapsed.value;
}
function setCollapsed(val){
  isCollapsed.value = val;
}

// 语音搜索
const keyword = ref('')
function setSearch(val){
  keyword.value = val;
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
</style>