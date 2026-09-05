<template>
<div class="head glass-background">
  <!--左侧按钮组-->
  <div class="left-button-group">
    <button @click="emit('toggle')">
      <i class="icon icon-unfold" v-if="isCollapsed"></i>
      <i class="icon icon-fold" v-if="!isCollapsed"></i>
    </button>
    <button>
      <i class="icon icon-moon" v-if="isDark"></i>
      <i class="icon icon-sun" v-if="!isDark"></i>
    </button>
  </div>
  <!--搜索栏-->
  <div class="search-group">
    <search-input
        ref="searchInputRef"
        :isSimple=true
        :model-value="formData"
        @update:modelValue="handleInput"
        @blur="handleBlur"
        class="search">
    </search-input>
  </div>
  <!--右侧按钮组-->
  <div class="right-button-group">
    <button>
      <i class="icon-import"></i>
    </button>
    <button>
      <i class="icon-export"></i>
    </button>
    <button>
      <i class="icon-file-manager"></i>
    </button>
  </div>
</div>
</template>

<script setup lang="ts">
import SearchInput from "../components/SearchInput.vue";
import {computed, onMounted, onUnmounted, Ref, ref, UnwrapRef} from "vue";

defineProps({
  isCollapsed: Boolean
})

const emit = defineEmits(["toggle", "submit"]);
const isDark = ref<boolean>(true);

// 搜索栏关键字
const formData: Ref<UnwrapRef<string>, UnwrapRef<string> | string> = ref('');
const search = computed(() => formData.value.trim());
// 获取搜索栏的引用
const searchInputRef = ref<typeof SearchInput | null>(null);

function handleInput(value: string) {
  formData.value = value;
}

function handleBlur() {
  emit('submit', search.value);
}

const handleKeyDown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    console.log('DEBUG(keyboardWatch):按下了Ctrl+K');
    e.preventDefault(); // 阻止浏览器默认行为
    if (searchInputRef.value) {
      searchInputRef.value.focus?.();
      searchInputRef.value.select?.();
    }
  }
  if (e.key === 'Escape' || e.key === 'Enter') {
    console.log("DEBUG(keyboardWatch): 按下了失焦键");
    searchInputRef.value.blur?.();
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
i {
  font-family: "iconfont", serif;
  color: var(--primaryColor);
}

button {
  border: none;
  border-radius: 15px;
  background: transparent;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.head {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  height: 50px;
  flex: 0 0 50px;
  margin-top: 0;
  background-color: var(--head);
}

.left-button-group {
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex: 1;
  margin: 10px;
}

.left-button-group i {
  font-size: 17px;
}

/* 按钮动效 */
.left-button:active {
  transform: scale(0.9)
}

.search-group {
  display: flex;
  flex-direction: row;
  flex: 3;
}

.right-button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
  margin: 10px;
}

.icon-import { font-size: 23px; }
.icon-export { font-size: 22px; }
.icon-file-manager { font-size: 18px; }

.search {
  flex: 3;
  color: var(--textColor);
}
</style>