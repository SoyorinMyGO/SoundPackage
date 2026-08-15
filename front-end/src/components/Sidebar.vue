<template>
<div class="side-bar" :class="{ collapsed: isCollapsed }">
  <!-- 侧边栏 -->
  <!--搜索栏-->
  <SearchInput v-model="formData.name"></SearchInput>
  <!--语音包列表-->
  <div v-if="responseData" id="package-list">
    <div v-for="item in responseData"
    :key="item.id"
    class="package">
      <button @click="chooseHandle" class="package-button">
        <span>{{ item.name }}</span>
      </button>
      <button @click="isPin" class="pin-button">
        <i class="icon-pin"></i>
      </button>
    </div>
  </div>
</div>
</template>

<script setup>
import SearchInput from "./SearchInput.vue";
import {computed, onMounted, ref, watch} from "vue";
import apiClient from "../utils/axios_config.js";

defineProps({
  isCollapsed: Boolean
})

const responseData = ref(null)

// 获取语音包列表
const get_list = async () => {
  try {
    const res = await apiClient.get("/api/package");
    console.log('完整响应', res.data);
    console.log('数据列表', res.data.data);
    responseData.value = res.data.data;
  }
  catch (e) {
    console.error(e);
  }
}

// 解包
const packageList = computed(() => {
  // 检查是否有数据
  if (!responseData) {
    return [];
  }

  // 检查响应状态
  if (responseData.value.code !== 200) {
    return [];
  }

  return responseData.value.data;
})

// 处理语音包选择
const chooseHandle = () => {}

// 处理置顶
const isPin = () => {}

const search = ref('')
const formData = ref({ name: ''})
// 监听搜索栏数据变化
watch(() => formData.value.name, (newText) => {
  search = newText
})

onMounted(() => {
  get_list();
})
</script>

<style scoped>
.side-bar {
  width: 0;
  background: var(--sidebar);
  overflow: auto;
  transition: width 0.5s ease, padding 0.7s ease;
  border-top: 1px solid #141417;
  padding-top: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.collapsed {
  width: 25%;
  padding: 15px;
}

#package-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-top: 10px;
}

.package {
  display: flex;
  flex-direction: row;
  gap: 5px;
  width: 100%;
  height: 35px;
  margin: 3px;
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

</style>