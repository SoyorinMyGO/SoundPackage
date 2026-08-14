<template>
<div class="side-bar" :class="{ collapsed: isCollapsed }">
  <!-- 侧边栏 -->
  <SearchInput v-model="formData.name"></SearchInput>
  <div v-if="responseData">
    <div v-for="item in responseData"
    :key="item.id"
    class="package-list">
      <button @click="chooseHandle" class="package">{{ item.name }}</button>
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
  background: var(--side-bar);
  overflow: auto;
  transition: width 0.5s ease, padding 0.7s ease;
  border-top: 1px solid #141417;
  padding-top: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.collapsed {
  width: 250px;
  padding: 15px;
}


</style>