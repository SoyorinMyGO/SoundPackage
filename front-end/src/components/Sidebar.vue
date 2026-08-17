<template>
<div class="side-bar" ref="root" :class="{ collapsed: isCollapsed }">
  <!-- 侧边栏 -->
  <!--搜索栏-->
  <SearchInput v-model="formData.name"></SearchInput>
  <!--语音包列表-->
  <div v-if="packageList" id="package-list">
    <div v-for="item in packageList"
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
import {computed, onMounted, onBeforeUnmount, ref} from "vue";
import apiClient from "../utils/axios_config.js";

const props = defineProps({
  isCollapsed: Boolean
})

const emit = defineEmits(['collapse-request'])

const responseData = ref([])
const root = ref(null)
let lastCollapsed = null
const COLLAPSE_THRESHOLD = 180
let roInstance = null
let onResizeFn = null

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

const formData = ref({ name: ''})
const search = computed(() => formData.value.name.trim())

// 解包
const packageList = computed(() => {
  console.log("DEBUG:isCompute:", search.value)
  // 检查是否有数据
  if (!responseData.value || responseData.value.length === 0) {
    return [];
  }

  const keyword = search.value
  // 检查搜索列表
  if (!keyword) {
    console.log('无搜索词返回全部', responseData.value);
    return responseData.value;
  }

  const lowerKeyword = keyword.toLowerCase()
  const filtered = responseData.value.filter(item => {
    const nameMatch = item.name && item.name.toLowerCase().includes(lowerKeyword)
    const aliasMatch = item.alias && item.alias.toLowerCase().includes(lowerKeyword)
    return nameMatch || aliasMatch
  })

  console.log(`  → 找到 ${filtered.length} 项匹配`)
  return filtered
})

// 处理语音包选择
const chooseHandle = () => {}

// 处理置顶
const isPin = () => {}

onMounted(() => {
  get_list();
  //侧边栏展开状态
  // 初始化为当前 prop，避免首次发出与当前状态相同的事件
  lastCollapsed = props.isCollapsed

  const measureAndMaybeEmit = (w) => {
    const shouldCollapse = w < COLLAPSE_THRESHOLD
    // 如果期望状态等于当前 prop，说明无需变更（防止翻转）
    if (shouldCollapse === props.isCollapsed) {
      lastCollapsed = shouldCollapse
      return
    }
    // 只有当与上次不同且与当前 prop 不同的时候才发出请求
    if (shouldCollapse !== lastCollapsed) {
      lastCollapsed = shouldCollapse
      emit('collapse-request', shouldCollapse)
    }
  }

  if (window.ResizeObserver && root.value) {
    roInstance = new ResizeObserver(entries => {
      for (const entry of entries) {
        const w = entry.contentRect.width
        measureAndMaybeEmit(w)
      }
    })
    roInstance.observe(root.value)
  } else {
    onResizeFn = () => {
      const el = root.value
      if (!el) return
      const w = el.getBoundingClientRect().width
      measureAndMaybeEmit(w)
    }
    window.addEventListener('resize', onResizeFn)
    onResizeFn()
  }
})

onBeforeUnmount(() => {
  if (roInstance) roInstance.disconnect()
  if (onResizeFn) window.removeEventListener('resize', onResizeFn)
})
</script>

<style scoped>
.side-bar {
  width: 25%;
  background: var(--sidebar);
  overflow: hidden;
  transition: width 0.4s ease, padding 0.3s ease;
  border-top: 1px solid #141417;
  padding: 5px 15px 0 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.side-bar.collapsed {
  width: 0;
  padding: 0;
}

.side-bar.collapsed .search-wrapper,
.side-bar.collapsed #package-list {
  display: none;
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