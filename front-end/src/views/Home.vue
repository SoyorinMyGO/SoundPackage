<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 顶部栏 -->
    <Head :isCollapsed="isCollapsed" :packageChoose="packageChoose" @toggle="toggleCollapsed" @submit="setSearch" @refresh="refreshHomeMain"/>
    <!--主内容-->
    <div class="content">
      <!-- 侧边栏 -->
      <Sidebar :isCollapsed="isCollapsed" @collapse-request="setCollapsed" @choose="setPackageChoose"/>
      <!-- 主视图 -->
      <HomeMain :key="homeMainRefreshVersion" ref="homeMainRef" :search="keyword" :packageChoose="packageChoose"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from "./Sidebar.vue";
import Head from "./Head.vue";
import {ref} from "vue";
import HomeMain from "./HomeMain.vue";
import {PackageInfo} from "../model/Package";

const isCollapsed = ref<boolean>(false)
const keyword = ref<string>('')
const packageChoose = ref<PackageInfo>({id: 0, name: '全部语音'}) // 存储语音包对象，默认为id: name: 全部语音

const homeMainRef = ref<any>(null)
const homeMainRefreshVersion = ref(0)

// 侧边栏折叠
function toggleCollapsed(){
  isCollapsed.value = !isCollapsed.value;
}
function setCollapsed(val: boolean){
  isCollapsed.value = val;
}

// 语音搜索
function setSearch(val: string){
  keyword.value = val;
}

// 语音包选择
function setPackageChoose(val: PackageInfo){
  packageChoose.value = val;
}

// 其它子组件请求刷新 HomeMain 的数据时调用
function refreshHomeMain(){
  // 先强制组件重建，再重新拉取数据
  homeMainRefreshVersion.value += 1;
  if (homeMainRef.value && typeof homeMainRef.value.get_list === 'function') {
    console.log('DEBUG(Home): 重新获取列表, refreshVersion=', homeMainRefreshVersion.value);
    homeMainRef.value.get_list();
  }
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