<template>
<div class="root" :class="{ collapsed: isCollapsed }">
  <div class="sidebar" ref="root">
    <!--搜索栏-->
    <SearchInput class="search" v-model="formData.name" :isSimple=false></SearchInput>
    <!--语音包列表-->
    <el-scrollbar class="package-list">
      <!--全部语音固定置顶-->
      <div class="package">
        <button @click="chooseHandle({id: 0, name: '全部语音'})" class="package-button">
          <span>全部语音</span>
        </button>
        <button class="pin-button">
          <i class="icon-pin"></i>
        </button>
      </div>
      <!--其他语音包-->
      <div v-for="item in packageList"
      :key="item.id"
      class="package">
        <button @click="chooseHandle({id: item.id, name: item.name})" class="package-button" :title="item.alias ? `${item.name}(${item.alias})` : `${item.name}`">
          <span>{{ item.name }}</span>
        </button>
        <button @click="pinHandle(item)" class="pin-button">
          <i class="icon-pin" v-if="item.isTop"></i>
          <i class="icon-cancel-pin-line" v-if="!item.isTop"></i>
        </button>
      </div>
    </el-scrollbar>
  </div>
    <!--侧边底部栏-->
  <div class="bottom">
    <!--用户头像及用户名-->
    <img src="../assets/avator.jpg" alt="">
    <span>{{ userName }}</span>
  </div>
</div>
</template>

<script setup lang="ts">

import SearchInput from "../components/SearchInput.vue";
import {computed, onMounted, ref} from "vue";
import apiClient from "../config/axios_config.js";

interface PackageItem{
  id: number
  name: string
  alias: string | null
  isTop: boolean
  created_at: string
  updated_at: string
}

const props = defineProps({
  isCollapsed: Boolean
})

const emit = defineEmits(["collapse-request", "choose"])

const responseData = ref<PackageItem[]>([])
// 搜索信息
const formData = ref({ name: ''})
const search = computed(() => formData.value.name.trim())
// 用户信息
const userAvatorAdr = './assets/avator.jpg'
const userName = 'soyorin'

// 获取语音包列表
const get_list = async () => {
  try {
    const res = await apiClient.get("/api/package");
    responseData.value = res.data.data;
  }
  catch (e) {
    console.error(e);
  }
}

// 解包
const packageList = computed<PackageItem[]>(() => {
  // 检查是否有数据
  if (!responseData.value || responseData.value.length === 0) {
    return [];
  }

  const keyword = search.value
  // 检查搜索列表
  if (!keyword) {
    console.log('DEBUG(package_list):返回全部', responseData.value);
    return responseData.value;
  }

  const lowerKeyword = keyword.toLowerCase()
  return responseData.value.filter(item => {
    const nameMatch = item.name && item.name.toLowerCase().includes(lowerKeyword)
    const aliasMatch = item.alias && item.alias.toLowerCase().includes(lowerKeyword)
    return nameMatch || aliasMatch
  })
})

// 处理语音包选择
const chooseHandle = (id: number) => {
  emit("choose", id);
}

// 处理置顶
const pinHandle = (item: PackageItem) => {
  //上传数据至数据库
  apiClient.post(`/api/package/${item.id}/top`, null, {
  params: {
    isTop: item.isTop
  }})
  .then((res) => {
    console.log('更改置顶状态成功', res.data)})
  .catch((err) => {
    console.error('更改置顶状态失败', err);
  })
  // 更新本地数据
  item.isTop = !item.isTop;
  // 本地重新排序
  responseData.value = responseData.value.sort((a, b) => {
    if(a.isTop !== b.isTop) {
      // 优先根据置顶排序
      return (b.isTop ? 1 : 0) - (a.isTop ? 1 : 0)
    }
    return new Date(a.updated_at) - new Date(b.updated_at)
  })
}

onMounted(() => {
  get_list();
})
</script>

<style scoped>
.root{
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  border: none;
  width: 25%;
  height: 100%;
  min-height: 0;
  background: var(--sidebar);
  overflow: hidden;
  transition: width 0.4s ease, padding 0.3s ease;
  border-radius: 0 10px 0 0;
}

.sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1 1 auto;
  min-height: 0;
}

.root.collapsed {
  width: 0;
  padding: 0;
}

.search {
  margin: 20px 15px 0 15px;
}

.package-list {
  width: 100%;
  flex: 1 1 auto;
  min-height: 0;
  margin: 10px 15px 0 15px;
}

.package {
  display: flex;
  flex-direction: row;
  gap: 5px;
  width: 100%;
  height: 35px;
  padding: 3px 15px 0 15px;
}

.package>.package-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
  height: 100%;
  border: 2px solid var(--primaryColor);
  border-radius: 5px;
  background-color: var(--background);
  color: var(--textColor);
  position: relative;
  overflow: hidden;
}
/* package按钮动效 */
.package>.package-button:active {
  transform: scale(0.95);
}
.package-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--hover) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s;
}
.package-button:hover::after {
  opacity: 1;
}

/* 文字始终横向排列*/
.package-button>span {
  white-space: nowrap;
}


.package>.pin-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 36px;
  height: 35px;
  border: none;
  border-radius: 16px;
  background-color: var(--sidebar);
  color: var(--primaryColor);
  position: relative;
  overflow: hidden;
}
.package i{
  font-size: 22px;
  font-family: "iconfont", serif !important;
}
/* pin按钮动效 */
.package>.pin-button:active {
  transform: scale(0.95);
}
.pin-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--hover) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s;
}
.pin-button:hover::after {
  opacity: 1;
}

.bottom {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  height: 45px;
  width: 100%;
  flex-shrink: 0;
  padding: 0 10px;
  border-top: 1px solid #141417;
  box-sizing: border-box;
}

.bottom:hover {
  background-color: var(--hover);
}

.bottom > img {
  width: 27px;
  height: 27px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.bottom > span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>