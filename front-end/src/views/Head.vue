<template>
<div class="head">
  <!--左侧按钮组-->
  <div class="left-button-group">
    <button @click="emit('toggle')" id="toggleButton">
      <i class="icon icon-unfold" v-if="isCollapsed"></i>
      <i class="icon icon-fold" v-if="!isCollapsed"></i>
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
  display: flex;
  flex-direction: row;
  flex: 1;
}

.search-group {
  display: flex;
  flex-direction: row;
  flex: 3;
}

.right-button-group {
  display: flex;
  flex-direction: row;
  flex: 1;
}

#toggleButton {
  margin-left: 10px;
  width: 30px;
  height: 30px;
  align-self: flex-start;
  border: none;
  border-radius: 15px;
  background: transparent;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}
/* 按钮动效 */
#toggleButton:active {
  transform: scale(0.9)
}
#toggleButton i{
  font-family: "iconfont",serif !important;
  color: var(--primaryColor)
}

.search {
  flex: 3;
  color: var(--textColor);
}
</style>