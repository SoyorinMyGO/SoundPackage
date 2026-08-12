<template>
<div class="side-bar" :class="{ collapsed: isCollapsed }">
  <!-- 侧边栏 -->
  <SearchInput v-model="formData.name"></SearchInput>
</div>
</template>

<script setup>
import SearchInput from "../components/SearchInput.vue";
import {ref, watch} from "vue";

defineProps({
  isCollapsed: Boolean
})

const formData = ref({ name: ''})
watch(() => formData.value.name, (newText) => {
  console.log(newText)
})
</script>

<style scoped>
.side-bar {
  width: 0;
  background: var(--side-bar);
  overflow: auto;
  transition: width 0.5s ease, padding 0.7s ease;
  border-top: 1px solid #141417;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.collapsed {
  width: 250px;
  padding: 15px;
}


</style>